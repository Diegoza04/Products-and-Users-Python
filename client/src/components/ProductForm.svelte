<script>
  let {
    product = null,
    saving = false,
    onSave,
    onCancel,
  } = $props()

  let title = $state('')
  let description = $state('')
  let price = $state('')
  let isActive = $state(true)
  let error = $state('')

  $effect(() => {
    const current = product
    title = current?.title || ''
    description = current?.description || ''
    price = String(current?.price ?? '')
    isActive = current?.isActive !== false
    error = ''
  })

  function submit() {
    if (!title.trim()) {
      error = 'El nombre es obligatorio.'
      return
    }

    const numericPrice = Number(price)
    if (Number.isNaN(numericPrice) || numericPrice <= 0) {
      error = 'El precio debe ser mayor a 0.'
      return
    }

    error = ''
    onSave({
      title: title.trim(),
      description: description.trim(),
      price: numericPrice,
      isActive,
    })
  }
</script>

<section class="panel stack">
  <h3>{product ? 'Editar producto' : 'Nuevo producto'}</h3>

  {#if error}
    <p class="error">{error}</p>
  {/if}

  <label>
    Nombre
    <input bind:value={title} maxlength="100" />
  </label>

  <label>
    Descripcion
    <textarea bind:value={description} rows="3" maxlength="300"></textarea>
  </label>

  <label>
    Precio
    <input bind:value={price} type="number" min="0" step="0.01" />
  </label>

  <label style="display:flex;gap:.6rem;align-items:center">
    <input bind:checked={isActive} type="checkbox" style="width:auto" />
    Activo
  </label>

  <div style="display:flex;gap:.5rem;flex-wrap:wrap">
    <button class="btn-primary" type="button" disabled={saving} onclick={submit}>
      {saving ? 'Guardando...' : 'Guardar'}
    </button>
    <button class="btn-subtle" type="button" disabled={saving} onclick={onCancel}>Cancelar</button>
  </div>
</section>
