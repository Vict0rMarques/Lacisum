from typing import List
from models.Evento import Evento
from util.Database import Database

class EventoRepo:
    
    @classmethod
    def criarTabela(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS evento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL,
            datahora DATETIME DEFAULT CURRENT_TIMESTAMP,
            cidade TEXT NOT NULL,
            presencial TEXT NOT NULL,
            uf TEXT NOT NULL,
            foto BOOLEAN,
            url TEXT NOT NULL,
            idadeMinima INTEGER NOT NULL,
            gratuito TEXT NOT NULL,
            idArtista INTEGER,
            FOREIGN KEY (idArtista) REFERENCES usuario (id)
            )
        """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tableCreated = cursor.execute(sql).rowcount > 0
        conexao.commit()
        conexao.close()
        return tableCreated

    @classmethod
    def inserir(cls, evento: Evento) -> Evento:
        sql = "INSERT INTO evento (nome, descricao, cidade, presencial, uf, url, idadeMinima, gratuito) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (evento.nome, evento.descricao, evento.cidade, evento.presencial, evento.uf, evento.url, evento.idadeMinima, evento.gratuito)
        )
        if resultado.rowcount > 0:
            evento.id = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return evento
    
    @classmethod
    def alterar(cls, evento: Evento) -> Evento:
        sql = "UPDATE evento SET nome=?, descricao=?, cidade=?, presencial=?, uf=?, url=?, idadeMinima=? gratuito WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql,
            (
                evento.nome,
                evento.descricao,
                evento.cidade,
                evento.presencial,
                evento.uf,
                evento.url,
                evento.idadeMinima,
                evento.id,
            ),
        )
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return evento
        else:
            conexao.close()
            return None

    @classmethod
    def excluir(cls, id: int) -> bool:
        sql = "DELETE FROM evento WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id,))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def obterTodos(cls) -> List[Evento]:
        sql = "SELECT evento.nome, evento.descricao, evento.cidade, evento.presencial, evento.uf, evento.url, evento.idadeMinima, evento.gratuito evento.idArtista, usuario.nome AS nomeArtista FROM usuario INNER JOIN evento ON usuario.idEvento = evento.id ORDER BY evento.nome"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [
            Evento(
                id=x[0],
                nome=x[1],
                descricao=x[2],
                cidade=x[3],
                presencial=x[4],
                uf=x[5],
                url=x[6],
                idadeMinima=x[7],
                idArtista=x[8],
                nomeArtista=x[9],
            )
            for x in resultado
        ]
        return objetos