from typing import List
from util.Database import Database
from models.Usuario import Usuario

class UsuarioRepo:

    @classmethod
    def criarTabela(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            dataNascimento DATETIME NOT NULL,
            senha TEXT NOT NULL,
            admin BOOLEAN NOT NULL DEFAULT 0,
            token TEXT,
            biografia TEXT,
            qtdeSeguidores INTEGER,         
            dataCadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
            artista BOOLEAN,
            UNIQUE (email),
            UNIQUE (nome))
        """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tableCreated = cursor.execute(sql).rowcount > 0
        conexao.commit()
        conexao.close()
        return tableCreated

    @classmethod
    def criarUsuarioAdmin(cls) -> bool:
        sql = "INSERT OR IGNORE INTO usuario (nome, email, dataNascimento, senha, admin) VALUES (?, ?, ?, ?, ?)"
        # hash da senha 123456
        hash_senha = "$2b$12$WU9pnIyBUZOJHN7hgkhWtew8hI0Keiobr8idjIxYDwCyiSb5zh0iq"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql,
            ("Administrador", "admin@email.com", "2000-01-01", hash_senha, True))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def criarUsuarioSemArtista(cls) -> bool:
        sql = "INSERT OR IGNORE INTO usuario (nome, email, dataNascimento, senha, admin) VALUES (?, ?, ?, ?, ?)"
        # hash da senha 123456
        hash_senha = "$2b$12$WU9pnIyBUZOJHN7hgkhWtew8hI0Keiobr8idjIxYDwCyiSb5zh0iq"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql,
            ("Sem Artista", "semartista@email.com", "2000-01-01", hash_senha, False))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def inserir(cls, usuario: Usuario) -> Usuario:
        sql = "INSERT INTO usuario (nome, email, dataNascimento, senha) VALUES (?, ?, ?, ?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (usuario.nome, usuario.email, usuario.dataNascimento, usuario.senha))
        if resultado.rowcount > 0:
            usuario.id = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return usuario


    @classmethod
    def alterar(cls, usuario: Usuario) -> Usuario:
        sql = "UPDATE usuario SET nome=?, email=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (usuario.nome, usuario.email, usuario.id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return usuario
        else:
            conexao.close()
            return None

    @classmethod
    def alterarSenha(cls, id: int, senha: str) -> bool:
        sql = "UPDATE usuario SET senha=? WHERE id=?"
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
    def alterarToken(cls, email: str, token: str) -> bool:
        sql = "UPDATE usuario SET token=? WHERE email=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (token, email))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def alterarAdmin(cls, id: int, admin: bool) -> bool:
        sql = "UPDATE usuario SET admin=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (admin, id))
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
    def obterSenhaDeEmail(cls, email: str) -> str | None:
        sql = "SELECT senha FROM usuario WHERE email=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (email, )).fetchone()
        if resultado:
            return str(resultado[0])
        else:
            return None

    @classmethod
    def excluir(cls, id: int) -> bool:
        sql = "DELETE FROM usuario WHERE id=?"
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
    def obterTodos(cls) -> List[Usuario]:
        sql = "SELECT usuario.id, usuario.nome, usuario.email, usuario.dataNascimento, usuario.admin, usuario.biografia, usuario.qtdeSeguidores, usuario.dataCadastro, usuario.artista FROM usuario ORDER BY usuario.nome"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [
            Usuario(
                id=x[0],
                nome=x[1],
                email=x[2],
                dataNascimento=x[3],
                admin=x[4],
                biografia=x[5],
                qtdeSeguidores=x[6],
                dataCadastro=x[7],
                artista=x[8]
            ) for x in resultado
        ]
        return objetos

    @classmethod
    def obterPagina(cls, pagina: int, tamanhoPagina: int) -> List[Usuario]:
        inicio = (pagina - 1) * tamanhoPagina
        sql = "SELECT usuario.id, usuario.nome, usuario.email, usuario.dataNascimento, usuario.admin, usuario.biografia, usuario.qtdeSeguidores, usuario.dataCadastro, usuario.artista FROM usuario ORDER BY usuario.nome LIMIT ?, ?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (inicio, tamanhoPagina)).fetchall()
        objetos = [
            Usuario(
                id=x[0],
                nome=x[1],
                email=x[2],
                dataNascimento=x[3],
                admin=x[4],
                biografia=x[5],
                qtdeSeguidores=x[6],
                dataCadastro=x[7],
                artista=x[8]
            ) for x in resultado
        ]
        return objetos

    @classmethod
    def obterQtdePaginas(cls, tamanhoPagina: int) -> int:
        sql = "SELECT CEIL(CAST(COUNT(*) AS FLOAT) / ?) AS qtdePaginas FROM usuario"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (tamanhoPagina, )).fetchone()
        return int(resultado[0])

    @classmethod
    def obterPorId(cls, id: int) -> Usuario | None:
        sql = "SELECT usuario.id, usuario.nome, usuario.email, usuario.dataNascimento, usuario.admin, usuario.biografia, usuario.qtdeSeguidores, usuario.dataCadastro, usuario.artista FROM usuario WHERE usuario.id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id, )).fetchone()
        if resultado:
            objeto = Usuario(
                id=resultado[0],
                nome=resultado[1],
                email=resultado[2],
                dataNascimento=resultado[3],
                admin=resultado[4],
                biografia=resultado[5],
                qtdeSeguidores=resultado[6],
                dataCadastro=resultado[7],
                artista=resultado[8]
            )
            return objeto
        else:
            return None

    @classmethod
    def obterUsuarioPorToken(cls, token: str) -> Usuario | None:
        sql = "SELECT usuario.id, usuario.nome, usuario.email, usuario.dataNascimento, usuario.admin, usuario.biografia, usuario.qtdeSeguidores, usuario.dataCadastro, usuario.artista FROM usuario WHERE usuario.token=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        # quando se executa fetchone em um cursor sem resultado, ele retorna None
        resultado = cursor.execute(sql, (token,)).fetchone()
        if resultado:
            objeto = Usuario(
                id=resultado[0],
                nome=resultado[1],
                email=resultado[2],
                dataNascimento=resultado[3],
                admin=resultado[4],
                biografia=resultado[5],
                qtdeSeguidores=resultado[6],
                dataCadastro=resultado[7],
                artista=resultado[8]
            )
            return objeto
        else:
            return None
