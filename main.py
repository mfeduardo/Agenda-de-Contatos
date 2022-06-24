#####################################
# Agenda (versão 2.1)
# Desenvolvido por Eduardo Filgueiras
#####################################

from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
from sistema import Crud
import os


# Variáveis Globais
log = 0
usr = ''
ids = []
valor_id = 0
nivel = 'usr'
config = 0
# cadastro


def exibir_janela_cadastro():
    if log == 1:
        cadastro.show()
        reset_form_mensagens(cadastro)


def cadastrar():
    nome = cadastro.le_nome.text().strip()
    telefone = cadastro.le_telefone.text().strip()
    email = cadastro.le_email.text().strip()
    senha='#@s'
    reset_form_mensagens(cadastro)
    global nivel

    if nome and telefone and email:
        usuario = Crud()
        usuario.inserirUsuario(nome, telefone, email, senha, nivel)
        cadastro.le_nome.setText('')
        reset_form_cadastro()
        reset_form_mensagens(cadastro)
        msg = f'Contato inserido com sucesso!\nNome: {nome}'
        cadastro.lb_mensagem_2.setText(msg)
        cadastro.lb_mensagem_2.adjustSize()

        listar()

    else:
        reset_form_mensagens(cadastro)
        cadastro.lb_mensagem.setText('Preencha todas as informações!')
        cadastro.lb_mensagem.adjustSize()

# listagem


def listar(args=''):
    ids.clear()
    global valor_id
    valor_id = 0
    bd = Crud()
    contatos = bd.selecionarUsuarios(args)
    indice_id = -1
    main.tabela_listagem.setRowCount(len(contatos))
    main.tabela_listagem.setColumnCount(4)
    for contato in range(0, len(contatos)):
        for informacoes in range(0, 4):
            main.tabela_listagem.setItem(contato, informacoes, QtWidgets.QTableWidgetItem(
                str(contatos[contato][informacoes])))
            # adiciona id de referência para exclusão ou edição no array ids
            id_referencia = contatos[contato][0]
            if id_referencia != indice_id:
                ids.append(id_referencia)
            indice_id = id_referencia

# pesquisar


def pesquisar():
    busca = main.busca.text()
    if busca.isdigit():
        busca = int(busca)
    listar(busca)


# excluir

def excluir():
    registro_id = main.tabela_listagem.currentRow()
    id_excluir = ids[registro_id]
    bd = Crud()
    bd.excluirUsuario(id_excluir)
    ids.remove(id_excluir)
    main.tabela_listagem.removeRow(registro_id)

# editar


def exibir_janela_editar():
    if log == 1:
        registro_id = main.tabela_listagem.currentRow()
        id_editar = ids[registro_id]
        global valor_id
        valor_id = id_editar
        editar.show()
        reset_form_mensagens(editar)
        bd = Crud()
        contato = bd.selecionarUsuarios(id_editar)[0]
        editar.le_nome.setText(contato[1])
        editar.le_telefone.setText(contato[2])
        editar.le_email.setText(contato[3])


def atualizar():
    bd = Crud()
    bd.selecionarUsuarios(valor_id)
    nome = editar.le_nome.text().strip()
    telefone = editar.le_telefone.text().strip()
    email = editar.le_email.text().strip()
    

    if nome:
        bd = Crud()
        bd.atualizarUsuario(valor_id, nome, telefone, email)
        reset_form_mensagens(editar)
        editar.lb_mensagem_2.setText('Informações atualizadas!')
        editar.lb_mensagem_2.adjustSize()
        pesquisar()

    else:
        reset_form_mensagens(editar)
        editar.lb_mensagem.setText('Informe o nome do contato!')
        editar.lb_mensagem.adjustSize()

# reset forms


def reset_form_cadastro():
    cadastro.le_nome.setText('')
    cadastro.le_telefone.setText('')
    cadastro.le_email.setText('')


def reset_form_mensagens(janela):
    janela.lb_mensagem.setText('')
    janela.lb_mensagem_2.setText('')

# login


def logar():
    email = login.le_email.text().strip()
    senha = login.le_senha.text().strip()
    global config

    if email and senha:
        if config == 1:
            log_config(email, senha)

        bd = Crud()
        check = bd.checkLogin(email, senha)
        if check:
            login.close()
            global log
            log = 1
            global usr
            usr = check[0]
            main.show()
            listar()
        else:
            login.lb_mensagem.setText('Usuário ou senha incorreto!')
            login.lb_mensagem.adjustSize()
    else:
            login.lb_mensagem.setText('Preencha todas as informações!')
            login.lb_mensagem.adjustSize()


def log_config(email, senha):
    global config
    nome = 'admin'
    telefone = ''
    nivel = 'adm'
    usuario = Crud()
    usuario.inserirUsuario(nome, telefone, email, senha, nivel)
    config = 0


def logout():
    login.lb_mensagem.setText('')
    login.le_senha.setText('')
    global log
    log = 0
    global usr
    usr = ''
    editar.close()
    cadastro.close()
    main.close()
    login.show()

# messagebox


def msgbox():
    registro_id = main.tabela_listagem.currentRow()
    id_excluir = ids[registro_id]
    msg = QMessageBox()
    msg.setWindowTitle('Agenda | Excluir')
    msg.setText('Tem certeza que deseja excluir este contato?')
    msg.setIcon(QMessageBox.Icon.Question)
    msg.setStandardButtons(QMessageBox.StandardButton.Yes |
                           QMessageBox.StandardButton.No)
    msg.button(QMessageBox.StandardButton.Yes).setText('Sim')
    msg.button(QMessageBox.StandardButton.No).setText('Não')
    msg.setInformativeText(f'Código do Contato: {id_excluir}')

    dialogo = msg.exec()

    if dialogo == QMessageBox.StandardButton.Yes:
        excluir()


def infobox():
    info = QMessageBox()
    info.setWindowTitle('Agenda | Sobre')
    info.setText('Agenda (versão 2.1)\nPython/PyQt6/SQLite        ')
    info.setInformativeText(
        'Eduardo Filgueiras')
    info.exec()


# interface
app = QtWidgets.QApplication([])
# main
main = uic.loadUi('sistema/ui/main.ui')
main.bt_cadastrar.clicked.connect(exibir_janela_cadastro)
main.bt_sair.clicked.connect(logout)
main.bt_excluir.clicked.connect(msgbox)
main.bt_editar.clicked.connect(exibir_janela_editar)
main.tabela_listagem.setColumnWidth(0, 20)
main.tabela_listagem.setColumnWidth(1, 390)
main.tabela_listagem.setColumnWidth(2, 130)
main.tabela_listagem.setColumnWidth(3, 210)
main.actionNovo_Contato.triggered.connect(exibir_janela_cadastro)
main.bt_pesquisar.clicked.connect(pesquisar)
main.actionSair.triggered.connect(logout)
main.actionSobre.triggered.connect(infobox)
# cadastro
cadastro = uic.loadUi('sistema/ui/cadastro.ui')
cadastro.bt_cadastrar.clicked.connect(cadastrar)
# editar
editar = uic.loadUi('sistema/ui/editar.ui')
editar.bt_atualizar.clicked.connect(atualizar)
# login
login = uic.loadUi('sistema/ui/login.ui')
login.bt_login.clicked.connect(logar)
# config
if not os.path.exists('sistema/bd/agenda.db'):
    Crud.config()
if not Crud().selecionarAdmin():
    config = 1
    login.lb_mensagem.setText(
        'Este é o seu primeiro Acesso! Defina o seu login e senha!')
    login.lb_mensagem.adjustSize()
# inicializar
login.show()
app.exec()
