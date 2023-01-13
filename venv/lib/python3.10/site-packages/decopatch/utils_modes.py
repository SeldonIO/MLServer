from makefun import remove_signature_parameters, with_signature, wraps

try:  # python 3.3+
    from inspect import signature, Parameter
    funcsigs_used = False
except ImportError:
    from funcsigs import signature, Parameter
    funcsigs_used = True


class _Symbol:
    """
    Symbols used in your (double) flat-mode signatures to declare where the various objects should be injected
    These symbols have a nice representation.
    """
    __slots__ = ('repr_', )

    def __init__(self, repr_):
        self.repr_ = repr_

    def __repr__(self):
        return self.repr_


DECORATED = _Symbol('DECORATED')
# A symbol used in flat-mode signatures to declare where the decorated function should be injected


WRAPPED = _Symbol('WRAPPED')
# A symbol used in double flat-mode signatures to declare where the wrapped function should be injected


F_ARGS = _Symbol('F_ARGS')
# A symbol used in your double flat-mode signatures to declare where the wrapper args should be injected


F_KWARGS = _Symbol('F_KWARGS')
# A symbol used in your double flat-mode signatures to declare where the wrapper kwargs should be injected


def make_decorator_spec(impl_function,
                        flat_mode_decorated_name=None  # type: str
                        ):
    """
    Analyzes the implementation function


    If `flat_mode_decorated_name` is set, this is a shortcut for flat mode. In that case the implementation function
    is not analyzed.

    :param impl_function:
    :param flat_mode_decorated_name:
    :return: sig_info, function_for_metadata, nested_impl_function
    """
    # extract the implementation's signature
    implementors_signature = signature(impl_function)

    # determine the mode (nested, flat, double-flat) and check signature
    mode, injected_name, contains_varpositional, injected_pos, \
    injected_arg, f_args_name, f_kwargs_name = extract_mode_info(implementors_signature, flat_mode_decorated_name)

    # create the signature of the decorator function to create, according to mode
    if mode is None:
        # *nested: keep the signature 'as is'
        exposed_signature = implementors_signature
        function_for_metadata = impl_function
        nested_impl_function = impl_function

    elif mode is DECORATED:  # flat mode
        # use the same signature, but remove the injected arg.
        exposed_signature = remove_signature_parameters(implementors_signature, injected_name)

        # use the original function for the docstring/module metadata
        function_for_metadata = impl_function

        # generate the corresponding nested decorator
        nested_impl_function = make_nested_impl_for_flat_mode(exposed_signature, impl_function, injected_name,
                                                              injected_pos)

    elif mode is WRAPPED:
        # *double-flat: the same signature, but we remove the injected args.
        args_to_remove = (injected_name,) + ((f_args_name,) if f_args_name is not None else ()) \
                         + ((f_kwargs_name,) if f_kwargs_name is not None else ())
        exposed_signature = remove_signature_parameters(implementors_signature, *args_to_remove)

        # use the original function for the docstring/module metadata
        function_for_metadata = impl_function

        # generate the corresponding nested decorator
        nested_impl_function = make_nested_impl_for_doubleflat_mode(exposed_signature, impl_function, injected_name,
                                                                    f_args_name, f_kwargs_name, injected_pos)

    else:
        raise ValueError("Unknown mode: %s" % mode)

    # create an object to easily access the exposed signature information afterwards
    sig_info = SignatureInfo(exposed_signature, contains_varpositional, injected_pos)

    return sig_info, function_for_metadata, nested_impl_function


def make_nested_impl_for_flat_mode(decorator_signature, user_provided_applier, injected_name, injected_pos):
    """
    Creates the nested-mode decorator to be used when the implementation is provided in flat mode.

    Note: we set the signature correctly so that this behaves exactly like a nested implementation in terms of
    exceptions raised when the arguments are incorrect. Since the external method is called only once per decorator
    usage and does not impact the decorated object we can afford.

    :param decorator_signature:
    :param user_provided_applier:
    :param injected_name:
    :param argnames_before_varpos_arg:
    :return:
    """

    @with_signature(decorator_signature)
    def _decorator(*args, **kwargs):
        """ The decorator. Its signature will be overriden by `generated_signature` """

        def _apply_decorator(decorated):
            """ This is called when the decorator is applied to an object `decorated` """

            # inject `decorated` under the correct name
            # fix in case of var-positional arguments
            if injected_pos >= 0:
                new_args = args[:injected_pos] + (decorated, ) + args[injected_pos:]
            else:
                new_args = args
                kwargs[injected_name] = decorated

            return user_provided_applier(*new_args, **kwargs)

        return _apply_decorator

    return _decorator


