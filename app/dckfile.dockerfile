# Usa una imagen de Python
FROM python:3.7-slim

# Copia los archivos de tu aplicación al contenedor
COPY . /app

# Cambia al directorio de la aplicación
WORKDIR /app

# Instala las dependencias de tu aplicación
RUN pip install -r requirements.txt

# Ejecuta tu aplicación
CMD ["python", "dados_app.py"]