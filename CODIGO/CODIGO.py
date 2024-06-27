import wx
import sqlite3
import os

class CRUDFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(400, 300))
        
        self.panel = wx.Panel(self)
        
        self.lista_usuarios = wx.ListCtrl(self.panel, style=wx.LC_REPORT, pos=(10, 10), size=(380, 200))
        self.lista_usuarios.InsertColumn(0, 'ID', width=50)
        self.lista_usuarios.InsertColumn(1, 'Nome', width=150)
        
        btn_adicionar = wx.Button(self.panel, label='Adicionar', pos=(10, 220))
        btn_editar = wx.Button(self.panel, label='Editar', pos=(100, 220))
        btn_excluir = wx.Button(self.panel, label='Excluir', pos=(190, 220))
        
        self.Bind(wx.EVT_BUTTON, self.on_adicionar, btn_adicionar)
        self.Bind(wx.EVT_BUTTON, self.on_editar, btn_editar)
        self.Bind(wx.EVT_BUTTON, self.on_excluir, btn_excluir)
        
        self.carregar_usuarios()

    def conectar_bd(self):
        caminho_db = os.path.join(os.getcwd(), 'dados.db')  # Caminho absoluto do banco de dados
        conn = sqlite3.connect(caminho_db)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            )
        ''')
        conn.commit()
        return conn, cursor

    def fechar_bd(self, conn):
        conn.close()

    def carregar_usuarios(self):
        self.lista_usuarios.DeleteAllItems()
        conn, cursor = self.conectar_bd()
        cursor.execute('SELECT * FROM usuarios')
        for row in cursor.fetchall():
            index = self.lista_usuarios.InsertItem(self.lista_usuarios.GetItemCount(), str(row[0]))
            self.lista_usuarios.SetItem(index, 1, row[1])
        self.fechar_bd(conn)

    def on_adicionar(self, event):
        dialog = wx.TextEntryDialog(self.panel, 'Digite o nome do usuário:', 'Adicionar Usuário')
        if dialog.ShowModal() == wx.ID_OK:
            nome = dialog.GetValue()
            conn, cursor = self.conectar_bd()
            cursor.execute('INSERT INTO usuarios (nome) VALUES (?)', (nome,))
            conn.commit()
            self.fechar_bd(conn)
            self.carregar_usuarios()
        dialog.Destroy()

    def on_editar(self, event):
        index = self.lista_usuarios.GetFirstSelected()
        if index == -1:
            wx.MessageBox('Selecione um usuário para editar.', 'Erro', wx.OK | wx.ICON_ERROR)
            return
        
        dialog = wx.TextEntryDialog(self.panel, 'Digite o novo nome do usuário:', 'Editar Usuário')
        if dialog.ShowModal() == wx.ID_OK:
            novo_nome = dialog.GetValue()
            conn, cursor = self.conectar_bd()
            cursor.execute('UPDATE usuarios SET nome=? WHERE id=?', (novo_nome, int(self.lista_usuarios.GetItemText(index))))
            conn.commit()
            self.fechar_bd(conn)
            self.carregar_usuarios()
        dialog.Destroy()

    def on_excluir(self, event):
        index = self.lista_usuarios.GetFirstSelected()
        if index == -1:
            wx.MessageBox('Selecione um usuário para excluir.', 'Erro', wx.OK | wx.ICON_ERROR)
            return
        
        id_usuario = int(self.lista_usuarios.GetItemText(index))
        conn, cursor = self.conectar_bd()
        cursor.execute('DELETE FROM usuarios WHERE id=?', (id_usuario,))
        conn.commit()
        self.fechar_bd(conn)
        self.carregar_usuarios()

if __name__ == '__main__':
    app = wx.App()
    frame = CRUDFrame(None, 'CRUD com SQLite e wxPython')
    frame.Show()
    app.MainLoop()
