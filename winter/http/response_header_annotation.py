from typing import Any
from typing import MutableMapping

import dataclasses

from ..converters import convert
from ..core import annotate_method


class _ResponseHeaderMeta(type):
    def __getitem__(self, value_type):
        assert isinstance(value_type, type), 'value_type must be a type'
        return _ResponseHeaderMeta.__new__(
            type(self),
            f'{self.__name__}[{value_type.__name__}]',
            (self, ),
            {
                '_value_type': value_type,
            },

        )


@dataclasses.dataclass
class ResponseHeaderAnnotation:
    # TODO: add inspector for this annotation
    header_name: str
    argument_name: str


def response_header(header_name: str, argument_name: str):
    def wrapper(func_or_method):
        annotation = ResponseHeaderAnnotation(header_name, argument_name)
        annotation_decorator = annotate_method(annotation)
        method = annotation_decorator(func_or_method)
        argument = method.get_argument(argument_name)
        method_name = method.func.__name__
        assert argument is not None, f'Not found argument "{argument_name}" in "{method_name}"'
        return method
    return wrapper


class ResponseHeader(metaclass=_ResponseHeaderMeta):
    _value_type = str

    def __init__(self, headers: MutableMapping[str, Any], header_name: str):
        self._headers = headers
        self._header_name = header_name.lower()

    def __repr__(self):
        return f'{self.__class__.__name__}({self._header_name!r})'

    def set(self, value):
        # TODO: add value validation against self._value_type
        self._headers[self._header_name] = value
