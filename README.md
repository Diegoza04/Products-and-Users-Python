# Portal de Productos y Usuarios

Frontend en Svelte 5 y backend nuevo en FastAPI con SQLite, SQLAlchemy y JWT.

## Requisitos
- Python 3.11+ para el backend.
- Node.js 18+ para el frontend.

## Arranque del backend
1. Crear y activar un entorno virtual en `server/`.
2. Instalar dependencias con `pip install -r requirements.txt`.
3. Copiar `server/.env.example` a `.env` si quieres cambiar la clave JWT o la ruta de base de datos.
4. Ejecutar `uvicorn app.main:app --reload` desde la carpeta `server/`.

Credenciales iniciales:
- Usuario: `admin`
- Contraseña: `admin123`

## Arranque del frontend
1. Entrar en `client/`.
2. Ejecutar `npm install`.
3. Ejecutar `npm run dev`.

La app queda accesible en `http://localhost:5173` y consume el backend por `/api/...`.

## Arquitectura del backend
```text
server/app/
  core/         configuración, seguridad, base de datos, dependencias
  models/       modelos SQLAlchemy
  repositories/ acceso a datos
  services/     lógica de negocio
  schemas/      validación con Pydantic
  routers/      endpoints HTTP
```

## Endpoints principales
### Autenticación
- `POST /api/auth/register`
- `POST /api/auth/login`

### Productos
- `GET /api/products`
- `POST /api/products` solo `admin`
- `PUT /api/products/:id` solo `admin`
- `DELETE /api/products/:id` solo `admin`

### Usuarios
- `GET /api/admin/users` solo `admin`
- `POST /api/admin/users` solo `admin`
- `PUT /api/admin/users/:id` solo `admin`
- `DELETE /api/admin/users/:id` solo `admin`

### Compatibilidad extra
- `GET /api/chat/history` autenticado
- `GET /api/admin/orders` y `GET /api/admin/orders/:status` devuelven una lista vacía para mantener compatibilidad con el contrato antiguo.

## Documentacion de IA
La memoria de prompts e iteraciones está en [docs/memoria-ia.md](docs/memoria-ia.md).
