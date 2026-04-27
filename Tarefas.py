import tkinter as tk
from tkinter import messagebox
import sqlite3


with sqlite3.connect('tarefas.db') as conn:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT
        )
    ''')


root = tk.Tk()
root.title("To Do List - Versão 3")
root.geometry("420x500")

entry = tk.Entry(root, width=35)
entry.pack(pady=10)

lista = tk.Listbox(root, width=45, height=15)
lista.pack(pady=10)


def carregar():
    lista.delete(0, tk.END)

    with sqlite3.connect('tarefas.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, titulo FROM tarefas')

        for item in cursor.fetchall():
            lista.insert(tk.END, f'{item[0]} - {item[1]}')


def adicionar():
    titulo = entry.get().strip()

    if titulo:
        with sqlite3.connect('tarefas.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO tarefas (titulo) VALUES (?)',
                (titulo,)
            )

        entry.delete(0, tk.END)
        carregar()
    else:
        messagebox.showwarning("Aviso", "Digite uma tarefa.")


def remover():
    selecionado = lista.curselection()

    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione uma tarefa.")
        return

    texto = lista.get(selecionado[0])
    tarefa_id = int(texto.split(' - ')[0])

    with sqlite3.connect('tarefas.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tarefas WHERE id=?', (tarefa_id,))

    carregar()



btn_add = tk.Button(root, text="Adicionar", command=adicionar)
btn_add.pack(pady=5)

btn_del = tk.Button(root, text="Remover Selecionada", command=remover)
btn_del.pack(pady=5)


carregar()
root.mainloop()