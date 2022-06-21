import sqlite3
from contextlib import contextmanager

bd = 'sistema/bd/agenda.db'

@contextmanager
def nova_conexao():
    conexao = sqlite3.connect(bd)
    try:
        yield conexao
    finally:       
        conexao.close()

def criar_tabela():
    conexao = sqlite3.connect(bd)
    c = conexao.cursor()
    c.execute("""
    create table if not exists contatos(
    id integer primary key autoincrement,
    nome text,
    tel text,
    email text,
    senha text,
    nivel text default 'usr')
    """
    )
    
    conexao.commit()
    c.close()

