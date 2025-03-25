//lugar da camera
const videoCam = document.getElementById("video-stream");
// buttons
const startCam = document.getElementById("ligar-cam");
const stopCam = document.getElementById("desligar-cam");
const capturarFrames = document.getElementById("capturar-frame");
const iniciarGravacao = document.getElementById("iniciar-gravacao");
const pararGravacao = document.getElementById("desligar-gravacao");
const labelCam = document.getElementById("Infos-cam");

// colocar o src da camera
function startTracking() {
    fetch('/iniciar_tracking')
    .then(() => {
        // deixa apenas o botão de ligar camera desligado
        videoCam.src = "/iniciar_tracking";
        startCam.disabled = true;       
        stopCam.disabled = false;
        capturarFrames.disabled = false;
        iniciarGravacao.disabled = false;
        pararGravacao.disabled = false;
        labelCam.textContent = "Camera iniciada"
    })
    .catch(err => console.error("Error para iniciar a camera: ", err))
}

// função para parar a camera
function stopTracking() {
    //quando a rota fora acessada
    fetch ('/parar_tracking')
        .then(() => {
            // tirar o src da camera
            videoCam.src = "";
            startCam.disabled = false;
            stopCam.disabled = true;
            capturarFrames.disabled = true;
            iniciarGravacao.disabled = true;
            pararGravacao.disabled = true;
            labelCam.textContent = "Camera pausada"
            
        })
        .catch(err => console.error("Erro ao parar tracking:", err));
}

// função que muda label do print da camera
function capturePhoto() {
    labelCam.textContent = "Capturando foto...";
    // acessa a rota que tira a foto
    fetch('/capturar_foto')
        // recebe um json de response
        .then(response => response.json())
        .then(data => {
            if(data.status === "success") {
                labelCam.textContent = `Foto salva: ${data.filename}`;
            } else {
                labelCam.textContent = `Erro: ${data.message}`;
            }
        })
        .catch(error => {
            labelCam.textContent = "Erro ao capturar foto";
            console.error('Error:', error);
        });
}

// função para iniciar a gravação 
function startRecording() {
    labelCam.textContent = "Inicio da gravação";

    fetch('/iniciar_gravacao')
        .then(response => response.json())
        .then(data => {
            if(data.status === "sucess") {
                labelCam.textContent = `Gravação iniciada: ${data.filename}`;
                pararGravacao.disabled = false;
            } else {
                labelCam.textContent = `Error: ${data.message}`;
            }
        })
        .catch(error => {
            labelCam.textContent =  "Error de iniciar gravação";
            console.log('Error:', error);
        });
}


function stopRecording() {
    labelCam.textContent = "Parando gravação...";
    
    fetch('/parar_gravacao')
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                labelCam.textContent = "Gravação finalizada";
                pararGravacao.disabled = true; // Desabilita o botão de parar gravação
            } else {
                labelCam.textContent = `Erro: ${data.message}`;
            }
        })
        .catch(error => {
            labelCam.textContent = "Erro ao parar gravação";
            console.error('Error:', error);
        });
}


stopCam.disabled = true;
capturarFrames.disabled = true;
iniciarGravacao.disabled = true;
pararGravacao.disabled = true;