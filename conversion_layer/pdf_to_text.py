import PyPDF2
import os


class PdfText:
    def __init__(self, datasource, keep_last=True):
        self.data_source = datasource
        self.keep_last = keep_last

        if self.data_source.lower() == 's3':
            pass
        elif self.data_source.lower() == 'directory':
            self.pdf_input_dir_path = 'data/input/pdfs/'
            self.text_files_dir_path = 'data/input/text/'

    def extract_text_from_pdf(self, file_path):
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)

            if not self.keep_last:
                for page_number in range(num_pages):
                    page_obj = reader.pages[page_number]
                    text += page_obj.extract_text()
            else:
                page_obj = reader.pages[-1]
                text += page_obj.extract_text()

        return text

    def access_pdf_storage(self):
        if self.data_source == 's3':
            pass
        elif self.data_source == 'directory':
            pdf_files_list = os.listdir(self.pdf_input_dir_path)
            pdf_files_list = [file for file in pdf_files_list if '.pdf' in file]
            pdf_files_path = [self.pdf_input_dir_path + file_name for file_name in pdf_files_list]
            return pdf_files_path

    def save_pdf_text(self):
        if self.data_source == 's3':
            pass
        elif self.data_source == 'directory':
            pdf_files = self.access_pdf_storage()
            for i, pdf in enumerate(pdf_files):
                extracted_text = self.extract_text_from_pdf(pdf)
                pdf_name = os.listdir(self.pdf_input_dir_path)[i]
                write_path = self.text_files_dir_path + pdf_name.replace('.pdf', '') + '.txt'
                with open(write_path, 'w') as f:
                    f.write(extracted_text)
                    f.close()
                    print(f"Extracted text saved to {write_path}")
