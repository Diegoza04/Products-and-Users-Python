<script>
  import { app } from '../state/appState.svelte.js'

  let { displayName = 'Invitado', onLogout } = $props()

  let roleText = $derived(app.user?.role || 'sin rol')
  let tokenPreview = $derived(app.token ? app.token.slice(0, 24) + '...' : 'No hay token')
</script>

<section class="panel stack" style="max-width:640px">
  <h2>Perfil</h2>
  <p><strong>Usuario:</strong> {displayName}</p>
  <p><strong>Rol:</strong> {roleText}</p>
  <p class="muted"><strong>Token:</strong> {tokenPreview}</p>

  <button class="btn-primary" type="button" onclick={onLogout}>Cerrar sesion</button>
</section>
