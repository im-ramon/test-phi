from langchain.prompts import ChatPromptTemplate
from langchain_community.embeddings.spacy_embeddings import SpacyEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_PATH = "chroma"
DATA_PATH = "data"

PROMPT_TEMPLATE = """
Você um assistente virtual do C3 (Centro de Comando, Controle e Comunicação). O C3 pertence à Segurança Empresarial da Acelen, uma empresa de energia.
Sua função será responder mensagens sobre procedimentos de segurança da Acelen.

Vou lhe passar alguns contextos para você se familiarizar com o tipo de pergunta que você receberá.
Siga todas as regras abaixo:

REGRAS:
1/ Suas respostas devem ser bem similares ou até idênticas ao contexto passado.
2/ Parte do contexto pode conter cabeçalhos e informações irrelevantes. Preste atenção apenas ao conteúdo útil da mensagem.
3/ Se nenhum contexto se encaixar ao conteúdo da pergunta, responda que você não sabe responder com precisão a dúvida, pois ainda não foi treinado sobre o assunto ao não o encontrou no banco de dados.
4/ Sempre cite o documento fonte no final.

Aqui está uma nova mensagem recebida:
MENSAGEM: {message}

Aqui estão contextos de procedimentos de segurança que são os mais similares que encontrei sobre o que você irá responder:

{context}

Analise os contextos passados e escreva a melhor resposta, obedecendo às regras que já te passei. Por favor, não repita a pergunta feita nem as instruções.
"""


def get_embedding_function():
    embeddings = SpacyEmbeddings(model_name="pt_core_news_lg")
    return embeddings


def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH,
                embedding_function=embedding_function)

    # Search the DB.
    query_results = db.similarity_search_with_score(query_text, k=5)

    context = [f"CONTEXTO {i + 1}: {doc.page_content}" for i,
               (doc, _score) in enumerate(query_results)]
    sources = [doc.metadata.get("id", None) for doc, _score in query_results]

    formated_context = "\n\n---\n\n".join(
        [a + f"\n* Documento fonte: {b.replace('data\\', '')}" for a,
         b in zip(context, sources)]
    )

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(
        context=formated_context, message=query_text)

    return prompt
