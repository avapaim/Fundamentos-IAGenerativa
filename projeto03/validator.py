import json
import re

def validate_json(response_text):
    try:
        data = json.loads(response_text)
        if "status" not in data:
            raise ValueError("Campo 'status' obrigatório")
        return True, data
    except json.JSONDecodeError as e:
        raise ValueError(f"Erro ao decodificar JSON: {e}")


_INJECTION_PATTERNS = [
    r"system prompt",
    r"developer message",
    r"ignore (all|any|previous) instructions",
    r"disregard (all|any|previous) instructions",
    r"reveal.*prompt",
    r"show.*prompt",
    r"jailbreak",
    r"ignore as instru(ç|c)ões",
    r"mostre.*prompt",
    r"me diga.*prompt",
]

def is_prompt_injection(user_text: str) -> bool:
    t = (user_text or "").lower()
    return any(re.search(p, t) for p in _INJECTION_PATTERNS)

def injection_error_response():
    return {
        "status": "blocked",
        "resposta": "Solicitação bloqueada por segurança (tentativa de prompt injection)."
    }