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
        self.tabs_data = [
            {
                "tabTitle": "Personal Information",
                "inputFields": [
                    {"key": "firstName", "label": "First Name", "type": "text", "mandatory": True},
                    {"key": "lastName", "label": "Last Name", "type": "text", "mandatory": True},
                    {"key": "email", "label": "Email Address", "type": "email", "mandatory": False},
                    {"key": "email1", "label": "Email Address 1", "type": "email", "mandatory": False},
                    {"key": "email2", "label": "Email Address 2", "type": "email", "mandatory": False},
                    {"key": "email3", "label": "Email Address 3", "type": "email", "mandatory": False},
                    {"key": "phoneNumber", "label": "Phone Number", "type": "tel", "mandatory": False},
                    {"key": "dob", "label": "Date of Birth", "type": "date", "mandatory": True},
                ],
            },
            {
                "tabTitle": "Account Settings",
                "inputFields": [
                    {"key": "username", "label": "Username", "type": "text", "mandatory": True},
                    {"key": "password", "label": "Password", "type": "password", "mandatory": True},
                    {"key": "confirmPassword", "label": "Confirm Password", "type": "password", "mandatory": True},
                    {"key": "notifications", "label": "Receive Notifications", "type": "checkbox", "mandatory": False},
                ],
            },
        ]
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



