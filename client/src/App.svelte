<script>
  import NavBar from './components/NavBar.svelte'
  import LoginPage from './pages/LoginPage.svelte'
  import ProductsPage from './pages/ProductsPage.svelte'
  import ProfilePage from './pages/ProfilePage.svelte'
  import AdminUsersPage from './pages/AdminUsersPage.svelte'
  import { app, appRoutes, navigate, clearAuth } from './state/appState.svelte.js'

  // Derived UI values
  let displayName = $derived(app.user?.username || 'Invitado')
  let isAuthed = $derived(Boolean(app.user && app.token))
  let isAdmin = $derived(app.user?.role === 'admin')

  function goTo(path) {
    navigate(path)
  }

  function logout() {
    clearAuth()
    navigate('/login', true)
  }

  // Persist JWT token (Svelte 5 runes: must live in a component)
  $effect(() => {
    if (app.token) sessionStorage.setItem('jwt', app.token)
    else sessionStorage.removeItem('jwt')
  })

  // Handle browser back/forward
  $effect(() => {
    const onPopState = () => {
      navigate(window.location.pathname, true)
    }
    window.addEventListener('popstate', onPopState)
    return () => window.removeEventListener('popstate', onPopState)
  })

  // Simple route-guard
  $effect(() => {
    const route = app.route
    const authed = isAuthed

    if (!authed && appRoutes.PRIVATE_ROUTES.includes(route)) {
      navigate('/login', true)
      return
    }

    if (authed && route === '/login') {
      navigate('/products', true)
    }

    if (route === '/admin/users' && !isAdmin) {
      navigate('/products', true)
    }
  })
</script>

<div class="app-shell">
  <header class="app-header">
    <h1 class="brand">Portal Productos</h1>

    <NavBar
      route={app.route}
      isAuthed={isAuthed}
      {isAdmin}
      onNavigate={goTo}
      onLogout={logout}
    />
  </header>

  <main class="page">
    {#if app.globalError}
      <p class="error">{app.globalError}</p>
    {/if}

    {#if app.globalMessage}
      <p class="success">{app.globalMessage}</p>
    {/if}

    {#if app.route === '/login'}
      <LoginPage onLoggedIn={() => navigate('/products')} />
    {:else if app.route === '/products'}
      <ProductsPage />
    {:else if app.route === '/profile'}
      <ProfilePage displayName={displayName} onLogout={logout} />
    {:else if app.route === '/admin/users'}
      <AdminUsersPage />
    {:else}
      <p>Ruta no encontrada.</p>
    {/if}
  </main>
</div>

<style>
  .app-shell {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  .app-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 1rem 1.25rem;
    border-bottom: 1px solid #e5e7eb;
  }

  .brand {
    margin: 0;
    font-size: 1.1rem;
    font-weight: 700;
  }

  .page {
    flex: 1;
    padding: 1.25rem;
    max-width: 1000px;
    width: 100%;
    margin: 0 auto;
  }

  .error {
    background: #fee2e2;
    color: #991b1b;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    border: 1px solid #fecaca;
    margin: 0 0 1rem 0;
  }

  .success {
    background: #dcfce7;
    color: #166534;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    border: 1px solid #bbf7d0;
    margin: 0 0 1rem 0;
  }
</style>