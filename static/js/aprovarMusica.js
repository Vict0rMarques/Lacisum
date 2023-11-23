// Função para fazer a chamada da API
async function aprovarMusica(id) {
    try {
        const url = `/playlist/aprovarmusica/${id}`;        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });        
        const data = await response.json();
        if (data.ok) {
            ocultarTooltipErro(id);
            removerLinhaComAnimacao(id);            
        } else {
            mostrarTooltipErro(id);
        }
    } catch (error) {
        console.error('Erro ao chamar a API:', error);        
    }
}

function removerLinhaComAnimacao(id) {
    const linha = document.querySelector(`tr[data-id="${id}"]`);
    if (linha) {
        linha.remove();
        recarregarPagina();        
    }
}

function ocultarTooltipErro(id) {
    const botao = document.querySelector(`button.btn-success[data-id="${id}"]`);
    if (botao) {
        var tooltip = bootstrap.Tooltip.getInstance(botao);
        tooltip.hide();
    }
}

function mostrarTooltipErro(id) {
    const botao = document.querySelector(`button.btn-success[data-id="${id}"]`);
    if (botao) {
        var tooltip = bootstrap.Tooltip.getInstance(botao);
        tooltip._config.title = "Ocorreu um problema ao tentar aprovar a música.";
        tooltip.update();
        tooltip.show();
        setTimeout(() => {
            tooltip.hide();
        }, 3000);
    }
}

function recarregarPagina() {
    //const trs = document.querySelectorAll('tbody>tr');        
    //if (trs.length === 0) {
    window.location.href = '/playlist/aprovarmusica';
    //}
}

// Adicionar um evento de clique a todos os elementos <a> com classe "btn-success"
document.addEventListener('DOMContentLoaded', (event) => {    
    const botoes = document.querySelectorAll('.btn-aprovar');
    botoes.forEach((botao) => {
        botao.addEventListener('click', (event) => {
            event.preventDefault();
            const id = botao.getAttribute('data-id');           
            aprovarMusica(id);
        });
    });
});