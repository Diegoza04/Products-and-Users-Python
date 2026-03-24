# Frontend - Svelte 5 + Vite

Aplicacion SPA del cliente para gestion de autenticacion, productos y administracion de usuarios.

Este README documenta solo el frontend de la carpeta `client`.

## Requisitos

- Node.js 18 o superior
- npm 8 o superior

## Instalacion

Desde la carpeta `client`:

```bash
npm install
```

## Ejecucion

```bash
npm run dev
```

Servidor de desarrollo:

- http://localhost:5173

## Build y validacion

```bash
npm run lint
npm run build
```

## Scripts disponibles

- `npm run dev`: entorno de desarrollo
- `npm run build`: build de produccion
- `npm run preview`: previsualizacion de build
- `npm run lint`: analisis estatico

## Arquitectura frontend

Estructura principal:

```text
client/
  src/
    components/
      NavBar.svelte
      ProductCard.svelte
      ProductForm.svelte
    pages/
      LoginPage.svelte
      ProductsPage.svelte
      ProfilePage.svelte
      AdminUsersPage.svelte
    services/
      api.js
    state/
      appState.svelte.js
    App.svelte
    main.js
    styles.css
```

### Flujo de la aplicacion

1. `main.js` monta `App.svelte`.
2. `App.svelte` centraliza guardas de ruta, session y toasts globales.
3. `appState.svelte.js` almacena estado global (auth, ruta, productos, mensajes).
4. Las paginas ejecutan casos de uso (login, listado/CRUD, perfil, admin usuarios).
5. `api.js` encapsula peticiones HTTP y errores globales por estado.

## Pantallas y comportamiento

### Login

- Formulario con validaciones basicas (usuario/contrasena obligatorios).
- Estado de carga y errores de autenticacion.

Archivo: `src/pages/LoginPage.svelte`

### Productos

- Listado de productos con nombre, precio y estado.
- Filtros por texto, estado activo y rango de precio (min/max).
- Detalle en modal.
- Crear, editar y borrar (acciones restringidas por rol).

Archivo: `src/pages/ProductsPage.svelte`

### Perfil

- Vista de usuario autenticado, rol y token resumido.
- Accion de cierre de sesion.

Archivo: `src/pages/ProfilePage.svelte`

### Admin usuarios

- Listado de usuarios.
- Alta de usuarios.
- Cambio de rol.
- Baja de usuarios con confirmacion.

Archivo: `src/pages/AdminUsersPage.svelte`

## Runes de Svelte 5 utilizadas

### $state

Gestiona estado reactivo local y global.

- `src/state/appState.svelte.js`
  - token JWT
  - usuario autenticado
  - ruta actual
  - productos cargados
  - mensajes y errores globales
- `src/pages/LoginPage.svelte`
  - credenciales, loading, error local
- `src/pages/ProductsPage.svelte`
  - filtros, modal, formulario, loading, error
- `src/pages/AdminUsersPage.svelte`
  - listado, formulario admin, loading/saving/error
- `src/components/ProductForm.svelte`
  - campos y validacion local del formulario

### $derived

Calcula datos derivados sin recalculo manual.

- `src/App.svelte`
  - `displayName`, `isAuthed`, `isAdmin`
- `src/pages/ProductsPage.svelte`
  - `filteredProducts`, `productCount`, `canManage`
- `src/pages/AdminUsersPage.svelte`
  - `usersCount`
- `src/components/ProductCard.svelte`
  - texto de estado activo/no activo
- `src/pages/ProfilePage.svelte`
  - rol visible y token resumido

### $effect

Maneja side effects y sincronizacion con el entorno.

- `src/App.svelte`
  - persistencia de token en `sessionStorage`
  - listener de `popstate` para navegacion navegador
  - guardas de acceso por autenticacion/rol
  - auto-cierre de toasts globales
- `src/pages/ProductsPage.svelte`
  - recarga reactiva de productos
- `src/pages/AdminUsersPage.svelte`
  - carga inicial de usuarios para admin
- `src/components/ProductForm.svelte`
  - sincronizacion entre modo crear/editar

### $props

Define la API de los componentes reutilizables.

- `src/components/NavBar.svelte`
- `src/components/ProductCard.svelte`
- `src/components/ProductForm.svelte`
- `src/pages/LoginPage.svelte`
- `src/pages/ProfilePage.svelte`

## Navegacion SPA

Rutas frontend activas:

- `/login`
- `/products`
- `/profile`
- `/admin/users` (solo admin)

La navegacion y guardas se controlan desde:

- `src/App.svelte`
- `src/state/appState.svelte.js`
- `src/components/NavBar.svelte`

## Estilos y UX

- CSS propio en `src/styles.css`.
- Layout responsive para movil y desktop.
- Estados visuales de error y exito.
- Toast global para errores HTTP comunes y confirmaciones de acciones.
- Confirmacion antes de acciones destructivas.

## Solucion de problemas (frontend)

1. Pantalla en blanco:
- Verifica errores en consola del navegador (F12).
- Ejecuta `npm run build` para detectar errores de compilacion.

2. Dependencias inconsistentes:

```bash
rm -rf node_modules package-lock.json
npm install
```

3. Puerto ocupado:
- Cierra procesos previos de Vite o cambia el puerto en `vite.config.js`.

