from typing import List
from models.Anuncio import Anuncio
from util.Database import Database


class AnuncioRepo:
    @classmethod
    def criarTabela(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS anuncio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idAnunciante INTEGER,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            preco REAL NOT NULL,
            condicao TEXT NOT NULL,
            datahora DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (idAnunciante) REFERENCES usuario (id)
            )
        """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tableCreated = cursor.execute(sql).rowcount > 0
        conexao.commit()
        conexao.close()
        return tableCreated

    @classmethod
    def inserir(cls, anuncio: Anuncio) -> Anuncio:
        sql = "INSERT INTO anuncio (titulo, descricao, preco, condicao, idAnunciante) VALUES (?, ?, ?, ?, ?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (anuncio.titulo, anuncio.descricao, anuncio.preco, anuncio.condicao, anuncio.idAnunciante))
        if resultado.rowcount > 0:
            anuncio.id = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return anuncio
        
    @classmethod
    def alterar(cls, anuncio: Anuncio) -> Anuncio:
        sql = "UPDATE anuncio SET titulo=?, descricao=?, preco=?, condicao=?, nomeAnunciante WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (anuncio.titulo, anuncio.descricao, anuncio.preco, anuncio.condicao, anuncio.nomeAnunciante, anuncio.id,))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return anuncio
        else:
            conexao.close()
            return None
        
    @classmethod
    def excluir(cls, id: int) -> bool:
        sql = "DELETE FROM anuncio WHERE id=?"
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
    def obterTodos(cls) -> List[Anuncio]:
        sql = "SELECT anuncio.id, anuncio.titulo, anuncio.descricao, anuncio.preco, anuncio.condicao, anuncio.idUsuario, usuario.nome as nomeAnunciante FROM usuario INNER JOIN usuario ON usuario.id = anuncio.idAnunciante ORDER BY anuncio.titulo"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [
            Anuncio(
                id=x[0],
                titulo=x[1],
                descricao=x[2],
                preco=x[3],
                condicao=x[4],
                idAnunciante=x[5],
                nomeAnunciante=x[6]
            )
            for x in resultado
        ]
        return objetos

    @classmethod
    def obterTodosParaSelect(cls) -> List[Anuncio]:
        sql = "SELECT id, titulo, descricao, preco, condicao FROM anuncio ORDER BY titulo"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [
            Anuncio(
                id=x[0],
                titulo=x[1],
                descricao=x[2],
                preco=x[3],
                condicao=x[4],
                idAnunciante=x[5],
                nomeAnunciante=x[6]
            ) for x in resultado
        ]
        return objetos

    @classmethod
    def obterPagina(cls, pagina: int, tamanhoPagina: int) -> List[Anuncio]:
        inicio = (pagina - 1) * tamanhoPagina
        sql = "SELECT anuncio.id, anuncio.titulo, anuncio.descricao, anuncio.preco, anuncio.condicao, anuncio.idAnunciante, usuario.nome as nomeAnunciante FROM anuncio INNER JOIN usuario ON usuario.id = anuncio.idAnunciante ORDER BY anuncio.titulo LIMIT ?, ?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (inicio, tamanhoPagina)).fetchall()
        objetos = [
            Anuncio(
                id=x[0],
                titulo=x[1],
                descricao=x[2],
                preco=x[3],
                condicao=x[4],
                idAnunciante=x[5],
                nomeAnunciante=x[6]
            )
            for x in resultado
        ]
        return objetos


    @classmethod
    def obterQtdePaginas(cls, tamanhoPagina: int) -> int:
        sql = "SELECT CEIL(CAST((SELECT COUNT(*) FROM anuncio) AS FLOAT) / ?) AS qtdePaginas"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (tamanhoPagina,)).fetchone()
        return int(resultado[0])



    @classmethod
    def obterPorId(cls, id: int) -> Anuncio | None:
        sql = "SELECT anuncio.id, anuncio.titulo, anuncio.descricao, anuncio.preco, anuncio.condicao, anuncio.idUsuario, usuario.nome as nomeAnunciante FROM anuncio INNER JOIN anuncio ON usuario.idAnuncio = anuncio.id WHERE anuncio.id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id,)).fetchone()
        if resultado:
            objeto = Anuncio(
                id=resultado[0],
                titulo=resultado[1],
                descricao=resultado[2],
                preco=resultado[3],
                condicao=resultado[4],
                idAnunciante=resultado[5],
                nomeAnunciante=resultado[6]
            )
            return objeto
        else:
            return None

    # @classmethod
    # def obterAnunciantes(cls, id: int) -> List[str]:
    #     sql = "SELECT nome FROM usuario WHERE idAnuncio=? and aprovado=1 ORDER BY nome"
    #     conexao = Database.criarConexao()
    #     cursor = conexao.cursor()
    #     resultado = cursor.execute(sql, (id,)).fetchall()
    #     if resultado:
    #         return [x[0] for x in resultado]
    #     else:
    #         return []
