import flet as ft

from Components.AddDataPopUp import AddDataPopUp
from Components.TableView import TableView
from DB.DataCRUD import DataCRUD


class ComponentMapping:
    def __init__(self):
        json_data = '''
            {
                "header": {
                    "id": "ID",
                    "name": "Name",
                    "age": "Age",
                    "action": "Action"
                },
                "data": [
                    {"id": 1, "name": "Alice", "age": 25},
                    {"id": 2, "name": "Bob", "age": 30},
                    {"id": 3, "name": "Charlie", "age": 35}
                ]
            }
            '''

        table_view = TableView(json_data=json_data)

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



