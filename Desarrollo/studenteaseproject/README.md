# Cómo usar StudentEase

## 📥 Clonar el repositorio usando Git

Asegúrate de tener **Git** instalado antes de realizar este paso.

Abre la consola y escribe el siguiente comando:

```
git clone https://github.com/Manco312/SpyMonks-OmegaLab-2025.git
```


## 🐍 Instalar Python y pip

Antes de continuar, asegúrate de tener instalados **Python** y **pip** en tu equipo.

## 📚 Instalar las librerías necesarias

Abre la carpeta donde se encuentra el proyecto utilizando el comando `cd` después de clonar. Luego, instala las dependencias ejecutando:

```
pip install -r requirements.txt
```


## 🔑 Crear un archivo `.env` para la clave API de OpenAI

Crea un archivo llamado `openAI.env` en la carpeta principal del proyecto (`studenteaseproject`). Luego, agrega la siguiente línea, reemplazando las `X` por tu clave válida de OpenAI:


```
openAI_api_key = XXXXXXXXXX
```


## 🚀 Ejecutar el servidor local

Después de instalar las librerías, abre la consola en la carpeta del proyecto y ejecuta uno de los siguientes comandos:

```
py manage.py runserver
```

ó

```
python manage.py runserver
```


## 🌐 Usar StudentEase

Una vez que el servidor esté corriendo, accede a la siguiente dirección para usar StudentEase:

[http://localhost:8000](http://localhost:8000)
