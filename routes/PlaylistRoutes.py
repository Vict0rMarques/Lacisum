from io import BytesIO

from fastapi import APIRouter, Depends, File, Form, Path, HTTPException, Request, UploadFile, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from PIL import Image

from models.EstiloMusical import EstiloMusical
from models.Musica import Musica
from models.Usuario import Usuario

from repositories.EstiloMusicalRepo import EstiloMusicalRepo
from repositories.MusicaRepo import MusicaRepo
from repositories.UsuarioRepo import UsuarioRepo

from util.imageUtil import transformar_em_quadrada
from util.security import validar_usuario_logado
from util.templateFilters import formatarData, formatarIdParaImagem
from util.validators import *

router = APIRouter(prefix="/playlist")
templates = Jinja2Templates(directory="templates")

@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData
    templates.env.filters["id_img"] = formatarIdParaImagem


@router.get("/listagem", response_class=HTMLResponse)
async def getListagem(
    request: Request,
    pa: int = 1,
    tp: int = 30,
):
  estiloMusical = EstiloMusicalRepo.obterTodos()
  musicas = MusicaRepo.obterPagina(pa, tp)
  totalPaginas = MusicaRepo.obterQtdePaginas(tp)
  qtdeAprovar = MusicaRepo.obterQtdeAprovar()
  return templates.TemplateResponse(
    "playlist/playlist.html",
    {
      "request": request,
      "totalPaginas": totalPaginas,
      "musicas": musicas,
      "paginaAtual": pa,
      "tamanhoPagina": tp,
      "qtdeAprovar": qtdeAprovar,
      "estilos": estiloMusical,
    },
  )
  


@router.get("/novamusica", response_class=HTMLResponse)
async def getNovaMusica(
  request: Request,
  usuario: Usuario = Depends(validar_usuario_logado),
):
  if usuario:
    usuarios = UsuarioRepo.obterTodos()
    estilos = EstiloMusicalRepo.obterTodos()
    return templates.TemplateResponse(
      "playlist/novamusica.html", 
      {
        "request": request,
        "usuario": usuario,
        "estilos": estilos,
        "usuarios": usuarios
      },
    )
  else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/novamusica")
async def postNovaMusica(
    request: Request,
    nome: str = Form(""),
    nomeArtista: str = Form(""),
    nomeEstiloMusical: str = Form(""),
    usuario: Usuario = Depends(validar_usuario_logado),
    capaMusica: UploadFile = File(...)
):
    # Verificação de erros
    erros = {}

    # Validação da imagem
    if capaMusica.content_type not in ["image/jpeg", "image/png"]:
        add_error("capaMusica", "Formato de imagem não suportado. Use JPEG ou PNG.", erros)

    conteudo_arquivo = await capaMusica.read()

    try:
        imagem = Image.open(BytesIO(conteudo_arquivo))
    except:
        add_error("capaMusica", "Não foi possível abrir a imagem.", erros)

    if not imagem:
        add_error("capaMusica", "Nenhuma imagem foi enviada.", erros)

    nova_musica = MusicaRepo.inserir(
        Musica(
            id=0,
            nome=nome,
            nomeArtista=nomeArtista,
            nomeEstiloMusical=nomeEstiloMusical,
        )
    )

    if nova_musica:
        imagem_quadrada = transformar_em_quadrada(imagem)
        imagem_quadrada.save(f"static/img/Musicas/{nova_musica.id:04d}.jpg", "JPEG")

    return templates.TemplateResponse(
        "playlist/playlist.html",
        {"request": request, "usuario": usuario},
    )



@router.get("/excluirmusica/{id:int}", response_class=HTMLResponse)
async def getExcluirMusica(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    id: int = Path(),
):
  if usuario:
    if usuario.admin:
      musica = MusicaRepo.obterPorId(id)
      return templates.TemplateResponse(
        "playlist/excluirmusica.html",
        {
          "request": request,
          "usuario": usuario,
          "musica": musica
        },
      )
    else:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
  else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/excluirmusica", response_class=HTMLResponse)
async def postExcluirMusica(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    id: int = Form(0),
):
  if usuario:
    if usuario.admin:
      if MusicaRepo.excluir(id):
        return RedirectResponse("/playlist/listagem",
                                status_code=status.HTTP_303_SEE_OTHER)
      else:
        raise Exception("Não foi possível excluir a música.")
    else:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
  else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/aprovarmusica/{id:int}", response_class=HTMLResponse)
async def getAprovarMusica(
    request: Request,
    id: int,
    usuario: Usuario = Depends(validar_usuario_logado),
):
  if usuario:
    if usuario.admin:
      return JSONResponse({"ok": MusicaRepo.aprovarMusica(id)})
    else:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
  else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/desaprovarmusica/{id:int}", response_class=HTMLResponse)
async def getDesaprovarMusica(
    request: Request,
    id: int,
    usuario: Usuario = Depends(validar_usuario_logado),
):
  if usuario:
    if usuario.admin:
      return JSONResponse({"ok": MusicaRepo.aprovarMusica(id, False)})
    else:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
  else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/aprovarmusica", response_class=HTMLResponse)
async def getAprovarMusica(
    request: Request,
    pa: int = 1,
    tp: int = 12,
    usuario: Usuario = Depends(validar_usuario_logado),
):
  if usuario:
    if usuario.admin:
      musicas = MusicaRepo.obterPaginaAprovar(pa, tp)
      totalPaginas = MusicaRepo.obterQtdePaginasAprovar(tp)
      return templates.TemplateResponse(
        "playlist/aprovarmusica.html",
        {
          "request": request,
          "musicas": musicas,
          "totalPaginas": totalPaginas,
          "paginaAtual": pa,
          "tamanhoPagina": tp,
          "usuario": usuario
        },
      )
    else:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
  else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)