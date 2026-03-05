import json

# Lista de categorias permitidas
ALLOWED_CATEGORIES = [
    "vendas",
    "suporte",
    "financeiro",
    "geral"
]


def parse_json_response(response_text):
    """
    Converte o texto retornado pelo modelo em JSON.
    Retorna dict se válido, ou None se inválido.
    """
    try:
        data = json.loads(response_text)
        return data
    except json.JSONDecodeError:
        return None


def validate_category(data):
    """
    Verifica se a categoria retornada está na lista permitida.
    """
    if not data or "categoria" not in data:
        return None

    categoria = data["categoria"].lower()

    if categoria in ALLOWED_CATEGORIES:
        return categoria

    return None


def fallback_response():
    """
    Resposta segura caso o modelo falhe.
    """
    return {
        "categoria": "suporte",
        "fallback": True
    }


def safe_classification(response_text):
    """
    Pipeline completo:
    - Faz parse do JSON
    - Valida categoria
    - Retorna fallback se algo der errado
    """
    parsed = parse_json_response(response_text)

    if parsed is None:
        return fallback_response()

    categoria_valida = validate_category(parsed)

    if categoria_valida is None:
        return fallback_response()

    return {
        "categoria": categoria_valida,
        "fallback": False
    }
