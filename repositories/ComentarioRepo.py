from typing import List
from util.Database import Database
from models.Comentario import Comentario

class ComentarioRepo:
    
    @classmethod
    def criarTabela(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS comentario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comentario TEXT NOT NULL,
            dataComentario DATETIME DEFAULT CURRENT_TIMESTAMP
            nomeAutor TEXT NOT NULL,
            FOREIGN KEY (nomeAutor) REFERENCES Usuario (nome),
            nomeArtista TEXT NOT NULL,
            FOREIGN KEY (nomeArtista) REFERENCES Artista (nome))
        """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tableCreated = cursor.execute(sql).rowcount > 0
        conexao.commit()
        conexao.close()
        return tableCreated
    
    @classmethod
    def inserir(cls, musica: Musica) -> Musica:
        sql = "INSERT INTO musica (nome, nomeEstiloMusical, nomeArtista) VALUES (?, ?, ?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (musica.nome, musica.nomeEstiloMusical, musica.nomeArtista))
        if resultado.rowcount > 0:
            musica.id = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return musica
    
    @classmethod
    def alterar(cls, musica: Musica) -> Musica:
        sql = "UPDATE musica SET nome=?, nomeEstiloMusical=?, nomeArtista=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (musica.nome, musica.nomeEstiloMusical, musica.nomeArtista, musica.id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return musica
        else:
            conexao.close()
            return None
    
    @classmethod
    def excluir(cls, id: int) -> bool:
        sql = "DELETE FROM musica WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id, ))
        if resultado.rowcountc> 0:  
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False
        
    @classmethod
    def obterTodos(cls) -> List[Musica]:
        sql = "SELECT musica.id, musica.nome, musica.nomeEstiloMusical, musica.nomeArtista ORDER BY musica.nome"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [
            Musica(
                id=x[0],
                nome=x[1],
                nomeEstiloMusical=x[2],
                nomeArtista=x[3]
            ) for x in resultado
        ]
        return objetos
    
    @classmethod
    def obterPagina(cls, pagina: int, tamanhoPagina: int) -> List[Musica]:
        inicio = (pagina - 1) * tamanhoPagina
        sql = "SELECT musica.id, musica.nome, musica.nomeEstiloMusical, musica.nomeArtista ORDER BY musica.nome LIMIT ?, ?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (inicio, tamanhoPagina)).fetchall()
        objetos = [
            Musica(
                id=x[0],
                nome=x[1],
                nomeEstiloMusical=x[2],
                nomeArtista=x[3]
            ) for x in resultado
        ]
        return objetos
    
    @classmethod
    def obterQtdePaginas(cls, tamanhoPagina: int) -> int:
        sql = "SELECT CEIL(CAST(COUNT(*) AS FLOAT) / ?) AS qtdePaginas FROM musica WHERE idMusica IS NOT NULL"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (tamanhoPagina, )).fetchone()
        return int(resultado[0])

    @classmethod
    def obterPorId(cls, id: int) -> Musica | None:
        sql = "SELECT musica.id, musica.nome, musica.nomeEstiloMusical, musica.nomeArtista WHERE musica.id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id, )).fetchone()
        if (resultado):
            objeto = Musica(
                id=x[0],
                nome=x[1],
                nomeEstiloMusical=x[2],
                nomeArtista=x[3]
            )
            return objeto
        else:
            return None