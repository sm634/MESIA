import os
import re
import pandas as pd


class TextFiles:

    def __init__(self, datasource):
        self.datasource = datasource

        if self.datasource.lower() == 's3':
            pass
        elif self.datasource.lower() == 'directory':
            """
            The paths provided here are set so that the can be used statically when the program is executed and run from
            the main.py folder of the project. 
            """
            self.text_input_dir_path = 'data/input/text/'

    def get_text_files_list(self):
        text_dir = self.text_input_dir_path
        files = os.listdir(self.text_input_dir_path)

        texts_list = []
        for file in files:
            file_path = text_dir + file
            with open(file_path, 'r') as f:
                text = f.read()
                texts_list.append(text)

        return texts_list

    @staticmethod
    def txt_to_list(text):
        text_list = text.split('\n')
        text_list = [item for item in text_list if len(item) > 0]
        values_list = [item[item.index(':') + 2:] for item in text_list]
        values_list = [item for item in values_list if len(item) > 0]
        return values_list


class Invoice:

    def __init__(self, datasource):
        self.datasource = datasource

        if self.datasource.lower() == 's3':
            pass
        elif self.datasource.lower() == 'directory':
            """
            The paths provided here are set so that they can be used statically when the program is executed and run from
            the main.py folder of the project. 
            """
            self.text_input_dir_path = 'data/input/text/'

            with open('reference_docs/data_fields_to_extract.txt', 'r') as f:
                self.data_fields_text = f.read()

            self.data_fields_list = self.data_fields_text.split(',')

    @staticmethod
    def standardise_invoice_df(df):
        """
        A method used to standardise
        :param df: The input df
        :return: df with standardised columns
        """

        def clean_doc_number(text):
            doc_num_match = re.search(r"UMAR\d+", text)
            if doc_num_match:
                return doc_num_match.group()

        columns = df.columns.to_list()

        if 'GBP' in columns:
            if df['GBP'].dtype == str:
                df['GBP'] = df['GBP'].apply(lambda x: x.replace(',', ''))
                df['GBP'] = df['GBP'].astype(float)

        if 'Document Number' in columns:
            df['DOCUMENT NUMBER'] = df['DOCUMENT NUMBER'].apply(lambda x: clean_doc_number(x))

        return df


class Test:
    @staticmethod
    def check_dfs_accuracy(ref_df, df2):
        """
        A function that compares the values of the ref output with model generated output.
        :param ref_df: The correct, ref dataframe.
        :param df2: The current dataframe processed.
        :return: A Diff Dataframe with accuracy
        """
        checked_df = ref_df == df2

        row_total_counts = ref_df.count(axis=1)
        row_true_counts = checked_df[checked_df == True].count(axis=1)
        row_accuracy = row_true_counts / row_total_counts

        col_total_counts = ref_df.count(axis=0)
        col_true_counts = checked_df[checked_df == True].count(axis=0)
        col_accuracy = col_true_counts / col_total_counts

        checked_df = pd.concat([checked_df, pd.DataFrame([col_accuracy])])
        index_list = checked_df.index.to_list()
        index_list[-1] = 'accuracy'
        checked_df.index = index_list
        checked_df['accuracy'] = row_accuracy

        return checked_df


class Folder:

    @staticmethod
    def clear_directory(folder_path):
        """
        Clear a directory from the kept folders.
        :param folder_path: the path of to the folder, e.g. data/input/text/
        """
        files_list = os.listdir(folder_path)
        files_list = [file for file in files_list if '.py' not in file]
        for file in files_list:
            os.remove(folder_path + file)
            print(f"{file} deleted")
