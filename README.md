# UniRide 🚗

Sistema web desarrollado con Django para la gestión de viajes y reservas entre usuarios.

## 📋 Descripción

UniRide es una aplicación que permitirá a los usuarios:

* Registrarse e iniciar sesión
* Publicar viajes disponibles
* Buscar y reservar viajes
* Gestionar sus reservas

Este proyecto forma parte de un desarrollo académico enfocado en la implementación de lógica de negocio utilizando Django.

## 🛠️ Tecnologías

* **Backend**: Django
* **Base de Datos**: MySQL
* **Contenedores**: Docker (en configuración)
* **Control de versiones**: GitHub

## ⚙️ Estado del proyecto

🚧 Configuración inicial completada:

* Proyecto Django creado
* Conexión a base de datos MySQL configurada
* Entorno virtual y dependencias listas

⏳ Pendiente:

* Creación de apps
* Modelado de base de datos
* Implementación de lógica de negocio
* Desarrollo de vistas y templates

## 🚀 Instalación (desarrollo local)

```bash
# Clonar repositorio
git clone <url-del-repositorio>

# Entrar al proyecto
cd uniride_django

# Crear entorno virtual
python -m venv venv

# Activar entorno
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo de entorno
copy .env.example .env

# Ejecutar servidor
python manage.py runserver
```

## 📁 Estructura inicial

```
uniride_django/
├── apps/
├── config/
├── docs/
├── .env.example
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```

## 📌 Notas

* El archivo `.env` no se incluye en el repositorio por seguridad.
* Se proporciona un archivo `.env.example` como referencia para configuración.
* La carpeta `venv/` no se incluye ya que es un entorno local.
* La base de datos se gestiona mediante Django ORM.

---
