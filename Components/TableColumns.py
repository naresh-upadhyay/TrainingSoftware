from xmlrpc.client import DateTime

import flet as ft


class TableGenerator:
    def __init__(self, table_header, table_view, checkbox_scale=1.0, header_font_size=14, select_all=False):
        self.table_header = table_header
        self.checkbox_scale = checkbox_scale
        self.header_font_size = header_font_size
        self.select_all = select_all
        self.table_view = table_view
        self.sort_order = {}  # Keep track of sorting order for each column

    def select_all_changed(self, e):
        """Handle the change event for the 'Select All' checkbox."""
        # Implement the behavior for selecting/deselecting all rows
        pass

    def get_table_columns(self):
        """Generate columns for the table dynamically based on the provided headers."""
        columns = []
        # Iterate through the columns specified in the header
        for column in self.table_header['columns']:
            if column.get('visible', True):  # Include only visible columns
                header_name = column.get('header_name', '')
                field_type = column.get('field_type', 'text')  # Default to 'text'
                sortable = column.get('sortable', False)
                tooltip = column.get('tooltip', '')

                # Create sorting icon based on sort order
                sort_icon = None
                if sortable:
                    current_sort_order = self.sort_order.get(header_name, "asc")
                    if current_sort_order == 'asc':
                        sort_icon = ft.Icon(name=ft.icons.ARROW_UPWARD, tooltip="Sort Ascending")
                    elif current_sort_order == 'desc':
                        sort_icon = ft.Icon(name=ft.icons.ARROW_DOWNWARD, tooltip="Sort Descending")

                # Create a DataColumn based on field type
                if field_type == 'checkbox':
                    data_column = ft.DataColumn(
                        label=ft.Checkbox(
                            value=False,  # Default value, you may want to bind it to row data
                            on_change=self.select_all_changed,
                            scale=self.checkbox_scale,
                            tristate=True
                        ),
                        tooltip=tooltip
                    )
                elif field_type in ['text', 'number', 'date']:
                    numeric = (field_type == 'number')
                    data_column = ft.DataColumn(
                        label=ft.Row(
                            [ft.Text(header_name, size=self.header_font_size, weight=ft.FontWeight.BOLD)] +
                            ([sort_icon] if sort_icon else [])
                        ),
                        numeric=numeric,
                        tooltip=tooltip,
                        on_sort=(self.sort_column if sortable else None)
                    )
                elif field_type == 'actions':
                    actions = column.get('config', {}).get('actions', [])
                    buttons = []
                    for action in actions:
                        label = action.get('label', '')
                        icon = action.get('icon', 'info')
                        callback = action.get('callback', '')
                        button = ft.IconButton(
                            icon=icon,
                            on_click=lambda e, callback=callback: self.handle_action(callback),
                            tooltip=label
                        )
                        buttons.append(button)
                    data_column = ft.DataColumn(
                        label=ft.Row(buttons)
                    )

                columns.append(data_column)

        return columns

    def sort_column(self, e):
        """Handle sorting logic and toggle sort order."""
        column_index = e.column_index  # Access column_index from the event object
        column_name = self.table_header['columns'][column_index].get('header_name', '')  # Get column name using index

        current_sort_order = self.sort_order.get(column_name, None)

        # Toggle sort order
        if current_sort_order == 'asc':
            self.sort_order[column_name] = 'desc'
        else:
            self.sort_order[column_name] = 'asc'

        # Update sorting indicator icons
        print(f"Sorting column: {column_name} in {self.sort_order[column_name]} order")
        # Optionally, trigger the sorting of table data based on the column and order
        self.update_sort_icons()
        self.table_view.update_table()

    def update_sort_icons(self):
        """Update sorting indicator icons after sorting."""
        for column in self.table_header['columns']:
            header_name = column.get('header_name', '')
            sort_icon = None
            current_sort_order = self.sort_order.get(header_name, None)

            if current_sort_order == 'asc':
                sort_icon = ft.Icon(name=ft.icons.ARROW_UPWARD, tooltip="Sort Ascending")
            elif current_sort_order == 'desc':
                sort_icon = ft.Icon(name=ft.icons.ARROW_DOWNWARD, tooltip="Sort Descending")

            # Update the icon next to the column header
            # Update logic can be more complex depending on how you want to reflect the icon changes in the UI
            print(f"Column '{header_name}' has sort icon: {sort_icon}")

    def handle_action(self, callback):
        """Handle action callback (e.g., edit_row, delete_row, etc.)"""
        # Implement logic for actions like 'edit_row' and 'delete_row'
        print(f"Action triggered: {callback}")
