import flet as ft
import datetime
from Components.FormField import FormField


class AddDataPopUp:
    def __init__(self, tabs_data):
        self.popup_width = 800
        self.title_value = "Add Data"
        self.footer_save_title = "Save"
        self.footer_close_title = "Close"
        self.content_padding = (20, 20, 20, 20)
        self.border_radius = 8

        self.tabs_data = tabs_data

        self.form_data = {}
        self.dlg_modal = self._create_dialog()

    def _create_dialog(self):
        return ft.AlertDialog(
            modal=True,
            title=self._create_title(),
            content=self._create_content(),
            actions=self._create_actions(),
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed"),
            shape=ft.RoundedRectangleBorder(radius=self.border_radius),
            scrollable=True,
        )

    def _create_title(self):
        return ft.Row(
            controls=[
                ft.Text(self.title_value, style=ft.TextThemeStyle.HEADLINE_SMALL),
                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    tooltip="Close",
                    on_click=self.close_dialog,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def _create_content(self):
        tabs = []
        for tab_data in self.tabs_data:
            tab_fields = []
            for field in tab_data["inputFields"]:
                form_field = FormField(
                    key=field["key"],
                    label=field["label"],
                    field_type=field["type"],
                    mandatory=field["mandatory"],
                    callback=self.open_date_picker,
                )
                self.form_data[field["key"]] = {
                    "field": form_field.get(),
                    "mandatory": field["mandatory"],
                    "label": field["label"],
                }
                tab_fields.append(form_field.get())

            tabs.append(
                ft.Tab(
                    text=tab_data["tabTitle"],
                    content=ft.Container(ft.Column(tab_fields, spacing=10), margin=ft.Margin(0,10,0,0)),
                )
            )

        return ft.Tabs(tabs=tabs)

    def _create_actions(self):
        return [
            ft.TextButton(self.footer_save_title, on_click=self.save_form_data),
            ft.TextButton(self.footer_close_title, on_click=self.close_dialog),
        ]

    def open_dialog(self, e):
        e.page.dialog = self.dlg_modal
        self.dlg_modal.open = True
        e.page.update()

    def close_dialog(self, e):
        self.dlg_modal.open = False
        e.page.update()

    def save_form_data(self, e):
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

        if errors:
            print("Validation errors:")
            for error in errors:
                print(error)
        else:
            print("Form submitted successfully:")
            for key, field_data in self.form_data.items():
                field = field_data["field"]
                value = None
                if isinstance(field, ft.TextField):
                    value = field.value
                elif isinstance(field, ft.Checkbox):
                    value = field.value
                elif isinstance(field, ft.Column):
                    value = field.controls[1].value
                print(f"{key}: {value}")

        self.close_dialog(e)

    def open_date_picker(self, key, e):
        def handle_date_change(date_event):
            selected_date = date_event.control.value
            field = self.form_data[key]["field"]
            field.controls[1].value = selected_date
            e.page.update()

        # Create and open the DatePicker immediately
        date_picker = ft.DatePicker(
            first_date=datetime.date(1900, 1, 1),
            last_date=datetime.date(2100, 12, 31),
            on_change=handle_date_change,
        )

        # Add DatePicker to the page and open it
        e.page.dialog = date_picker
        date_picker.open = True
        e.page.update()  # Force page update to render the DatePicker instantly
