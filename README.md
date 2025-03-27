# Yolo tracking with site for ESP32
## TODO
- [x] Acessar camera
- [x] Utilizar o modelo yolo8vn.pt para detectar objetos
- [x] Front-end do site da camera
- [x] Flask para configurar as rotas e mostrar a camera no site

## Install

1. create virtual envrionments for project
```bash
python -m venv .env
```
2. acess venv 

```bash
source ./.env/bin/activate  #linux
env\Scripts\activate         #windows
```

3. execute main code

```bash
python main.py
```

Opcional: configure a variavel de camera para a camera que vc quer pegar, no arquivo main.py.

```python3
numero_da_camera = 0  # 0 é a camera padrão do computador,
                      # pode colocar o link de stream do esp32-cam. ou outra camera
```
foto do programa rodando:
![Image](https://github.com/user-attachments/assets/0016d2ba-458f-4abe-842d-d2a998087b54)
