import threading
import time

from pi import config, leitor, atuadores, api, offline


def atualizar_cache():
    try:
        colaboradores = api.buscar_colaboradores()
        offline.salvar_cache(colaboradores)
        return len(colaboradores)
    except Exception:
        print("[CACHE] Servidor indisponível, usando cache local")
        return None


def atualizar_cache_periodicamente():
    while True:
        time.sleep(config.INTERVALO_CACHE_SEGUNDOS)
        atualizar_cache()


def validar(tag_uid):
    try:
        resultado, mensagem = api.validar(tag_uid)
        return "ONLINE", resultado, mensagem
    except Exception:
        resultado, mensagem = offline.validar(tag_uid)
        return "OFFLINE", resultado, mensagem


def main():
    total = atualizar_cache()
    if total is not None:
        print(f"[CACHE] {total} colaboradores carregados")
    threading.Thread(target=atualizar_cache_periodicamente, daemon=True).start()

    ultima_tag = None
    ultima_leitura = 0

    print("Aguardando crachá...")
    try:
        while True:
            tag_uid = leitor.ler_tag()

            if tag_uid == ultima_tag and time.monotonic() - ultima_leitura < config.DEBOUNCE_SEGUNDOS:
                ultima_leitura = time.monotonic()
                continue

            modo, resultado, mensagem = validar(tag_uid)
            offline.atualizar_estado(tag_uid, resultado)
            print(f"[{modo}] {tag_uid} {resultado}: {mensagem}")
            atuadores.sinalizar(resultado)

            ultima_tag = tag_uid
            ultima_leitura = time.monotonic()
    except KeyboardInterrupt:
        print("\nEncerrando...")
    finally:
        leitor.encerrar()


if __name__ == "__main__":
    main()
