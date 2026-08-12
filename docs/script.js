const botao = document.getElementById("enviar");
const mensagem = document.getElementById("mensagem");


// =========================
// VERIFICAR SE JÁ ENVIOU
// =========================

const formularioJaEnviado = localStorage.getItem("formularioFAB");

if (formularioJaEnviado === "true") {

    mensagem.innerHTML = "✓ Você já preencheu o formulário.";
    mensagem.className = "mensagem-ja-enviado";

    botao.disabled = true;
    botao.innerHTML = "Formulário já preenchido";

    const campos = document.querySelectorAll(".campo input");

    campos.forEach(function(campo) {
        campo.disabled = true;
    });
}


// =========================
// ENVIAR FORMULÁRIO
// =========================

botao.addEventListener("click", async function() {

    // Impede novo envio
    if (localStorage.getItem("formularioFAB") === "true") {
        return;
    }


    // =========================
    // PEGAR CAMPOS
    // =========================

    const nome = document.getElementById("nome");
    const discord = document.getElementById("dc");
    const idade = document.getElementById("idade");
    const local = document.getElementById("place");
    const simulador = document.getElementById("sim");
    const servidor = document.getElementById("server");


    const campos = [
        nome,
        discord,
        idade,
        local,
        simulador,
        servidor
    ];


    let formularioValido = true;


    // Limpar erros

    campos.forEach(function(campo) {

        campo.style.borderColor = "";
        campo.style.boxShadow = "";

    });


    mensagem.innerHTML = "";
    mensagem.className = "";


    // =========================
    // VERIFICAR CAMPOS
    // =========================

    campos.forEach(function(campo) {

        if (campo.value.trim() === "") {

            campo.style.borderColor = "#c95c5c";

            campo.style.boxShadow =
                "0 0 10px rgba(201, 92, 92, 0.25)";

            formularioValido = false;
        }

    });


    // =========================
    // VERIFICAR IDADE
    // =========================

    if (idade.value !== "") {

        const idadeNumero = Number(idade.value);

        if (idadeNumero < 10 || idadeNumero > 100) {

            idade.style.borderColor = "#c95c5c";

            idade.style.boxShadow =
                "0 0 10px rgba(201, 92, 92, 0.25)";

            formularioValido = false;
        }
    }


    // =========================
    // SE HOUVER ERRO
    // =========================

    if (!formularioValido) {

        mensagem.innerHTML =
            "⚠️ Preencha corretamente todos os campos.";

        mensagem.className = "mensagem-erro";

        return;
    }


    // =========================
    // DESABILITAR BOTÃO
    // =========================

    botao.disabled = true;
    botao.innerHTML = "Enviando...";


    // =========================
    // ENVIAR PARA PYTHON
    // =========================

    try {

        const resposta = await fetch(
            "https://fab-virtual-server.onrender.com/enviar",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    nome: nome.value,
                    discord: discord.value,
                    idade: idade.value,
                    local: local.value,
                    simulador: simulador.value,
                    servidor: servidor.value

                })
            }
        );


        const resultado = await resposta.json();


        // =========================
        // SE DEU CERTO
        // =========================

        if (resultado.sucesso) {

            localStorage.setItem(
                "formularioFAB",
                "true"
            );


            campos.forEach(function(campo) {
                campo.disabled = true;
            });


            botao.innerHTML =
                "Formulário enviado";


            mensagem.innerHTML =
                "✓ Formulário preenchido com sucesso!";


            mensagem.className =
                "mensagem-sucesso";


            // Ir para saiba mais

            setTimeout(function() {

                window.location.href =
                    "saibamais.html";

            }, 2500);

        }

    }

    catch (erro) {

        console.error(erro);

        botao.disabled = false;

        botao.innerHTML =
            "Enviar Formulário";


        mensagem.innerHTML =
            "❌ Não foi possível enviar o formulário. Verifique se o servidor está funcionando.";

        mensagem.className =
            "mensagem-erro";

    }

});