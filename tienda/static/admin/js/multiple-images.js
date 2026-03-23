// JavaScript para manejar los datos adicionales de las imágenes múltiples
document.addEventListener('DOMContentLoaded', function() {
    // Función para recopilar datos de las imágenes
    function collectImageData() {
        const imageItems = document.querySelectorAll('.image-item');
        const data = {};
        
        imageItems.forEach((item, index) => {
            const sku = item.querySelector('.sku-input')?.value || '';
            const precio = item.querySelector('.price-input')?.value || '';
            const orden = item.querySelector('.order-input')?.value || (index + 1);
            const esPrincipal = item.querySelector('.principal-checkbox')?.checked || false;
            
            data[index] = {
                sku: sku,
                precio: precio,
                orden: parseInt(orden),
                es_principal: esPrincipal
            };
        });
        
        return data;
    }
    
    // Función para actualizar el campo oculto con los datos
    function updateImageData() {
        const data = collectImageData();
        const hiddenField = document.querySelector('input[name="imagenes_data"]');
        if (hiddenField) {
            hiddenField.value = JSON.stringify(data);
        }
    }
    
    // Escuchar cambios en los campos de las imágenes
    document.addEventListener('input', function(e) {
        if (e.target.matches('.sku-input, .price-input, .order-input')) {
            updateImageData();
        }
    });
    
    document.addEventListener('change', function(e) {
        if (e.target.matches('.principal-checkbox')) {
            updateImageData();
        }
    });
    
    // Actualizar datos antes de enviar el formulario
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function() {
            updateImageData();
        });
    }
    
    // Observer para detectar cuando se agregan nuevas imágenes
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1 && node.classList.contains('image-item')) {
                        // Agregar event listeners a los nuevos campos
                        const inputs = node.querySelectorAll('.sku-input, .price-input, .order-input');
                        inputs.forEach(input => {
                            input.addEventListener('input', updateImageData);
                        });
                        
                        const checkbox = node.querySelector('.principal-checkbox');
                        if (checkbox) {
                            checkbox.addEventListener('change', updateImageData);
                        }
                        
                        updateImageData();
                    }
                });
            }
        });
    });
    
    // Observar cambios en las listas de imágenes
    const imageLists = document.querySelectorAll('.image-list');
    imageLists.forEach(list => {
        observer.observe(list, { childList: true });
    });
});