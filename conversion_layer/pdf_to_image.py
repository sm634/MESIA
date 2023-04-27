import os

import pdf2image.exceptions
from pdf2image import convert_from_path


class PdfToImage:

    def __init__(self, datasource):
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
            self.poppler_path = 'C:/Users/safmuk01/AppData/Local/anaconda3/pkgs/poppler-23.01.0/Library/bin'
            self.pdf_input_dir_path = 'data/input/pdfs/'
            self.images_input_dir_path = 'data/input/images/'

    def __get_pdf_file_paths(self):
        """
        Finds all pdf files in a directory and stores them in a list along with their relative path.
        :param dir_path: the directory to search for the pdf files.
        :return: list
            Returns a list of pdf documents and their paths.
        """
        pdf_files = os.listdir(self.pdf_input_dir_path)
        pdf_file_paths = [self.pdf_input_dir_path + file for file in pdf_files if '.pdf' in file]
        return pdf_file_paths

    def __get_pdf_names_file(self):
        """
        Finds all pdf file names in a directory and stores them in a list along with their relative path.
        :param dir_path: the directory to search for the pdf files.
        :return: list
            Returns a list of pdf documents and their names.
        """
        pdf_files = os.listdir(self.pdf_input_dir_path)
        pdf_file_names = [file.replace('.pdf', '') for file in pdf_files if '.pdf' in file]
        return pdf_file_names

    def __save_images_file(self, pages, doc_name):
        """
        Take in pdf to image converted pages and save them in a designated directory.
        :param page: the input pdf pages converted to from_images to be saved
        :param doc_name: name of the document to save as.
        :param output_dir: the directory to save the output from_images.
        :return: output from_images
        """
        for i, page in enumerate(pages):
            image_name = f"{doc_name}_page_{i + 1}.jpg"
            output_img = self.images_input_dir_path + image_name
            page.save(output_img, "JPEG")

    def pdf_to_images(self):

        if self.data_source == 'directory':
            pdfs_paths = self.__get_pdf_file_paths()
            pdf_names = self.__get_pdf_names_file()
            for j, pdf in enumerate(pdfs_paths):
                try:
                    print(f'currently processing pdf file {pdf}')
                    pages = convert_from_path(pdf,
                                              poppler_path=self.poppler_path)
                    file_name = pdf_names[j]
                    # only save the last page as it contains all the information.
                    page_to_save = [pages[-1]]
                    self.__save_images_file(pages=page_to_save, doc_name=file_name)
                    print(f"image {file_name} saved")
                except pdf2image.exceptions.PDFPageCountError:
                    print(f"Conversion Failed for {pdf}")
                    pass

        elif self.data_source == 's3':
            pass

        else:
            print("Please provide a valid data source. Options ['directory', 's3'].")
