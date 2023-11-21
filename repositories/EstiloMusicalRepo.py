from typing import List
from util.Database import Database
from models.EstiloMusical import EstiloMusical


class EstiloMusicalRepo:

  @classmethod
  def criarTabela(cls):
    sql = """
            CREATE TABLE IF NOT EXISTS estilomusical (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT)
        """
    conexao = Database.criarConexao()
    cursor = conexao.cursor()
    tableCreated = cursor.execute(sql).rowcount > 0
    conexao.commit()
    conexao.close()
    return tableCreated

  @classmethod
  def inserirTodos(cls) -> None:
    estilos_musicais = [
      EstiloMusical(id=1, nome="Bossa Nova"),
      EstiloMusical(id=2, nome="Blues"),
      EstiloMusical(id=3, nome="Country"),
      EstiloMusical(id=4, nome="Eletrônica"),
      EstiloMusical(id=5, nome="Forró"),
      EstiloMusical(id=6, nome="Funk"),
      EstiloMusical(id=7, nome="Gospel"),
      EstiloMusical(id=8, nome="Hip Hop"),
      EstiloMusical(id=9, nome="Indie"),
      EstiloMusical(id=10, nome="Jazz"),
      EstiloMusical(id=11, nome="K-Pop"),
      EstiloMusical(id=12, nome="Metal"),
      EstiloMusical(id=13, nome="MPB"),
      EstiloMusical(id=14, nome="Punk"),
      EstiloMusical(id=15, nome="Pop"),
      EstiloMusical(id=16, nome="Reggae"),
      EstiloMusical(id=17, nome="Rock"),
      EstiloMusical(id=18, nome="Samba"),
      EstiloMusical(id=19, nome="Sertanejo"),
      EstiloMusical(id=20, nome="Trap")
    ]

    conexao = Database.criarConexao()
    cursor = conexao.cursor()

    for estilo in estilos_musicais:
      sql = "INSERT INTO estilomusical (nome) VALUES (?)"
      cursor.execute(sql, (estilo.nome, ))

    conexao.commit()
    conexao.close()

  @classmethod
  def obterTodos(cls) -> List[EstiloMusical]:
    sql = "SELECT id, nome FROM estilomusical ORDER BY nome"
    conexao = Database.criarConexao()
    cursor = conexao.cursor()
    resultado = cursor.execute(sql).fetchall()
    objetos = [EstiloMusical(*x) for x in resultado]
    return objetos

  @classmethod
  def obterPorId(cls, id: int) -> EstiloMusical:
    sql = "SELECT id, nome FROM estilomusical WHERE id=?"
    conexao = Database.criarConexao()
    cursor = conexao.cursor()
    resultado = cursor.execute(sql, (id, )).fetchone()
    objeto = EstiloMusical(*resultado)
    return objeto