def make_nested_impl_for_doubleflat_mode(decorator_signature, user_provided_wrapper, injected_name,
                                         f_args_name, f_kwargs_name, injected_pos):
    """
    Creates the nested-mode decorator to be used when the implementation is provided in double-flat mode.

    Note: we set the signature correctly so that this behaves exactly like a nested implementation in terms of
    exceptions raised when the arguments are incorrect. Since the external method is called only once per decorator
    usage and does not impact the decorated object / created wrappe, we can afford.

    :param decorator_signature:
    :param user_provided_wrapper:
    :param injected_name:
    :param f_args_name:
    :param f_kwargs_name:
    :return:
    """

    @with_signature(decorator_signature)
    def _decorator(*args, **kwargs):
        """ The decorator. Its signature will be overriden by `generated_signature` """

        def _apply_decorator(decorated):
            """ This is called when the decorator is applied to an object `decorated` """

            # inject `decorated` under the correct name
            # fix in case of var-positional arguments
            if injected_pos >= 0:
                new_args = args[:injected_pos] + (decorated,) + args[injected_pos:]
            else:
                new_args = args
                kwargs[injected_name] = decorated

            # create a signature-preserving wrapper using `makefun.wraps`
            @wraps(decorated)
            def wrapper(*f_args, **f_kwargs):
                # if the user wishes us to inject the actual args and kwargs, let's inject them
                # note: for these it is always keyword-based.
                if f_args_name is not None:
                    kwargs[f_args_name] = f_args
                if f_kwargs_name is not None:
                    kwargs[f_kwargs_name] = f_kwargs

                # finally call the user-provided implementation
                return user_provided_wrapper(*new_args, **kwargs)

            return wrapper

        return _apply_decorator

    return _decorator


class InvalidSignatureError(Exception):
    """
    Exception raised when a decorator signature is invalid with respect to the selected mode.
    Typically when you use flat-mode or wrapped-mode symbols but your signature does not allow them to be safely
    injected as keyword because they are followed by a var-positional argument.
    """
    pass


def extract_mode_info(impl_sig,                      # type: Signature
                      flat_mode_decorated_name=None  # type: str
                      ):
    """
    Returns the (name, Parameter) for the parameter with default value DECORATED

    :param impl_sig: the implementing function's signature
    :param flat_mode_decorated_name: an optional name of decorated argument. If provided a "flat mode" is automatically
        set
    :return:
    """
    mode = None
    injected = None
    injected_pos = None
    position_of_varpos = -1
    f_args = None
    f_kwargs = None

    if flat_mode_decorated_name is not None:
        # validate that the 'decorated' parameter is a string representing a real parameter of the function
        if not isinstance(flat_mode_decorated_name, str):
            raise InvalidSignatureError("'flat_mode_decorated_name' argument should be a string with the argument name "
                                        "where the wrapped object should be injected")

        mode = DECORATED

        # analyze signature to detect injected arg and potentially varpositional
        for i, (k, p) in enumerate(impl_sig.parameters.items()):
            if k == flat_mode_decorated_name:
                # this is the injected parameter
                injected = p
                injected_pos = i
            elif p.kind is Parameter.VAR_POSITIONAL:
                position_of_varpos = i

        if injected is None:
            return ValueError("Function '%s' does not have an argument named '%s'" % (impl_sig.__name__,
                                                                                      flat_mode_decorated_name))
        if injected.kind in {Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD}:
            raise InvalidSignatureError("`flat_mode_decorated_name` cannot correspond to a Var-pos nor Var-kw")
    else:
        # analyze signature to detect
        for i, (p_name, p) in enumerate(impl_sig.parameters.items()):
            if p.kind is Parameter.VAR_POSITIONAL:
                position_of_varpos = i
                if f_args is not None or f_kwargs is not None:
                    raise InvalidSignatureError("f_args and f_kwargs can only be used *after* var-positional arguments")
            elif p.default is DECORATED:
                if mode is not None:
                    raise InvalidSignatureError("only one of `DECORATED` or `WRAPPED` can be used in your signature")
                else:
                    mode = DECORATED
                    injected = p
                    injected_pos = i
            elif p.default is WRAPPED:
                if mode is not None:
                    raise InvalidSignatureError("only one of `DECORATED` or `WRAPPED` can be used in your signature")
                else:
                    mode = WRAPPED
                    injected = p
                    injected_pos = i
            elif p.default is F_ARGS:
                f_args = p
            elif p.default is F_KWARGS:
                f_kwargs = p

        if mode in {None, DECORATED} and (f_args is not None or f_kwargs is not None):
            raise InvalidSignatureError("`F_ARGS` or `F_KWARGS` should only be used if you use `WRAPPED`")

    # argnames_before_varpos_arg = None
    # if position_of_varpos > 0:
    #     # if there is a var-positional we will have to inject arguments before it manually
    #     argnames_before_varpos_arg = tuple(k for k in list(impl_sig.parameters.keys())[0:position_of_varpos])
    #
    # if argnames_before_varpos_arg is None:
    #     argnames_before_varpos_arg = tuple()

    contains_varpositional = position_of_varpos >= 0

    if not contains_varpositional or (injected_pos is not None and position_of_varpos < injected_pos):
        # do not inject as positional but as keyword argument
        injected_pos = -1

    return mode, (injected.name if injected is not None else None), contains_varpositional, injected_pos, \
           injected, (f_args.name if f_args is not None else None), (f_kwargs.name if f_kwargs is not None else None)


