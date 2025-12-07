# 🚀 FastAPI User Management API

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

> Microservicio empresarial REST API construido con FastAPI, implementando arquitectura limpia, autenticación JWT, y mejores prácticas de desarrollo.

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [API Endpoints](#-api-endpoints)
- [Testing](#-testing)
- [Docker](#-docker)
- [Variables de Entorno](#-variables-de-entorno)
- [Contribuir](#-contribuir)

---

## ✨ Características

### 🔐 Seguridad
- ✅ Autenticación JWT (Access & Refresh Tokens)
- ✅ Hash de contraseñas con bcrypt
- ✅ Validación de datos con Pydantic v2
- ✅ Protección CORS configurable
- ✅ Rate limiting para prevenir abusos

### 🏗️ Arquitectura
- ✅ **Clean Architecture** (Separación de capas)
- ✅ **Repository Pattern** para acceso a datos
- ✅ **Dependency Injection** nativo de FastAPI
- ✅ **DTOs** con Pydantic para validación
- ✅ **Service Layer** para lógica de negocio

### 📊 Base de Datos
- ✅ PostgreSQL con SQLAlchemy 2.0
- ✅ Migraciones con Alembic
- ✅ Modelos relacionales
- ✅ Connection pooling
- ✅ Transacciones ACID

### 🛠️ DevOps & Testing
- ✅ Tests unitarios con pytest
- ✅ Tests de integración
- ✅ Cobertura de código
- ✅ Docker & Docker Compose
- ✅ CI/CD ready
- ✅ Logging estructurado

### 📚 Documentación
- ✅ OpenAPI/Swagger automático
- ✅ ReDoc interactivo
- ✅ Ejemplos de requests/responses
- ✅ Schemas detallados

---

## 🏛️ Arquitectura

```
fastapi-user-management-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py                    # Punto de entrada de la aplicación
│   │
│   ├── api/                       # Capa de API/Presentación
│   │   ├── __init__.py
│   │   ├── deps.py               # Dependencias globales
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── endpoints/
│   │       │   ├── __init__.py
│   │       │   ├── auth.py       # Endpoints de autenticación
│   │       │   └── users.py      # Endpoints de usuarios
│   │       └── router.py         # Router principal v1
│   │
│   ├── core/                      # Configuración y utilidades core
│   │   ├── __init__.py
│   │   ├── config.py             # Configuración de la app
│   │   ├── security.py           # JWT, hashing, etc.
│   │   └── logging.py            # Configuración de logging
│   │
│   ├── models/                    # Modelos de SQLAlchemy
│   │   ├── __init__.py
│   │   ├── base.py               # Modelo base
│   │   └── user.py               # Modelo de usuario
│   │
│   ├── schemas/                   # Pydantic schemas (DTOs)
│   │   ├── __init__.py
│   │   ├── user.py               # Schemas de usuario
│   │   └── token.py              # Schemas de token
│   │
│   ├── repositories/              # Capa de acceso a datos
│   │   ├── __init__.py
│   │   ├── base.py               # Repository base genérico
│   │   └── user.py               # User repository
│   │
│   ├── services/                  # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── auth.py               # Servicio de autenticación
│   │   └── user.py               # Servicio de usuarios
│   │
│   └── db/                        # Database
│       ├── __init__.py
│       ├── base.py               # Import de todos los modelos
│       └── session.py            # Configuración de sesión DB
│
├── tests/                         # Tests
│   ├── __init__.py
│   ├── conftest.py               # Configuración de pytest
│   ├── test_auth.py
│   └── test_users.py
│
├── alembic/                       # Migraciones de BD
│   ├── versions/
│   └── env.py
│
├── docker/
│   └── Dockerfile
│
├── .env.example                   # Ejemplo de variables de entorno
├── .gitignore
├── alembic.ini                    # Configuración de Alembic
├── docker-compose.yml
├── pyproject.toml                 # Poetry dependencies
├── requirements.txt               # Pip dependencies
└── README.md
```

### 📐 Patrón de Flujo de Datos

```mermaid
graph LR
    A[Cliente] --> B[API Endpoint]
    B --> C[Service Layer]
    C --> D[Repository]
    D --> E[Database]
    E --> D
    D --> C
    C --> B
    B --> A

    style A fill:#61DAFB,stroke:#000,stroke-width:2px
    style B fill:#009688,stroke:#000,stroke-width:2px
    style C fill:#FF9800,stroke:#000,stroke-width:2px
    style D fill:#9C27B0,stroke:#000,stroke-width:2px
    style E fill:#4CAF50,stroke:#000,stroke-width:2px
```

---

## 🛠️ Tecnologías

| Categoría | Tecnología | Versión | Propósito |
|-----------|-----------|---------|-----------|
| **Framework** | FastAPI | 0.104+ | Framework web async de alto rendimiento |
| **Base de Datos** | PostgreSQL | 15 | Base de datos relacional |
| **ORM** | SQLAlchemy | 2.0+ | Object-Relational Mapping |
| **Migraciones** | Alembic | 1.12+ | Gestión de migraciones de BD |
| **Validación** | Pydantic | 2.0+ | Validación de datos y settings |
| **Autenticación** | python-jose | 3.3+ | JWT tokens |
| **Seguridad** | passlib | 1.7+ | Hash de contraseñas |
| **Testing** | pytest | 7.4+ | Framework de testing |
| **ASGI Server** | uvicorn | 0.24+ | Servidor ASGI |
| **Containerización** | Docker | Latest | Containerización |

---

## 📦 Instalación

### Prerrequisitos

- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose (opcional)

### Opción 1: Instalación Local

```bash
# 1. Clonar el repositorio
git clone https://github.com/Devdprivity/fastapi-user-management-api.git
cd fastapi-user-management-api

# 2. Crear entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# 5. Ejecutar migraciones
alembic upgrade head

# 6. Iniciar la aplicación
uvicorn app.main:app --reload
```

### Opción 2: Con Docker

```bash
# 1. Clonar el repositorio
git clone https://github.com/Devdprivity/fastapi-user-management-api.git
cd fastapi-user-management-api

# 2. Construir y ejecutar
docker-compose up --build

# La API estará disponible en http://localhost:8000
```

---

## 🚀 Uso

### Acceder a la Documentación

Una vez iniciada la aplicación:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Ejemplo de Uso

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# 1. Registrar usuario
response = requests.post(
    f"{BASE_URL}/auth/register",
    json={
        "email": "user@example.com",
        "password": "SecurePass123!",
        "full_name": "John Doe"
    }
)
print(response.json())

# 2. Login
response = requests.post(
    f"{BASE_URL}/auth/login",
    data={
        "username": "user@example.com",
        "password": "SecurePass123!"
    }
)
tokens = response.json()
access_token = tokens["access_token"]

# 3. Obtener perfil (autenticado)
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get(
    f"{BASE_URL}/users/me",
    headers=headers
)
print(response.json())
```

---

## 📡 API Endpoints

### Autenticación

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/auth/register` | Registrar nuevo usuario | No |
| POST | `/api/v1/auth/login` | Iniciar sesión | No |
| POST | `/api/v1/auth/refresh` | Refrescar access token | Refresh Token |
| POST | `/api/v1/auth/logout` | Cerrar sesión | Sí |

### Usuarios

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/users/me` | Obtener perfil actual | Sí |
| PUT | `/api/v1/users/me` | Actualizar perfil | Sí |
| DELETE | `/api/v1/users/me` | Eliminar cuenta | Sí |
| GET | `/api/v1/users` | Listar usuarios (admin) | Admin |
| GET | `/api/v1/users/{id}` | Obtener usuario por ID (admin) | Admin |

### Ejemplos de Request/Response

#### POST `/api/v1/auth/register`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2025-12-07T10:30:00Z"
}
```

#### POST `/api/v1/auth/login`

**Request (form-data):**
```
username: user@example.com
password: SecurePass123!
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

---

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=app --cov-report=html

# Tests específicos
pytest tests/test_auth.py -v

# Ver reporte de cobertura
# Abrir htmlcov/index.html en el navegador
```

### Estructura de Tests

```python
# tests/test_users.py
def test_create_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "Test123!",
            "full_name": "Test User"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
```

---

## 🐳 Docker

### Servicios

El `docker-compose.yml` incluye:

- **app**: API de FastAPI
- **db**: PostgreSQL 15
- **pgadmin**: PgAdmin 4 (opcional)

### Comandos Útiles

```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f app

# Ejecutar migraciones
docker-compose exec app alembic upgrade head

# Acceder al contenedor
docker-compose exec app bash

# Detener servicios
docker-compose down

# Limpiar volúmenes (¡CUIDADO! Elimina datos)
docker-compose down -v
```

---

## 🔐 Variables de Entorno

Crear archivo `.env` basado en `.env.example`:

```bash
# Application
PROJECT_NAME=FastAPI User Management
VERSION=1.0.0
API_V1_PREFIX=/api/v1
DEBUG=True

# Server
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fastapi_db
DB_ECHO=False

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
ALLOWED_METHODS=*
ALLOWED_HEADERS=*

# First Superuser
FIRST_SUPERUSER_EMAIL=admin@example.com
FIRST_SUPERUSER_PASSWORD=admin123
```

### 🔑 Generar SECRET_KEY

```python
import secrets
print(secrets.token_urlsafe(32))
```

---

## 🏆 Mejores Prácticas Implementadas

### 🔒 Seguridad
- ✅ Contraseñas hasheadas con bcrypt
- ✅ JWT con expiración configurable
- ✅ Validación de entrada con Pydantic
- ✅ CORS configurado
- ✅ Rate limiting
- ✅ No se exponen errores sensibles

### 📊 Base de Datos
- ✅ Migraciones versionadas con Alembic
- ✅ Repository pattern
- ✅ Índices en campos críticos
- ✅ Soft deletes (campos `deleted_at`)
- ✅ Timestamps automáticos

### 🧪 Testing
- ✅ Test coverage > 80%
- ✅ Tests unitarios y de integración
- ✅ Fixtures reusables
- ✅ Database isolation entre tests

### 📝 Código
- ✅ Type hints en todo el código
- ✅ Docstrings en funciones públicas
- ✅ Nombres descriptivos
- ✅ Separación de responsabilidades
- ✅ DRY (Don't Repeat Yourself)

---

## 📈 Roadmap

- [ ] Implementar rate limiting con Redis
- [ ] Agregar roles y permisos (RBAC)
- [ ] Implementar paginación avanzada
- [ ] WebSockets para notificaciones en tiempo real
- [ ] Integración con OAuth2 (Google, GitHub)
- [ ] Sistema de auditoría de cambios
- [ ] Caché con Redis
- [ ] Métricas con Prometheus

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: Amazing feature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 👨‍💻 Autor

**David Badell**
- GitHub: [@Devdprivity](https://github.com/Devdprivity)
- Email: davidbadell42@gmail.com

---

## 🙏 Agradecimientos

- [FastAPI](https://fastapi.tiangolo.com/) - El increíble framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - El ORM más completo de Python
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Validación de datos

---

<div align="center">

**⭐ Si te gustó este proyecto, dale una estrella en GitHub ⭐**

![Made with Love](https://img.shields.io/badge/Made%20with-❤️-red?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green?style=for-the-badge&logo=fastapi)

</div>
