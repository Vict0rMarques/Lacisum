from fastapi import APIRouter, Depends, Form, HTTPException, Path, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.Clube import Clube
from models.Usuario import Usuario
from repositories.ClubeRepo import ClubeRepo
from util.security import validar_usuario_logado
from util.templateFilters import formatarData
from util.validators import *


router = APIRouter(prefix="/clube")
templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData


@router.get("/clube", response_class=HTMLResponse)
async def getListagem(
    request: Request,
    pa: int = 1,
    tp: int = 5,
    usuario: Usuario = Depends(validar_usuario_logado),
):
    if usuario:
        if usuario.admin:
            clubes = ClubeRepo.obterPagina(pa, tp)
            totalPaginas = ClubeRepo.obterQtdePaginas(tp)
            return templates.TemplateResponse(
                "clube/clube.html",
                {
                    "request": request,
                    "clubes": clubes,
                    "totalPaginas": totalPaginas,
                    "paginaAtual": pa,
                    "tamanhoPagina": tp,
                    "usuario": usuario,
                },
            )
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/novoclube", response_class=HTMLResponse)
async def getNovo(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        if usuario.admin:
            return templates.TemplateResponse(
                "clube/novoclube.html", {"request": request, "usuario": usuario}
            )
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/novoclube")
async def postNovo(
    request: Request,
    nome: str = Form(""),
    descricao: str = Form(""),
    tipo: str = Form(""),
    condicao: str = Form(""),
    privacidade: str = Form(""),
    idadeMinima: int = Form(""),
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
                    "clube/novoclube.html",
                    {
                        "request": request,
                        "usuario": usuario,
                        "erros": erros,
                        "valores": valores,
                    },
                )

            # grava os dados no banco e redireciona para a listagem
            ClubeRepo.inserir(Clube(0, nome, descricao, tipo, condicao, privacidade, idadeMinima))
            return RedirectResponse(
                "/clube/listagem", status_code=status.HTTP_303_SEE_OTHER
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
            clube = ClubeRepo.obterPorId(id)
            return templates.TemplateResponse(
                "clube/excluir.html",
                {"request": request, "usuario": usuario, "clube": clube},
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
            if ClubeRepo.excluir(id):
                return RedirectResponse("/clube/listagem", status_code=status.HTTP_303_SEE_OTHER)
            else:
                raise Exception("Não foi possível excluir o clube.")
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)