from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class KeywordExtractor:
    def __init__(self, model_name="bloomberg/KeyBART"):
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name, clean_up_tokenization_spaces=True)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def extract_keywords(self, prompt, max_length=100, num_beams=5, early_stopping=True):
        # Encode the prompt
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids

        # Generate the response
        output = self.model.generate(
            input_ids, max_length=max_length, num_beams=num_beams, early_stopping=early_stopping)

        # Decode the response
        response = self.tokenizer.decode(output[0])

        # Parse the output to list
        parsed_response = response.split(';')
        parsed_response = [item.replace('</s>', '').strip()
                           for item in parsed_response]

        return response, parsed_response


# Example usage:
if __name__ == "__main__":
    extractor = KeywordExtractor()
    response, parsed_response = extractor.extract_keywords(
        "who is theo depraetere")
    print(response)
    print(parsed_response)
