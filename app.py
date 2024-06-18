import onnxruntime_genai as og

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SpacyEmbeddings
from langchain_community.document_loaders import CSVLoader


loader = CSVLoader(file_path="data.csv")
documents = loader.load()

embeddings = SpacyEmbeddings(model_name="pt_core_news_lg")
db = FAISS.from_documents(documents, embeddings)


def retrive_info(query):
    similar_response = db.similarity_search(query, k=3)
    return [doc.page_content for doc in similar_response]


model = og.Model('cpu_and_mobile/cpu-int4-rtn-block-32-acc-level-4')
tokenizer = og.Tokenizer(model)
tokenizer_stream = tokenizer.create_stream()

# Set the max length to something sensible by default,
# since otherwise it will be set to the entire context length
search_options = {
    'max_length': 2048,
}

text = input("Input: ")
if not text:
    print("Error, input cannot be empty")
    exit

context = retrive_info(text)

chat_template = """
<|user|>
Você se chama JOAQUIM. Você é uma assistem de uma central de monitoramento.
Sua função é responder os operadores sobre dúvidas sobre procedimentos de segurança.

Reponda a pergunta que irei te passar, baseando-se na melhor resposta desse contexto
CONTEXTO: {context}
PERGUNTA: {input}
<|end|>\n<|assistant|>
"""


prompt = f'{chat_template.format(input=text, context=context)}'

input_tokens = tokenizer.encode(prompt)

params = og.GeneratorParams(model)
params.set_search_options(**search_options)
params.input_ids = input_tokens
generator = og.Generator(model, params)

print("Output: ", end='', flush=True)

try:
    x = ''
    while not generator.is_done():
        generator.compute_logits()
        generator.generate_next_token()

        new_token = generator.get_next_tokens()[0]
        x += tokenizer_stream.decode(new_token)
        print(tokenizer_stream.decode(new_token), end='', flush=True)
    # print(x)
except KeyboardInterrupt:
    print("  --control+c pressed, aborting generation--")

print()
del generator
