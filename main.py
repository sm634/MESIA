import os

import pandas as pd
from time import time

from conversion_layer.pdf_to_image import PdfToImage
from conversion_layer.image_to_text import ImageToText
from utils.utils_functions import TextFiles, Invoice
from extraction_layer.prompts import Prompts

t1 = time()

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
invoices = Invoice(datasource='directory')

data_fields_text = invoices.data_fields_text
data_fields_list = invoices.data_fields_list

"""Using GPT model prompt to extract fields"""
# initialize GPT and specify the model to use.
prompts = Prompts(model='text-davinci-003')

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
output_df = output_df.set_index('invoice_index')
output_df = invoices.standardise_invoice_df(output_df)

print("Saving data to file.")
output_df.to_csv("data/output/sample_output.csv")

t2 = (time() - t1)

print(f"Saving finished. Process took {t2:.2f} seconds.")
