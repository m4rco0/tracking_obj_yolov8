import cv2 as cv
from ultralytics import YOLO
import os
from datetime import datetime

class Camera:
    def __init__(self, capture_cam="/dev/video0") -> None:
        self.captura = capture_cam
        self.camRunning = True
        self.streaming = None
        self.modelo = YOLO('yolov8n.pt')
        self.frame = None
        self.isRecording = False 
        self.videoWriter = None

    def record_frame(self, save_dir="uploads"):
        if not self.camRunning:
            print("Abra a camera")
            return False
        
        if self.isRecording:
            print("Ja esta gravando")
            return False
        

        
        

        # definir codex de AVI
        fourcc =cv.VideoWriter_fourcc(*'XVID')
        timestamp = datetime.now().strftime("%d_%m_%Y_%H%M%S")
        filename = os.path.join(save_dir, f"video_{timestamp}.mp4")


        os.makedirs(save_dir, exist_ok=True)

        frame_width = int(self.streaming.get(cv.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.streaming.get(cv.CAP_PROP_FRAME_HEIGHT))
        fps = 20.0

        self.videoWriter = cv.VideoWriter(filename, fourcc, fps, (frame_width, frame_height))

        if not self.videoWriter.isOpened():
            print(f"ERRO: Não foi possível abrir o VideoWriter para {filename}")
            print(f"Verifique codec, resolução ou permissões")
            return False
        
        self.isRecording = True

        print(f"Tentando salvar em: {os.path.abspath(filename)}")
        return filename

    def parar_gravacao(self):
        if not self.isRecording:
            print("Não está gravando")
            return False
        if self.videoWriter is None:
            print("Não tem o video Writer")
            return False
        
        self.videoWriter.release()
        self.isRecording = False
        self.videoWriter = None
        return True
        

    def capture_frame(self, save_dir="uploads"):
        if self.frame is None:
            return
        
        try:
            # Cria o diretório se não existir
            os.makedirs(save_dir, exist_ok=True)
                
            # Gera um nome de arquivo com timestamp
            timestamp = datetime.now().strftime("%d_%m_%Y_%H%M%S")
            filename = os.path.join(save_dir, f"capture_{timestamp}.jpg")
            
            abs_path = os.path.abspath(filename)
            print(f"Tentando salvar em {abs_path}")
            # Salva a imagem
            cv.imwrite(abs_path, self.frame)
            
            return filename
        except Exception as e:
            print(f"Erro ao captirar o frame: {e}")
            return None


    def generate_frame(self):
        self.streaming = cv.VideoCapture(self.captura)
        while self.camRunning:
            sucess, frame = self.streaming.read()
            if not sucess:
                print("Error em carregar o frame")
                break

            # tracking do YOLO
            resultados = self.modelo.track(frame, persist=True)
            frame_tracking = resultados[0].plot()
            self.frame = frame_tracking

            # se estiver gravando, salva os frames no videoWriter
            if self.isRecording and self.videoWriter is not None:
                self.videoWriter.write(frame_tracking)
                

            ret, buffer = cv.imencode('.jpg', frame_tracking)
            if not ret:
                print("Erro no buffer")
                continue

            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n') 

        self.streaming.release()
        cv.destroyAllWindows()
    
    def stop(self):
        self.camRunning = False
        self.streaming.release()
        if self.streaming is not None:
            self.streaming.release()
        cv.destroyAllWindows()