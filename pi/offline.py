import json
import os
from datetime import date, datetime

from comum.regras import decidir
from pi import config

CAMINHO_CACHE = os.path.join(config.PASTA_DADOS, "cache.json")
CAMINHO_ESTADO = os.path.join(config.PASTA_DADOS, "estado.json")
CAMINHO_EVENTOS = os.path.join(config.PASTA_DADOS, "eventos_offline.jsonl")


def ler_json(caminho, padrao):
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return padrao


def salvar_json(caminho, dados):
    os.makedirs(config.PASTA_DADOS, exist_ok=True)
    temporario = caminho + ".tmp"
    with open(temporario, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)
        arquivo.flush()
        os.fsync(arquivo.fileno())
    os.replace(temporario, caminho)


def salvar_cache(colaboradores):
    salvar_json(CAMINHO_CACHE, colaboradores)


def buscar_colaborador(tag_uid):
    for colaborador in ler_json(CAMINHO_CACHE, []):
        if colaborador["tag_uid"] == tag_uid:
            return colaborador
    return None


def carregar_estado():
    hoje = date.today().isoformat()
    estado = ler_json(CAMINHO_ESTADO, None)
    if estado is None or estado["data"] != hoje:
        estado = {"data": hoje, "dentro": [], "entraram": []}
    return estado


def atualizar_estado(tag_uid, resultado):
    estado = carregar_estado()
    if resultado == "ENTRADA":
        if tag_uid not in estado["dentro"]:
            estado["dentro"].append(tag_uid)
        if tag_uid not in estado["entraram"]:
            estado["entraram"].append(tag_uid)
    elif resultado == "SAIDA" and tag_uid in estado["dentro"]:
        estado["dentro"].remove(tag_uid)
    salvar_json(CAMINHO_ESTADO, estado)


def registrar_evento(tag_uid, nome, resultado):
    os.makedirs(config.PASTA_DADOS, exist_ok=True)
    evento = {
        "data_hora": datetime.now().isoformat(timespec="seconds"),
        "tag_uid": tag_uid,
        "nome": nome,
        "resultado": resultado,
    }
    with open(CAMINHO_EVENTOS, "a", encoding="utf-8") as arquivo:
        arquivo.write(json.dumps(evento, ensure_ascii=False) + "\n")


def validar(tag_uid):
    colaborador = buscar_colaborador(tag_uid)
    estado = carregar_estado()
    esta_dentro = tag_uid in estado["dentro"]
    entrou_hoje = tag_uid in estado["entraram"]
    resultado, mensagem = decidir(colaborador, esta_dentro, entrou_hoje)
    nome = colaborador["nome"] if colaborador else None
    registrar_evento(tag_uid, nome, resultado)
    return resultado, mensagem
