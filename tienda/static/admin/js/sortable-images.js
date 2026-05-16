document.addEventListener('DOMContentLoaded', function () {

    // Cargar SortableJS dinámicamente
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/Sortable.min.js';
    script.onload = initSortable;
    document.head.appendChild(script);

    function initSortable() {
        const tbody = document.querySelector('#imagenproducto_set-group tbody');
        if (!tbody) return;

        // Estilizar filas para que se vean arrastrables
        styleRows(tbody);

        Sortable.create(tbody, {
            animation: 150,
            handle: '.drag-handle',
            ghostClass: 'sortable-ghost',
            onEnd: updateOrden
        });

        // Observar si se agregan nuevas filas (botón "Agregar otro")
        new MutationObserver(() => styleRows(tbody)).observe(tbody, { childList: true });
    }

    function styleRows(tbody) {
        tbody.querySelectorAll('tr.form-row, tr.dynamic-imagenproducto_set').forEach(row => {
            if (row.querySelector('.drag-handle')) return;
            const td = row.querySelector('td');
            if (!td) return;
            const handle = document.createElement('span');
            handle.className = 'drag-handle';
            handle.innerHTML = '&#9776;';
            handle.title = 'Arrastra para reordenar';
            handle.style.cssText = 'cursor:grab;font-size:1.2rem;color:#aaa;padding:0 8px;user-select:none;';
            td.insertBefore(handle, td.firstChild);
        });

        // Estilo ghost
        if (!document.getElementById('sortable-style')) {
            const style = document.createElement('style');
            style.id = 'sortable-style';
            style.textContent = `
                .sortable-ghost { opacity: 0.4; background: #fff0f9 !important; }
                .drag-handle:active { cursor: grabbing; }
                #imagenproducto_set-group tbody tr { transition: background 0.2s; }
            `;
            document.head.appendChild(style);
        }
    }

    function updateOrden() {
        const rows = document.querySelectorAll('#imagenproducto_set-group tbody tr.form-row, #imagenproducto_set-group tbody tr.dynamic-imagenproducto_set');
        rows.forEach((row, index) => {
            const ordenInput = row.querySelector('input[name$="-orden"]');
            if (ordenInput) ordenInput.value = index + 1;

            // La primera fila se marca como principal automáticamente
            const principalInput = row.querySelector('input[name$="-es_principal"]');
            if (principalInput) principalInput.checked = (index === 0);
        });
    }
});
