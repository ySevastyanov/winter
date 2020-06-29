from typing import Type

from winter.data.repository import Repository
from winter_sqlalchemy import sqla_crud

_repository_implementations = {}


class DummyImplementation:
    pass


def sqla_repository_implementation(for_repository):
    if not issubclass(for_repository, Repository):
        raise TypeError('for_repository class must be inherited from Repository')

    def decorator(repository_implementation_cls: Type):
        global _repository_implementations
        _repository_implementations[for_repository] = repository_implementation_cls
        return repository_implementation_cls

    return decorator


def get_repository_implementation(for_repository) -> Type:
    global _repository_implementations
    return _repository_implementations.get(for_repository, sqla_crud(for_repository))
