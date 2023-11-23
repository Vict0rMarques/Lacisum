from typing import List
from models.Artista import Artista
from models.Usuario import Usuario
from repositories.UsuarioRepo import UsuarioRepo
from util.Database import Database


class ArtistaRepo:

    @classmethod
    def criarTabela(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS artista (
            idArtista INTEGER PRIMARY KEY,
            qtdeOuvintes INTEGER,
            FOREIGN KEY (idArtista) REFERENCES Usuario (id))
        """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tableCreated = cursor.execute(sql).rowcount > 0
        conexao.commit()
        conexao.close()
        return tableCreated

    @classmethod
    def inserir(cls, artista: Artista) -> Artista:
        usuario = UsuarioRepo.inserir(
          Usuario(
            artista.nome,
            artista.email,
            artista.dataNascimento,
            artista.senha,
            artista.biografia
          )
        )
        sql = "INSERT INTO artista (idArtista, qtdeOuvintes) VALUES ( ?, ?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (usuario.id, artista.qtdeOuvintes)
        )
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            artista.id = usuario.id
            return artista
        else:
          conexao.close()
          return None

    # @classmethod
    # def alterar(cls, artista: Artista) -> Artista:
    #     usuario = Usuario(
    #         idUsuario=artista.id,
    #         nome=artista.nome,
    #         dataNascimento=artista.dataNascimento,

    #     )
    #     UsuarioRepo.alterar(usuario)
    #     sql = "UPDATE artista SET nome=?, artista.email=?, idProjeto=? WHERE id=?"
    #     conexao = Database.criarConexao()
    #     cursor = conexao.cursor()
    #     resultado = cursor.execute(sql,
    #                                (artista.nome, artista.idProjeto, artista.id))
    #     if resultado.rowcount > 0:
    #         conexao.commit()
    #         conexao.close()
    #         return artista
    #     else:
    #         conexao.close()
    #         return None

    # @classmethod
    # def alterarSenha(cls, id: int, senha: str) -> bool:
        sql = "UPDATE artista SET senha=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (senha, id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def emailExiste(cls, email: str) -> bool:
        sql = "SELECT EXISTS (SELECT 1 FROM usuario WHERE email=?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (email, )).fetchone()
        return bool(resultado[0])

    @classmethod
    def obterPagina(cls, pagina: int, tamanhoPagina: int) -> List[Artista]:
        inicio = (pagina - 1) * tamanhoPagina
        sql = "SELECT idArtista, usuario.nome, usuario.email, usuario.dataNascimento, usuario.biografia FROM artista INNER JOIN usuario ON artista.idArtista = usuario.id ORDER BY usuario.nome LIMIT ?, ?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (inicio, tamanhoPagina)).fetchall()
        objetos = [
            Artista(
                id=x[0],
                nome=x[1],
                email=x[2],
                dataNascimento=x[3],
                biografia=x[4]
            ) for x in resultado
        ]
        return objetos

    @classmethod
    def obterQtdePaginas(cls, tamanhoPagina: int) -> int:
        sql = "SELECT CEIL(CAST((SELECT COUNT(*) FROM artista) AS FLOAT) / ?) AS qtdePaginas"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (tamanhoPagina, )).fetchone()
        return int(resultado[0])

    @classmethod
    def obterPorId(cls, idUsuario: int) -> Artista | None:
        sql = "SELECT idUsuario, usuario.nome, usuario.email, usuario.dataNascimento, usuario.biografia FROM artista INNER JOIN usuario ON artista.idArtista = usuario.id WHERE artista.idArtista = ?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id, )).fetchone()
        if (resultado):
            objeto = Artista(
                idUsuario=resultado[0],
                nome=resultado[1],
                email=resultado[2],
                dataNascimento=resultado[3],
                biografia=resultado[4]
            )
            return objeto
        else:
            return None