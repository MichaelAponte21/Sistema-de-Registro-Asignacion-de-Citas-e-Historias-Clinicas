# Usamos la imagen base de Python
FROM python:3.14-slim

# Establecemos el directorio de trabajo en el contenedor
WORKDIR /app

# Copiamos el archivo de dependencias al contenedor
COPY requirements.txt .

# Instalamos las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de los archivos del proyecto
COPY . .

# Exponemos el puerto en el que corre la aplicación (8000 por defecto)
EXPOSE 8000

# Definimos el comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
