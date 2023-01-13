from makefun import with_signature, add_signature_parameters
from decopatch.utils_modes import SignatureInfo, make_decorator_spec
from decopatch.utils_disambiguation import create_single_arg_callable_or_class_disambiguator, disambiguate_call, \
    DecoratorUsageInfo, can_arg_be_a_decorator_target
from decopatch.utils_calls import with_parenthesis_usage, no_parenthesis_usage, call_in_appropriate_mode

try:  # python 3.3+
    from inspect import signature, Parameter
except ImportError:
    from funcsigs import signature, Parameter

try:  # python 3.5+
    from typing import Callable, Any, Optional
except ImportError:
    pass


def function_decorator(enable_stack_introspection=False,  # type: bool
                       custom_disambiguator=None,         # type: Callable[[Any], FirstArgDisambiguation]
                       flat_mode_decorated_name=None,     # type: Optional[str]
                       ):
    """
    A decorator to create function decorators.
    Equivalent to

        decorator(is_function_decorator=True, is_class_decorator=False)

    :param enable_stack_introspection:
    :param custom_disambiguator:
    :param flat_mode_decorated_name:
    :return:
    """
    if callable(enable_stack_introspection):
        # no-parenthesis call
        f = enable_stack_introspection
        return decorator(is_function_decorator=True,
                         is_class_decorator=False)(f)
    else:
        return decorator(is_function_decorator=True,
                         is_class_decorator=False,
                         enable_stack_introspection=enable_stack_introspection,
                         custom_disambiguator=custom_disambiguator,
                         flat_mode_decorated_name=flat_mode_decorated_name)


def class_decorator(enable_stack_introspection=False,  # type: bool
                    custom_disambiguator=None,         # type: Callable[[Any], FirstArgDisambiguation]
                    flat_mode_decorated_name=None,     # type: Optional[str]
                    ):
    """
    A decorator to create class decorators
    Equivalent to

        decorator(is_function_decorator=False, is_class_decorator=True)

    :param enable_stack_introspection:
    :param custom_disambiguator:
    :param flat_mode_decorated_name:
    :return:
    """
    if callable(enable_stack_introspection):
        # no-parenthesis call
        f = enable_stack_introspection
        return decorator(is_function_decorator=False,
                         is_class_decorator=True)(f)
    else:
        return decorator(is_function_decorator=False,
                         is_class_decorator=True,
                         enable_stack_introspection=enable_stack_introspection,
                         custom_disambiguator=custom_disambiguator,
                         flat_mode_decorated_name=flat_mode_decorated_name)


def decorator(is_function_decorator=True,  # type: bool
              is_class_decorator=True,  # type: bool
              enable_stack_introspection=False,  # type: bool
              custom_disambiguator=None,  # type: Callable[[Any], FirstArgDisambiguation]
              use_signature_trick=True,  # type: bool
              flat_mode_decorated_name=None,  # type: str
              ):
    """
    A decorator to create decorators.

    It support two main modes: "nested", and "flat".

    In "flat" mode your implementation is flat:

    ```python
    def my_decorator(a, b, f=DECORATED):
        # ...
        return <replacement for f>
    ```

    For this mode to be automatically detected, your implementation has to have an argument with default value
    `DECORATED`, or a non-None `decorated` argument name should be provided. This argument will be injected with the
    decorated target when your decorator is used.

    Otherwise the "nested" mode is activated. In this mode your implementation is nested, as usual in python:

    ```python
    def my_decorator(a, b):
        def replace_f(f):
            # ...
            return <replacement for f>
        return replace_f
    ```

    In both modes, because python language does not redirect no-parenthesis usages (@my_decorator) to no-args usages
    (@my_decorator()), `decopatch` tries to disambiguate automatically the type of call. See documentation for details.

    Finally you can use this function to directly create a "signature preserving function wrapper" decorator. This mode
    is called "double flat" because it saves you from 2 levels of nesting. For this, use the `WRAPPED` default value
    instead of `DECORATED`, and include two arguments with default values `F_ARGS` and `F_KWARGS`:

    ```python
    @function_decorator
    def say_hello(person="world", f=WRAPPED, f_args=F_ARGS, f_kwargs=F_KWARGS):
        '''
        This decorator wraps the decorated function so that a nice hello
        message is printed before each call.

        :param person: the person name in the print message. Default = "world"
        '''
        print("hello, %s !" % person)  # say hello
        return f(*f_args, **f_kwargs)  # call f
    ```

    :param is_function_decorator:
    :param is_class_decorator:
    :param enable_stack_introspection:
    :param custom_disambiguator:
    :param use_signature_trick: if set to `True`, generated decorators will have a generic signature but the `help`
        and `signature` modules will still think that they have the specific signature, because by default they
        follow the `__wrapped__` attribute if it is set. See
        https://docs.python.org/3/library/inspect.html#inspect.signature for details.
    :param flat_mode_decorated_name:
    :return:
    """

    if callable(is_function_decorator):
        # called without argument: the first argument is actually the decorated function
        f = is_function_decorator
        return create_decorator(f)
    else:
        # called with argument. Return a decorator function
        def _apply_on(f):
            return create_decorator(f,
                                    is_function_decorator=is_function_decorator,
                                    is_class_decorator=is_class_decorator,
                                    enable_stack_introspection=enable_stack_introspection,
                                    custom_disambiguator=custom_disambiguator,
                                    flat_mode_decorated_name=flat_mode_decorated_name,
                                    use_signature_trick=use_signature_trick)
        return _apply_on


