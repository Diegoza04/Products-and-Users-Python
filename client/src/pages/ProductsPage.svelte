<script>
  import ProductCard from '../components/ProductCard.svelte'
  import ProductForm from '../components/ProductForm.svelte'
  import {
    createProduct,
    deleteProduct,
    getProducts,
    updateProduct,
  } from '../services/api.js'
  import { app } from '../state/appState.svelte.js'

  let search = $state('')
  let onlyActive = $state(false)
  let showForm = $state(false)
  let editingProduct = $state(null)
  let detailProduct = $state(null)
  let formSaving = $state(false)
  let localError = $state('')

  let canManage = $derived(app.user?.role === 'admin')

  let filteredProducts = $derived.by(() => {
    const term = search.trim().toLowerCase()

    return app.products.filter((product) => {
      const active = product.isActive !== false
      const matchesState = onlyActive ? active : true
      const matchesTerm = term
        ? (product.title || '').toLowerCase().includes(term)
        : true

      return matchesState && matchesTerm
    })
  })

  let productCount = $derived(filteredProducts.length)

  async function refreshProducts() {
    app.productsLoading = true
    localError = ''
    app.globalError = ''

    try {
      const products = await getProducts()
      app.products = products
    } catch (requestError) {
      localError = requestError.message || 'No se pudo cargar productos.'
    } finally {
      app.productsLoading = false
    }
  }

  $effect(() => {
    const role = app.user?.role
    if (!role) return

    // En esta entrega se recarga cuando cambia rol o filtro principal.
    const activeFilter = onlyActive
    void activeFilter

    void refreshProducts()
  })

  function openCreate() {
    if (!canManage) return
    editingProduct = null
    showForm = true
  }

  function openEdit(product) {
    editingProduct = product
    showForm = true
  }

  async function handleSave(payload) {
    formSaving = true
    localError = ''
    app.globalError = ''

    try {
      if (editingProduct?._id) {
        await updateProduct(editingProduct._id, payload)
        app.globalMessage = 'Producto actualizado.'
      } else {
        await createProduct(payload)
        app.globalMessage = 'Producto creado.'
      }

      showForm = false
      editingProduct = null
      await refreshProducts()
    } catch (requestError) {
      localError = requestError.message || 'No se pudo guardar el producto.'
    } finally {
      formSaving = false
    }
  }

  async function handleDelete(productId) {
    const confirmed = window.confirm('Esta accion eliminara el producto. Deseas continuar?')
    if (!confirmed) return

    localError = ''
    app.globalError = ''

    try {
      await deleteProduct(productId)
      app.globalMessage = 'Producto eliminado.'
      await refreshProducts()
    } catch (requestError) {
      localError = requestError.message || 'No se pudo eliminar el producto.'
    }
  }
</script>

<section class="stack">
  <div class="panel stack">
    <div style="display:flex;justify-content:space-between;align-items:center;gap:.5rem;flex-wrap:wrap">
      <h2 style="margin:0">Productos ({productCount})</h2>
      <div style="display:flex;gap:.5rem;flex-wrap:wrap">
        <button class="btn-subtle" type="button" onclick={refreshProducts} disabled={app.productsLoading}>
          {app.productsLoading ? 'Cargando...' : 'Recargar'}
        </button>
        {#if canManage}
          <button class="btn-primary" type="button" onclick={openCreate}>Nuevo producto</button>
        {/if}
      </div>
    </div>

    <div style="display:grid;grid-template-columns:2fr 1fr;gap:.5rem">
      <input bind:value={search} placeholder="Buscar por nombre" />
      <label style="display:flex;align-items:center;gap:.5rem;padding:.3rem .2rem">
        <input style="width:auto" type="checkbox" bind:checked={onlyActive} />
        Solo activos
      </label>
    </div>

    {#if localError}
      <p class="error">{localError}</p>
    {/if}
  </div>

  {#if showForm}
    <ProductForm
      product={editingProduct}
      saving={formSaving}
      onSave={handleSave}
      onCancel={() => {
        showForm = false
        editingProduct = null
      }}
    />
  {/if}

  <div class="grid-products">
    {#if filteredProducts.length === 0 && !app.productsLoading}
      <div class="panel">
        <p>No hay productos para mostrar.</p>
      </div>
    {/if}

    {#each filteredProducts as product (product._id)}
      <ProductCard
        {product}
        {canManage}
        onView={(item) => (detailProduct = item)}
        onEdit={openEdit}
        onDelete={handleDelete}
      />
    {/each}
  </div>
</section>

{#if detailProduct}
  <div class="modal-backdrop" role="dialog" aria-modal="true">
    <section class="modal panel stack">
      <h3 style="margin:0">{detailProduct.title}</h3>
      <p class="muted">${Number(detailProduct.price || 0).toFixed(2)}</p>
      <p>{detailProduct.description || 'Sin descripcion'}</p>
      <span class="tag">Estado: {detailProduct.isActive === false ? 'No activo' : 'Activo'}</span>

      <button class="btn-subtle" type="button" onclick={() => (detailProduct = null)}>Cerrar</button>
    </section>
  </div>
{/if}