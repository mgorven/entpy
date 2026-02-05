from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from entpy.framework.fields.core import Field, FieldWithDefault
from entpy.gencode.utils import ImportedObject

if TYPE_CHECKING:
    from entpy.framework.pattern import Pattern


class Descriptor(ABC):
    """
    A descriptor is a class that describes how an Ent should be handled.
    It might be abstract (Pattern) or concrete (Schema).
    """

    @abstractmethod
    def get_fields(self) -> list[Field]:
        pass

    def get_patterns(self) -> list["Pattern"]:
        return []

    def get_sorted_fields(self) -> list[Field]:
        return _sort_fields(self.get_fields())

    def get_all_fields(self) -> list[Field]:
        # First gather all the fields
        fields = self.get_fields()
        for pattern in self.get_patterns():
            fields += pattern.get_all_fields()
        return _sort_fields(fields)

    def get_description(self) -> str:
        return ""

    def get_mixins(self) -> list[ImportedObject]:
        return []


def _sort_fields(fields: list[Field]) -> list[Field]:
    # Separate nullable fields, fields with defaults, and non-nullable fields
    # We always process the mandatory fields first
    nullable_fields: list[Field] = []
    non_nullable_fields: list[Field] = []
    fields_with_default: list[Field] = []

    for f in fields:
        if isinstance(f, FieldWithDefault) and f.generate_default():
            fields_with_default.append(f)
        elif f.nullable:
            nullable_fields.append(f)
        else:
            non_nullable_fields.append(f)

    fields_with_default.sort(key=lambda f: f.name)
    nullable_fields.sort(key=lambda f: f.name)
    non_nullable_fields.sort(key=lambda f: f.name)

    return non_nullable_fields + fields_with_default + nullable_fields