def create_decorator(impl_function,
                     is_function_decorator=True,  # type: bool
                     is_class_decorator=True,  # type: bool
                     enable_stack_introspection=False,  # type: bool
                     custom_disambiguator=None,  # type: Callable[[Any], FirstArgDisambiguation]
                     use_signature_trick=True,  # type: bool
                     flat_mode_decorated_name=None,  # type: Optional[str]
                     ):
    """
    Main function to create a decorator implemented with the `decorator_function` implementation.

    :param impl_function:
    :param is_function_decorator:
    :param is_class_decorator:
    :param enable_stack_introspection:
    :param custom_disambiguator:
    :param use_signature_trick:
    :param flat_mode_decorated_name:
    :return:
    """
    # input checks
    if not is_function_decorator and not is_class_decorator:
        raise ValueError("At least one of `is_function_decorator` and `is_class_decorator` must be True")

    # (1) --- Detect mode and prepare signature to generate --------
    sig_info, f_for_metadata, nested_impl_function = make_decorator_spec(impl_function, flat_mode_decorated_name)
    sig_info.use_signature_trick = use_signature_trick

    # (2) --- Generate according to the situation--------
    # check if the resulting function has any parameter at all
    if len(sig_info.exposed_signature.parameters) == 0:
        # (A) no argument at all. Special handling.
        return create_no_args_decorator(nested_impl_function, function_for_metadata=f_for_metadata)

    else:
        # (B) general case: at least one argument

        # if the decorator has at least 1 mandatory argument, we allow it to be created but its default behaviour
        # is to raise errors only on ambiguous cases. Usually ambiguous cases are rare (not nominal cases)
        disambiguator = create_single_arg_callable_or_class_disambiguator(nested_impl_function,
                                                                          is_function_decorator,
                                                                          is_class_decorator,
                                                                          custom_disambiguator,
                                                                          enable_stack_introspection,
                                                                          signature_knowledge=sig_info)

        if sig_info.is_first_arg_keyword_only:
            # in this case the decorator *can* be used without arguments but *cannot* with one positional argument,
            # which will happen in the no-parenthesis case. We have to modify the signature to allow no-parenthesis
            return create_kwonly_decorator(sig_info, nested_impl_function, disambiguator,
                                           function_for_metadata=f_for_metadata)

        # general case
        return create_general_case_decorator(sig_info, nested_impl_function, disambiguator,
                                             function_for_metadata=f_for_metadata)


def create_no_args_decorator(decorator_function,
                             function_for_metadata=None,
                             ):
    """
    Utility method to create a decorator that has no arguments at all and is implemented by `decorator_function`, in
    implementation-first mode or usage-first mode.

    The created decorator is a function with var-args. When called it checks the length
    (0=called with parenthesis, 1=called without, 2=error).

    Note: we prefer to use this var-arg signature rather than a "(_=None)" signature, because it is more readable for
    the decorator's help.

    :param decorator_function:
    :param function_for_metadata: an alternate function to use for the documentation and module metadata of the
        generated function
    :return:
    """
    if function_for_metadata is None:
        function_for_metadata = decorator_function

    @with_signature(None,
                    func_name=function_for_metadata.__name__,
                    doc=function_for_metadata.__doc__,
                    module_name=function_for_metadata.__module__)
    def new_decorator(*_):
        """
        Code for your decorator, generated by decopatch to handle the case when it is called without parenthesis
        """
        if len(_) == 0:
            # called with no args BUT parenthesis: @foo_decorator().
            return with_parenthesis_usage(decorator_function, *_)

        elif len(_) == 1:
            first_arg_value = _[0]
            if can_arg_be_a_decorator_target(first_arg_value):
                # called with no arg NOR parenthesis: @foo_decorator
                return no_parenthesis_usage(decorator_function, first_arg_value)

        # more than 1 argument or non-decorable argument: not possible
        raise TypeError("Decorator function '%s' does not accept any argument."
                        "" % decorator_function.__name__)

    return new_decorator


