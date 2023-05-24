from decouple import config
import openai

openai.api_key = config('OPENAI_API_KEY')


class Prompts:

    def __init__(self, model="text-davinci-003", max_tokens=1000, temperature=0):
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.model = model

    @staticmethod
    def __extract_invoice_prompt(data_fields, invoice_text):
        return f"""extract the values for {data_fields}.
        
                Some examples:
                Document Number: UMAR123456
                Document Date: 01/05/21
                Account No.: 101022
                Payment Reference: UMAR123456 / 101022
                Payment Terms: 90 Days after month end
                OR
                Payment Terms: 50 Days Date of Invoice
                GBP: 5,235.05
         
                Extract those values from the text below:
                
                "{invoice_text}"
            """

    def extract_invoice_info(self, data_fields, invoice_text, file_index):
        """
        :param file_index: For output, to provide reference for the file being processed by model.
        :param invoice_text: The text from invoice as input to extract information from.
        :param data_fields: values for data fields to extract
        :return: a string, comma separated with all the values we require.
        """

        extracted_values = ''

        if self.model == 'text-davinci-003':
            response = openai.Completion.create(
                engine=self.model,
                prompt=self.__extract_invoice_prompt(data_fields=data_fields, invoice_text=invoice_text),
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            extracted_values = response.choices[0].text
            print(f"Extracting data field values from document {file_index}")

        elif self.model == 'gpt-3.5-turbo':
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful reading assistant who will be provided text"
                                                  "from an invoice. You will be asked to extract values for a set of"
                                                  "data fields from that invoice text and return it as a response."},
                    {"role": "user", "content": self.__extract_invoice_prompt(data_fields=data_fields,
                                                                              invoice_text=invoice_text)}
                ],
                temperature=self.temperature,
                n=1,
                max_tokens=self.max_tokens
            )
            extracted_values = response['choices'][0]['message']['content']
            print(f"Extracting data field values from document {file_index}")

        return extracted_values
