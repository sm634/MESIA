import json
import pandas as pd

"""User choose the prompt you want to use"""
prompt_choice = 1


def save_prompt_instructions(choice=prompt_choice):
    """Edit the fields to extract and prompt used for that choice below."""
    dict_output = {
        str(1): {"fields to extract": """Document Number,Document Date,Account No.,Payment Reference,Payment Terms,GBP""",
            "prompt": """Characteristics of the data fields you should extract are:
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

                        Extract those values from the text below and return nothing else:"""
            },
        str(2): {
            "fields to extract": """Invoice Number,Invoice Date,Organisation No.,Receipt Reference, Payment Terms, USD""",
            "prompt": """Characteristics of the data fields you should extract are:
                        Invoice Number - has prefix UMAR followed by 6 digits, ensure you bring these.
                        Invoice Date - is in format dd/mm/yy
                        Organisation No. - has 6 digits
                        Receipt Reference - has the Document Number / Account No.
                        Payment Terms - Can vary but includes time period related words and nothing else.
                        USD - Is a price value.

                        Some examples:
                        Invoice Number: UMAR123456
                        Invoice Date: 01/05/21
                        Organisation No.: 101022
                        Receipt Reference: UMAR123456 / 101022
                        Payment Terms: 90 Days after month end
                        OR
                        Payment Terms: 50 Days Date of Invoice
                        USD: 5,235.05

                        Extract those values from the text below and return nothing else:"""
        }
    }

    choice = str(choice)
    json_output = json.dumps(dict_output[choice])
    with open('reference_docs/prompt_instructions.json', 'w') as f:
        f.write(json_output)
        f.close()
