from typing import List
from models.Clube import Clube
from util.Database import Database

class ClubeRepo:
    
    @classmethod
    def criarTabela(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS clube (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL,
            tipo INTEGER NOT NULL,
            condicao TEXT NOT NULL,
            privacidade INTEGER NOT NULL,
            qtdeMembros INTEGER NOT NULL,
            idadeMinima INTEGER NOT NULL,
            idArtista INTEGER,
            idPropietario INTEGER,
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
    def inserir(cls, clube: Clube) -> Clube:
        sql = "INSERT INTO clube (nome, descricao, tipo, condicao, privacidade, qtdeMembros, idadeMinima) VALUES (?, ?, ?, ?, ?, ?, ?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (clube.nome, clube.descricao, clube.tipo, clube.condicao, clube.privacidade, clube.qtdeMembros, clube.idadeMinima)
        )
        if resultado.rowcount > 0:
            clube.id = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return clube
    
    @classmethod
    def alterar(cls, clube: Clube) -> Clube:
        sql = "UPDATE clube SET nome=?, descricao=?, tipo=?, condicao=?, privacidade=?, idadeMinima=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql,
            (
                clube.nome,
                clube.descricao,
                clube.tipo,
                clube.condicao,
                clube.privacidade,
                clube.idadeMinima,
                clube.id,
            ),
        )
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return clube
        else:
            conexao.close()
            return None

    @classmethod
    def excluir(cls, id: int) -> bool:
        sql = "DELETE FROM clube WHERE id=?"
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
    def obterTodos(cls) -> List[Clube]:
        sql = "SELECT clube.id, clube.nome, clube.descricao, clube.tipo, clube.condicao, clube.privacidade, clube.idadeMinima clube.idArtista, usuario.nome AS nomeArtista FROM usuario INNER JOIN clube ON usuario.idClube = clube.idArtista ORDER BY clube.nome"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [
            Clube(
                id=x[0],
                nome=x[1],
                descricao=x[2],
                tipo=x[3],
                condicao=x[4],
                privacidade=x[5],
                qtdeMembros=x[6],
                idadeMinima=x[7],
                idArtista=x[8],
                nomeArtista=x[9],
            )
            for x in resultado
        ]
        return objetos
    
    @classmethod
    def obterPagina(cls, pagina: int, tamanhoPagina: int) -> List[Clube]:
        inicio = (pagina - 1) * tamanhoPagina
        sql = "SELECT clube.id, clube.nome, clube.descricao, clube.tipo, clube.condicao, clube.privacidade, clube.idadeMinima clube.idArtista, usuario.nome AS nomeArtista FROM usuario INNER JOIN clube ON usuario.idClube = clube.idArtista ORDER BY clube.nome"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (inicio, tamanhoPagina)).fetchall()
        objetos = [
            Clube(
                id=x[0],
                nome=x[1],
                descricao=x[2],
                tipo=x[3],
                condicao=x[4],
                privacidade=x[5],
                qtdeMembros=x[6],
                idadeMinima=x[7],
                idArtista=x[8],
                nomeArtista=x[9],
            )
            for x in resultado
        ]
        return objetos