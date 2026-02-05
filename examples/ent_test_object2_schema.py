from ent_test_thing_pattern import EntTestThingPattern
from ent_test_pattern_pattern import EntTestPatternPattern
from entpy import (
    Action,
    AllowAll,
    EdgeDelegate,
    PrivacyRule,
    Field,
    Pattern,
    Schema,
    StringField,
)
from entpy.gencode.utils import ImportedObject


class EntTestObject2Schema(Schema):
    def get_patterns(self) -> list[Pattern]:
        return [EntTestThingPattern(), EntTestPatternPattern()]

    def get_fields(self) -> list[Field]:
        return [StringField("some_field", 100)]

    def get_privacy_config(self, action: Action) -> list[EdgeDelegate | PrivacyRule]:
        return [AllowAll()]

    def get_mixins(self) -> list[ImportedObject]:
        return [ImportedObject("ent_test_object2_mixin", "EntTestObject2Mixin")]
