import flet as ft


class PopupColorItem(ft.PopupMenuItem):
    def __init__(self, color, name):
        super().__init__()
        self.content = ft.Row(
            controls=[
                ft.Icon(name=ft.Icons.COLOR_LENS_OUTLINED, color=color),
                ft.Text(name),
            ],
        )
        self.on_click = self.seed_color_changed
        self.data = color

    def seed_color_changed(self, e):
        self.page.theme = self.page.dark_theme = ft.Theme(color_scheme_seed=self.data)
        self.page.update()
