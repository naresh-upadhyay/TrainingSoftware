import flet as ft
import functools

class FormField:
    def __init__(self, key, label, field_type, mandatory, callback=None):
        self.key = key
        self.label = label
        self.field_type = field_type
        self.mandatory = mandatory
        self.callback = callback

        self.field = self._create_field()

    def _create_field(self):
        if self.field_type == "text":
            return ft.TextField(label=self.label)
        elif self.field_type == "email":
            return ft.TextField(label=self.label, keyboard_type=ft.KeyboardType.EMAIL)
        elif self.field_type == "password":
            return ft.TextField(label=self.label, password=True)
        elif self.field_type == "tel":
            return ft.TextField(label=self.label, keyboard_type=ft.KeyboardType.PHONE)
        elif self.field_type == "number":
            return ft.TextField(label=self.label, keyboard_type=ft.KeyboardType.NUMBER)
        elif self.field_type == "checkbox":
            return ft.Checkbox(label=self.label)
        elif self.field_type == "date":
            # Create a button and text field for date selection
            return ft.Column(
                [
                    ft.ElevatedButton(
                        text=f"Pick {self.label}",
                        icon=ft.Icons.CALENDAR_MONTH,
                        on_click=functools.partial(self.callback, self.key) if self.callback else None,
                    ),
                    ft.Text(""),
                ]
            )
        else:
            raise ValueError(f"Unsupported field type: {self.field_type}")

    def get(self):
        return self.field
