from openai import OpenAI
from keyword_extractor import KeywordExtractor
from google_search import google_query, scrape_url


class LlamaQuery:
    def __init__(self, prompt, api_key, base_url="http://localhost:7777/v1"):
        self.prompt = prompt
        self.api_key = api_key
        self.base_url = base_url
        self.keywords = []
        self.url_list = []
        self.context = ""
        self.num_search_results = 1
        self.max_num_keywords = 5

    def reset(self):
        self.keywords = []
        self.url_list = []
        self.context = ""

    def get_urls(self):
        return ', '.join(self.url_list)
    
    def get_keywords(self):
        return ', '.join(self.keywords)

    def set_num_searches(self, num_searches):
        self.num_search_results = num_searches

    def set_language(self, language):
        self.language = language

    def set_region(self, region):     
        self.region = region

    def set_max_num_keywords(self, max_num_keywords):
        self.max_num_keywords = max_num_keywords

    def run(self, RAG=False):
        if RAG:
            self.extract_keywords()
            self.perform_google_search()
            self.scrape_urls()
            self.save_context()

    def set_prompt(self, prompt):
        self.prompt = prompt

    def extract_keywords(self):
        response, keywords = KeywordExtractor().extract_keywords(self.prompt)
        print("------- Keywords: -------")
        self.keywords = keywords[:self.max_num_keywords]
        print(self.keywords)

    def perform_google_search(self):
        for query in self.keywords:
            if query.strip():
                search_results = google_query(query, self.num_search_results, self.language, self.region)
                if search_results:
                    self.url_list.extend(search_results)
        self.url_list = list(set(self.url_list))
        print("------- URL list: -------")
        print(self.url_list)

    def scrape_urls(self):
        for url in self.url_list:
            content = scrape_url(url)
            self.context += content + " "
        self.context = self.context.replace('\n', ' ').replace(
            '\r', ' ').replace('\t', ' ').strip()
        print("------- Context: -------")
        print(self.context[:100])

    def save_context(self, filename="context.txt"):
        with open(filename, "w", encoding="utf-8") as file:
            file.truncate(0)
            file.write(self.context)

    def get_completion(self):
        client = OpenAI(base_url=self.base_url, api_key=self.api_key)
        completion = client.chat.completions.create(
            model="1mstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
            messages=[
                {"role": "system", "content": ""},
                {"role": "user", "content": self.prompt},
                {"role": "assistant", "content": self.context},
            ],
            temperature=0.7,
        )
        return completion.choices[0].message.content


# Example usage
if __name__ == "__main__":
    prompt = "Who is ..."
    api_key = "lm-studio"

    llama_query = LlamaQuery(prompt, api_key)
    response = llama_query.run()
    print("\n------- Response: -------\n")
    print(response)
