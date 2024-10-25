# CI/CD Práctica con CircleCI, Docker, SonarCloud y Kubernetes

Este repositorio contiene una aplicación de ejemplo que sigue un flujo de CI/CD implementado utilizando CircleCI para las pruebas, análisis de código estático, generación de artefactos, y publicación de imágenes Docker. Además, está configurada para desplegarse en Kubernetes usando ArgoCD.

## Requisitos previos

1. **Cuenta en Docker Hub** (para subir imágenes de Docker).
2. **Cuenta en SonarCloud** (para análisis de código estático).
3. **Cuenta en CircleCI** (para gestionar el CI/CD).
4. **Acceso a un cluster de Kubernetes** (para realizar despliegues).
5. **Instalación de herramientas locales**:
   - [Docker](https://www.docker.com/products/docker-desktop)
   - [Kubectl](https://kubernetes.io/docs/tasks/tools/)
   - [Helm](https://helm.sh/docs/intro/install/)
   - [ArgoCD](https://argo-cd.readthedocs.io/en/stable/)

## Estructura del proyecto

```bash
.
├── .circleci
│   └── config.yml               # Configuración de CircleCI
├── Dockerfile                   # Definición del contenedor Docker
├── manifests                    # Manifestos de Kubernetes para despliegue
├── requirements.txt             # Dependencias de Python
├── sonar-project.properties      # Configuración de SonarCloud
├── tests
│   └── test_example.py          # Pruebas unitarias
├── .flake8                      # Configuración de Flake8
├── coverage/coverage.xml        # Reporte de cobertura de código
└── README.md                    # Este archivo

## Paso 1: Creación de tokens de acceso
1.1. Docker Hub Token
Ve a tu cuenta de Docker Hub y genera un Access Token.
Configura el token en CircleCI:
Crea dos variables de entorno en la configuración de tu proyecto de CircleCI:
DOCKER_USER: Tu nombre de usuario de Docker Hub.
DOCKER_PASS: El token generado.
1.2. SonarCloud Token
Accede a SonarCloud y genera un token en tu perfil.
Configura el token en CircleCI:
Crea las siguientes variables de entorno en CircleCI:
SONAR_TOKEN: El token generado.
SONAR_PROJECT_KEY: El identificador de tu proyecto en SonarCloud.
SONAR_ORG: La organización a la que pertenece el proyecto.

## Paso 2: Crear el archivo requirements.txt
Define las dependencias de tu proyecto en este archivo para gestionar el entorno de Python.
fastapi==0.78.0
pytest==6.2.4
pytest-cov==2.12.1
httpx==0.21.0
flake8==3.9.2


## Paso 3: Configuración de CircleCI
Dentro de la carpeta .circleci, crea el archivo config.yml que define los trabajos a ejecutar en el pipeline.
version: 2.1

orbs:
  sonarcloud: sonarsource/sonarcloud@2.0.0

jobs:
  test:
    docker:
      - image: cimg/python:3.9
    steps:
      - checkout
      - run:
          name: Instalar dependencias
          command: |
            pip install --upgrade pip
            pip install -r requirements.txt
      - run:
          name: Ejecutar pruebas
          command: pytest --cov=backend --cov-report xml:coverage.xml
      - run:
          name: Ejecutar linting
          command: flake8 .
      - store_test_results:
          path: test-results
      - store_artifacts:
          path: coverage/coverage.xml
      - sonarcloud/scan
      - setup_remote_docker
      - run:
          name: Build Docker image
          command: docker build -t andyn151/mi-app:latest .
      - run:
          name: Test Docker image
          command: docker run --rm andyn151/mi-app:latest pytest
      - run:
          name: Login to Docker Hub
          command: |
            echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
      - run:
          name: Push Docker image to Docker Hub
          command: docker push andyn151/mi-app:latest

workflows:
  version: 2
  workflow_test:
    jobs:
      - test


## Paso 4: Configurar SonarCloud
Crea el archivo sonar-project.properties en la raíz del proyecto.
sonar.host.url=https://sonarcloud.io
sonar.token=$SONAR_TOKEN
sonar.projectKey=Andyn151_CI-CD_practica
sonar.organization=andyn151
sonar.python.coverage.reportPaths=coverage/coverage.xml
sonar.exclusions=**/*.js, **/*.css, docs_src/**, scripts/**
sonar.sonarcloud.disableAutomaticAnalysis=true

##Paso 5: Crear pruebas unitarias y reporte de cobertura
En la carpeta tests, crea el archivo test_example.py con una prueba simple.

def test_example():
    assert 1 + 1 == 2


Luego, asegúrate de que CircleCI esté generando un reporte de cobertura que SonarCloud pueda leer. El archivo coverage.xml se genera en la carpeta coverage/.

pytest --cov=scripts --cov-report xml:coverage/coverage.xml

##Paso 6: Crear el Dockerfile
Este archivo define cómo se construye la imagen de Docker que se sube a Docker Hub y luego se despliega.

FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


##Paso 7: Manifestos de Kubernetes para ArgoCD
En la carpeta manifests, crea los manifiestos necesarios para desplegar la aplicación en Kubernetes usando ArgoCD.
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mi-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mi-app
  template:
    metadata:
      labels:
        app: mi-app
    spec:
      containers:
        - name: mi-app
          image: andyn151/mi-app:latest
          ports:
            - containerPort: 8000

# service.yaml

apiVersion: v1
kind: Service
metadata:
  name: mi-app-service
spec:
  selector:
    app: mi-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer


## Paso 8: Despliegue en Kubernetes usando ArgoCD
Sube los manifiestos a tu repositorio de GitHub y configúralos en ArgoCD para desplegar la aplicación automáticamente al hacer push a la rama main.

## Paso 9: Generación de artefactos 
En el archivo config.yml, puedes agregar un paso para generar y publicar artefactos de la aplicación en Nexus o Docker Hub, si así lo deseas.





