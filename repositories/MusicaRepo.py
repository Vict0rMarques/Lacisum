from typing import List
from util.Database import Database
from models.Musica import Musica
from models.Artista import Artista

class MusicaRepo:

    @classmethod
    def criarTabela(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS musica (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idArtista INTEGER,
            idEstiloMusical INTEGER,
            nome TEXT NOT NULL,
            aprovado BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY (idArtista) REFERENCES Artista (idArtista),
            FOREIGN KEY (idEstiloMusical) REFERENCES EstiloMusical (id))
        """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tableCreated = cursor.execute(sql).rowcount > 0
        conexao.commit()
        conexao.close()
        return tableCreated

    @classmethod
    def inserir(cls, musica: Musica) -> Musica:
        sql = "INSERT INTO musica (nome, aprovado, idArtista, idEstiloMusical) VALUES (?, ?, ?, ?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (musica.nome, musica.aprovado, musica.idArtista, musica.idEstiloMusical))
        if resultado.rowcount > 0:
            musica.id = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return musica

    @classmethod
    def alterar(cls, musica: Musica) -> Musica:
        sql = "UPDATE musica SET nome=?, nomeArtista=?, aprovado=?, nomeEstiloMusical=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (musica.nome, musica.nomeArtista, musica.aprovado, musica.nomeEstiloMusical, musica.id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return musica
        else:
            conexao.close()
            return None

    @classmethod
    def aprovarMusica(cls, id: int, aprovar: bool = True) -> bool:
        sql = "UPDATE musica SET aprovado=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (aprovar, id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def excluir(cls, id: int) -> bool:
        sql = "DELETE FROM musica WHERE id=?"
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
    def obterTodos(cls) -> List[Musica]:
        sql = "SELECT musica.id, musica.nome, musica.idArtista, usuario.nome as nomeArtista, musica.idEstiloMusical, estilomusical.nome as nomeEstiloMusical FROM musica INNER JOIN usuario ON usuario.id = musica.idArtista INNER JOIN estilomusical ON estilomusical.id = musica.idEstiloMusical WHERE musica.aprovado = 1 ORDER BY  musica.nome"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [
            Musica(
                id=x[0],
                nome=x[1],
                idArtista=x[2],
                nomeArtista=x[3],
                idEstiloMusical=x[4],
                nomeEstiloMusical=x[5]
            ) for x in resultado
        ]
        return objetos

    @classmethod
    def obterTodosParaSelect(cls) -> List[Musica]:
        sql = "SELECT id, nome, nomeArtista, nomeEstiloMusical FROM musica ORDER BY nome"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [
            Musica(
                id=x[0],
                nome=x[1],
                nomeArtista=x[2],
                nomeEstiloMusical=x[3]
            ) for x in resultado
        ]
        return objetos

    @classmethod
    def obterPagina(cls, pagina: int, tamanhoPagina: int) -> List[Musica]:
        inicio = (pagina - 1) * tamanhoPagina
        sql = "SELECT musica.id, musica.nome, musica.idArtista, usuario.nome as nomeArtista, musica.idEstiloMusical, estilomusical.nome as nomeEstiloMusical FROM musica INNER JOIN usuario ON usuario.id = musica.idArtista INNER JOIN estilomusical ON estilomusical.id = musica.idEstiloMusical WHERE musica.aprovado = 1 ORDER BY musica.nome LIMIT ?, ?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (inicio, tamanhoPagina)).fetchall()
        objetos = [
            Musica(
                id=x[0],
                nome=x[1],
                idArtista=x[2],
                nomeArtista=x[3],
                idEstiloMusical=x[4],
                nomeEstiloMusical=x[5]
            ) for x in resultado
        ]
        return objetos

    @classmethod
    def obterQtdePaginas(cls, tamanhoPagina: int) -> int:
        sql = "SELECT CEIL(CAST((SELECT COUNT(*) FROM musica WHERE aprovado = 1) AS FLOAT) / ?) AS qtdePaginas"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (tamanhoPagina, )).fetchone()
        return int(resultado[0])

    @classmethod
    def obterPaginaAprovar(cls, pagina: int, tamanhoPagina: int) -> List[Musica]:
        inicio = (pagina - 1) * tamanhoPagina
        sql = "SELECT musica.id, musica.nome, musica.idArtista, usuario.nome as nomeArtista, musica.idEstiloMusical, estilomusical.nome as nomeEstiloMusical FROM musica INNER JOIN usuario ON usuario.id = musica.idArtista INNER JOIN estilomusical ON estilomusical.id = musica.idEstiloMusical WHERE musica.aprovado = 0 ORDER BY musica.nome LIMIT ?, ?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (inicio, tamanhoPagina)).fetchall()
        objetos = [
            Musica(
                id=x[0],
                nome=x[1],
                idArtista=x[2],
                nomeArtista=x[3],
                idEstiloMusical=x[4],
                nomeEstiloMusical=x[5]
            ) for x in resultado
        ]
        return objetos

    @classmethod
    def obterQtdePaginasAprovar(cls, tamanhoPagina: int) -> int:
        sql = "SELECT CEIL(CAST((SELECT COUNT(*) FROM musica WHERE aprovado = 0) AS FLOAT) / ?) AS qtdePaginas"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (tamanhoPagina, )).fetchone()
        return int(resultado[0])

    @classmethod
    def obterQtdeAprovar(cls) -> int:
        sql = "SELECT COUNT(*) FROM musica WHERE aprovado = 0"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchone()
        return int(resultado[0])

    @classmethod
    def obterPorId(cls, id: int) -> Musica | None:
        sql = "SELECT musica.id, musica.nome, musica.idArtista, usuario.nome as nomeArtista, musica.idEstiloMusical, estilomusical.nome as nomeEstiloMusical FROM musica WHERE musica.id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id,)).fetchone()
        conexao.close()
        if resultado:
            objeto = Musica(
                id=resultado[0],
                nome=resultado[1],
                idArtista=resultado[2],
                nomeArtista=resultado[3],
                idEstiloMusical=resultado[4],
                nomeEstiloMusical=resultado[5]
            )
            return objeto
        else:
            return None
