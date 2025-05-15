import pandas as pd

def carregar_dados_atletas(futebol_file, futesal_file):
    """Carrega dados de futebol e futsal, adicionando a coluna 'Modalidade' com base no ficheiro de origem."""
    df_futebol = pd.read_csv(futebol_file, sep=';')
    df_futebol['Modalidade'] = 'Futebol'

    df_futsal = pd.read_csv(futesal_file, sep=';')
    df_futsal['Modalidade'] = 'Futsal'

    df_total = pd.concat([df_futebol, df_futsal], ignore_index=True)
    return df_total

def carregar_precos(precos_file):
    precos = {}
    with open(precos_file, "r") as f:
        for linha in f:
            # Cada linha é do tipo "modalidade: valor"
            modalidade, valor = linha.strip().split(":")
            precos[modalidade.strip()] = float(valor.strip())
    return precos

def categorizar_pagamentos(transferencias, futebol_file, futesal_file, precos_file):
    # Carregar os dados dos atletas e preços
    df_atletas = carregar_dados_atletas(futebol_file, futesal_file)
    precos = carregar_precos(precos_file)

    # Adicionar as colunas necessárias para pagamento e valor recebido
    df_atletas['Pago'] = False
    df_atletas['Valor Recebido'] = 0.0

    # Indexar NIBs (considerar até 3 por atleta)
    nib_para_nome = {}
    for _, row in df_atletas.iterrows():
        nome = row['Nome']
        for i in range(1, 4):
            nib = str(row.get(f'NIB {i}', '')).strip()
            if nib:
                nib_para_nome[nib] = nome

    # Registar os pagamentos
    for nib, valor in transferencias:
        nome = nib_para_nome.get(nib)
        if nome:
            # Atualizar o valor recebido para o atleta correspondente
            idx = df_atletas[df_atletas['Nome'] == nome].index
            df_atletas.loc[idx, 'Valor Recebido'] += valor

    pagos = []
    em_divida = []

    # Categorizar os atletas como pagos ou em dívida
    for _, row in df_atletas.iterrows():
        chave = (row['Modalidade'])
        print("chave:", chave)
        esperado = precos.get(chave, 0.0)
        print("esperado:", esperado)
        recebido = row['Valor Recebido']

        row_dict = row.to_dict()
        row_dict['Pago'] = recebido >= esperado and esperado > 0

        if row_dict['Pago']:
            pagos.append(row_dict)
        else:
            em_divida.append(row_dict)

    # Criar DataFrames para 'pagos' e 'em_divida'
    if not pagos:
        df_pago = pd.DataFrame(columns=['Nome', 'Escalao', 'Email', 'Modalidade', 'Pago', 'Valor Recebido'])
    else:
        df_pago = pd.DataFrame(pagos)

    if not em_divida:
        df_em_divida = pd.DataFrame(columns=['Nome', 'Escalao', 'Email', 'Modalidade', 'Pago', 'Valor Recebido'])
    else:
        df_em_divida = pd.DataFrame(em_divida)

    return df_pago, df_em_divida
