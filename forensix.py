import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import base64
import sqlite3
import psutil
import winreg
import sys
from datetime import datetime 

# === Funções Lógicas ===
def log(message):
    output_text.insert(tk.END, message + "\n")
    output_text.see(tk.END)
    with open(report_file, "a", encoding="utf-8") as f:
        f.write(message + "\n")

def collect_running_processes():
    log("\n[+] Running Processes:")
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        log(f"PID: {proc.info['pid']} | Name: {proc.info['name']} | User: {proc.info['username']}")

def collect_installed_applications():
    log("\n[+] Installed Applications:")
    try:
        reg_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        for reg_path in reg_paths:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                for i in range(0, winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            app_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            log(f"Application: {app_name}")
                    except FileNotFoundError:
                        continue
                    except Exception as e:
                        log(f"[!] Error reading application: {e}")
    except Exception as e:
        log(f"[!] Error collecting installed applications: {e}")

def collect_network_connections():
    log("\n[+] Active Network Connections:")
    for conn in psutil.net_connections(kind='inet'):
        if conn.raddr:
            log(f"IP: {conn.raddr[0]} | Port: {conn.raddr[1]} | Status: {conn.status}")

def collect_browser_history():
    path = browser_entry.get()
    if not os.path.exists(path):
        messagebox.showerror("Erro", "Caminho inválido.")
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
results_dir = os.path.join(os.environ["USERPROFILE"], "Desktop", "Forensix", "RESULTS")
os.makedirs(results_dir, exist_ok=True)
report_file = os.path.join(results_dir, "forensics_report.txt")

# === GUI ===
root = tk.Tk()
root.title("Forensix - Digital Forensics Tool")
root.geometry("700x500")
root.configure(bg="#1e1e2e")

tk.Label(root, text="Forensix - GUI", font=("Arial", 16, "bold"), fg="#cba6f7", bg="#1e1e2e").pack(pady=10)

browser_frame = tk.Frame(root, bg="#1e1e2e")
browser_frame.pack(pady=5)

tk.Label(browser_frame, text="Path to Browser History:", fg="white", bg="#1e1e2e").pack(side=tk.LEFT)
browser_entry = tk.Entry(browser_frame, width=60)
browser_entry.pack(side=tk.LEFT, padx=5)
tk.Button(browser_frame, text="📁", command=lambda: browser_entry.insert(0, filedialog.askopenfilename())).pack()

button_frame = tk.Frame(root, bg="#1e1e2e")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Coletar Processos", command=collect_running_processes, width=20).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Aplicativos Instalados", command=collect_installed_applications, width=20).grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Conexões de Rede", command=collect_network_connections, width=20).grid(row=1, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Histórico do Navegador", command=collect_browser_history, width=20).grid(row=1, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Salvar como RTF", command=save_results_as_rtf, width=20).grid(row=2, column=0, columnspan=2, pady=5)

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, bg="#282a36", fg="#f8f8f2", insertbackground="white")
output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

log("Forensix - A Digital Forensics Tool\nMade by BABY\nVersion Sublevandis (1.2.0)\n------------------------------------")

root.mainloop()