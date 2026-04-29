import sqlite3

with sqlite3.connect('tarefas.db') as conn:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT
        )
    ''')

print("Banco de dados criado com sucesso!")