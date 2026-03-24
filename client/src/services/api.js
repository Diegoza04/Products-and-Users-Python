import { app } from '../state/appState.svelte.js'

export async function apiFetch(path, options = {}) {
  const headers = {
    ...(options.headers || {}),
  }

  if (app.token) {
    headers.Authorization = 'Bearer ' + app.token
  }

  if (!(options.body instanceof FormData) && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json'
  }

  const response = await fetch('/api' + path, {
    ...options,
    headers,
  })

  const body = await response.json().catch(() => null)

  if (!response.ok) {
    if (response.status === 401){
      app.globalError = 'Sesion expirada o credenciales invalidas (401)'
    } else if (response.status === 403) {
      app.globalError = 'No tienes permisos para esta accion (403)'
    } else if (response.status >= 500) {
      app.globalError = 'Error interno del servidor. Intenta nuevamente mas tarde'
    }
    
    const error = new Error(body?.message || 'Error de API')
    error.status = response.status
    error.body = body
    throw error
  }

  return body
}

export async function login(username, password) {
  return apiFetch('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  })
}

export async function getProducts() {
  return apiFetch('/products')
}

export async function createProduct(payload) {
  return apiFetch('/products', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function updateProduct(productId, payload) {
  return apiFetch('/products/' + productId, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export async function deleteProduct(productId) {
  return apiFetch('/products/' + productId, {
    method: 'DELETE',
  })
}

export async function getUsers() {
  return apiFetch('/admin/users')
}

export async function createUser(payload) {
  return apiFetch('/admin/users', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function updateUserRole(userId, role) {
  return apiFetch('/admin/users/' + userId, {
    method: 'PUT',
    body: JSON.stringify({ role }),
  })
}

export async function deleteUser(userId) {
  return apiFetch('/admin/users/' + userId, {
    method: 'DELETE',
  })
}