<script>
  let { route, isAuthed = false, isAdmin = false, onNavigate, onLogout } = $props()

  const routes = [
    { path: '/products', label: 'Productos', private: true },
    { path: '/profile', label: 'Perfil', private: true },
    { path: '/admin/users', label: 'Admin usuarios', private: true, adminOnly: true },
    { path: '/login', label: 'Login', private: false },
  ]
</script>

<nav class="nav-links" aria-label="Navegacion principal">
  {#each routes as item}
    {#if (!item.private || isAuthed) && (!item.adminOnly || isAdmin)}
      <button
        class="nav-btn {route === item.path ? 'active' : ''}"
        type="button"
        onclick={() => onNavigate(item.path)}
      >
        {item.label}
      </button>
    {/if}
  {/each}

  {#if isAuthed}
    <button type="button" class="nav-btn" onclick={onLogout}>Salir</button>
  {/if}
</nav>