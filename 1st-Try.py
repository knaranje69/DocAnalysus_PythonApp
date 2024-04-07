# Got success scrolling and the response is getting a good designed output

from kivymd.app import MDApp                                
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import os
import openai
import pytesseract
import fitz
from PIL import Image
from io import BytesIO
import docx

openai.api_key = "api-key"

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path
        )

        self.add_widget(Label(text='Document Analysis- Please upload the document below:'))

        self.upload_button = MDRaisedButton(
            text='Upload File',
            on_press=self.show_file_manager,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.upload_button)

        self.image_label = Label(text='No file uploaded')
        self.add_widget(self.image_label)

        self.question_input = MDTextField(
            hint_text="Enter your question",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.8, None),
            height=50
        )
        self.add_widget(self.question_input)

        self.analyze_button = MDRaisedButton(
            text='Analyze',
            on_press=self.process_file,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.analyze_button)
        
        self.result_box = BoxLayout(orientation='vertical')
        self.result_label = Label(text='')
        self.result_box.add_widget(self.result_label)
        self.add_widget(self.result_box)

        self.file_path = None
        
        self.response_scrollview = ScrollView(do_scroll_x=False, do_scroll_y=True)
        self.response_box = BoxLayout(orientation='vertical', size_hint_y=None)
        self.response_box.bind(minimum_height=self.response_box.setter('height'))
        self.response_scrollview.add_widget(self.response_box)
        
        self.add_widget(self.response_scrollview)

    def show_file_manager(self, *args):
        self.file_manager.show('/')

    def select_path(self, path):
        self.exit_manager()
        self.display_file(path)
        self.file_path = path

    def exit_manager(self, *args):
        self.file_manager.close()

    def display_file(self, path):
        if os.path.isfile(path):
            self.image_label.text = f'Uploaded file: {os.path.basename(path)}'
        else:
            self.image_label.text = 'No file uploaded'

    def process_file(self, *args):
        try:
            if self.file_path:
                text1 = self.convert_any_to_string(self.file_path)
                question = self.question_input.text
                prompt = f"Given the following document {text1}\n\nAnswer the questions:{question}"

                response = openai.Completion.create(
                    engine="gpt-3.5-turbo-instruct",
                    prompt=prompt,
                    max_tokens=100,
                    n=1,
                    stop=None,
                    temperature=0.7
                )
                answer = response.choices[0].text.strip()
                self.response_box.clear_widgets()
                response_label = Label(text=f"Answer: {answer}", size_hint=(1, None), halign="left")
                response_label.bind(size=response_label.setter('text_size'))
                self.response_box.add_widget(response_label)
            else:
                self.response_box.clear_widgets()
                response_label = Label(text="Please upload a file first.", size_hint=(1, None), halign="left")
                response_label.bind(size=response_label.setter('text_size'))
                self.response_box.add_widget(response_label)
        except Exception as e:
            self.response_box.clear_widgets()
            response_label = Label(text=f"Error: {e}", size_hint=(1, None))
            response_label.bind(size=response_label.setter('text_size'))
            self.response_box.add_widget(response_label)

    def document_to_string(self, document_path, list_dict_final_images=None):
        _, file_extension = os.path.splitext(document_path)

        if file_extension.lower() in ['.png', '.jpeg', '.jpg']:
            image = Image.open(document_path)
            list_final_images = pytesseract.image_to_string(image)
            return list_final_images

        all_images = [list(data.values())[0] for data in list_dict_final_images]

        for index, image_bytes in enumerate(all_images):
            image = Image.open(BytesIO(image_bytes))
            figure = plt.figure(figsize=(image.width / 100, image.height / 100))

            plt.title(f"--- Page Number {index + 1} ---")
            plt.imshow(image)
            plt.axis("off")
            plt.show()

    def pdf_to_image(self, file_path, scale=300 / 72):
        text = ""
        pdf_document = fitz.open(file_path)

        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()

        pdf_document.close()
        return text

    def png_to_string(self, filepath):
        try:
            image = Image.open(filepath)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"Error converting PNG to string: {e}")
            return None

    def txt_to_string(self, filepath):
        try:
            with open(filepath, 'r') as file:
                text = file.read()
            return text
        except Exception as e:
            print(f"Error converting TXT to string: {e}")
            return None

    def docx_to_string(self, filepath):
        try:
            doc = docx.Document(filepath)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            print(f"Error converting DOCX to string: {e}")
            return None

    def convert_any_to_string(self, filepath):
        my_path = filepath
        if my_path.endswith(".pdf"):
            return self.pdf_to_image(my_path)
        elif my_path.endswith(".png"):
            return self.png_to_string(my_path)
        elif my_path.endswith(".jpeg"):
            return self.document_to_string(my_path)
        elif my_path.endswith(".txt"):
            return self.txt_to_string(my_path)
        elif my_path.endswith(".docx"):
            return self.docx_to_string(my_path)
        elif my_path.endswith(".jpg"):
            return self.document_to_string(my_path)
        else:
            return "The extension is not valid!"

class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return MainLayout()

if __name__ == '__main__':
    Window.size = (1000, 800)
    MyApp().run()