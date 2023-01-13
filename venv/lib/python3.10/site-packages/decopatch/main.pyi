from typing import Any, Callable, Optional, Protocol, TypeVar, overload

from decopatch.utils_disambiguation import FirstArgDisambiguation
from decopatch.utils_modes import SignatureInfo

try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec

P = ParamSpec("P")
F = TypeVar("F", bound=Callable[..., Any])

class _Decorator(Protocol[P]):
    """
    This is callable Protocol, to distinguish between cases where
    created decorator is called as `@decorator` or `@decorator()`
    """

    # decorator is called without parenthesis: @decorator
    @overload
    def __call__(self, func: F) -> F: ...
    # decorator is called with options or parenthesis: @decorator(some_option=...)
    @overload
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> Callable[[F], F]: ...

# @function_decorator is called without options or parenthesis
@overload
def function_decorator(
    enable_stack_introspection: Callable[P, Any],
    custom_disambiguator: Callable[[Any], FirstArgDisambiguation] = ...,
    flat_mode_decorated_name: Optional[str] = ...,
) -> _Decorator[P]: ...

# @function_decorator() is called with options or parenthesis.
@overload
def function_decorator(
    enable_stack_introspection: bool = ...,
    custom_disambiguator: Callable[[Any], FirstArgDisambiguation] = ...,
    flat_mode_decorated_name: Optional[str] = ...,
) -> Callable[[Callable[P, Any]], _Decorator[P]]: ...
def class_decorator(
    enable_stack_introspection: bool = ...,
    custom_disambiguator: Callable[[Any], FirstArgDisambiguation] = ...,
    flat_mode_decorated_name: Optional[str] = ...,
): ...
def decorator(
    is_function_decorator: bool = ...,
    is_class_decorator: bool = ...,
    enable_stack_introspection: bool = ...,
    custom_disambiguator: Callable[[Any], FirstArgDisambiguation] = ...,
    use_signature_trick: bool = ...,
    flat_mode_decorated_name: str = ...,
): ...
def create_decorator(
    impl_function,
    is_function_decorator: bool = ...,
    is_class_decorator: bool = ...,
    enable_stack_introspection: bool = ...,
    custom_disambiguator: Callable[[Any], FirstArgDisambiguation] = ...,
    use_signature_trick: bool = ...,
    flat_mode_decorated_name: Optional[str] = ...,
): ...
def create_no_args_decorator(
    decorator_function, function_for_metadata: Any | None = ...
): ...
def create_kwonly_decorator(
    sig_info: SignatureInfo, decorator_function, disambiguator, function_for_metadata
): ...
def create_general_case_decorator(
    sig_info: SignatureInfo, impl_function, disambiguator, function_for_metadata
): ...
