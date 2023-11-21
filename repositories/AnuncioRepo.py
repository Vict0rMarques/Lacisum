from typing import List
from models.Anuncio import Anuncio
from util.Database import Database


class AnuncioRepo:
    @classmethod
    def criarTabela(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS anuncio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            preco REAL NOT NULL,
            condicao TEXT NOT NULL,
            aprovado BOOLEAN,
            datahora DATETIME DEFAULT CURRENT_TIMESTAMP,
            idAnunciante INTEGER,
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
        sql = "INSERT INTO anuncio (titulo, descricao, preco, condicao) VALUES (?, ?, ?, ?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (anuncio.titulo, anuncio.descricao, anuncio.preco, anuncio.condicao)
        )
        if resultado.rowcount > 0:
            anuncio.id = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return anuncio


    @classmethod
    def alterar(cls, anuncio: Anuncio) -> Anuncio:
        sql = "UPDATE anuncio SET titulo=?, descricao=?, preco=?, condicao=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql,
            (
                anuncio.titulo,
                anuncio.descricao,
                anuncio.preco,
                anuncio.condicao,
                anuncio.id,
            ),
        )
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
        resultado = cursor.execute(sql, (id,))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def obterTodos(cls) -> List[Anuncio]:
        sql = "SELECT anuncio.id, anuncio.titulo, anuncio.descricao, anuncio.preco, anuncio.condicao, anuncio.idAnunciante, usuario.nome AS nomeAnunciante FROM usuario INNER JOIN anuncio ON usuario.id = anuncio.idAnunciante ORDER BY anuncio.titulo"
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
                nomeAnunciante=x[6],
            )
            for x in resultado
        ]
        return objetos

    @classmethod
    def obterTodosParaSelect(cls) -> List[Anuncio]:
        sql = "SELECT id, titulo FROM anuncio ORDER BY titulo"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [Anuncio(id=x[0], nome=x[1]) for x in resultado]
        return objetos

    @classmethod
    def obterPagina(cls, pagina: int, tamanhoPagina: int) -> List[Anuncio]:
        inicio = (pagina - 1) * tamanhoPagina
        sql = "SELECT anuncio.id, anuncio.titulo, anuncio.descricao, anuncio.preco, anuncio.condicao, anuncio.idAnunciante, usuario.nome AS nomeAnunciante FROM usuario INNER JOIN anuncio ON usuario.id = anuncio.idAnunciante ORDER BY anuncio.titulo LIMIT ?, ?"
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
                nomeAnunciante=x[6],
            )
            for x in resultado
        ]
        return objetos


    @classmethod
    def obterQtdePaginas(cls, tamanhoPagina: int) -> int:
        sql = "SELECT CEIL(CAST((SELECT COUNT(*) FROM anuncio WHERE aprovado = 1 AND idAnunciante IS NOT NULL) AS FLOAT) / ?) AS qtdePaginas"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (tamanhoPagina,)).fetchone()
        return int(resultado[0])

    @classmethod
    def obterPaginaAprovar(cls, pagina: int, tamanhoPagina: int) -> List[Anuncio]:
        inicio = (pagina - 1) * tamanhoPagina
        sql = "SELECT anuncio.id, anuncio.titulo, anuncio.descricao, anuncio.preco, anuncio.condicao, anuncio.idAnunciante, usuario.nome AS nomeAnunciante FROM usuario INNER JOIN anuncio ON usuario.idAnuncio = anuncio.id WHERE anuncio.aprovado = 0 ORDER BY anuncio.datahora LIMIT ?, ?"
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
                nomeAnunciante=x[6],
            )
            for x in resultado
        ]
        return objetos

    @classmethod
    def obterQtdePaginasAprovar(cls, tamanhoPagina: int) -> int:
        sql = "SELECT CEIL(CAST((SELECT COUNT(*) FROM anuncio WHERE aprovado = 0 AND idAnunciante IS NOT NULL) AS FLOAT) / ?) AS qtdePaginas"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (tamanhoPagina,)).fetchone()
        return int(resultado[0])

    @classmethod
    def obterQtdeAprovar(cls) -> int:
        sql = "SELECT COUNT(*) FROM anuncio WHERE aprovado = 0 AND idAnunciante IS NOT NULL"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchone()
        return int(resultado[0])

    @classmethod
    def obterPorId(cls, id: int) -> Anuncio | None:
        sql = "SELECT anuncio.id, anuncio.titulo, anuncio.descricao, anuncio.preco, anuncio.condicao, anuncio.aprovado, anuncio.idAnunciante, usuario.nome AS nomeAnunciante FROM usuario INNER JOIN anuncio ON usuario.idAnuncio = anuncio.id WHERE anuncio.id=?"
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
                aprovado=resultado[5],
                idAnunciante=resultado[6],
                nomeAnunciante=resultado[7],
            )
            return objeto
        else:
            return None

    @classmethod
    def obterAnunciantes(cls, id: int) -> List[str]:
        sql = "SELECT nome FROM usuario WHERE idAnuncio=? and aprovado=1 ORDER BY nome"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id,)).fetchall()
        if resultado:
            return [x[0] for x in resultado]
        else:
            return []
