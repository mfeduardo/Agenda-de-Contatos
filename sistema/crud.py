from msilib.schema import Error
from .bd import nova_conexao, criar_tabela
from hashlib import md5

class Crud:

    def inserirUsuario(self, nome, telefone, email, senha, nivel):
        with nova_conexao() as conexao:
            senha = senha.encode('utf8')
            cripto = md5(senha).hexdigest()

            try:
                cursor = conexao.cursor()
                cursor.execute("insert into contatos (nome, tel, email, senha, nivel) values ('" +
                               nome + "', '" + telefone + "', '" + email + "', '" + cripto + "', '" + nivel + "')")
                conexao.commit()
            except:
                print(f' Erro de inserção do registro!')

    def selecionarUsuarios(self, busca):
        args = (busca,)
        sql = f"SELECT * FROM contatos WHERE id = ? and nivel = 'usr'"

        with nova_conexao() as conexao:
            try:
                cursor = conexao.cursor()
                if type(busca) == str:
                    sql = f"SELECT * FROM contatos WHERE nome LIKE '%{busca}%' and nivel='usr' order by nome"
                    cursor.execute(sql)
                else:
                    cursor.execute(sql, args)
            except:
                print(f' Erro na consulta ao banco de dados!')
            else:
                resultado = [contato for contato in cursor]
                return resultado

    def selecionarAdmin(self):
        sql = "SELECT * FROM contatos WHERE id = 1 and nivel = 'adm'"
        with nova_conexao() as conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(sql)
            except:
                print(f' Erro na consulta ao banco de dados!')
            else:
                resultado = [contato for contato in cursor]
                return resultado
        

    def atualizarUsuario(self, id, nome, telefone, email):
        args = (id,)
        sql = "UPDATE contatos SET nome = '" + nome + "',tel = '" + \
            telefone + "', email = '" + email + "' where id = ? "

        with nova_conexao() as conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(sql, args)
                conexao.commit()

            except Error as e:
                print(f' Erro na na atualização do registro!', e)

    def excluirUsuario(self, id):
        sql = "delete from contatos where id=?"
        args = (id,)
        with nova_conexao() as conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(sql, args)
                conexao.commit()
            except:
                print(f' Erro na na exclusão do registro!')

    def checkLogin(self, email, senha):
        senha = senha.encode('utf8')
        cripto = md5(senha).hexdigest()
        args = (email, cripto)
        with nova_conexao() as conexao:
            try:
                sql = "SELECT * FROM contatos WHERE email=? AND senha=? AND nivel='adm' "
                cursor = conexao.cursor()
                cursor.execute(sql, args)
            except:
                print(f' Erro na consulta ao banco de dados!')
            else:
                resultado = [contato for contato in cursor]
                if resultado:
                    return resultado

    def config():
        criar_tabela()
