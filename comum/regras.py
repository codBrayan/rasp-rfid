def decidir(colaborador, esta_dentro, entrou_hoje):
    if colaborador is None:
        return "INVASAO", "Acesso negado, tag não cadastrada"

    nome = colaborador["nome"]

    if esta_dentro:
        return "SAIDA", f"Até logo, {nome}"

    if not colaborador["ativo"] or not colaborador["acesso_sala"]:
        return "NEGADO", f"Acesso negado, {nome}"

    if entrou_hoje:
        return "ENTRADA", f"Bem-vindo de volta, {nome}"

    return "ENTRADA", f"Bem-vindo, {nome}"
