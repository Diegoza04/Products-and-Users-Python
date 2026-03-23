<script>
  let {
    product,
    canManage = false,
    onView,
    onEdit,
    onDelete,
  } = $props()

  let statusText = $derived(product?.isActive === false ? 'No activo' : 'Activo')
</script>

<article class="product-card">
  <div class="stack">
    <h3>{product.title}</h3>
    <p class="muted">${Number(product.price || 0).toFixed(2)}</p>
    <span class="tag">Estado: {statusText}</span>

    <div style="display:flex;gap:.4rem;flex-wrap:wrap">
      <button type="button" class="btn-subtle" onclick={() => onView(product)}>Detalle</button>
      {#if canManage}
        <button type="button" class="btn-subtle" onclick={() => onEdit(product)}>Editar</button>
        <button type="button" class="btn-primary" onclick={() => onDelete(product._id)}>Borrar</button>
      {/if}
    </div>
  </div>
</article>