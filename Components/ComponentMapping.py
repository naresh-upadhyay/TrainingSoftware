import flet as ft
from flet.core import page

from Components.AddDataPopUp import AddDataPopUp
from Components.TableView import TableView


class ComponentMapping:
    def __init__(self):
        self.components = {
            "dashboard": TableView(),
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
        self.add_student = AddDataPopUp()

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



