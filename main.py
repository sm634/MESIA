import os

import pandas as pd
from time import time

from conversion_layer.pdf_to_image import PdfToImage
from conversion_layer.image_to_text import ImageToText
from utils.utils_functions import TextFiles, Invoice
from extraction_layer.prompts import Prompts

t1 = time()

pdf_indexes = [item[0:item.index(" ")] for item in os.listdir('data/input/pdfs/')]

"""Pdfs to images step"""
pdf_to_image = PdfToImage(datasource='directory')
# save images
pdf_to_image.pdf_to_images()

"""Images to text step"""
img_to_text = ImageToText(datasource='directory')
# save text
img_to_text.img_to_txt()

"""Setup for model"""
text_utils = TextFiles(datasource='directory')
invoices_list = text_utils.get_text_files_list()

# initialise invoice class
invoices = Invoice()

data_fields_text = invoices.data_fields
data_fields_list = data_fields_text.split(',')

"""Using GPT model prompt to extract fields"""
# initialize GPT
prompts = Prompts()

print(f"Extraction of data fields: {data_fields_text} from source text files.")

output_data_list = []
for text in invoices_list:
    invoice_data = prompts.extract_invoice_info(data_fields=data_fields_text, invoice_text=text)
    output_data_list.append(text_utils.txt_to_list(invoice_data))

print(f"Extraction complete.")

output_df = pd.DataFrame(data=output_data_list, columns=data_fields_list)
output_df['invoice_index'] = pdf_indexes
output_df = output_df.set_index('invoice_index')

print("Saving data to file.")
output_df.to_csv("data/output/sample_output.csv")

t2 = (time() - t1)

print(f"Saving finished. Process took {t2:.2f} seconds.")
