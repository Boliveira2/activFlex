import tkinter as tk
import pyexcel

from tkinter import filedialog, messagebox, ttk
from scripts.leitor import processar_ficheiro, get_debug_log, clean_debug_log
from scripts.processador_new import categorizar_pagamentos
from scripts.relatorio_new import gerar_relatorios
import os
import sys


def recurso_absoluto(rel_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.join(os.path.abspath("."), rel_path)

# Interface Tkinter
root = tk.Tk()
root.title("ActivFlex")
root.geometry("700x600")
root.configure(bg="#f0f0f0")
# Ícone removido para evitar erro
# root.iconbitmap(recurso_absoluto("assets/logo.ico"))


# Variáveis para caminhos dos ficheiros
caminho_futebol = tk.StringVar()
caminho_futsal = tk.StringVar()
caminho_precos = tk.StringVar()
caminho_extrato = tk.StringVar()

# Área de LOGS de debug (não editável)
text_debug = tk.Text(root, height=12, width=80, state='disabled', bg="#eeeeee", font=("Courier", 10))
text_debug.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

def atualizar_debug_texto():
    text_debug.config(state='normal')
    text_debug.delete(1.0, tk.END)
    text_debug.insert(tk.END, get_debug_log())
    text_debug.config(state='disabled')

def selecionar_ficheiro(var_destino, titulo, extensoes):
    caminho = filedialog.askopenfilename(title=titulo, filetypes=extensoes)
    if caminho:
        var_destino.set(caminho)

def carregar_e_processar_extrato():
    clean_debug_log()
    banco = combo_banco.get()

    if banco != "Crédito Agrícola":
        messagebox.showinfo("Banco não suportado", f"O parser ainda não suporta '{banco}'.")
        return

    if not all([caminho_futebol.get(), caminho_futsal.get(), caminho_precos.get(), caminho_extrato.get()]):
        messagebox.showwarning("Ficheiros em falta", "Por favor selecione todos os ficheiros: Futebol, Futsal e Preços.")
        return

    try:
        filepath = caminho_extrato.get()
        transferencias = processar_ficheiro(filepath)
        atualizar_debug_texto()
        if transferencias:
            messagebox.showinfo("Sucesso", f"{len(transferencias)} transferências processadas com sucesso!")
            df_pago, df_em_divida = categorizar_pagamentos(
                transferencias,
                caminho_futebol.get(),
                caminho_futsal.get(),
                caminho_precos.get()
            )
            gerar_relatorios(df_pago, df_em_divida)
        else:
            messagebox.showwarning("Aviso", "Nenhuma transferência encontrada ou erro durante o processamento.")
    except Exception as e:
        atualizar_debug_texto()
        messagebox.showerror("Erro", f"Erro ao processar o ficheiro: {e}")

# ComboBox do banco
label_banco = ttk.Label(root, text="Banco:", background="#f0f0f0", font=("Arial", 12))
label_banco.grid(row=0, column=0, padx=20, pady=10, sticky="e")

combo_banco = ttk.Combobox(root, values=["Crédito Agrícola", "Outros"], state="readonly", width=20, font=("Arial", 12))
combo_banco.grid(row=0, column=1, padx=20, pady=10, sticky="w")
combo_banco.current(0)

# Seleção dos ficheiros
def adicionar_selector(label_texto, var_destino, linha):
    lbl = ttk.Label(root, text=label_texto, background="#f0f0f0", font=("Arial", 11))
    lbl.grid(row=linha, column=0, sticky="e", padx=20, pady=5)
    entry = ttk.Entry(root, textvariable=var_destino, width=40, font=("Arial", 10))
    entry.grid(row=linha, column=1, sticky="w", padx=5)
    btn = ttk.Button(root, text="Selecionar", command=lambda: selecionar_ficheiro(var_destino, f"Selecionar {label_texto}", [("CSV", "*.csv"), ("Todos", "*.*")]))
    btn.grid(row=linha, column=1, sticky="e", padx=5)

def adicionar_selectortxt(label_texto, var_destino, linha):
    lbl = ttk.Label(root, text=label_texto, background="#f0f0f0", font=("Arial", 11))
    lbl.grid(row=linha, column=0, sticky="e", padx=20, pady=5)
    entry = ttk.Entry(root, textvariable=var_destino, width=40, font=("Arial", 10))
    entry.grid(row=linha, column=1, sticky="w", padx=5)
    btn = ttk.Button(root, text="Selecionar", command=lambda: selecionar_ficheiro(var_destino, f"Selecionar {label_texto}", [("TXT", "*.txt"), ("Todos", "*.*")]))
    btn.grid(row=linha, column=1, sticky="e", padx=5)

def adicionar_selectorextrato(label_texto, var_destino, linha):
    lbl = ttk.Label(root, text=label_texto, background="#f0f0f0", font=("Arial", 11))
    lbl.grid(row=linha, column=0, sticky="e", padx=20, pady=5)
    entry = ttk.Entry(root, textvariable=var_destino, width=40, font=("Arial", 10))
    entry.grid(row=linha, column=1, sticky="w", padx=5)
    btn = ttk.Button(root, text="Selecionar", command=lambda: selecionar_ficheiro(var_destino, f"Selecionar {label_texto}",
     [("Ficheiros de Extrato", "*.xlsx *.xls *.ods *.csv"), ("Todos os ficheiros", "*.*")]))
    btn.grid(row=linha, column=1, sticky="e", padx=5)

adicionar_selector("Ficheiro Futebol:", caminho_futebol, 1)
adicionar_selector("Ficheiro Futsal:", caminho_futsal, 2)
adicionar_selectortxt("Ficheiro Preços:", caminho_precos, 3)
adicionar_selectorextrato("Ficheiro Extrato:", caminho_extrato, 4)

# Botão principal
btn_carregar = tk.Button(root, text="Processar Pagamentos", command=carregar_e_processar_extrato,
                         width=25, height=2, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
btn_carregar.grid(row=5, column=0, columnspan=2, padx=20, pady=20)

root.mainloop()

def run_gui():
    print("GUI RUNNING")
