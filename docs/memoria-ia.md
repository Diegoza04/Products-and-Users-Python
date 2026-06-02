# Memoria de uso de IA

## Objetivo
Usé IA como asistente técnico para acelerar la migración del backend a Python, pero revisando y corrigiendo manualmente las partes sensibles: autenticación, validación, persistencia y compatibilidad con el frontend.

## Prompts clave utilizados

### 1. Migración a FastAPI con arquitectura limpia
Prompt base:
> "Crea un backend en FastAPI compatible con el frontend Svelte existente, manteniendo los endpoints `/api/auth/login`, `/api/products` y `/api/admin/users`, con separación en routers, services y repositories."

Refinamiento:
> "No concentres lógica en un único archivo. Usa SQLAlchemy con SQLite, schemas Pydantic, repositorios para acceso a datos y respuestas JSON compatibles con `_id`, `isActive` y `createdAt`."

### 2. JWT y compatibilidad con el frontend
Prompt base:
> "Implementa login JWT para que el frontend pueda seguir decodificando el token y guardándolo en `sessionStorage`."

Refinamiento:
> "El token debe incluir `id`, `username` y `role`, y la extracción del header `Authorization` debe hacerse con una dependencia de FastAPI, devolviendo 401/403 según corresponda."

### 3. Validación y errores
Prompt base:
> "Añade validación de productos y usuarios."

Refinamiento:
> "Usa Pydantic para devolver 422 en datos inválidos y un manejador global de errores para traducir excepciones de negocio a JSON uniforme con `message`."

## Error o alucinación detectada
La primera versión asistida por IA trató el header `Authorization` como si fuera un parámetro normal de la función, lo que en FastAPI no lee el valor real de la petición. Eso habría dejado todas las rutas protegidas fallando con falsos 401/403.

## Corrección manual aplicada
Lo corregí moviendo la autenticación a una dependencia real con `Header(default=None)` y `Depends`, de modo que FastAPI inyecta el token del request correctamente.

Otro problema fue el mapeo de productos: el frontend envía `isActive`, pero la base de datos usa `is_active`. La IA no resolvía bien esa traducción y podía romper el alta/edición. Lo corregí usando alias en Pydantic y serialización explícita en la capa de salida.

## Conclusión crítica
La IA fue útil para esbozar la estructura, pero no era suficiente para garantizar compatibilidad de contrato ni seguridad. La corrección manual fue necesaria para asegurar que el backend cumpliera el patrón por capas, la validación real y el mismo JSON que espera Svelte.