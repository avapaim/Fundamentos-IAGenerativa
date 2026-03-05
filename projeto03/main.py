from llm_client import LLMClient
from retriever import load_conhecimento, simple_retriever
from validator import validate_json, is_prompt_injection, injection_error_response
from prompt import build_system_prompt


def main():
    provider = input("Escolha o provedor (openai/groq): ").strip().lower()
    client = LLMClient(provider=provider)
    conhecimento = load_conhecimento()

    while True:
        query = input("Digite sua pergunta (ou 'sair' para encerrar): ").strip()
        if query.lower() == "sair":
            break

        # Proteção contra prompt injection
        if is_prompt_injection(query):
            data = injection_error_response()
            print(f"Resposta: {data['resposta']}")
            continue

        contexto = simple_retriever(query, conhecimento)
        system_prompt = build_system_prompt()

        user_prompt = f"CONTEXTO:\n{contexto}\n\nPERGUNTA:\n{query}"

        response_text = client.generate_text(system_prompt, user_prompt)

        try:
            is_valid, data = validate_json(response_text)
            if is_valid:
                print(f"Resposta: {data.get('resposta', '(sem campo resposta)')}")
        except ValueError as e:
            print(f"Erro de validação: {e}")


if __name__ == "__main__":
    main()