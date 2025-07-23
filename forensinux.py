import os
import platform
import sqlite3
import psutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, colorchooser, ttk
from datetime import datetime

# Confirma se o sistema é Linux
if platform.system() != "Linux":
    print("Este programa foi feito para rodar apenas no Linux.")
    exit()

# === Pergunta ao usuário o modo de operação ===
modo = input("Deseja usar a interface gráfica (GUI)? [s/n]: ").strip().lower()
USE_GUI = modo == "s"

# === Funções Lógicas ===
def log(message):
    if USE_GUI:
        output_text.insert(tk.END, message + "\n")
        output_text.see(tk.END)
    print(message)
    with open(report_file, "a", encoding="utf-8") as f:
        f.write(message + "\n")

def collect_running_processes():
    log("\n[+] Running Processes:")
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        log(f"PID: {proc.info['pid']} | Name: {proc.info['name']} | User: {proc.info['username']}")

def collect_installed_applications():
    log("\n[+] Installed Applications:")
    log("[-] Coleta de aplicativos instalada indisponível no Linux via este método.")

def collect_network_connections():
    log("\n[+] Active Network Connections:")
    for conn in psutil.net_connections(kind='inet'):
        if conn.raddr:
            log(f"IP: {conn.raddr[0]} | Port: {conn.raddr[1]} | Status: {conn.status}")

def collect_browser_history():
    path = browser_entry.get() if USE_GUI else input("Digite o caminho do banco de histórico do navegador (arquivo .sqlite): ")
    if not os.path.exists(path):
        if USE_GUI:
            messagebox.showerror("Erro", "Caminho inválido.")
        else:
            print("[ERRO] Caminho inválido.")
        return
    try:
        log("\n[+] Collecting Browser History:")
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute("SELECT url, title, visit_count FROM urls")
        for row in cursor.fetchall():
            log(f"URL: {row[0]} | Title: {row[1]} | Visit Count: {row[2]}")
        conn.close()
    except Exception as e:
        log(f"[!] Error reading browser history: {e}")

def save_results_as_rtf():
    try:
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        user = os.getlogin()
        rtf_file = filedialog.asksaveasfilename(defaultextension=".rtf", filetypes=[("RTF files", "*.rtf")])
        if not rtf_file:
            return
        with open(rtf_file, "w", encoding="utf-8") as f:
            f.write("{\\rtf1\\ansi\\deff0\n")
            f.write(f"\\b Forensix Report - {date_time} - User: {user} \\b0\n")
            f.write("\\par\n")
            with open(report_file, "r", encoding="utf-8") as report:
                for line in report:
                    f.write(line.replace("\n", "\\par\n"))
            f.write("}")
        messagebox.showinfo("Sucesso", "Resultados salvos como RTF!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar o arquivo RTF: {e}")

# === Setup Inicial ===
home = os.path.expanduser("~")
results_dir = os.path.join(home, "Desktop", "Forensix", "RESULTS")
os.makedirs(results_dir, exist_ok=True)
report_file = os.path.join(results_dir, "forensics_report.txt")

# === Se for modo terminal, executa os comandos direto ===
if not USE_GUI:
    log("Forensix - Modo Terminal Ativado\nFeito por BABY\nVersão 1.3.0\n------------------------------------")
    print("1 - Coletar Processos")
    print("2 - Conexões de Rede")
    print("3 - Histórico do Navegador")
    print("4 - Aplicativos Instalados (indisponível)")
    print("0 - Sair")
    while True:
        opc = input("\nEscolha uma opção: ").strip()
        if opc == "1":
            collect_running_processes()
        elif opc == "2":
            collect_network_connections()
        elif opc == "3":
            collect_browser_history()
        elif opc == "4":
            collect_installed_applications()
        elif opc == "0":
            break
        else:
            print("Opção inválida.")
    exit()

# === GUI ===
root = tk.Tk()
root.title("Forensix - Digital Forensics Tool")
root.geometry("700x500")
root.configure(bg="#1e1e2e")

notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Aba principal
main_frame = tk.Frame(notebook, bg="#1e1e2e")
notebook.add(main_frame, text="Principal")

tk.Label(main_frame, text="Forensix - GUI", font=("Arial", 16, "bold"), fg="#cba6f7", bg="#1e1e2e").pack(pady=10)

browser_frame = tk.Frame(main_frame, bg="#1e1e2e")
browser_frame.pack(pady=5)

tk.Label(browser_frame, text="Path to Browser History:", fg="white", bg="#1e1e2e").pack(side=tk.LEFT)
browser_entry = tk.Entry(browser_frame, width=60)
browser_entry.pack(side=tk.LEFT, padx=5)
tk.Button(browser_frame, text="📁", command=lambda: browser_entry.insert(0, filedialog.askopenfilename())).pack()

button_frame = tk.Frame(main_frame, bg="#1e1e2e")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Coletar Processos", command=collect_running_processes, width=20).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Aplicativos Instalados", command=collect_installed_applications, width=20).grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Conexões de Rede", command=collect_network_connections, width=20).grid(row=1, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Histórico do Navegador", command=collect_browser_history, width=20).grid(row=1, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Salvar como RTF", command=save_results_as_rtf, width=20).grid(row=2, column=0, columnspan=2, pady=5)

output_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=15, bg="#282a36", fg="#f8f8f2", insertbackground="white")
output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Aba de customização de cores
def choose_bg_color():
    color = colorchooser.askcolor()[1]
    if color:
        main_frame.configure(bg=color)
        browser_frame.configure(bg=color)
        button_frame.configure(bg=color)
        output_text.configure(bg=color)
        for widget in main_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=color)
            if isinstance(widget, tk.Frame):
                widget.configure(bg=color)

def choose_text_color():
    color = colorchooser.askcolor()[1]
    if color:
        output_text.configure(fg=color)

custom_frame = tk.Frame(notebook, bg="#1e1e2e")
notebook.add(custom_frame, text="Cores")

tk.Label(custom_frame, text="Personalizar Cores", font=("Arial", 14, "bold"), fg="#cba6f7", bg="#1e1e2e").pack(pady=10)
tk.Button(custom_frame, text="Cor do Fundo", command=choose_bg_color, width=20).pack(pady=5)
tk.Button(custom_frame, text="Cor do Texto", command=choose_text_color, width=20).pack(pady=5)

log("Forensix - A Digital Forensics Tool\nMade by BABY\nVersion 1.3.0\n------------------------------------")

root.mainloop()
