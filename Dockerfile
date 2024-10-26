# Usa una imagen base de Python 3.9
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios
COPY requirements.txt .

# Instala las dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto del código fuente
COPY . .

# Define el comando para ejecutar la aplicación con uvicorn
CMD ["uvicorn", "docs.main:app", "--host", "0.0.0.0", "--port", "8000"]
