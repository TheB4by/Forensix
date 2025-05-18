# Forensix - Digital Forensics Tool

**Forensix** is a beginner-friendly, GUI-based digital forensics tool built with Python and Tkinter. It allows users to collect and export forensic data from a Windows system, including running processes, installed applications, active network connections, and browser history. The interface features a dark theme, a modern layout, and a simple, intuitive button-based control system.

## 🔍 Features

- Collect running processes with PID, name, and user information  
- List installed applications from the Windows Registry  
- Display active network connections (IPv4/IPv6)  
- Extract browser history from a selected SQLite file (e.g., Chrome)  
- Export all collected data as an `.rtf` document with formatting

## 📂 Report Location

All collected data is saved automatically at:

```
C:\Users\<YourUser>\Desktop\Forensix\RESULTS\forensics_report.txt
```

## 🌐 Browser History Tip

To analyze browser history, select a valid SQLite file. For Chrome, it’s usually:

```
C:\Users\<YourUser>\AppData\Local\Google\Chrome\User Data\Default\History
```

> ⚠ Ensure the browser is closed before selecting the file to avoid read permission errors.

## 🛠 Requirements

- Python 3.x  
- Install required library:

```bash
pip install psutil
```

## 🚀 How to Run (Terminal)

1. Clone or download this repository  
2. Run the script using:

```bash
python forensix.py
```

## 🚀 How to Run (Windows)

1. Clone or download this repository  
2. Run the forensix.exe


## ⚠ Disclaimer

This tool is intended for **educational and forensic research purposes only**.  
Use it responsibly and **only with proper authorization**.
Sorry Linux users, Forensix does not yet support Linux in this version😔.

## ✔ Next Update!!!
1. Linux Terminal Suport
2. UI Improvement
3. Customization System
---

**Developer:** BABY  
**Version:** Sublevandis (1.2.0)  

```
Forensix - A Digital Forensics Tool
Made by BABY
Version Sublevandis (1.2.0)
------------------------------------
```
