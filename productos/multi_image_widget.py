from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings
import os

class MultipleImageWidget(forms.Widget):
    """Widget personalizado para subir múltiples imágenes con interfaz moderna"""
    
    def __init__(self, attrs=None):
        default_attrs = {'multiple': True, 'accept': 'image/*', 'type': 'file'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
    
    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}
        attrs.update(self.attrs)
        
        # Crear el input file con atributos (oculto)
        attrs_str = ' '.join([f'{k}="{v}"' for k, v in attrs.items()])
        html = f'<input name="{name}" {attrs_str} style="display: none;">'
        
        # Interfaz moderna con drag & drop y miniaturas
        extra_html = f'''
        <div class="modern-upload-container">
            <div class="upload-box" id="uploadBox-{name}">
                📷 Arrastra imágenes aquí o haz clic para seleccionar
                <br><small>Configura SKU, precios y orden para cada imagen</small>
            </div>
            <div class="image-list" id="imageList-{name}"></div>
        </div>
        
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const uploadBox = document.getElementById('uploadBox-{name}');
            const fileInput = document.querySelector('input[name="{name}"]');
            const imageList = document.getElementById('imageList-{name}');
            
            // Click para abrir selector
            uploadBox.addEventListener('click', () => fileInput.click());
            
            // Drag & Drop
            uploadBox.addEventListener('dragover', e => {{
                e.preventDefault();
                uploadBox.style.borderColor = '#4CAF50';
                uploadBox.style.backgroundColor = '#f0f8f0';
            }});
            
            uploadBox.addEventListener('dragleave', e => {{
                e.preventDefault();
                uploadBox.style.borderColor = '#ccc';
                uploadBox.style.backgroundColor = '#fff';
            }});
            
            uploadBox.addEventListener('drop', e => {{
                e.preventDefault();
                uploadBox.style.borderColor = '#ccc';
                uploadBox.style.backgroundColor = '#fff';
                handleFiles(e.dataTransfer.files);
            }});
            
            // Input change
            fileInput.addEventListener('change', () => {{
                handleFiles(fileInput.files);
            }});
            
            // Procesar archivos
            function handleFiles(files) {{
                [...files].forEach((file, index) => {{
                    if (!file.type.startsWith('image/')) return;
                    
                    const reader = new FileReader();
                    reader.onload = () => {{
                        createImageItem(reader.result, file.name, index);
                    }};
                    reader.readAsDataURL(file);
                }});
            }}
            
            // Crear item de imagen con miniatura y campos
            function createImageItem(src, fileName, index) {{
                const div = document.createElement('div');
                div.classList.add('image-item');
                div.dataset.index = index;
                
                div.innerHTML = `
                    <img src="${{src}}" alt="${{fileName}}">
                    <div class="image-info">
                        <div class="file-name">${{fileName}}</div>
                        <div class="image-fields">
                            <input type="text" placeholder="SKU (opcional)" class="sku-input" data-field="sku">
                            <input type="number" placeholder="Precio específico" class="price-input" step="0.01" data-field="precio">
                            <input type="number" placeholder="Orden" class="order-input" value="${{index + 1}}" data-field="orden">
                        </div>
                        <div class="image-options">
                            <label>
                                <input type="checkbox" class="principal-checkbox" data-field="es_principal"> 
                                Imagen principal
                            </label>
                        </div>
                        <div class="image-help">
                            <small>Si defines SKU o precio, se creará una opción de producto automáticamente</small>
                        </div>
                    </div>
                    <button type="button" class="delete-btn">✕</button>
                `;
                
                // Eliminar imagen
                div.querySelector('.delete-btn').addEventListener('click', () => {{
                    div.remove();
                    updateImageCount();
                    updateImageData();
                }});
                
                // Solo una imagen principal
                div.querySelector('.principal-checkbox').addEventListener('change', function() {{
                    if (this.checked) {{
                        // Desmarcar otras imágenes principales
                        document.querySelectorAll('.principal-checkbox').forEach(cb => {{
                            if (cb !== this) cb.checked = false;
                        }});
                    }}
                    updateImageData();
                }});
                
                // Actualizar datos cuando cambien los campos
                div.querySelectorAll('input').forEach(input => {{
                    input.addEventListener('input', updateImageData);
                    input.addEventListener('change', updateImageData);
                }});
                
                imageList.appendChild(div);
                updateImageCount();
                updateImageData();
            }}
            
            // Actualizar contador
            function updateImageCount() {{
                const count = imageList.children.length;
                
                if (count > 0) {{
                    uploadBox.innerHTML = `
                        📷 ${{count}} imagen(es) configurada(s)<br>
                        <small>Haz clic para agregar más imágenes</small>
                    `;
                }} else {{
                    uploadBox.innerHTML = `
                        📷 Arrastra imágenes aquí o haz clic para seleccionar<br>
                        <small>Configura SKU, precios y orden para cada imagen</small>
                    `;
                }}
            }}
            
            // Actualizar datos en campo oculto
            function updateImageData() {{
                const data = {{}};
                const items = imageList.querySelectorAll('.image-item');
                
                items.forEach((item, index) => {{
                    const sku = item.querySelector('.sku-input').value.trim();
                    const precio = item.querySelector('.price-input').value;
                    const orden = item.querySelector('.order-input').value;
                    const esPrincipal = item.querySelector('.principal-checkbox').checked;
                    
                    data[index] = {{
                        sku: sku,
                        precio: precio ? parseFloat(precio) : null,
                        orden: parseInt(orden) || (index + 1),
                        es_principal: esPrincipal
                    }};
                }});
                
                // Buscar el campo oculto imagenes_data
                const hiddenField = document.querySelector('input[name="imagenes_data"]');
                if (hiddenField) {{
                    hiddenField.value = JSON.stringify(data);
                }}
            }}
        }});
        </script>
        
        <style>
        .modern-upload-container {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        
        .upload-box {{
            width: 100%;
            min-height: 120px;
            border: 2px dashed #ccc;
            border-radius: 10px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            background: #fff;
            margin-bottom: 20px;
            transition: all 0.3s ease;
            text-align: center;
            padding: 20px;
        }}
        
        .upload-box:hover {{
            border-color: #4CAF50;
            background: #f9f9f9;
        }}
        
        .image-list {{
            display: flex;
            flex-direction: column;
            gap: 15px;
            max-height: 400px;
            overflow-y: auto;
        }}
        
        .image-item {{
            display: flex;
            align-items: center;
            gap: 15px;
            background: white;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #ddd;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        
        .image-item:hover {{
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}
        
        .image-item img {{
            width: 80px;
            height: 80px;
            object-fit: cover;
            border-radius: 8px;
            border: 1px solid #eee;
        }}
        
        .image-info {{
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        
        .file-name {{
            font-weight: 600;
            color: #333;
            font-size: 14px;
        }}
        
        .image-fields {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        .image-fields input {{
            padding: 6px 10px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 13px;
            min-width: 100px;
        }}
        
        .image-fields input:focus {{
            outline: none;
            border-color: #4CAF50;
            box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
        }}
        
        .image-options {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .image-options label {{
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 13px;
            color: #666;
            cursor: pointer;
        }}
        
        .image-help {{
            margin-top: 5px;
        }}
        
        .image-help small {{
            color: #888;
            font-style: italic;
        }}
        
        .delete-btn {{
            background: #ff4757;
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s ease;
        }}
        
        .delete-btn:hover {{
            background: #ff3742;
            transform: scale(1.05);
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .image-item {{
                flex-direction: column;
                text-align: center;
            }}
            
            .image-fields {{
                justify-content: center;
            }}
        }}
        </style>
        '''
        
        return mark_safe(html + extra_html)