# -----------


class SignatureInfo(object):
    """
    Represents the knowledge we have on the decorator signature.
    Provides handy properties to separate the code requirements from the implementation (and possibly cache).
    """
    __slots__ = '_exposed_signature', 'first_arg_def', '_use_signature_trick', 'contains_varpositional', \
                'injected_pos'

    def __init__(self, decorator_signature, contains_varpositional, injected_pos):
        self._exposed_signature = decorator_signature
        _, self.first_arg_def = get_first_parameter(decorator_signature)
        self._use_signature_trick = False
        self.contains_varpositional = contains_varpositional
        self.injected_pos = injected_pos

    # --

    @property
    def use_signature_trick(self):
        return self._use_signature_trick

    @use_signature_trick.setter
    def use_signature_trick(self, use_signature_trick):
        # note: as of today python 2.7 backport does not handle it properly, but hopefully it will :)
        # see https://github.com/testing-cabal/funcsigs/issues/33.
        self._use_signature_trick = use_signature_trick and not funcsigs_used

    # --

    @property
    def exposed_signature(self):
        return self._exposed_signature

    @exposed_signature.setter
    def exposed_signature(self, new_sig):
        """
        If the signature is changed then we should be careful..
        :param new_sig:
        :return:
        """
        # this currently only happen in a single specific case, control that to avoid future mistakes
        if self.first_arg_kind is not Parameter.VAR_KEYWORD or len(self._exposed_signature.parameters) != 1:
            raise NotImplementedError("This case should not happen")

        self._exposed_signature = new_sig
        self.contains_varpositional = any(p.kind is Parameter.VAR_POSITIONAL for p in new_sig.parameters.values())
        _, self.first_arg_def = get_first_parameter(new_sig)

    # --

    @property
    def first_arg_name(self):
        return self.first_arg_def.name  # if self.first_arg_def is not None else None

    @property
    def first_arg_name_with_possible_star(self):
        return ('*' if self.is_first_arg_varpositional else '') + self.first_arg_name

    @property
    def first_arg_kind(self):
        return self.first_arg_def.kind  # if self.first_arg_def is not None else None

    @property
    def is_first_arg_keyword_only(self):
        return self.first_arg_kind in {Parameter.KEYWORD_ONLY, Parameter.VAR_KEYWORD}

    @property
    def is_first_arg_varpositional(self):
        return self.first_arg_kind is Parameter.VAR_POSITIONAL

    @property
    def is_first_arg_positional_only(self):
        return self.first_arg_kind is Parameter.POSITIONAL_ONLY

    @property
    def is_first_arg_mandatory(self):
        return self.first_arg_def.default is Parameter.empty and self.first_arg_kind not in {Parameter.VAR_POSITIONAL,
                                                                                             Parameter.VAR_KEYWORD}


def get_first_parameter(ds  # type: Signature
                        ):
    """
    Returns the (name, Parameter) for the first parameter in the signature

    :param ds:
    :return:
    """
    try:
        return next(iter(ds.parameters.items()))
    except StopIteration:
        return None, None
