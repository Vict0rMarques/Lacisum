from fastapi import APIRouter, Depends, Form, HTTPException, Path, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.Anuncio import Anuncio
from models.Usuario import Usuario
from repositories.AnuncioRepo import AnuncioRepo
from util.security import validar_usuario_logado
from util.templateFilters import formatarData
from util.validators import *


router = APIRouter(prefix="/vitrine")
templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData


@router.get("/listagem", response_class=HTMLResponse)
async def getListagem(
    request: Request,
    pa: int = 1,
    tp: int = 8,
    usuario: Usuario = Depends(validar_usuario_logado),
):    
    anuncios = AnuncioRepo.obterPagina(pa, tp)
    print(anuncios)  # Adicione esta linha para verificar os anúncios
    totalPaginas = AnuncioRepo.obterQtdePaginas(tp)
    return templates.TemplateResponse(
        "vitrine/vitrine.html",
        {
            "request": request,
            "anuncios": anuncios,
            "totalPaginas": totalPaginas,
            "paginaAtual": pa,
            "tamanhoPagina": tp,
            "usuario": usuario,
        },
    )

        
@router.get("/novoanuncio", response_class=HTMLResponse)
async def getNovo(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        if usuario.admin:
            return templates.TemplateResponse(
                "vitrine/novoanuncio.html", {"request": request, "usuario": usuario}
            )
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/novoanuncio")
async def postNovo(
    request: Request,
    titulo: str = Form(""),
    descricao: str = Form(""),
    preco: float = Form(""),
    condicao: str = Form(""),
    usuario: Usuario = Depends(validar_usuario_logado),
):
    if usuario:
        if usuario.admin:

            # tratamento de erros
            erros = {}
            # validação do campo descricao
            is_not_empty(descricao, "descricao", erros)
            is_size_between(descricao, "descricao", 4, 512, erros)

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
            AnuncioRepo.inserir(Anuncio(0, titulo, descricao, preco, condicao))
            return RedirectResponse(
                "/vitrine/listagem", status_code=status.HTTP_303_SEE_OTHER
            )
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/excluir/{id:int}", response_class=HTMLResponse)
async def getExcluir(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    id: int = Path(),
):
    if usuario:
        if usuario.admin:
            anuncio = AnuncioRepo.obterPorId(id)
            return templates.TemplateResponse(
                "anuncio/excluir.html",
                {"request": request, "usuario": usuario, "anuncio": anuncio},
            )
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/excluir", response_class=HTMLResponse)
async def postExcluir(
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