from entpy.framework.descriptor import Descriptor
from entpy.gencode.generated_content import GeneratedContent


def generate(descriptor: Descriptor, base_name: str) -> GeneratedContent:
    return GeneratedContent(
        imports=[
            f"from {descriptor.__class__.__module__} import {descriptor.__class__.__name__}"
        ],
        code=f"""def _get_field(field_name: str) -> Field:
        schema = {base_name}Schema()
        fields = schema.get_all_fields()
        field = next(
            filter(
                lambda field: field.name == field_name,
                fields,
            )
        )
        if not field:
            raise ValueError(f"Unknown field: {{field_name}}")
        return field
""",
    )
