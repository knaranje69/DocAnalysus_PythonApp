from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivymd.uix.filemanager import MDFileManager
from kivy.core.window import Window
import os
import kivymd
from kivymd.uix.button import MDRaisedButton

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path
        )

        self.add_widget(Label(text='Click the button to upload a file'))

        self.upload_button = MDRaisedButton(
            text='Upload File',
            on_press=self.show_file_manager
        )
        self.add_widget(self.upload_button)

        self.image_label = Label(text='No file uploaded')
        self.add_widget(self.image_label)

    def show_file_manager(self, *args):
        self.file_manager.show('/')

    def select_path(self, path):
        self.exit_manager()
        self.display_file(path)

    def exit_manager(self, *args):
        self.file_manager.close()

    def display_file(self, path):
        if os.path.isfile(path):
            self.image_label.text = f'Uploaded file: {os.path.basename(path)}'
        else:
            self.image_label.text = 'No file uploaded'

class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return MainLayout()

if __name__ == '__main__':
    Window.size = (400, 600)
    MyApp().run()