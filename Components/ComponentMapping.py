import flet as ft

from Components.AddDataPopUp import AddDataPopUp
from Components.TableView import TableView
from DB.DataCRUD import DataCRUD


class ComponentMapping:
    def __init__(self):

        self.table_header = {
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
                    "field_name": "_id",
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

        self.sample_data = [
            {"_id": "1", "name": "Alice", "selected": False},
            {"_id": "2", "name": "Bob", "selected": False},
            {"_id": "3", "name": "Charlie", "selected": False},
        ]


        table_view = TableView(header=self.table_header, data=self.sample_data)

        self.components = {
            "dashboard": table_view,
            "candidates": ft.Text("king upadhyay"),
        }
        self.title_font_size = 20
        self.titles = {
            "dashboard": ft.Text("Dashboard", size=self.title_font_size,weight=ft.FontWeight.BOLD),
            "candidates": ft.Text("Candidates", size=self.title_font_size,weight=ft.FontWeight.BOLD)
        }
        self.buttons ={
            "dashboard": ft.FilledTonalButton("Dashboard", on_click=self.addDashboardData, icon="add"),
            "candidates": ft.FilledTonalButton("Candidates", on_click=self.addDashboardData, icon="add")
        }

        db_name = "training_software"
        collection_name = "forms_schema"
        crud = DataCRUD(db_name, collection_name)
        self.tabs_data = crud.read()
        self.add_student = AddDataPopUp(self.tabs_data)

    def addDashboardData(self, e):
        self.add_student.open_dialog(e)
        print("Adding Dashboard")
        #return self.components["dashboard"]

    def addComponent(self, key, value):
        self.components[key] = value

    def getComponent(self, key):
        return self.components[key]

    def getTitle(self, key):
        return self.titles[key]

    def getButton(self, key):
        return self.buttons[key]

    def removeComponent(self, key):
        if key in self.components:
            del self.components[key]

    def __repr__(self):
        return str(self.components)



