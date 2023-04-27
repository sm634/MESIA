from decouple import config
import openai

openai.api_key = config('OPENAI_API_KEY')


class Prompts:

    def __init__(self, max_tokens=2500, temperature=0):
        self.max_tokens = max_tokens
        self.temperature = temperature

    @staticmethod
    def __extract_invoice_prompt(data_fields, invoice_text):
        return f"""extract the values for {data_fields} from the text below:
                "{invoice_text}"
            """

    def extract_invoice_info(self, data_fields, invoice_text):
        """
        :param data_fields: values for data fields to extract
        :return: a string, comma separated with all of the values we require.
        """
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=self.__extract_invoice_prompt(data_fields=data_fields, invoice_text=invoice_text),
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        extracted_values = response.choices[0].text
        print("Extracting data field values")
        return extracted_values
