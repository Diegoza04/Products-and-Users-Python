<script>
  import { login } from '../services/api.js'
  import { app, setAuth } from '../state/appState.svelte.js'

  let { onLoggedIn } = $props()

  let username = $state('')
  let password = $state('')
  let loading = $state(false)
  let error = $state('')

  async function submit() {
    error = ''
    app.globalMessage = ''
    app.globalError = ''

    if (!username.trim() || !password.trim()) {
      error = 'Usuario y contrasena son obligatorios.'
      return
    }

    loading = true
    try {
      const response = await login(username.trim(), password)
      const ok = setAuth(response.token)
      if (!ok) {
        error = 'Token recibido invalido.'
        return
      }
      app.globalMessage = 'Sesion iniciada correctamente.'
      onLoggedIn()
    } catch (requestError) {
      error = requestError.message || 'No se pudo iniciar sesion.'
    } finally {
      loading = false
    }
  }
</script>

<section class="panel stack" style="max-width:420px;margin:0 auto">
  <h2>Iniciar sesion</h2>
  <p class="muted">Ingresa tus credenciales </p>

  {#if error}
    <p class="error">{error}</p>
  {/if}

  <label>
    Usuario
    <input bind:value={username} placeholder="admin" autocomplete="username" />
  </label>

  <label>
    Contrasena
    <input bind:value={password} type="password" autocomplete="current-password" />
  </label>

  <button type="button" class="btn-primary" disabled={loading} onclick={submit}>
    {loading ? 'Validando...' : 'Entrar'}
  </button>
</section>
