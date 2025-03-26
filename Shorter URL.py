import requests
import tkinter as tk
from tkinter import messagebox, ttk
import pyperclip

TOKEN = ""

def shorten_url():
    long_url = entry.get()
    
    if not long_url:
        messagebox.showwarning("Peringatan", "Harap masukkan URL terlebih dahulu!")
        return
    
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }

    data = {
        "long_url": long_url,
        "domain": "bit.ly",
        "group_guid": "Bk23fMSTXih"
    }

    try:
        response = requests.post("https://api-ssl.bitly.com/v4/shorten", json=data, headers=headers)

        if response.status_code == 200:
            short_url = response.json()["link"]
            result_label.config(text=f"Short URL: {short_url}", fg="blue")
            
            history_table.insert("", "end", values=(long_url, short_url))
        else:
            error_msg = response.json().get("message", "Terjadi kesalahan!")
            messagebox.showerror("Error", f"Gagal memperpendek URL!\n{error_msg}")

    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

def copy_url():
    selected_item = history_table.selection()
    if selected_item:
        short_url = history_table.item(selected_item, "values")[1]
        pyperclip.copy(short_url)
        messagebox.showinfo("Info", "Short URL berhasil disalin ke clipboard!")
    else:
        messagebox.showwarning("Peringatan", "Pilih URL yang ingin disalin!")

root = tk.Tk()
root.title("Bit.ly URL Shortener")
root.geometry("500x400")

tk.Label(root, text="Masukkan URL yang ingin dipendekkan:", font=("Arial", 12)).pack(pady=5)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

tk.Button(root, text="Shorten", command=shorten_url, bg="blue", fg="white").pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=5)

tk.Label(root, text="Riwayat Link", font=("Arial", 12)).pack(pady=5)
columns = ("Long URL", "Short URL")
history_table = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    history_table.heading(col, text=col)
    history_table.column(col, width=200)
history_table.pack(pady=5)

tk.Button(root, text="Copy Selected URL", command=copy_url, bg="green", fg="white").pack(pady=10)

root.mainloop()