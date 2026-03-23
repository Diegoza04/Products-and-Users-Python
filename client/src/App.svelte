<script>
  import NavBar from './components/NavBar.svelte'
  import LoginPage from './pages/LoginPage.svelte'
  import ProductsPage from './pages/ProductsPage.svelte'
  import ProfilePage from './pages/ProfilePage.svelte'
  import { app, appRoutes, navigate, clearAuth } from './state/appState.svelte.js'

  let displayName = $derived(app.user?.username || 'Invitado')
  let isAuthed = $derived(Boolean(app.user && app.token))

  function goTo(path) {
    navigate(path)
  }

  function logout() {
    clearAuth()
    navigate('/login', true)
  }

  $effect(() => {
    const onPopState = () => {
      navigate(window.location.pathname, true)
    }
    window.addEventListener('popstate', onPopState)
    return () => window.removeEventListener('popstate', onPopState)
  })

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
  })
</script>

<div class="app-shell">
  <header class="app-header">
    <h1 class="brand">Portal Productos</h1>
    <NavBar
      route={app.route}
      isAuthed={isAuthed}
      isAdmin={app.user?.role === 'admin'}
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
    {/if}
  </main>
  </div>