import flet as ft

class FormDataManager:
    def __init__(self):
        self.form_data = {}

    def register_field(self, key, field, mandatory, label):
        self.form_data[key] = {"field": field, "mandatory": mandatory, "label": label}

    def validate(self):
        errors = []
        for key, field_data in self.form_data.items():
            field = field_data["field"]
            mandatory = field_data["mandatory"]
            label = field_data["label"]

            value = None
            if isinstance(field, ft.TextField):
                value = field.value
            elif isinstance(field, ft.Checkbox):
                value = field.value
            elif isinstance(field, ft.Column):  # Date field
                value = field.controls[1].value

            if mandatory and not value:
                errors.append(f"Field '{label}' is mandatory.")

        return errors

    def get_form_values(self):
        form_values = {}
        for key, field_data in self.form_data.items():
            field = field_data["field"]
            value = None
            if isinstance(field, ft.TextField):
                value = field.value
            elif isinstance(field, ft.Checkbox):
                value = field.value
            elif isinstance(field, ft.Column):
                value = field.controls[1].value

            form_values[key] = value
        return form_values
