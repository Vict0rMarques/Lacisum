from io import BytesIO

from fastapi import APIRouter, Depends, File, Form, Path, HTTPException, Request, UploadFile, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from PIL import Image

from models.Musica import Musica
from models.Usuario import Usuario
from models.Anuncio import Anuncio

from repositories.MusicaRepo import MusicaRepo
from repositories.UsuarioRepo import UsuarioRepo
from repositories.AnuncioRepo import AnuncioRepo

from util.imageUtil import transformar_em_quadrada
from util.security import validar_usuario_logado
from util.templateFilters import formatarData, formatarIdParaImagem
from util.validators import *

router = APIRouter(prefix="/vitrine")
templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData
    templates.env.filters["id_img"] = formatarIdParaImagem


@router.get("/listagem", response_class=HTMLResponse)
async def getListagem(
    request: Request,
    pa: int = 1,
    tp: int = 12,
    usuario: Usuario = Depends(validar_usuario_logado)
):    
    anuncios = AnuncioRepo.obterPagina(pa, tp)
    totalPaginas = AnuncioRepo.obterQtdePaginas(tp)
    return templates.TemplateResponse(
        "vitrine/vitrine.html",
        {
            "request": request,
            "usuario": usuario,
            "anuncios": anuncios,
            "totalPaginas": totalPaginas,
            "paginaAtual": pa,
            "tamanhoPagina": tp
        },
    )

        
@router.get("/novoanuncio", response_class=HTMLResponse)
async def getNovoAnuncio(
    request: Request, 
    usuario: Usuario = Depends(validar_usuario_logado),
    ):
    if usuario:
        musicas = MusicaRepo.obterTodos()
        return templates.TemplateResponse(
            "vitrine/novoanuncio.html", 
            {
              "request": request, 
              "usuario": usuario,
              "musicas": musicas
            },
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/novoanuncio")
async def postNovoAnuncio(
    request: Request,
    titulo: str = Form(""),
    descricao: str = Form(""),
    preco: float = Form(""),
    condicao: str = Form(""),
    idUsuario: int = Form(""),
    usuario: Usuario = Depends(validar_usuario_logado),
    fotoAnuncio: UploadFile = File(...)
):
    
    if usuario:
        
        # tratamento de erros
        erros = {}
        # validação do campo descricao
        is_not_empty(descricao, "descricao", erros)
        is_size_between(descricao, "descricao", 4, 512, erros)


        # Validação da imagem
        if fotoAnuncio.content_type not in ["image/jpeg", "image/png"]:
            add_error("fotoAnuncio", "Formato de imagem não suportado. Use JPEG ou PNG.", erros)

        conteudo_arquivo = await fotoAnuncio.read()

        try:
            imagem = Image.open(BytesIO(conteudo_arquivo))
        except:
            add_error("fotoAnuncio", "Não foi possível abrir a imagem.", erros)

        if not imagem:
            add_error("fotoAnuncio", "Nenhuma imagem foi enviada.", erros)

        # se tem erro, mostra o formulário novamente
        if len(erros) > 0:
            valores = {}
            valores["descricao"] = descricao
            return templates.TemplateResponse(
                "vitrine/novoanuncio.html",
                {
                    "request": request,
                    "usuario": usuario,
                    "erros": erros,
                    "valores": valores,
                },
            )

        # grava os dados no banco e redireciona para a listagem
        
        novo_anuncio = AnuncioRepo.inserir(
            Anuncio(
                id=0,
                titulo=titulo,
                descricao=descricao,
                preco=preco,
                condicao=condicao,
                idAnunciante=idUsuario,
            )
        )
        
        if novo_anuncio:
            imagem_quadrada = transformar_em_quadrada(imagem)
            imagem_quadrada.save(f'static/img/Anuncios/{novo_anuncio.id:04d}.jpg')

        return RedirectResponse("listagem", status_code=status.HTTP_303_SEE_OTHER)
        
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/excluiranuncio/{id:int}", response_class=HTMLResponse)
async def getExcluirAnuncio(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    id: int = Path(),
):
    if usuario:
        if usuario.admin:
            anuncio = AnuncioRepo.obterPorId(id)
            return templates.TemplateResponse(
                "anuncio/excluiranuncio.html",
                {
                  "request": request, 
                  "usuario": usuario, 
                  "anuncio": anuncio},
            )
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/excluiranuncio", response_class=HTMLResponse)
async def postExcluirAnuncio(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    id: int = Form(0),
):
    if usuario:
        if usuario.admin:
            if AnuncioRepo.excluir(id):
                return RedirectResponse("/vitrine/listagem", status_code=status.HTTP_303_SEE_OTHER)
            else:
                raise Exception("Não foi possível excluir o anúncio.")
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)