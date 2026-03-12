from openai import OpenAI
from dotenv import load_dotenv
from tools import data_atual
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Histórico de mensagens para manter o contexto da conversa
historico_mensagens = []


def salvar_historico(mensagem):
    historico_mensagens.append(mensagem)


def chat(pergunta):
    salvar_historico({"role": "user", "content": pergunta})

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=historico_mensagens
    )

    resposta_conteudo = resposta.choices[0].message.content
    salvar_historico({"role": "assistant", "content": resposta_conteudo})
    return resposta_conteudo


while True:
    pergunta = input("Você: ")

    if pergunta.lower() in ["sair", "exit", "quit"]:
        print("Encerrando o chat. Até mais!")
        break

    if "data" in pergunta.lower():
        salvar_historico({"role": "user", "content": pergunta})
        resposta = "Hoje é " + str(data_atual())
        salvar_historico({"role": "assistant", "content": resposta})
        print("Assistente: " + resposta)
        continue

    resposta = chat(pergunta)
    print("Assistente: ", resposta)
