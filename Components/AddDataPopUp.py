import flet as ft
from flet.core import padding

from Components.AddStudentForm import AddStudentForm


class AddDataPopUp:
    def __init__(
        self,
        title_value="Add Data",
        footer_save_title="Save",
        footer_close_title="Close",
        content_padding=(100, 0, 100, 0),
        border_radius=0,
        header_icon_plus=ft.Icons.CLOSE,
        header_icon_minus=ft.Icons.REMOVE,
        border_color=ft.colors.BLACK,
        border_width=1,
    ):
        self.titleValue = title_value
        self.footerSaveTitle = footer_save_title
        self.footerCloseTitle = footer_close_title

        self.title = ft.Text(self.titleValue)
        self.headerIconPlus = ft.IconButton(
            icon=header_icon_plus,
            tooltip="Close",
        )
        self.headerIconMinus = ft.IconButton(
            icon=header_icon_minus,
            tooltip="Minimize",
        )
        self.footerSave = ft.TextButton(text=self.footerSaveTitle)
        self.footerClose = ft.TextButton(text=self.footerCloseTitle)

        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=self.getTitle(border_color, border_width),
            content=self.getMainContent(),
            actions=self.getBottomAction(border_color, border_width),
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed"),
            inset_padding=padding.symmetric(vertical=5, horizontal=5),
            shape=ft.RoundedRectangleBorder(radius=border_radius),
            title_padding=ft.padding.all(0),  # left, top, right, bottom
            actions_padding=ft.padding.all(0),  # left, top, right, bottom
            content_padding=ft.Padding(*content_padding),
            scrollable=True,
        )

    def open_dialog(self, e):
        page = e.page
        page.dialog = self.dlg_modal
        self.dlg_modal.open = True
        page.update()

    def close_dialog(self, e):
        page = e.page
        self.dlg_modal.open = False
        page.update()

    def getTitle(self, border_color, border_width):
        titleWidget = ft.Container(
            content=ft.Row(
                controls=[
                    self.title,
                    ft.Row(controls=[self.headerIconMinus, self.headerIconPlus])
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=500
            ),
            padding=padding.all(5),
            border=ft.Border(bottom=ft.BorderSide(border_width, border_color)),
        )
        return titleWidget

    def getBottomAction(self, border_color, border_width):
        bottomAction = [
            ft.Container(
                ft.Row(
                    [self.footerSave, self.footerClose],
                    alignment=ft.MainAxisAlignment.END
                ),
                padding=ft.Padding(0, 10, 25, 10),
                border=ft.Border(top=ft.BorderSide(border_width, border_color)),
            )
        ]
        return bottomAction

    def getMainContent(self):
        mainContent = ft.Container(
            content=AddStudentForm(self.close_dialog),
            expand=True,
        )
        return mainContent
