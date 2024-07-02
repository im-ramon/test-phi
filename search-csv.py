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
    print(*similar_response, sep='\n')
    return [doc.page_content for doc in similar_response]


text = input("Input: ")
if not text:
    print("Error, input cannot be empty")
    exit

context = retrive_info(text)

print(context)
