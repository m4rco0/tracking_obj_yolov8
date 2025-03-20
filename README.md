# Instalação

Crie o seu ambiente virtual primeiro.
```bash
python3 -m env env
source venv/bin/activate
```
Logo após baixe as dependências para rodar o detector de objetos YOLOv8 e o opencv, para mostrar a imagem em tempo real.
```bash
pip install -r requirements.txt
```

Agora você pode executar o codigo, se quiser utilizar a camera modifique essa parte do codigo:

```python3
stream_cam = 0
```

e para utilizar camera no site, tipo o stream do ESP32:

```python3
stream_cam="[IP]:[porta]/steam"
```