_GENERATED_VARPOS_NAME = '_'


def create_kwonly_decorator(sig_info,  # type: SignatureInfo
                            decorator_function,
                            disambiguator,
                            function_for_metadata,
                            ):
    """
    Utility method to create a decorator that has only keyword arguments and is implemented by `decorator_function`, in
    implementation-first mode or usage-first mode.

    When the decorator to create has a mandatory argument, it is exposed "as-is" because it is directly protected.

    Otherwise (if all arguments are optional and keyword-only), we modify the created decorator's signature to add a
    leading var-args, so that users will be able to call the decorator without parenthesis.
    When called it checks the length of the var-positional received:
     - 0 positional=called with parenthesis,
     - 1 and the positional argument is not a callable/class : called with parenthesis
     - 1 and the positional argument is a callable/class: disambiguation is required to know if this is without
     parenthesis or with positional arg
     - 2 positional=error).

    Note: we prefer to use this var-arg signature rather than a "(_=None)" signature, because it is more readable for
    the decorator's help.

    :param sig_info:
    :param decorator_function:
    :param function_for_metadata: an alternate function to use for the documentation and module metadata of the
        generated function
    :return:
    """
    if sig_info.is_first_arg_mandatory:
        # The first argument is mandatory AND keyword. So we do not need to change the signature to be fully protected
        # indeed python will automatically raise a `TypeError` when users will use this decorator without parenthesis
        # or with positional arguments.
        @with_signature(sig_info.exposed_signature,
                        func_name=function_for_metadata.__name__,
                        doc=function_for_metadata.__doc__,
                        modulename=function_for_metadata.__module__)
        def new_decorator(*no_args, **kwargs):
            """
            Code for your decorator, generated by decopatch to handle the case when it is called without parenthesis
            """
            # this is a parenthesis call, because otherwise a `TypeError` would already have been raised by python.
            return with_parenthesis_usage(decorator_function, *no_args, **kwargs)

        return new_decorator
    elif sig_info.use_signature_trick:
        # no need to modify the signature, we will expose *args, **kwargs
        pass
    else:
        # modify the signature to add a var-positional first
        gen_varpos_param = Parameter(_GENERATED_VARPOS_NAME, kind=Parameter.VAR_POSITIONAL)
        sig_info.exposed_signature = add_signature_parameters(sig_info.exposed_signature, first=[gen_varpos_param])

    # we can fallback to the same case than varpositional
    return create_general_case_decorator(sig_info, decorator_function, disambiguator,
                                         function_for_metadata=function_for_metadata)


def create_general_case_decorator(sig_info,  # type: SignatureInfo
                                  impl_function,
                                  disambiguator,
                                  function_for_metadata,
                                  ):
    """
    This method supports both with-trick and without-trick

    :param sig_info:
    :param impl_function:
    :param disambiguator:
    :param function_for_metadata: an alternate function to use for the documentation and module metadata of the
        generated function
    :return:
    """
    # Note: since we expose a decorator with a preserved signature and not (*args, **kwargs)
    # we lose the information about the number of arguments *actually* provided.
    # `@with_signature` will send us all arguments, including the defaults (because it has no way to
    # determine what was actually provided by the user and what is just the default). So in this decorator we may
    # receive several kwargs
    # - even if user did not provide them
    # - and even if user provided them as positional !! (except for var-positional and fuutre positional-only args)

    @with_signature(None if sig_info.use_signature_trick else sig_info.exposed_signature,
                    func_name=function_for_metadata.__name__,
                    doc=function_for_metadata.__doc__,
                    module_name=function_for_metadata.__module__)
    def new_decorator(*args, **kwargs):
        """
        Code for your decorator, generated by decopatch to handle the case when it is called without parenthesis
        """
        # disambiguate
        dk = DecoratorUsageInfo(sig_info, args, kwargs)
        disambiguation_result = disambiguate_call(dk, disambiguator)

        # call
        return call_in_appropriate_mode(impl_function, dk, disambiguation_result)

    # trick to declare that our true signature is different than our actual one
    if sig_info.use_signature_trick:
        # thanks to setting this field, python help() and signature() will be tricked without compromising the
        # actual code signature (so, no dynamic function creation in @with_signature above).
        # Indeed by default they follow the `__wrapped__` attribute if it is set. See
        # https://docs.python.org/3/library/inspect.html#inspect.signature for details.
        new_decorator.__wrapped__ = impl_function

    return new_decorator
