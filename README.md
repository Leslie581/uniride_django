# UniRide 🚗

Sistema web desarrollado con Django para la gestión de viajes y reservas entre usuarios.

## 📋 Descripción

UniRide es una aplicación que permitirá a los usuarios:

* Registrarse e iniciar sesión  
* Publicar viajes disponibles  
* Buscar y reservar viajes  
* Gestionar sus reservas  

Este proyecto forma parte de un desarrollo académico enfocado en la implementación de lógica de negocio utilizando Django y Docker.

---

## 🛠️ Tecnologías

* **Backend**: Django  
* **Base de Datos**: MySQL  
* **Contenedores**: Docker & Docker Compose  
* **Control de versiones**: GitHub  

---

## ⚙️ Estado del proyecto

🚧 Configuración inicial completada:

* Proyecto Django creado  
* Docker configurado (web + base de datos)  
* Conexión a MySQL mediante contenedores  
* Estructura base del proyecto definida  

⏳ Pendiente:

* Creación de apps  
* Modelado de base de datos en Django  
* Implementación de lógica de negocio  
* Desarrollo de vistas y templates  

---

## 🚀 Instalación (con Docker)

### 🔧 Prerrequisitos

* Tener instalado **Docker Desktop**  
* Tener **Git**  

---

### 📥 Pasos para ejecutar el proyecto

```bash
# 1. Clonar repositorio
git clone <url-del-repositorio>

# 2. Entrar al proyecto
cd uniride_django

# 3. Crear archivo de entorno
copy .env.example .env   # Windows
# cp .env.example .env   # Mac/Linux

# 4. Levantar contenedores
docker compose up --build

´´´

🌐 Acceso al sistema
👉 http://localhost:8001


´´´

## 📁 Estructura actualizada

```
uniride_django_pruebas/
├── apps/                 # Apps del sistema
├── config/               # Configuración Django
├── docs/                 # Documentación
├── media/                # Archivos subidos (imágenes, etc.)
├── templates/            # Templates HTML
├── .env.example          # Variables de entorno de ejemplo
├── .gitignore
├── docker-compose.yml    # Configuración de servicios
├── Dockerfile            # Imagen de la app
├── manage.py
├── README.md
└── requirements.txt
```

## 📌 Notas

* El archivo .env no se incluye en el repositorio por seguridad.
* Se proporciona un archivo .env.example como base para configuración.
* La carpeta `venv/` no se incluye ya que es un entorno local.
* La base de datos corre dentro de un contenedor Docker.
* La carpeta media/ se utiliza para almacenar archivos subidos por usuarios.

---