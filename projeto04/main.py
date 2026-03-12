from groq import Groq
from dotenv import load_dotenv
from tools import data_atual, calcular_imc
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

ARQUIVO_MEMORIA = "memoria_chat.json"

# Persona do assistente
SYSTEM_PROMPT = {
    "role": "system",
    "content": "Você é um assistente corporativo educado, objetivo e útil. Sempre responda de forma clara e profissional."
}

historico_mensagens = []


# -------------------------------
# Carregar histórico salvo
# -------------------------------

def carregar_memoria():
    global historico_mensagens
    if os.path.exists(ARQUIVO_MEMORIA):
        with open(ARQUIVO_MEMORIA, "r", encoding="utf-8") as f:
            historico_mensagens = json.load(f)
    else:
        historico_mensagens = [SYSTEM_PROMPT]


# -------------------------------
# Salvar histórico
# -------------------------------

def salvar_memoria():
    with open(ARQUIVO_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(historico_mensagens, f, indent=2, ensure_ascii=False)


# -------------------------------
# Adicionar mensagem ao histórico
# -------------------------------

def salvar_historico(mensagem):
    historico_mensagens.append(mensagem)

    # limitar memória (últimas 10 mensagens)
    if len(historico_mensagens) > 11:  
        historico_mensagens.pop(1)

    salvar_memoria()


# -------------------------------
# Limpar memória
# -------------------------------

def limpar_memoria():
    global historico_mensagens
    historico_mensagens = [SYSTEM_PROMPT]
    salvar_memoria()
    print("Assistente: Memória da conversa apagada.")


# -------------------------------
# Chat com LLM
# -------------------------------

def chat(pergunta):
    salvar_historico({"role": "user", "content": pergunta})

    resposta = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=historico_mensagens
    )

    resposta_conteudo = resposta.choices[0].message.content

    salvar_historico({"role": "assistant", "content": resposta_conteudo})

    return resposta_conteudo


# -------------------------------
# Programa principal
# -------------------------------

carregar_memoria()

while True:

    pergunta = input("Você: ")

    if pergunta.lower() in ["sair", "exit", "quit"]:
        print("Encerrando o chat.")
        break

    if pergunta.lower() == "/limpar":
        limpar_memoria()
        continue

    # Função 1 -> data
    if "data" in pergunta.lower():
        resposta = f"Hoje é {data_atual()}"
        salvar_historico({"role": "assistant", "content": resposta})
        print("Assistente:", resposta)
        continue

    # Função 2 -> IMC
    if "imc" in pergunta.lower():
        try:
            peso = float(input("Digite seu peso (kg): "))
            altura = float(input("Digite sua altura (m): "))

            resultado = calcular_imc(peso, altura)

            resposta = f"Seu IMC é {resultado:.2f}"

            salvar_historico({"role": "assistant", "content": resposta})

            print("Assistente:", resposta)

        except:
            print("Assistente: Não consegui calcular o IMC.")

        continue

    resposta = chat(pergunta)

    print("Assistente:", resposta)