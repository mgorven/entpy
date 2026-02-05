from generated.ent_test_object2_models import EntTestObject2Gen


class EntTestObject2Mixin(EntTestObject2Gen):
    def some_field_upper(self) -> str:
        return self.some_field.upper()
