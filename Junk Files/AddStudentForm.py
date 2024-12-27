import datetime

import flet as ft

class AddStudentForm(ft.Container):
    def __init__(self, close_dialog, border_width=0.1):
        super().__init__()
        self.close_dialog = close_dialog
        self.border_width =border_width
        # Define fields
        self.name_field = ft.TextField(label="Student Name", hint_text="Enter the student's name",border_width=self.border_width)
        self.age_field = ft.ElevatedButton(
            "Pick date of birth",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: e.page.open(
                ft.DatePicker(
                    first_date=datetime.datetime(year=1800, month=10, day=1),
                    last_date=datetime.datetime(year=2500, month=10, day=1),
                    on_change=self.handle_change,
                    on_dismiss=self.handle_dismissal,
                )
            ),
        )
        self.gender_toggle = ft.Switch(label="Gender (Male/Female)")
        self.grade_field = ft.Dropdown(
            label="Grade",
            options=[
                ft.dropdown.Option("Grade 1"),
                ft.dropdown.Option("Grade 2"),
                ft.dropdown.Option("Grade 3"),
            ],
            border_width=self.border_width
        )
        self.role_field = ft.TextField(label="Role", hint_text="Enter role (e.g., Monitor)",border_width=self.border_width)
        self.description_field = ft.TextField(
            label="Description",
            hint_text="Enter additional details",
            multiline=True,
            height=100,
            border_width=self.border_width
        )

        # Validation and submission logic
        def validate_and_submit(e):
            is_valid = True

            # Validate each field
            if not self.name_field.value:
                self.name_field.error_text = "Name is required"
                is_valid = False
            else:
                self.name_field.error_text = None

            if not self.age_field.value or not self.age_field.value.isdigit() or int(self.age_field.value) <= 0:
                self.age_field.error_text = "Valid age is required"
                is_valid = False
            else:
                self.age_field.error_text = None

            if self.gender_toggle.value is None:
                self.gender_toggle.error_text = "Gender selection is required"
                is_valid = False
            else:
                self.gender_toggle.error_text = None

            if not self.grade_field.value:
                self.grade_field.error_text = "Grade is required"
                is_valid = False
            else:
                self.grade_field.error_text = None

            if not self.role_field.value:
                self.role_field.error_text = "Role is required"
                is_valid = False
            else:
                self.role_field.error_text = None

            # If all validations pass
            if is_valid:
                print("Student Added Successfully")
                self.close_dialog(e)  # Close the dialog after submission
            self.update()

        # Wrap the form fields inside a Column
        form_column = ft.Column(
            [
                self.name_field,
                ft.Row([ft.Text("Date of Birth"), self.age_field]),  # Wrap DatePicker with a Text label
                self.gender_toggle,
                self.grade_field,
                self.role_field,
                self.description_field,
                ft.Row(
                    [
                        ft.ElevatedButton("Submit", on_click=validate_and_submit),
                        ft.ElevatedButton("Cancel", on_click=self.close_dialog),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            spacing=10,
        )

        tabsData = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Info",
                    content=ft.Container(content=form_column,margin=ft.Margin(0,10,0,0) ),
                ),
                ft.Tab(
                    text="Student Details",
                    #tab_content=ft.Icon(ft.Icons.SEARCH),
                    content=ft.Text("Student Details"),
                ),
                ft.Tab(
                    text="More Info",
                    content=ft.Text("More Info"),
                ),
            ],
            scrollable=None,
            expand=None,
            expand_loose=None,
        )

        # Wrap the Column in a ListView, which is the scrollable container for the whole form.
        scrollable_content = ft.Container(
                content=tabsData,
                margin=ft.Margin(0,10,0,0),
                padding=ft.Padding(0,10,0,10),
                #border=ft.border.all(1, ft.colors.BLACK)
            )

        # Content inside the container
        self.content = scrollable_content
        #self.border = ft.border.all(1, ft.colors.BLACK)
        #self.border_radius = ft.border_radius.all(5)


    def handle_change(self, e):
        self.age_field.text = e.control.value.strftime('%Y-%m-%d')
        print(e.control.value.strftime('%Y-%m-%d'))
        e.page.update()

    def handle_dismissal(self, e):
        print(e.control.value.strftime('%Y-%m-%d'))
        e.page.update()
