# MESIA
Migrate + Extract Simple Invoice Application

An application that makes use of open source OCR and GPT in a relatively lean codebase to extract data values from pdf invoices. 

The lean nature of the application means that it can be repurposed for other text extraction tasks with relatively small number of code development.

### Design Overview

![MESIA](https://user-images.githubusercontent.com/50050912/235702279-94b33e08-066d-4c77-8423-279839f07320.jpg)

### Environment Set-up

The environment used for this requires the installation of tesseract-ocr for text recognition. If you use windows, you can install it from here: 
https://github.com/UB-Mannheim/tesseract/wiki

You should take note of where the destination folder for the install location. It will likely look as follows: C:\Users\username\AppData\Local\Programs\Tesseract-OCR
This will be required when runnin Tesseract-OCR through the python script.

You will also need the Poppler library if you are converting your PDF to images. This can be installed here: [install poppler]([https://github.com/oschwartz10612/poppler-windows/releases/r](https://github.com/oschwartz10612/poppler-windows/releases/). Read the instructions to ensure you extract all of the documents in the correct pkgs or library folder.

The environment.yml file will have the required libraries needed to run the application. 


### How to Use

Place the pdf invoices in the following directory of the project repository: 

```data\input\pdfs```

Once the pdf invoices are placed in the specified directory. Run the following command in the terminal:

```python main.py```

The output .csv file will be available in once the execution has completed successfully.

```data\output\``` 

### Debugging

This application is still in development phase. Please contact safal.mukhia@protiviti.co.uk if any support is required.
