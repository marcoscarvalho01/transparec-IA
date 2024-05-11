from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Load environment variables
google_api_key = os.getenv("GOOGLE_API_KEY")

# instanciando o modelo:
model = 'gemini-pro'
llm = ChatGoogleGenerativeAI(google_api_key=google_api_key, model=model)

template = """você deve extrair do texto apenas os nomes dos parlamentares mencionados na pergunta e retornar apenas os nomes identificados e mais nada.
quando houver mais de um nome, retorne todos os nomes em uma única linha separados por vírgula.

pergunta: {question}
nomes:
"""

prompt = PromptTemplate.from_template(template)

get_name_chain = (
    prompt
    | llm
    | StrOutputParser()
)