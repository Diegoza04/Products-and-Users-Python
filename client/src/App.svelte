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

  function clearGlobalError() {
    app.globalError = ''
  }

  function clearGlobalMessage() {
    app.globalMessage = ''
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

  $effect(() => {
    const err = app.globalError
    if (!err) return
    const timeoutId = window.setTimeout(() => {
      if (app.globalError === err) app.globalError = ''
    }, 4200)
    return () => window.clearTimeout(timeoutId)
  })

  $effect(() => {
    const msg = app.globalMessage
    if (!msg) return
    const timeoutId = window.setTimeout(() => {
      if (app.globalMessage === msg) app.globalMessage = ''
    }, 2600)
    return () => window.clearTimeout(timeoutId)
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

  <div class="toast-stack" aria-live="polite">
    {#if app.globalError}
      <div class="toast toast-error" role="alert">
        <span>{app.globalError}</span>
        <button type="button" class="toast-close" onclick={clearGlobalError}>x</button>
      </div>
    {/if}

    {#if app.globalMessage}
      <div class="toast toast-success" role="status">
        <span>{app.globalMessage}</span>
        <button type="button" class="toast-close" onclick={clearGlobalMessage}>x</button>
      </div>
    {/if}
  </div>

  <main class="page">
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

  .toast-stack {
    position: fixed;
    top: 1rem;
    right: 1rem;
    display: grid;
    gap: 0.5rem;
    z-index: 50;
    width: min(360px, calc(100vw - 2rem));
  }

  .toast {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 0.75rem 0.85rem;
    border-radius: 8px;
    border: 1px solid transparent;
    box-shadow: 0 10px 26px rgba(15, 23, 42, 0.18);
  }

  .toast-error {
    background: #fee2e2;
    color: #991b1b;
    border-color: #fecaca;
  }

  .toast-success {
    background: #dcfce7;
    color: #166534;
    border-color: #bbf7d0;
  }

  .toast-close {
    border: 0;
    background: transparent;
    color: inherit;
    cursor: pointer;
    padding: 0;
    min-width: 1rem;
    line-height: 1;
  }
</style>