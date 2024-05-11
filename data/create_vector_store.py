from langchain_community.document_loaders import DataFrameLoader
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_chroma import Chroma
import pandas as pd
import json
def create_vector_store():
    # Load JSON into DataFrame
    with open('./ranking.json', encoding='utf-8') as f:
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

    # instanciar embeddings: O modelo BGE-Small-EN é um modelo de embeddings de texto multilíngue treinado pela BAAI. Ele é open source e gratuito. Poderíamos também utilizar o modelo de embeddings do próprio google, que teria um custo baixo, mas geraria um custo.
    model_name = "BAAI/bge-small-en"
    model_kwargs = {"device": "cpu"}
    encode_kwargs = {"normalize_embeddings": True}
    embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

    # instanciar vector store 
    vectorstore = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory='./data/vectorstore')
    return vectorstore