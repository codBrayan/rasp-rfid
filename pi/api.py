import requests

from pi import config


def validar(tag_uid):
    resposta = requests.post(
        f"{config.SERVIDOR_URL}/api/validar",
        json={"tag_uid": tag_uid},
        timeout=config.TIMEOUT_SEGUNDOS,
    )
    resposta.raise_for_status()
    dados = resposta.json()
    return dados["resultado"], dados["mensagem"]


def buscar_colaboradores():
    resposta = requests.get(
        f"{config.SERVIDOR_URL}/api/colaboradores",
        timeout=config.TIMEOUT_SEGUNDOS,
    )
    resposta.raise_for_status()
    return resposta.json()
