from fastapi import APIRouter, Depends, Form, Path, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from models.Usuario import Usuario
from repositories.UsuarioRepo import UsuarioRepo

from util.security import obter_hash_senha, validar_usuario_logado, verificar_senha
from util.templateFilters import formatarData
from util.validators import *


router = APIRouter(prefix="/usuario")
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
    if usuario:
        if usuario.admin:
            usuario = UsuarioRepo.obterPagina(pa, tp)
            totalPaginas = UsuarioRepo.obterQtdePaginas(tp)
            return templates.TemplateResponse(
                "usuario/listagem.html",
                {
                    "request": request,
                    "totalPaginas": totalPaginas,
                    "usuario": usuario,
                    "paginaAtual": pa,
                    "tamanhoPagina": tp
                },
            )
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@router.get("/cadastro", response_class=HTMLResponse)
async def getCadastro(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
): 
    return templates.TemplateResponse(
        "usuario/cadastro.html", {"request": request, "usuario": usuario},
    )

@router.post("/cadastro")
async def postCadastro(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    nome: str = Form(""),
    email: str = Form(""),
    dataNascimento: str = Form(""),
    senha: str = Form(""),
):
    # normalização dos dados
    nome = nome.strip()
    email = email.lower().strip()
    senha = senha.strip()

    # verificação de erros
    erros = {}
    # validação do campo nome
    is_not_empty(nome, "nome", erros)
    is_person_fullname(nome, "nome", erros)
    # validação do campo email
    is_not_empty(email, "email", erros)
    if is_email(email, "email", erros):
        if UsuarioRepo.emailExiste(email):
            add_error("email", "Já existe um usuário cadastrado com este e-mail.", erros)
    # validação do campo senha
    is_not_empty(senha, "senha", erros)
    is_password(senha, "senha", erros)
    

    # se tem erro, mostra o formulário novamente
    if len(erros) > 0:
        valores = {}
        valores["nome"] = nome
        valores["email"] = email.lower()
        return templates.TemplateResponse(
            "usuario/cadastro.html",
            {
                "request": request,
                "usuario": usuario,
                "erros": erros,
                "valores": valores,
            },
        )

    # inserção no banco de dados
    UsuarioRepo.inserir(
        Usuario(
            id=0,
            nome=nome,
            email=email,
            dataNascimento=dataNascimento,
            senha=obter_hash_senha(senha)
        )
    )

    # mostra página de sucesso
    return templates.TemplateResponse(
        "/main/index.html",
        {"request": request, "usuario": usuario},
    )


@router.get("/excluir/{id:int}", response_class=HTMLResponse)
async def getExcluir(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    id: int = Path(),
):
    if usuario:
        if usuario.admin:
            usuario = UsuarioRepo.obterPorId(id)
            return templates.TemplateResponse(
                "usuario/excluir.html",
                {"request": request, "usuario": usuario},
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
            if UsuarioRepo.excluir(id):
                return RedirectResponse(
                    "/usuario/listagem", status_code=status.HTTP_303_SEE_OTHER
                )
            else:
                raise Exception("Não foi possível excluir o usuário.")
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/dashboard", response_class=HTMLResponse)
async def getDashboard(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
    if usuario:
        usuario = UsuarioRepo.obterPorId(usuario.id)
        if usuario:
            return templates.TemplateResponse(
                "usuario/dashboard.html",
                {"request": request, "usuario": usuario},
            )
        else:
            return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/alterarsenha", response_class=HTMLResponse)
async def getAlterarSenha(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
    if usuario:
        return templates.TemplateResponse(
            "usuario/alterarsenha.html", {"request": request, "usuario": usuario}
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/alterarsenha", response_class=HTMLResponse)
async def postAlterarSenha(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    senhaAtual: str = Form(""),
    novaSenha: str = Form(""),
    confNovaSenha: str = Form(""),    
):
    # normalização dos dados
    senhaAtual = senhaAtual.strip()
    novaSenha = novaSenha.strip()
    confNovaSenha = confNovaSenha.strip()    

    # verificação de erros
    erros = {}
    # validação do campo senhaAtual
    is_not_empty(senhaAtual, "senhaAtual", erros)
    is_password(senhaAtual, "senhaAtual", erros)    
    # validação do campo novaSenha
    is_not_empty(novaSenha, "novaSenha", erros)
    is_password(novaSenha, "novaSenha", erros)
    # validação do campo confNovaSenha
    is_not_empty(confNovaSenha, "confNovaSenha", erros)
    is_matching_fields(confNovaSenha, "confNovaSenha", novaSenha, "Nova Senha", erros)
    
    # só verifica a senha no banco de dados se não houverem erros de validação
    if len(erros) == 0:    
        hash_senha_bd = UsuarioRepo.obterSenhaDeEmail(usuario.email)
        if hash_senha_bd:
            if not verificar_senha(senhaAtual, hash_senha_bd):            
                add_error("senhaAtual", "Senha atual está incorreta.", erros)
    
    # se tem erro, mostra o formulário novamente
    if len(erros) > 0:
        valores = {}        
        return templates.TemplateResponse(
            "usuario/alterarsenha.html",
            {
                "request": request,
                "usuario": usuario,                
                "erros": erros,
                "valores": valores,
            },
        )

    # se passou pelas validações, altera a senha no banco de dados
    hash_nova_senha = obter_hash_senha(novaSenha)
    UsuarioRepo.alterarSenha(usuario.id, hash_nova_senha)
    
    # mostra página de sucesso
    return templates.TemplateResponse(
        "usuario/alterousenha.html",
        {"request": request, "usuario": usuario},
    )
    
    # TODO: Não está mostrando mensagens de erros nos campos do formulário

@router.get("/configuracoes", response_class=HTMLResponse)
async def getConfiguracoes(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
    if usuario:
        return templates.TemplateResponse(
            "usuario/configuracoes.html", {"request": request, "usuario": usuario}
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)