from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.retrievers import BM25Retriever
from secondary_chain import get_name_chain
from langchain_community.document_loaders import DataFrameLoader
import pandas as pd
import json
import markdown
import json
import os

def get_ai_response(questao):
    # Load environment variables
    google_api_key = os.getenv("GOOGLE_API_KEY")
    
    # Load JSON into DataFrame
    with open('./data/ranking.json', encoding='utf-8') as f:
        response = json.load(f)
        data = response['data']

    # Normalizar o json e selecionar as colunas que serão utilizadas
    df = pd.json_normalize(data)

    # substituir valores nulos por vazio
    df = df.fillna('')

    #preparar coluna para servir de índice
    df['parliamentarian.name.searchIndex'] ='nome do parlamentar: ' + df['parliamentarian.name']+'\nnomesalternativos (se houver): ' + df['parliamentarian.page.metaKeywords'] + ' ' + df['parliamentarian.nickname']

    columns_to_keep = ['parliamentarian.name','parliamentarian.name.searchIndex','parliamentarian.state.name','parliamentarian.position','parliamentarian.party.name','parliamentarian.relevantPositions','parliamentarian.summary','parliamentarian.academic','parliamentarian.quantityVote','parliamentarian.instagram','parliamentarian.page.metaDescription','parliamentarianStaffMaxYear','parliamentarianStaffAmountUsed','parliamentarianQuotaMaxYear','scoreSaveQuotaFormula']
    df = df[columns_to_keep]

    df.rename(columns={'parliamentarianStaffMaxYear':'orçamento de gastos com gabinete','parliamentarianStaffAmountUsed':'Gastos gabinete','parliamentarianQuotaMaxYear':"",'scoreSaveQuotaFormula':'relação (formula gastos totais / gastos totais disponiveis)'}, inplace=True)

    # carregar documentos
    loader = DataFrameLoader(df, page_content_column='parliamentarian.name.searchIndex')
    docs = loader.load()

    # intanciando o retriever BM25 para recuperar o contexto:
    retriever = BM25Retriever.from_documents(docs)

    # instanciando o modelo:
    model = 'gemini-pro'
    llm = ChatGoogleGenerativeAI(google_api_key=google_api_key, model=model)

    # definindo o prompt:
    template = """Você é um Assistente que tem acesso a dados de parlamentares do brasil referentes ao ano de 2023 fornecido no contexto.
    Dada uma pergunta sobre um parlamentar, você deve responder com informações sobre o parlamentar. responda a pergunta ao fim utilizando SOMENTE o contexto fornecido e quando aplicável, informe que os dados são referentes ao ano de 2023.
    caso não tenha dados suficientes para responder a pergunta, informe que não há dados suficientes sobre o parlamentar solicitado e peça para para que informa o nome completo do parlamentar.
    formatar a resposta apenas como html.

    contexto: {context}

    pergunta: {question}
    """

    prompt = PromptTemplate.from_template(template)

    #função para formatar os documentos para servir de contexto
    def format_docs(docs):
        context = []
        print('docs: ',docs)
        for doc in docs:
            page_content = doc.page_content
            for metadata_key, metadata_value in doc.metadata.items():
                page_content += f"\n{metadata_key}: {metadata_value}"
            context.append(page_content)
        context_string = "\n\n".join(context)
                
        return context_string
    
    #formatar a resposta final para html para ser consumida no front-end
    def format_response(response):
        formatted_response = markdown.markdown(response.replace("\n", "<br>"))
        print ('resposta: ',formatted_response)
        return formatted_response
    
    # cadeia de execução utilizando a biblioteca langchain
    rag_chain = (
        get_name_chain
        | {"context": retriever | format_docs, "question": lambda x: questao}
        | prompt
        | llm
        | StrOutputParser()
        | format_response
    )
    
    return rag_chain.invoke(questao)