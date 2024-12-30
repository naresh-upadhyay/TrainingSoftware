import json
import flet as ft

from Components.TableColumns import TableGenerator


class TableViewNew(ft.Column):
    def __init__(
            self,
            row_font_size=12,
            header_font_size=15,
            action_icon_size=16,
            checkbox_scale=1,
            row_spacing=5,
            padding=2,
            row_min_height=20,
            row_max_height=30,
            heading_row_height=30,
            column_spacing=80,
            rows_per_page=20,
            table_header={},
            table_data=[],
            **kwargs
    ):
        super().__init__(**kwargs)

        self.table_header = table_header
        self.table_data = table_data
        self.current_page = 1
        self.selected_rows = set()
        self.select_all = False

        # Customizable Settings
        self.row_font_size = row_font_size
        self.header_font_size = header_font_size
        self.action_icon_size = action_icon_size
        self.checkbox_scale = checkbox_scale
        self.row_spacing = row_spacing
        self.padding = padding
        self.row_min_height = row_min_height
        self.row_max_height = row_max_height
        self.column_spacing = column_spacing
        self.rows_per_page = rows_per_page
        self.heading_row_height = heading_row_height

    def build(self):
        """Build the Flet UI and return the root control."""
        self.data_table = ft.DataTable(
            columns=self.get_table_columns(),
            #rows=self.get_table_rows(),  # Set the initial rows
            column_spacing=self.column_spacing,  # Space between columns
            data_row_min_height=self.row_min_height,  # Minimum row height
            data_row_max_height=self.row_max_height,  # Maximum row height
            border=ft.border.all(1, "#E5E5E5"),
            vertical_lines=ft.BorderSide(1, "#E5E5E5"),
            horizontal_lines=ft.BorderSide(1, "#E5E5E5"),
            heading_row_height=self.heading_row_height
        )

        # Create a Scrollable container for the DataTable
        scrollable_table = ft.Column(
            controls=[self.data_table],
            scroll=True,  # Enable scrolling
        )

        # Pagination controls
        self.pagination_controls = ft.Row(
            controls=self.get_bottom_buttons(),
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # Return the container with the scrollable table and pagination controls
        return ft.Column(
            controls=[scrollable_table, self.pagination_controls],
            spacing=10,
        )

    def get_table_rows(self):
        """Generate the rows for the table."""
        rows = []
        start = (self.current_page - 1) * self.rows_per_page
        end = start + self.rows_per_page
        for row in self.table_data[start:end]:
            rows.append(
                ft.DataRow(
                    cells=self.get_data_for_row(row, self.table_header)
                )
            )
        return rows

    def checkbox_changed(self, e, row_id):
        """Handle individual checkbox state change."""
        if e.control.value:
            self.selected_rows.add(row_id)
        else:
            self.selected_rows.remove(row_id)

        # Update the "Select All" checkbox state
        if len(self.selected_rows) == len(self.get_rows_for_page()):
            self.select_all = True
        else:
            self.select_all = False

        # If no rows are selected, uncheck the "Select All" checkbox
        if not self.selected_rows:
            self.select_all = False

        self.update_table()

    def select_all_changed(self, e):
        """Handle "Select All" checkbox state change."""
        self.select_all = e.control.value
        if self.select_all:
            self.selected_rows = set(row["id"] for row in self.get_rows_for_page())
        else:
            self.selected_rows = set()

        self.update_table()

    def edit_row(self, row):
        print(f"Edit: {row}")

    def delete_row(self, row):
        """Delete a single row."""
        self.table_data = [r for r in self.data if r["id"] != row["id"]]
        self.selected_rows.discard(row["id"])  # Remove from selection if deleted
        self.update_table()
        self.adjust_page_after_deletion()

    def delete_selected_rows(self, e):
        """Delete all selected rows."""
        self.table_data = [r for r in self.data if r["id"] not in self.selected_rows]
        self.selected_rows.clear()  # Clear selected rows after deletion
        self.select_all = False  # Uncheck "Select All" when all selected rows are deleted
        self.update_table()
        self.adjust_page_after_deletion()

    def adjust_page_after_deletion(self):
        """Adjust page and re-calculate total pages after deletion."""
        total_pages = self.total_pages()

        # If current page exceeds total pages, go to the last page
        if self.current_page > total_pages:
            self.current_page = total_pages

        self.update_table()

    def go_to_previous_page(self, e):
        """Handle page change to the previous page."""
        if self.current_page > 1:
            self.current_page -= 1
            self.update_table()

    def go_to_next_page(self, e):
        """Handle page change to the next page."""
        if self.current_page < self.total_pages():
            self.current_page += 1
            self.update_table()

    def total_pages(self):
        """Calculate the total number of pages based on data size."""
        return (len(self.table_data) + self.rows_per_page - 1) // self.rows_per_page

    def get_rows_for_page(self):
        """Get rows for the current page."""
        start = (self.current_page - 1) * self.rows_per_page
        end = start + self.rows_per_page
        return self.data[start:end]

    def get_data_for_row(self, row, header):
        """Get row data for table."""
        row_data = []

        # Checkbox for selection in row
        row_data.append(ft.DataCell(
            ft.CupertinoCheckbox(
                on_change=lambda e, row_id=row["id"]: self.checkbox_changed(e, row_id),
                value=row["id"] in self.selected_rows,
                scale=self.checkbox_scale  # Use the scale passed to the constructor
            )
        ))

        # Other cells (ID, Name, Age) with reduced padding
        for key in header.keys():
            if key != "id" and key != "action":
                row_data.append(ft.DataCell(
                    ft.Text(str(row[key]), size=self.row_font_size),
                ))

        # Action buttons (Edit, Delete)
        row_data.append(ft.DataCell(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.EDIT,
                        on_click=lambda e, row=row: self.edit_row(row),
                        icon_size=self.action_icon_size  # Use the action icon size passed
                    ),
                    ft.IconButton(
                        icon=ft.icons.DELETE,
                        on_click=lambda e, row=row: self.delete_row(row),
                        icon_size=self.action_icon_size  # Use the action icon size passed
                    ),
                ],
                spacing=self.row_spacing,  # Use the row spacing passed
            )
        ))

        return row_data

    def get_bottom_buttons(self):
        """Generate pagination controls."""
        bottom_buttons = [
            ft.ElevatedButton("Previous", on_click=self.go_to_previous_page),
            ft.Text(f"Page {self.current_page} of {self.total_pages()}", size=14, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton("Next", on_click=self.go_to_next_page),
            ft.ElevatedButton("Delete Selected", on_click=self.delete_selected_rows),
        ]
        return bottom_buttons

    def get_table_columns(self):
        """Generate columns for the table."""
        # Example usage:
        table_header = {
            "columns": [
                {
                    "field_name": "select",
                    "header_name": "",
                    "visible": True,
                    "searchable": False,
                    "sortable": False,
                    "alignment": "center",
                    "tooltip": "Select row",
                    "field_type": "checkbox",
                    "config": {
                        "checkbox_column": True,
                        "actions": []
                    }
                },
                {
                    "field_name": "id",
                    "header_name": "ID",
                    "visible": True,
                    "searchable": False,
                    "sortable": True,
                    "alignment": "center",
                    "tooltip": "Unique identifier",
                    "field_type": "text",
                    "config": {
                        "format": None,
                        "actions": []
                    }
                },
                {
                    "field_name": "name",
                    "header_name": "Name",
                    "visible": True,
                    "searchable": True,
                    "sortable": True,
                    "alignment": "left",
                    "tooltip": "Full name of the user",
                    "field_type": "text",
                    "config": {
                        "format": None,
                        "actions": []
                    }
                },
                {
                    "field_name": "actions",
                    "header_name": "Actions",
                    "visible": True,
                    "searchable": False,
                    "sortable": False,
                    "alignment": "center",
                    "tooltip": "Actions for the row",
                    "field_type": "actions",
                    "config": {
                        "actions": [
                            {
                                "type": "button",
                                "label": "Edit",
                                "icon": "edit",
                                "callback": "edit_row"
                            },
                            {
                                "type": "button",
                                "label": "Delete",
                                "icon": "delete",
                                "callback": "delete_row"
                            }
                        ]
                    }
                }
            ]
        }

        # Instantiate TableGenerator and get columns
        table_gen = TableGenerator(table_header,self)
        columns = table_gen.get_table_columns()

        # Print out the generated columns for debugging purposes
        for column in columns:
            print(column)

        return columns

    def update_table(self):
        """Update the rows after actions like delete or checkbox change."""
        self.pagination_controls.controls = self.get_bottom_buttons()
        self.data_table.columns = self.get_table_columns()
        self.data_table.rows = self.get_table_rows()
        self.update()

