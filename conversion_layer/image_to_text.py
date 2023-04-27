import os

import pytesseract
from PIL import Image


class ImageToText:

    def __init__(self, datasource):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Users\safmuk01\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

        self.data_source = datasource

        if self.data_source.lower() == 's3':
            pass
        elif self.data_source.lower() == 'directory':
            """
            The paths provided here are set so that the can be used statically when the program is executed and run from
            the main.py folder of the project. 

            Future: The Poppler path will have to be updated to account for getting the poppler path from a different
            machine.
            """
            self.images_input_dir_path = 'data/input/images/'
            self.images_output_dir_path = 'data/input/text/'

    def __img_to_txt_file(self):
        """
        A function that grabs all input images, uses ocr from tesseract-ocr to convert them to text and saves them as a
        txt file in an output folder.
        :param input_dir: the input directory containing the images to be converted to text.
        :param output_dir: the output directory to save the converted text data into
        :return: text
        """
        file_extensions = ['.jpg', '.png']
        images_file = os.listdir(self.images_input_dir_path)
        for file in images_file:
            file_path = self.images_input_dir_path + file
            text = pytesseract.image_to_string(Image.open(file_path))
            # replace the extensions to text.
            for ext in file_extensions:
                if ext in file:
                    file = file.replace(ext, '.txt')
            with open(self.images_output_dir_path + file, 'w') as f:
                f.write(text)
                f.close()
            print(f"image {file} converted to text and saved.")

    def img_to_txt(self):

        if self.data_source.lower() == 'directory':
            self.__img_to_txt_file()
        elif self.data_source.lower() == 's3':
            pass
        else:
            print("Please provide a valid data source. Options: ['directory', 's3']")
