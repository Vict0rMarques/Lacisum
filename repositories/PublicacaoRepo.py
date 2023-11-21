from typing import List
from util.Database import Database
from models.Publicacao import Publicacao

class PublicacaoRepo:

    @classmethod
    def criarTabela(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS publicacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            legenda TEXT NOT NULL,
            publico BOOLEAN NOT NULL DEFAULT 0,
            dataPublicacao DATETIME DEFAULT CURRENT_TIMESTAMP,
            idAutor INTEGER NOT NULL,
            nomeAutor TEXT NOT NULL,
            nomeMusica TEXT NOT NULL,
            nomeArtista TEXT NOT NULL,
            FOREIGN KEY (idAutor) REFERENCES Usuario (id),
            FOREIGN KEY (nomeMusica) REFERENCES Musica (nome),
            FOREIGN KEY (nomeArtista) REFERENCES Musica (artista))
        """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tableCreated = cursor.execute(sql).rowcount > 0
        conexao.commit()
        conexao.close()
        return tableCreated

    @classmethod
    def inserir(cls, publicacao: Publicacao) -> Publicacao:
        sql = "INSERT INTO publicacao (legenda, publico, idAutor, nomeMusica, nomeArtista) VALUES (?, ?, ?, ?, ?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (publicacao.legenda, publicacao.publico, publicacao.idAutor, publicacao.nomeMusica, publicacao.nomeArtista))
        if resultado.rowcount > 0:
            publicacao.id = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return publicacao

    @classmethod
    def alterar(cls, publicacao: Publicacao) -> Publicacao:
        sql = "UPDATE publicacao SET legenda=?, publico=?, idAutor=?, nomeMusica=?, nomeArtista=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (publicacao.legenda, publicacao.publico, publicacao.idAutor, publicacao.nomeMusica, publicacao.nomeArtista, publicacao.id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return publicacao
        else:
            conexao.close()
            return None

    @classmethod
    def excluir(cls, id: int) -> bool:
        sql = "DELETE FROM publicacao WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id, ))
        if resultado.rowcount > 0:  
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def obterTodos(cls) -> List[Publicacao]:
        sql = "SELECT id, legenda, publico, dataPublicacao, idAutor, nomeMusica, nomeArtista FROM publicacao ORDER BY dataPublicacao"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [
            Publicacao(
                id=x[0],
                legenda=x[1],
                publico=x[2],
                dataPublicacao=x[3],
                idAutor=x[4],
                nomeMusica=x[5],
                nomeArtista=x[6]
            ) for x in resultado
        ]
        return objetos

    @classmethod
    def obterPorId(cls, id: int) -> Publicacao | None:
        sql = "SELECT id, legenda, publico, dataPublicacao, idAutor, nomeMusica, nomeArtista FROM publicacao WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id, )).fetchone()
        conexao.close()
        if resultado:
            objeto = Publicacao(
                id=resultado[0],
                legenda=resultado[1],
                publico=resultado[2],
                dataPublicacao=resultado[3],
                idAutor=resultado[4],
                nomeMusica=resultado[5],
                nomeArtista=resultado[6]
            )
            return objeto
        else:
            return None