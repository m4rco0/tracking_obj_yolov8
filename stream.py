import cv2 as cv
from ultralytics import YOLO
import os
from datetime import datetime
""" Classe da camera, que possui o yolov8n
    - streaming -> camera utilizada para o tracking. 
    - modelo -> Modelo do yolo .
    - captura -> numeração da Camera.
    - camRunning -> Se a camera está ligada ou não .
    - frame -> frames de camera .
    - isRecording -> Se a estiver gravando ou não.
    - videoWriter -> usado para gravar o video em um arquivo.
"""
class Camera:

    """
    Inicializando a camera e o modelo yolo
    """
    def __init__(self, capture_cam="/dev/video0") -> None:
        self.captura = capture_cam
        self.camRunning = False  # Inicia como False
        self.streaming = cv.VideoCapture(self.captura)
        if not self.streaming.isOpened():
            print(f"Erro: Não foi possível abrir a câmera {self.captura}")
            return
            
        self.camRunning = True
        self.modelo = YOLO('yolov8n.pt')
        self.frame = None
        self.isRecording = False 
        self.videoWriter = None

    """
    Metodo record_frame tem a função de testar se a camera ja está ativa ou gravando,
    criar o diretorio de Uploads e salvar o video no formato .avi. Retornando true se conseguiu gravar e false caso contrario.

    entradas:
    - save_dir -> nome do diretorio no formato de string
    """
    def record_frame(self, save_dir="uploads"):
        if not self.camRunning:
            print("Erro: Câmera não está aberta")
            return False
        
        if self.isRecording:
            print("Aviso: Já está gravando")
            return False

        # Garante que o diretório existe
        os.makedirs(save_dir, exist_ok=True)

        # Tenta diferentes codecs
        codecs = ['mp4v', 'XVID', 'MJPG', 'DIVX']
        timestamp = datetime.now().strftime("%d_%m_%Y_%H%M%S")
        filename = os.path.join(save_dir, f"video_{timestamp}.avi")  # .avi tem melhor compatibilidade

        frame_width = int(self.streaming.get(cv.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.streaming.get(cv.CAP_PROP_FRAME_HEIGHT))
        fps = 20.0

        # Tenta cada codec até encontrar um que funcione
        for codec in codecs:
            fourcc = cv.VideoWriter_fourcc(*codec)
            self.videoWriter = cv.VideoWriter(filename, fourcc, fps, (frame_width, frame_height))
            
            if self.videoWriter.isOpened():
                print(f"Codec {codec} funcionando. Gravando em: {os.path.abspath(filename)}")
                self.isRecording = True
                return filename
            else:
                print(f"Codec {codec} falhou, tentando próximo...")
                continue

        print("Erro: Nenhum codec funcionou")
        return False

    """
    Metódo da Camera para parar a gravação caso não esteja gravando, não fará nada.
    """
    def parar_gravacao(self):
        if not self.isRecording:
            print("Aviso: Não está gravando")
            return False
            
        if self.videoWriter:
            self.videoWriter.release()
            self.videoWriter = None
            
        self.isRecording = False
        print("Gravação finalizada com sucesso")
        return True

    """
    Metódo capture_frame utilizado pela Camera para tirar print da camera, se não tiver o arquivo uploads irá criar e salvar as images 
    no formato capture_day/mounth/year_H:M:S.jpg
    
    retorna true se conseguir, e false caso contrario
    """
    def capture_frame(self, save_dir="uploads"):
        if self.frame is None:
            print("Erro: Nenhum frame disponível")
            return None
        
        try:
            os.makedirs(save_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%d_%m_%Y_%H%M%S")
            filename = os.path.join(save_dir, f"capture_{timestamp}.jpg")
            
            if cv.imwrite(filename, self.frame):
                print(f"Foto salva em: {os.path.abspath(filename)}")
                return filename
            else:
                print("Erro: Falha ao salvar foto")
                return None
        except Exception as e:
            print(f"Erro ao capturar frame: {str(e)}")
            return None

    """
    O Metódo generate_frame vai começar mandar o stream da camera para que o nosso front-end consiga pegar, por meio de um buffer de imagem
    """
    def generate_frame(self):
        if not self.camRunning:
            print("Erro: Câmera não inicializada")
            return

        while self.camRunning:
            success, frame = self.streaming.read()
            if not success:
                print("Erro: Falha ao capturar frame")
                self.camRunning = False
                break

            try:
                resultados = self.modelo.track(frame, persist=True)
                frame_tracking = resultados[0].plot()
                self.frame = frame_tracking

                if self.isRecording and self.videoWriter:
                    self.videoWriter.write(frame_tracking)

                ret, buffer = cv.imencode('.jpg', frame_tracking)
                if ret:
                    yield (b'--frame\r\n'
                          b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
                else:
                    print("Aviso: Falha ao codificar frame")
            except Exception as e:
                print(f"Erro no processamento: {str(e)}")
                continue

    """
    Metódo stop, finaliza todas as operações da camera
    """
    def stop(self):
        if self.isRecording:
            self.parar_gravacao()
            
        if self.streaming and self.streaming.isOpened():
            self.streaming.release()
            
        self.camRunning = False
        cv.destroyAllWindows()
        print("Câmera liberada com sucesso")
