from django import forms
from django.utils.safestring import mark_safe
from django.urls import reverse
import os

class DragDropImageWidget(forms.ClearableFileInput):
    """
    Widget personalizado para subida de imágenes con drag & drop y vista previa
    """
    template_name = 'admin/widgets/dragdrop_image.html'
    
    def __init__(self, attrs=None, multiple=False):
        default_attrs = {'class': 'dragdrop-image-input'}
        if multiple:
            default_attrs['multiple'] = True
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
        self.multiple = multiple
    
    def format_value(self, value):
        if hasattr(value, 'url'):
            return value.url
        return value
    
    def render(self, name, value, attrs=None, renderer=None):
        # Obtener la URL de la imagen actual si existe
        image_url = ''
        if value and hasattr(value, 'url'):
            image_url = value.url
        
        # Contenido de la imagen o texto de placeholder
        if image_url:
            image_content = f'<img src="{image_url}" class="preview-image" />'
            preview_gallery = f'<div class="current-image"><img src="{image_url}" class="gallery-thumb" /></div>'
        else:
            image_content = '''
                    <div class="upload-text">
                        <i class="fas fa-camera"></i><br>
                        Arrastra una imagen o haz clic aquí
                    </div>
                    '''
            preview_gallery = ''
        
        multiple_attr = 'multiple' if self.multiple else ''
        
        # HTML del widget personalizado
        html = f'''
        <div class="dragdrop-container">
            <div class="upload-box" id="uploadBox_{name}">
                <div class="upload-content" id="uploadContent_{name}">
                    {image_content}
                </div>
                <input type="file" 
                       name="{name}" 
                       id="id_{name}" 
                       accept="image/*" 
                       class="file-input" 
                       {multiple_attr}
                       style="display: none;">
            </div>
            
            <div class="preview-gallery" id="previewGallery_{name}">
                {preview_gallery}
            </div>
            
            {self._render_clear_checkbox(name, value) if value else ''}
        </div>
        
        <script>
        (function() {{
            const uploadBox = document.getElementById('uploadBox_{name}');
            const fileInput = document.getElementById('id_{name}');
            const uploadContent = document.getElementById('uploadContent_{name}');
            const previewGallery = document.getElementById('previewGallery_{name}');
            
            // Click para abrir selector
            uploadBox.addEventListener('click', () => {{
                fileInput.click();
            }});
            
            // Drag over
            uploadBox.addEventListener('dragover', (e) => {{
                e.preventDefault();
                uploadBox.classList.add('dragover');
            }});
            
            // Drag leave
            uploadBox.addEventListener('dragleave', () => {{
                uploadBox.classList.remove('dragover');
            }});
            
            // Drop
            uploadBox.addEventListener('drop', (e) => {{
                e.preventDefault();
                uploadBox.classList.remove('dragover');
                const files = e.dataTransfer.files;
                if (files.length > 0) {{
                    fileInput.files = files;
                    handleFiles(files);
                }}
            }});
            
            // File input change
            fileInput.addEventListener('change', () => {{
                const files = fileInput.files;
                if (files.length > 0) {{
                    handleFiles(files);
                }}
            }});
            
            // Manejar múltiples archivos
            function handleFiles(files) {{
                // Limpiar galería previa si es imagen única
                if (!fileInput.hasAttribute('multiple')) {{
                    previewGallery.innerHTML = '';
                }}
                
                [...files].forEach(file => {{
                    if (!file.type.startsWith('image/')) return;
                    
                    const reader = new FileReader();
                    reader.onload = () => {{
                        // Actualizar contenido principal
                        if (!fileInput.hasAttribute('multiple')) {{
                            uploadContent.innerHTML = `<img src="${{reader.result}}" class="preview-image" />`;
                        }}
                        
                        // Agregar a galería
                        const img = document.createElement('img');
                        img.src = reader.result;
                        img.className = 'gallery-thumb';
                        img.onclick = () => {{
                            uploadContent.innerHTML = `<img src="${{reader.result}}" class="preview-image" />`;
                        }};
                        previewGallery.appendChild(img);
                    }};
                    reader.readAsDataURL(file);
                }});
            }}
        }})();
        </script>
        '''
        
        return mark_safe(html)
    
    def _render_clear_checkbox(self, name, value):
        """Renderizar checkbox para limpiar imagen existente"""
        return f'''
        <div class="clear-image">
            <label>
                <input type="checkbox" name="{name}-clear" id="{name}-clear_id">
                Eliminar imagen actual
            </label>
        </div>
        '''
    
    class Media:
        css = {
            'all': ('admin/css/dragdrop-image.css',)
        }
        js = ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/js/all.min.js',)


class MultipleImageWidget(DragDropImageWidget):
    """
    Widget específico para múltiples imágenes
    """
    def __init__(self, attrs=None):
        super().__init__(attrs, multiple=True)