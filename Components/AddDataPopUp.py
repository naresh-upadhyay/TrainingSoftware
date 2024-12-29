import flet as ft
import datetime

from Components.FormDataManager import FormDataManager
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
        self.form_manager = FormDataManager()
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
                self.form_manager.register_field(
                    field["key"],
                    form_field.get(),
                    field["mandatory"],
                    field["label"],
                )
                tab_fields.append(form_field.get())

            tabs.append(
                ft.Tab(
                    text=tab_data["tabTitle"],
                    content=ft.Container(
                        ft.Column(tab_fields, spacing=10), margin=ft.Margin(0, 10, 0, 0)
                    ),
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
        errors = self.form_manager.validate()
        if errors:
            print("Validation errors:")
            for error in errors:
                print(error)
        else:
            form_values = self.form_manager.get_form_values()
            print("Form submitted successfully:")
            for key, value in form_values.items():
                print(f"{key}: {value}")

        self.close_dialog(e)

    def open_date_picker(self, key, e):
        def handle_date_change(date_event):
            selected_date = date_event.control.value
            field = self.form_manager.form_data[key]["field"]
            field.controls[1].value = selected_date
            e.page.update()

        # Create a new DatePicker instance or reuse an existing one
        if not hasattr(self, "date_picker"):
            self.date_picker = ft.DatePicker(
                first_date=datetime.date(1900, 1, 1),
                last_date=datetime.date(2100, 12, 31),
                on_change=handle_date_change,
            )

        # Ensure the DatePicker is bound to the page's dialog
        e.page.dialog = self.date_picker
        self.date_picker.open = True
        e.page.update()
