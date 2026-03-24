<script>
  import { app } from '../state/appState.svelte.js'
  import {
    createUser,
    deleteUser,
    getUsers,
    updateUserRole,
  } from '../services/api.js'

  let users = $state([])
  let loading = $state(false)
  let saving = $state(false)
  let error = $state('')

  let newUsername = $state('')
  let newPassword = $state('')
  let newRole = $state('user')

  let usersCount = $derived(users.length)

  async function loadUsers() {
    loading = true
    error = ''
    try {
      users = await getUsers()
    } catch (requestError) {
      error = requestError.message || 'No se pudo cargar usuarios.'
    } finally {
      loading = false
    }
  }

  async function handleCreate() {
    if (!newUsername.trim() || !newPassword.trim()) {
      error = 'Usuario y contrasena son obligatorios.'
      return
    }

    saving = true
    error = ''
    try {
      await createUser({
        username: newUsername.trim(),
        password: newPassword,
        role: newRole,
      })
      newUsername = ''
      newPassword = ''
      newRole = 'user'
      app.globalMessage = 'Usuario creado.'
      await loadUsers()
    } catch (requestError) {
      error = requestError.message || 'No se pudo crear usuario.'
    } finally {
      saving = false
    }
  }

  async function handleRoleChange(userId, role) {
    saving = true
    error = ''
    try {
      await updateUserRole(userId, role)
      app.globalMessage = 'Rol actualizado.'
      await loadUsers()
    } catch (requestError) {
      error = requestError.message || 'No se pudo actualizar el rol.'
    } finally {
      saving = false
    }
  }

  async function handleDelete(userId, username) {
    if (!window.confirm('Eliminar usuario ' + username + '?')) return

    saving = true
    error = ''
    try {
      await deleteUser(userId)
      app.globalMessage = 'Usuario eliminado.'
      await loadUsers()
    } catch (requestError) {
      error = requestError.message || 'No se pudo eliminar usuario.'
    } finally {
      saving = false
    }
  }

  $effect(() => {
    const role = app.user?.role
    if (role === 'admin') {
      void loadUsers()
    }
  })
</script>

<section class="stack">
  <div class="panel stack">
    <h2 style="margin:0">Usuarios ({usersCount})</h2>
    <p class="muted">Zona de administracion de usuarios y roles.</p>

    {#if error}
      <p class="error">{error}</p>
    {/if}

    <div style="display:grid;grid-template-columns:2fr 2fr 1fr auto;gap:.5rem">
      <input bind:value={newUsername} placeholder="Nuevo usuario" />
      <input bind:value={newPassword} type="password" placeholder="Contrasena" />
      <select bind:value={newRole}>
        <option value="user">user</option>
        <option value="admin">admin</option>
      </select>
      <button class="btn-primary" type="button" onclick={handleCreate} disabled={saving}>
        {saving ? 'Guardando...' : 'Crear'}
      </button>
    </div>

    <button class="btn-subtle" type="button" onclick={loadUsers} disabled={loading}>
      {loading ? 'Cargando...' : 'Recargar usuarios'}
    </button>
  </div>

  <div class="panel">
    {#if users.length === 0 && !loading}
      <p>No hay usuarios para mostrar.</p>
    {/if}

    <div class="stack">
      {#each users as user (user._id)}
        <div class="product-card" style="display:grid;grid-template-columns:2fr 1fr auto;gap:.5rem;align-items:center">
          <div>
            <strong>{user.username}</strong>
            <div class="muted">ID: {user._id}</div>
          </div>

          <select
            value={user.role}
            onchange={(event) => handleRoleChange(user._id, event.currentTarget.value)}
            disabled={saving || user._id === app.user?.id}
          >
            <option value="user">user</option>
            <option value="admin">admin</option>
          </select>

          <button
            class="btn-primary"
            type="button"
            onclick={() => handleDelete(user._id, user.username)}
            disabled={saving || user._id === app.user?.id}
          >
            Eliminar
          </button>
        </div>
      {/each}
    </div>
  </div>
</section>