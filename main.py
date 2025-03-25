from flask import Flask, Response, render_template, jsonify
from stream import Camera
import os

numero_da_camera = 0
app = Flask(__name__)
cam = None 

@app.route('/')
def index():
  print(f"Diretório atual: {os.getcwd()}")
  print(f"Caminho uploads: {os.path.abspath('uploads')}")
  return render_template('index.html')

@app.route('/iniciar_tracking')
def iniciar_tracking():
  global cam
  if cam is None: 
    cam = Camera(numero_da_camera)
  return Response(cam.generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/parar_tracking')
def parar_tracking():
  global cam
  if cam is not None:
    cam.stop()
    cam = None
  return render_template('index.html') 

@app.route('/capturar_foto')
def capturar_foto():
  global cam
  if cam is None:
    return jsonify({"status": "error", "message":"Camera não esta ligada"}), 400
  
  try:
    filename = cam.capture_frame()
    if filename:
      return jsonify({
        "status": "success", 
        "filename": filename,
        "url": f"/{filename}"  
      })
    else:
      return jsonify({"status": "error", "message": "Falha ao capturar foto"}), 500
  except Exception as e:
    return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/iniciar_gravacao')
def iniciar_gravacao():
  global cam
  if cam is None:
    cam = Camera(numero_da_camera)
  

  filename = cam.record_frame()
  if filename:
    return jsonify({
      "status": "sucess",
      "filename": filename,
      "message": "Gravação iniciada"
    })
  else:
    return jsonify({"status": "error", "message": "Falha ao iniciar gravação"}), 500

@app.route('/parar_gravacao')
def parar_gravacao():
  global cam
  if cam is None:
    return jsonify({"status": "error", "message":"Camera não ligada"}), 400
  
  if cam.parar_gravacao():
    return jsonify({
      "status": "sucess",
      "message": "gravação acabou"
    })
  else:
    return jsonify({
      "status": "error",
      "message": "Nenhuma gravação rodando"
    }), 400
  


if __name__ == "__main__":
  os.makedirs('uploads', exist_ok=True)
  app.run( host="0.0.0.0",port=5000)