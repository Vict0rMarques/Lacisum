from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

#from repositories.AnuncioRepo import AnuncioRepo
#from repositories.ArtistaRepo import ArtistaRepo
#from repositories.ClubeRepo import ClubeRepo
#from repositories.ComentarioRepo import ComentarioRepo
from repositories.EstiloMusicalRepo import EstiloMusicalRepo
#from repositories.EventoRepo import EventoRepo
from repositories.MusicaRepo import MusicaRepo
from repositories.PublicacaoRepo import PublicacaoRepo
from repositories.UsuarioRepo import UsuarioRepo

from routes.MainRoutes import router as mainRouter
from routes.UsuarioRoutes import router as UsuarioRouter
from routes.VitrineRoutes import router as VitrineRouter
from routes.ClubeRoutes import router as ClubeRouter
from routes.EventoRoutes import router as EventoRouter
from routes.PlaylistRoutes import router as PlaylistRouter

from util.exceptionHandler import configurar as configurarExcecoes

#AnuncioRepo.criarTabela()
#ArtistaRepo.criarTabela()
#ClubeRepo.criarTabela()
#ComentarioRepo.criarTabela()
EstiloMusicalRepo.criarTabela()
#EventoRepo.criarTabela()
MusicaRepo.criarTabela()
PublicacaoRepo.criarTabela()
UsuarioRepo.criarTabela()
UsuarioRepo.criarUsuarioAdmin()
UsuarioRepo.criarUsuarioSemArtista()
estilos = EstiloMusicalRepo.obterTodos()
if len(estilos) == 0:
  EstiloMusicalRepo.inserirTodos()


app = FastAPI()

configurarExcecoes(app)

app.mount(path="/static", app=StaticFiles(directory="static"), name="static")

app.include_router(mainRouter)
app.include_router(VitrineRouter)
app.include_router(ClubeRouter)
app.include_router(EventoRouter)
app.include_router(PlaylistRouter)
app.include_router(UsuarioRouter)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)