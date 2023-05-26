import os
import argparse

import pandas as pd
from time import time

from conversion_layer.pdf_to_image import PdfToImage
from conversion_layer.image_to_text import ImageToText
from conversion_layer.pdf_to_text import PdfText
from utils.utils_functions import TextFiles, Invoice, Test, Folder
from extraction_layer.prompts import Prompts

parser = argparse.ArgumentParser()

parser.add_argument('--model', type=str, default='text-davinci-003',
                    choices=['text-davinci-003', 'gpt-3.5-turbo', 'gpt-3.5-turbo-0301'])
parser.add_argument('--extractor', type=str, default='pytesseract',
                    choices=['pytesseract', 'pypdf'])
parser.add_argument('--delete_files', type=str, default='true',
                    choices=['true', 'false'])
parser.add_argument('--run_test', type=str, default='true',
                    choices=['true', 'false'])

args = parser.parse_args()

t1 = time()

if args.extractor == 'pytesseract':
    """Pdfs to images step"""
    pdf_to_image = PdfToImage(datasource='directory')
    # save images
    pdf_to_image.pdf_to_images()

    """Images to text step"""
    img_to_text = ImageToText(datasource='directory')
    # save text
    img_to_text.img_to_txt()

elif args.extractor == 'pypdf':
    """PDF to text option"""
    pdfs = PdfText(datasource='directory')
    pdfs.save_pdf_text()


"""Setup for model"""
text_utils = TextFiles(datasource='directory')
invoices_list = text_utils.get_text_files_list()

# initialise invoice class
invoices = Invoice(datasource='directory')

data_fields_text = invoices.data_fields_text
data_fields_list = invoices.data_fields_list

"""Using GPT model prompt to extract fields"""
# initialize GPT and specify the model to use.
prompts = Prompts(model=args.model)

print(f"Extraction of data fields: {data_fields_text} from source text files.")

# store a variable with the pdf numbers as the index for the sheet.
pdf_indexes = [item[0:item.index(" ")] for item in os.listdir('data/input/pdfs/') if '.pdf' in item]

output_data_list = []
for text, i in zip(invoices_list, pdf_indexes):
    invoice_data = prompts.extract_invoice_info(data_fields=data_fields_text, invoice_text=text, file_index=i)
    output_data_list.append(text_utils.txt_to_list(invoice_data))

print(f"Extraction complete.")


output_df = pd.DataFrame(data=output_data_list, columns=data_fields_list)
output_df['invoice_index'] = pdf_indexes
output_df['invoice_index'] = output_df['invoice_index'].astype(int)
output_df = output_df.set_index('invoice_index')

print("Saving data to file.")
output_file = f"{args.model}_{args.extractor}_output"
output_df.to_csv("data/output/" + output_file + '.csv')

t2 = (time() - t1)

print(f"Saving finished. Process took {t2:.2f} seconds.")

"""Clean up directories"""
if args.delete_files == 'true':
    img_dir = 'data/input/images/'
    Folder.clear_directory(img_dir)
    txt_dir = 'data/input/text/'
    Folder.clear_directory(txt_dir)

"""Run tests"""
if args.run_test == 'true':
    ref_df = pd.read_csv('reference_docs/reference_output.csv',
                         index_col='invoice_index')
    checked_df = Test.check_dfs_accuracy(ref_df, output_df)
    checked_df.to_csv(f'data/output/{output_file}_check.csv')
