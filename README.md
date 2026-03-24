# Portal de Productos y Usuarios (Svelte 5 + Node.js)

Repositorio: https://github.com/Diegoza04/Products-and-users-Svelte.git 

Aplicacion fullstack con:
- Frontend SPA en Svelte 5 (Vite)
- Backend en Node.js + Express + JWT + MongoDB
- CRUD de productos y gestion de usuarios por rol

## Instalacion y ejecucion

### Requisitos
- Node.js 18+
- npm 8+
- MongoDB local o MongoDB Atlas

### 1) Clonar repositorio
```bash
git clone https://github.com/Diegoza04/Products-and-users-Svelte.git 
cd Products-and-users-Svelte.git 
```

### 2) Configurar backend
Entrar a `server/` y crear archivo `.env`:
```env
PORT=3000
MONGO_URI=mongodb://127.0.0.1:27017/practica1
JWT_SECRET=tu_clave_jwt
```

Instalar y ejecutar backend:
```bash
cd server
npm install
npm run dev
```

### 3) Configurar frontend
En otra terminal:
```bash
cd client
npm install
npm run dev
```

Frontend: http://localhost:5173

## Estructura principal
```text
client/
  src/
    components/
    pages/
    services/
    state/
server/
  routes/
  models/
  middleware/
```

## Runas de Svelte 5 usadas

### $state
Se usa para estado reactivo local y global.
- `client/src/state/appState.svelte.js`: token, usuario, ruta actual, productos, errores/mensajes globales.
- `client/src/pages/LoginPage.svelte`: formulario y estado de carga/error.
- `client/src/pages/ProductsPage.svelte`: filtros, modal, formulario de producto, carga.
- `client/src/pages/AdminUsersPage.svelte`: listado, formularios y estado de guardado/carga.
- `client/src/components/ProductForm.svelte`: campos del formulario.

### $derived
Se usa para valores derivados del estado.
- `client/src/App.svelte`: `displayName`, `isAuthed`, `isAdmin`.
- `client/src/pages/ProductsPage.svelte`: `filteredProducts`, `productCount`, permisos por rol.
- `client/src/pages/AdminUsersPage.svelte`: contador de usuarios.
- `client/src/components/ProductCard.svelte`: texto de estado activo/no activo.
- `client/src/pages/ProfilePage.svelte`: rol y preview del token.

### $effect
Se usa para side effects y sincronizacion.
- `client/src/App.svelte`:
  - persistencia de JWT en sessionStorage
  - escuchar back/forward del navegador
  - guardas de rutas segun autenticacion y rol
  - auto cierre de toast global
- `client/src/pages/ProductsPage.svelte`: recargar productos cuando cambian rol/filtros clave.
- `client/src/pages/AdminUsersPage.svelte`: cargar usuarios cuando entra admin.
- `client/src/components/ProductForm.svelte`: sincronizar formulario al editar/crear.

### $props
Se usa para props en componentes reutilizables.
- `client/src/components/NavBar.svelte`
- `client/src/components/ProductCard.svelte`
- `client/src/components/ProductForm.svelte`
- `client/src/pages/LoginPage.svelte`
- `client/src/pages/ProfilePage.svelte`

## Backend utilizado (endpoints y roles)

### Autenticacion
- `POST /api/auth/login` (publico)
- `POST /api/auth/register` (publico)

### Productos
- `GET /api/products` (publico)
- `POST /api/products` (admin)
- `PUT /api/products/:id` (admin)
- `DELETE /api/products/:id` (admin)

### Administracion de usuarios (solo admin)
- `GET /api/admin/users`
- `POST /api/admin/users`
- `PUT /api/admin/users/:id` (cambio de rol)
- `DELETE /api/admin/users/:id`

### Pedidos admin (solo admin)
- `GET /api/admin/orders`
- `GET /api/admin/orders/:status`

## Roles requeridos
- `user`: acceso a login, perfil y vista de productos.
- `admin`: ademas de lo anterior, puede crear/editar/borrar productos y gestionar usuarios.

## Scripts utiles

### Frontend (`client/package.json`)
- `npm run dev`
- `npm run build`
- `npm run lint`

### Backend (`server/package.json`)
- `npm run dev`
- `npm start`

## Nota para cuando vayas a levantar el repositorio
Para probar todo el flujo de la practica, el backend debe estar levantado junto con MongoDB. Si MongoDB no esta disponible, el frontend abre pero las llamadas API fallan.
