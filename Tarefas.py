import tkinter as tk
from tkinter import messagebox
import sqlite3


class BancoTarefas:
    def __init__(self, db_name='tarefas.db'):
        self.db_name = db_name

    def listar(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, titulo FROM tarefas')
            return cursor.fetchall()

    def adicionar(self, titulo):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO tarefas (titulo) VALUES (?)',
                (titulo,)
            )

    def remover(self, tarefa_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'DELETE FROM tarefas WHERE id=?',
                (tarefa_id,)
            )


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("To Do List")
        self.root.geometry("420x500")

        self.db = BancoTarefas()

        self.entry = tk.Entry(root, width=35)
        self.entry.pack(pady=10)

        self.lista = tk.Listbox(root, width=45, height=15)
        self.lista.pack(pady=10)

        btn_add = tk.Button(root, text="Adicionar", command=self.adicionar)
        btn_add.pack(pady=5)

        btn_del = tk.Button(root, text="Remover Selecionada", command=self.remover)
        btn_del.pack(pady=5)

        self.carregar()

    def carregar(self):
        self.lista.delete(0, tk.END)

        for item in self.db.listar():
            self.lista.insert(tk.END, f'{item[0]} - {item[1]}')

    def adicionar(self):
        titulo = self.entry.get().strip()

        if not titulo:
            messagebox.showwarning("Aviso", "Digite uma tarefa.")
            return

        self.db.adicionar(titulo)

        self.entry.delete(0, tk.END)
        self.carregar()

    def remover(self):
        selecionado = self.lista.curselection()

        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma tarefa.")
            return

        texto = self.lista.get(selecionado[0])
        tarefa_id = int(texto.split(' - ')[0])

        self.db.remover(tarefa_id)
        self.carregar()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()