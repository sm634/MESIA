from decouple import config
import openai
from openai.error import RateLimitError
import backoff

openai.api_key = config('OPENAI_API_KEY')


class Prompts:

    def __init__(self, model="text-davinci-003", max_tokens=1000, temperature=0):
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.model = model

    @staticmethod
    def __extract_invoice_prompt(data_fields, invoice_text):
        return f"""your job is to extract the values for the following data fields {data_fields}.
                
                Characteristics of the data fields you should extract are:
                Document Number - has prefix UMAR followed by 6 digits, ensure you bring these.
                Document Date - is in format dd/mm/yy
                Account No. - has 6 digits
                Payment Reference - has the Document Number / Account No.
                Payment Terms - Can vary but includes time period related words and nothing else.
                GBP - Is a price value.
                
                Some examples:
                Document Number: UMAR123456
                Document Date: 01/05/21
                Account No.: 101022
                Payment Reference: UMAR123456 / 101022
                Payment Terms: 90 Days after month end
                OR
                Payment Terms: 50 Days Date of Invoice
                GBP: 5,235.05
         
                Extract those values from the text below and return nothing else:
                
                "{invoice_text}"
            """

    @backoff.on_exception(backoff.expo, RateLimitError, max_time=300)
    def chat_completions_with_backoff(self, data_fields, invoice_text, retry=True):
        while retry:
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a helpful reading assistant who will be provided text"
                                                      "from an invoice. You will be asked to extract values for a set of"
                                                      "data fields from that invoice text and return it as a response. The text"
                                                      "you will be provided are not always easy to read, but you should make"
                                                      "the best guess based on the characteristics and examples provided in the"
                                                      "prompts for you."},
                        {"role": "user", "content": self.__extract_invoice_prompt(data_fields=data_fields,
                                                                                  invoice_text=invoice_text)}
                    ],
                    temperature=self.temperature,
                    n=1,
                    max_tokens=self.max_tokens
                )
                return response['choices'][0]['message']['content']
            except RateLimitError:
                print(f"Requests to the model are at maximum capacity, cooling off before retrying the requests"
                      f" using exponential backoff.")
            except openai.error.APIError as e:
                print(f"The request ran into an OpenAI server issue. Retrying the request again.")

    @backoff.on_exception(backoff.expo, RateLimitError, max_time=300)
    def completions_with_backoff(self, data_fields, invoice_text, retry=True):
        # try - except clause to handle bad gateway problems.
        while retry:
            try:
                response = openai.Completion.create(
                    engine=self.model,
                    prompt=self.__extract_invoice_prompt(data_fields=data_fields, invoice_text=invoice_text),
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                )
                return response.choices[0].text
            except RateLimitError:
                print(f"Requests to the model are at maximum capacity, cooling off before retrying the requests"
                      f" using exponential backoff.")
            except openai.error.APIError:
                print(f"The request ran into an OpenAI server issue. Retrying the request again.")

    def extract_invoice_info(self, data_fields, invoice_text, file_index):
        """
        :param file_index: For output, to provide reference for the file being processed by model.
        :param invoice_text: The text from invoice as input to extract information from.
        :param data_fields: values for data fields to extract
        :return: a string, comma separated with all the values we require.
        """

        extracted_values = ''

        if self.model == 'text-davinci-003':
            extracted_values = self.completions_with_backoff(data_fields, invoice_text)
            print(f"Extracting data field values from document {file_index}")

        elif self.model == 'gpt-3.5-turbo' or self.model == 'gpt-3.5-turbo-0301':

            extracted_values = self.chat_completions_with_backoff(data_fields, invoice_text)
            print(f"Extracting data field values from document {file_index}")

        return extracted_values
