document.addEventListener('DOMContentLoaded', function() {
    // Mejorar la apariencia de los campos de color
    const colorInputs = document.querySelectorAll('input[type="color"]');
    
    colorInputs.forEach(function(input) {
        // Crear contenedor
        const container = document.createElement('div');
        container.className = 'color-field';
        
        // Crear campo de texto para mostrar el valor hex
        const textInput = document.createElement('input');
        textInput.type = 'text';
        textInput.className = 'color-text';
        textInput.value = input.value;
        textInput.maxLength = 7;
        
        // Insertar antes del input original
        input.parentNode.insertBefore(container, input);
        container.appendChild(input);
        container.appendChild(textInput);
        
        // Sincronizar valores
        input.addEventListener('change', function() {
            textInput.value = input.value;
        });
        
        textInput.addEventListener('input', function() {
            if (/^#[0-9A-F]{6}$/i.test(textInput.value)) {
                input.value = textInput.value;
            }
        });
    });
});