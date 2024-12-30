import flet as ft
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from typing import List, Dict, Callable


# Class to handle actions on the table, like Edit/Delete
class TableAction:
    def __init__(self, action_type: str, label: str, callback: Callable):
        self.action_type = action_type
        self.label = label
        self.callback = callback


# Class to define the structure of each column
class DataColumn:
    def __init__(self, field_name: str, header_name: str, field_type: str, visible: bool,
                 searchable: bool, sortable: bool, alignment: str, tooltip: str, config: dict):
        self.field_name = field_name
        self.header_name = header_name or field_name.capitalize()  # Default header is field_name capitalized
        self.field_type = field_type
        self.visible = visible
        self.searchable = searchable
        self.sortable = sortable
        self.alignment = alignment
        self.tooltip = tooltip
        self.config = config
        # Initialize actions from the column configuration
        self.actions = [TableAction(action['type'], action['label'], action['callback'])
                        for action in config.get("actions", [])]


# Class to handle the data table rendering and functionality
class DataTable:
    def __init__(self, table_name: str, columns: List[DataColumn], pagination: dict, filters: dict,
                 sort: dict, export: dict):
        self.table_name = table_name
        self.columns = columns
        self.pagination = pagination
        self.filters = filters
        self.sort = sort
        self.export = export

    def render(self, page: ft.Page, data: List[Dict]):
        # Create rows for the table based on the data
        rows = []
        for record in data:
            row = []
            for column in self.columns:
                if isinstance(column, DataColumn):  # Ensure the column is a DataColumn instance
                    print(f"Rendering column: {column.header_name}")  # Debug: Print column being processed
                    if column.visible:  # Ensure the column is visible
                        value = record.get(column.field_name, "")

                        # Handle the field types such as date or checkbox
                        if column.field_type == 'date' and value:
                            try:
                                if 'T' in value:
                                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%m/%d/%Y")
                                else:
                                    value = datetime.strptime(value, "%Y-%m-%d").strftime("%m/%d/%Y")
                            except ValueError as e:
                                print(f"Error parsing date: {e}")
                                value = "Invalid date format"

                        if column.field_type == 'checkbox':
                            value = ft.Checkbox(value=value, disabled=True)

                        row.append(ft.DataCell(value))
                else:
                    print(f"Error: Column {column} is not a valid DataColumn!")  # Debug print if column is invalid

            rows.append(row)

        # Create the DataTable widget for Flet
        data_table = ft.DataTable(
            columns=[ft.DataColumn(label=ft.Text(column.header_name), tooltip=column.tooltip)
                     for column in self.columns if isinstance(column, DataColumn) and column.visible],
            rows=[ft.DataRow(cells=row) for row in rows]
        )

        # Add action buttons (like Edit/Delete) if any actions are defined for the column
        for i, row in enumerate(rows):
            for column in self.columns:
                if isinstance(column, DataColumn):
                    for action in column.actions:
                        if action.action_type == 'button':
                            button = ft.IconButton(icon=action.label.lower(), on_click=action.callback)
                            data_table.rows[i].cells.append(ft.DataCell(button))

        # Add the DataTable to the page
        page.add(data_table)

        # Add filters if enabled
        if self.filters.get('enabled'):
            filter_inputs = []
            for filter_field in self.filters.get('fields', []):
                filter_input = ft.TextField(label=f"Search {filter_field.capitalize()}", on_change=self.apply_filter)
                filter_inputs.append(filter_input)
            page.add(ft.Row(filter_inputs))

        # Export functionality (mocked here)
        if self.export.get('enabled'):
            export_buttons = []
            for format in self.export.get('formats', []):
                export_buttons.append(ft.ElevatedButton(f"Export to {format.upper()}",
                                                        on_click=lambda e, format=format: self.export_data(format)))
            page.add(ft.Row(export_buttons))

    def apply_filter(self, e):
        # Apply filtering logic based on the input fields
        pass

    def export_data(self, format: str):
        if format == "csv":
            self.export_csv()
        elif format == "excel":
            self.export_excel()
        elif format == "pdf":
            self.export_pdf()

    def export_csv(self):
        # Example data export to CSV
        data = [{"name": "John Doe", "email": "john@example.com", "age": 30, "created_at": "2023-01-01"}]
        df = pd.DataFrame(data)
        df.to_csv("table_export.csv", index=False)

    def export_excel(self):
        data = [{"name": "John Doe", "email": "john@example.com", "age": 30, "created_at": "2023-01-01"}]
        df = pd.DataFrame(data)
        df.to_excel("table_export.xlsx", index=False)

    def export_pdf(self):
        data = [{"name": "John Doe", "email": "john@example.com", "age": 30, "created_at": "2023-01-01"}]
        c = canvas.Canvas("table_export.pdf", pagesize=letter)
        c.drawString(100, 750, f"Name: {data[0]['name']}, Email: {data[0]['email']}")  # Add more fields as needed
        c.save()


# Example usage:
def main(page: ft.Page):
    # Define columns, making sure each column is a DataColumn instance
    columns = [
        DataColumn("name", "Name", "text", True, True, True, "left", "User's full name", {}),
        DataColumn("email", "Email", "text", True, True, True, "left", "User's email address", {}),
        DataColumn("age", "Age", "number", True, True, True, "right", "User's age", {}),
        DataColumn("created_at", "Created At", "date", True, False, True, "right", "Date of record", {}),
    ]

    # Create the DataTable instance
    data_table = DataTable(
        "example_table", columns,
        {"enabled": True, "page_size": 10, "options": [10, 20, 50, 100]},
        {"enabled": True, "fields": ["name", "email", "age", "created_at"]},
        {"default_field": "created_at", "default_order": "desc"},
        {"enabled": True, "formats": ["csv", "excel", "pdf"]}
    )

    # Sample data
    data = [{"name": "John Doe", "email": "john@example.com", "age": 30, "created_at": "2023-01-01"}]

    # Render the table on the page
    data_table.render(page, data)


# Start the Flet application
ft.app(target=main)
