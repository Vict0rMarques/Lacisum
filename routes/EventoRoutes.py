from fastapi import APIRouter, Depends, Form, HTTPException, Path, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.Evento import Evento
from models.Usuario import Usuario
from repositories.EventoRepo import EventoRepo
from util.security import validar_usuario_logado
from util.templateFilters import formatarData
from util.validators import *


router = APIRouter(prefix="/evento")
templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData


@router.get("/listagem", response_class=HTMLResponse)
async def getListagem(
    request: Request,
    pa: int = 1,
    tp: int = 10,
    usuario: Usuario = Depends(validar_usuario_logado),
):
    eventos = EventoRepo.obterPagina(pa, tp)
    totalPaginas = EventoRepo.obterQtdePaginas(tp)
    return templates.TemplateResponse(
        "evento/evento.html",
        {
            "request": request,
            "eventos": eventos,
            "totalPaginas": totalPaginas,
            "paginaAtual": pa,
            "tamanhoPagina": tp,
            "usuario": usuario,
        },
    )
    


@router.get("/novoevento", response_class=HTMLResponse)
async def getNovo(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        if usuario.admin:
            return templates.TemplateResponse(
                "evento/novoevento.html", {"request": request, "usuario": usuario}
            )
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/novoevento")
async def postNovo(
    request: Request,
    nome: str = Form(""),
    descricao: str = Form(""),
    cidade: str = Form(""),
    presencial: str = Form(""),
    uf: str = Form(""),
    url: str = Form(""),
    idadeMinima: int = Form(""),
    gratuito: str = Form(""),
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
                    "evento/novoevento.html",
                    {
                        "request": request,
                        "usuario": usuario,
                        "erros": erros,
                        "valores": valores,
                    },
                )

            # grava os dados no banco e redireciona para a listagem
            EventoRepo.inserir(Evento(0, nome, descricao, cidade, presencial, uf, url, idadeMinima, gratuito))
            return RedirectResponse(
                "/evento/listagem", status_code=status.HTTP_303_SEE_OTHER
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
            evento = EventoRepo.obterPorId(id)
            return templates.TemplateResponse(
                "evento/excluir.html",
                {"request": request, "usuario": usuario, "evento": evento},
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
            if EventoRepo.excluir(id):
                return RedirectResponse("/evento/listagem", status_code=status.HTTP_303_SEE_OTHER)
            else:
                raise Exception("Não foi possível excluir o evento.")
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)