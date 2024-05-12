# transparec-IA

## Introdução
Projeto Transparenc-IA: assistente para tirar dúvidas sobre o seu parlamentar (deputado ou senador) utilizando a inteligência artificial do google (Gemini) para processamento de linguagem natural. Possui UI de chat desenvolvida em Flask.

## Tecnologias utilizadas
- Flask - para o front e backend
- Langchain - para gerenciar cadeias de prompt de forma mais simples
- Dados obtidos do site [Ranking dos Políticos](https://politicos.org.br/)

## Como Reproduzir o projeto
1. Rode seguinte o comando no terminal para instalar os pacotes necessários:
~~~~sh
pip install -q requirements.txt
~~~~
2. crie um arquivo ".env" coloque a chave de api do google ai studio para adicionar a variável de ambiente ou coloque diretamente no projeto na variável `google_api_key`.
3. Rode o arquivo app.py e acesse (localmente) no http://localhost:5000/

## Screenshot:
![print](https://i.imghippo.com/files/IGPcp1715472586.png)