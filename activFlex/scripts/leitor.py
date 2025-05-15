import pyexcel as pe
import pandas as pd
import tempfile
import os
import re

# Variável global para armazenar mensagens de debug
debug_log = []

def clean_debug_log():
    debug_log.clear()
    
def xlsx_para_csv(ficheiro, caminho_csv_temp):
    """Converte um ficheiro XLSX para CSV utilizando pandas."""
    try:
        debug(f"[INFO] A converter XLSX para CSV: {ficheiro}")
        df = pd.read_excel(ficheiro, engine='openpyxl')
        df.to_csv(caminho_csv_temp, index=False)
        debug(f"[SUCESSO] Ficheiro XLSX convertido para CSV.")
    except Exception as e:
        debug(f"[ERRO] Erro ao converter XLSX para CSV: {e}")
        raise


def xls_para_csv(ficheiro, caminho_csv_temp):
    """Converte um ficheiro XLS para CSV utilizando pandas."""
    try:
        debug(f"[INFO] A converter XLS para CSV: {ficheiro}")
        df = pd.read_excel(ficheiro, engine='xlrd')
        df.to_csv(caminho_csv_temp, index=False)
        debug(f"[SUCESSO] Ficheiro XLS convertido para CSV.")
    except Exception as e:
        debug(f"[ERRO] Erro ao converter XLS para CSV: {e}")
        raise

def debug(msg):
    """Adiciona uma mensagem ao log de debug."""
    debug_log.append(msg)
    print(msg)  # Opcional: pode ser removido em produção

def get_debug_log():
    """Retorna todo o conteúdo do log de debug como string."""
    return "\n".join(debug_log)


def converter_ods_para_xlsx(ficheiro_ods, ficheiro_xlsx):
    """Converte ficheiro ODS para XLSX."""
    try:
        debug(f"[INFO] A converter ODS para XLSX: {ficheiro_ods}")
        dados = pe.get_sheet(file_name=ficheiro_ods)
        dados.save_as(ficheiro_xlsx)
        debug(f"[SUCESSO] Conversão concluída: {ficheiro_xlsx}")
    except Exception as e:
        debug(f"[ERRO] Erro ao converter ODS para XLSX: {e}")


def ods_para_csv(caminho_arquivo_ods, caminho_arquivo_csv):
    """Converte um ficheiro ODS para CSV utilizando pyexcel."""
    try:
        debug(f"[INFO] A converter ODS para CSV: {caminho_arquivo_ods}")
        dados = pe.get_sheet(file_name=caminho_arquivo_ods)
        dados.save_as(caminho_arquivo_csv)
        debug(f"[SUCESSO] Ficheiro ODS convertido para CSV.")
    except Exception as e:
        debug(f"[ERRO] Erro ao converter ODS para CSV: {e}")
        raise  # Propagar o erro para que o `processar_ficheiro` o capture


def ler_csv_convertido(csv_path):
    """Extrai pares (NIB, valor transferido) com base na estrutura especificada."""
    df = pd.read_csv(csv_path, header=None, encoding='utf-8')
    transferencias = []

    for idx in range(2, len(df)):
        valor_celula_coluna_a = str(df.iloc[idx, 0]).strip()

        if valor_celula_coluna_a == "NIB/IBAN/Conta Ordenante":
            nib = str(df.iloc[idx, 1]).strip()
            if nib.startswith("PT50"):
                nib = nib[4:]

            valor = df.iloc[idx - 2, 4]

            try:
                valor_float = float(str(valor).replace(',', '.'))
                transferencias.append((nib, valor_float))
            except ValueError:
                debug(f"[AVISO] Valor inválido ignorado (linha {idx - 2}): '{valor}'")

    debug(f"[INFO] Extração concluída: {len(transferencias)} transferências válidas.")
    return transferencias


def processar_ficheiro(ficheiro):
    """Processa um ficheiro ODS e extrai NIBs e Montantes."""
    try:
        debug(f"[INFO] Início de processamento: {ficheiro}")

        ext = ficheiro.split('.')[-1].lower()
        caminho_csv_temp = 'extrato_bancario.csv'

        if ext == 'ods':
            ods_para_csv(ficheiro, caminho_csv_temp)
            return ler_csv_convertido(caminho_csv_temp)
        if ext == 'xlsx':
            xlsx_para_csv(ficheiro, caminho_csv_temp)
            return ler_csv_convertido(caminho_csv_temp)
        if ext == 'xls':
            xls_para_csv(ficheiro, caminho_csv_temp)
            return ler_csv_convertido(caminho_csv_temp)
        if ext == 'csv':
            return ler_csv_convertido(ficheiro)
        else:
            raise ValueError("Tipo de ficheiro não suportado. Apenas ODS é aceite.")

    except Exception as e:
        debug(f"[ERRO] Erro ao processar ficheiro: {e}")
        return []
