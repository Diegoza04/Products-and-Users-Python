const PUBLIC_ROUTES = ['/login']
const PRIVATE_ROUTES = ['/products', '/profile']

function decodeJwt(token) {
  try {
    const payload = token.split('.')[1]
    if (!payload) return null
    const base64 = payload.replace(/-/g, '+').replace(/_/g, '/')
    const json = decodeURIComponent(
      atob(base64)
        .split('')
        .map((char) => '%' + ('00' + char.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    )
    return JSON.parse(json)
  } catch (_error) {
    return null
  }
}

function normalizeRoute(pathname) {
  if (PUBLIC_ROUTES.includes(pathname) || PRIVATE_ROUTES.includes(pathname)) {
    return pathname
  }
  return '/products'
}

const initialToken = sessionStorage.getItem('jwt') || ''
const initialUser = initialToken ? decodeJwt(initialToken) : null

export const app = $state({
  token: initialToken,
  user: initialUser,
  route: normalizeRoute(window.location.pathname),
  products: [],
  productsLoading: false,
  globalMessage: '',
  globalError: '',
})

export function navigate(path, replace = false) {
  const route = normalizeRoute(path)
  if (replace) {
    window.history.replaceState({}, '', route)
  } else {
    window.history.pushState({}, '', route)
  }
  app.route = route
}

export function setAuth(token) {
  const user = decodeJwt(token)
  if (!user) {
    app.globalError = 'No se pudo validar el token JWT.'
    return false
  }
  app.token = token
  app.user = user
  app.globalError = ''
  return true
}

export function clearAuth() {
  app.token = ''
  app.user = null
  sessionStorage.removeItem('jwt')
}

$effect(() => {
  if (app.token) {
    sessionStorage.setItem('jwt', app.token)
  } else {
    sessionStorage.removeItem('jwt')
  }
})

export const appRoutes = {
  PUBLIC_ROUTES,
  PRIVATE_ROUTES,
}