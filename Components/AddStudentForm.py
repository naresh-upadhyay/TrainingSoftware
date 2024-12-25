import flet as ft

class AddStudentForm(ft.Container):
    def __init__(self, close_dialog):
        super().__init__()
        self.close_dialog = close_dialog

        # Define fields
        self.name_field = ft.TextField(label="Student Name", hint_text="Enter the student's name")
        self.age_field = ft.TextField(
            label="Age",
            hint_text="Enter the student's age",
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        self.dob_field = ft.DatePicker()  # DatePicker doesn't have a label argument
        self.gender_toggle = ft.Switch(label="Gender (Male/Female)")
        self.grade_field = ft.Dropdown(
            label="Grade",
            options=[
                ft.dropdown.Option("Grade 1"),
                ft.dropdown.Option("Grade 2"),
                ft.dropdown.Option("Grade 3"),
            ],
        )
        self.role_field = ft.TextField(label="Role", hint_text="Enter role (e.g., Monitor)")
        self.description_field = ft.TextField(
            label="Description",
            hint_text="Enter additional details",
            multiline=True,
            height=100,
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

            if not self.dob_field.value:
                self.dob_field.error_text = "Date of Birth is required"
                is_valid = False
            else:
                self.dob_field.error_text = None

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
                self.age_field,
                ft.Column([ft.Text("Date of Birth"), self.dob_field]),  # Wrap DatePicker with a Text label
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

        # Wrap the Column in a ListView, which is the scrollable container for the whole form.
        scrollable_content = ft.Container(
                content=form_column,
                margin=ft.Margin(0,10,0,0),
                padding=ft.Padding(0,10,0,10),
                #border=ft.border.all(1, ft.colors.BLACK)
            )

        # Content inside the container
        self.content = scrollable_content
        #self.border = ft.border.all(1, ft.colors.BLACK)
        #self.border_radius = ft.border_radius.all(5)
