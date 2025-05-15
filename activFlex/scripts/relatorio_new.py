import os

def gerar_relatorios(pago, em_divida):
    """Gera os relatórios de 'Pago' e 'Em Dívida'."""
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # Limpar espaços extras nos nomes das colunas
    pago.columns = pago.columns.str.strip()
    em_divida.columns = em_divida.columns.str.strip()

    # Verificar se as colunas necessárias estão presentes
    colunas_finais = ['Nome','Email', 'Modalidade','Escalao', 'Pago', 'Valor Recebido']

    # Verificar se os DataFrames têm as colunas necessárias
    print("Verificando colunas necessárias...")
    if not all(col in pago.columns for col in colunas_finais) or not all(col in em_divida.columns for col in colunas_finais):
        
        return

    # Filtrar as colunas necessárias
    if not pago.empty:
        print("Gerando relatório para 'Pago'...")
        pago = pago[colunas_finais]
        pago.to_csv("output/pagos.csv", index=False, sep=';')
        print("Ficheiro 'pagos.csv' gerado.")

    if not em_divida.empty:
        print("Gerando relatório para 'Em Dívida'...")
        em_divida = em_divida[colunas_finais]
        em_divida.to_csv("output/em_divida.csv", index=False, sep=';')
        print("Ficheiro 'em_divida.csv' gerado.")

    print("Relatórios gerados com sucesso!")
