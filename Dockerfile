# Usar la imagen base de Python ligera
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . /app

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando predeterminado al ejecutar el contenedor
CMD ["python", "bot.py"]