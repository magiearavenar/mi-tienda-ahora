document.addEventListener('DOMContentLoaded', function () {

    // Ocultar "Actualmente" y "Modificar" del widget de imagen
    function limpiarWidgetImagen() {
        document.querySelectorAll('#imagenproducto_set-group td.field-imagen').forEach(td => {
            // Ocultar todo excepto el input file
            td.childNodes.forEach(node => {
                if (node.nodeType === 1 && node.tagName !== 'INPUT') {
                    node.style.display = 'none';
                }
                if (node.nodeType === 3) { // texto plano
                    node.textContent = '';
                }
            });
            // Ocultar p, a, span dentro del td
            td.querySelectorAll('p, a, span, br').forEach(el => {
                if (el.tagName !== 'INPUT') el.style.display = 'none';
            });
        });
    }

    limpiarWidgetImagen();

    // Cargar SortableJS y SweetAlert2
    loadScript('https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/Sortable.min.js', function () {
        initSortable();
    });
    loadScript('https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.js');
    loadCSS('https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css');

    function loadScript(src, cb) {
        const s = document.createElement('script');
        s.src = src;
        if (cb) s.onload = cb;
        document.head.appendChild(s);
    }

    function loadCSS(href) {
        const l = document.createElement('link');
        l.rel = 'stylesheet';
        l.href = href;
        document.head.appendChild(l);
    }

    function initSortable() {
        const tbody = document.querySelector('#imagenproducto_set-group tbody');
        if (!tbody) return;

        addDeleteButtons(tbody);
        styleRows(tbody);

        Sortable.create(tbody, {
            animation: 150,
            handle: '.drag-handle',
            ghostClass: 'sortable-ghost',
            onEnd: updateOrden
        });

        new MutationObserver(() => {
            addDeleteButtons(tbody);
            styleRows(tbody);
            limpiarWidgetImagen();
        }).observe(tbody, { childList: true });
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
            handle.style.cssText = 'cursor:grab;font-size:1.3rem;color:#d2a8dd;padding:0 10px;user-select:none;';
            td.insertBefore(handle, td.firstChild);
        });

        if (!document.getElementById('sortable-style')) {
            const style = document.createElement('style');
            style.id = 'sortable-style';
            style.textContent = `
                .sortable-ghost { opacity:0.4; background:#fff0f9 !important; }
                .drag-handle:active { cursor:grabbing; }
            `;
            document.head.appendChild(style);
        }
    }

    function addDeleteButtons(tbody) {
        tbody.querySelectorAll('tr.form-row, tr.dynamic-imagenproducto_set').forEach(row => {
            if (row.querySelector('.btn-eliminar-imagen')) return;

            // Buscar la celda de delete nativa
            const deleteCell = row.querySelector('td.delete');
            if (!deleteCell) return;

            const deleteCheckbox = deleteCell.querySelector('input[type="checkbox"]');
            if (!deleteCheckbox) return;

            // Crear botón bonito
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'btn-eliminar-imagen';
            btn.innerHTML = '🗑 Eliminar';

            btn.addEventListener('click', function () {
                // Obtener miniatura si existe
                const img = row.querySelector('img');
                const imgHtml = img
                    ? `<img src="${img.src}" style="width:80px;height:80px;object-fit:cover;border-radius:8px;margin:10px auto;display:block;">`
                    : '';

                Swal.fire({
                    title: '¿Eliminar imagen?',
                    html: `${imgHtml}<p style="color:#888;font-size:0.9rem;margin-top:8px;">Esta acción no se puede deshacer.</p>`,
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonText: 'Sí, eliminar',
                    cancelButtonText: 'Cancelar',
                    confirmButtonColor: '#ffc1ea',
                    cancelButtonColor: '#f0f0f0',
                    customClass: {
                        confirmButton: 'swal-confirm-magie',
                        cancelButton: 'swal-cancel-magie',
                        popup: 'swal-popup-magie'
                    }
                }).then(result => {
                    if (result.isConfirmed) {
                        deleteCheckbox.checked = true;
                        row.style.opacity = '0.4';
                        row.style.pointerEvents = 'none';

                        Swal.fire({
                            title: '¡Eliminada!',
                            text: 'La imagen será eliminada al guardar.',
                            icon: 'success',
                            timer: 1800,
                            showConfirmButton: false,
                            confirmButtonColor: '#ffc1ea',
                            customClass: { popup: 'swal-popup-magie' }
                        });
                    }
                });
            });

            deleteCell.innerHTML = '';
            deleteCell.appendChild(btn);
        });
    }

    function updateOrden() {
        const rows = document.querySelectorAll(
            '#imagenproducto_set-group tbody tr.form-row, #imagenproducto_set-group tbody tr.dynamic-imagenproducto_set'
        );
        let orden = 1;
        rows.forEach((row, index) => {
            if (row.style.opacity === '0.4') return; // ignorar eliminadas
            const ordenInput = row.querySelector('input[name$="-orden"]');
            if (ordenInput) ordenInput.value = orden++;

            const principalInput = row.querySelector('input[name$="-es_principal"]');
            if (principalInput) principalInput.checked = (index === 0);
        });
    }
});
