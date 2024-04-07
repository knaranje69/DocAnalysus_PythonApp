from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.button import MDFlatButton
from kivy.lang import Builder
from kivy.core.window import Window

# Set window size
Window.size = (350, 500)

# Load Kivy file
KV = """
Screen:
    MDFlatButton:
        text: "Upload File"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        on_release: app.file_manager_open()
"""

class UploadApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path
        )

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)

    def file_manager_open(self):
        self.file_manager.show('/')  # output manager to the screen

    def select_path(self, path):
        self.exit_manager()
        # get selected file path here
        print(path)

    def exit_manager(self, *args):
        self.file_manager.close()

UploadApp().run()