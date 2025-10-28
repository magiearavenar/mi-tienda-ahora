from django import forms
from django.utils.safestring import mark_safe

class ColorPickerWidget(forms.TextInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({
            'class': 'color-input',
            'style': 'width: 100px; padding: 5px; border: 1px solid #ddd; border-radius: 4px;',
            'placeholder': '#ffffff'
        })
    
    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = '#ffffff'
        
        # Input de texto para el código hex
        text_input = super().render(name, value, attrs, renderer)
        
        # Color picker nativo
        color_attrs = {
            'type': 'color',
            'id': f'{name}_picker',
            'style': 'width: 40px; height: 40px; border: none; cursor: pointer; border-radius: 4px; margin-left: 10px;',
            'value': value
        }
        color_input = f'<input{self._format_attrs(color_attrs)} />'
        
        # Preview del color
        preview = f'<div id="{name}_preview" style="width: 30px; height: 30px; background-color: {value}; border: 1px solid #ddd; border-radius: 4px; margin-left: 10px; display: inline-block;"></div>'
        
        # JavaScript para sincronizar
        script = f'''
        <script>
        (function() {{
            const textInput = document.querySelector('input[name="{name}"]');
            const colorPicker = document.getElementById('{name}_picker');
            const preview = document.getElementById('{name}_preview');
            
            function updateColor(color) {{
                if (color.match(/^#[0-9A-F]{{6}}$/i)) {{
                    colorPicker.value = color;
                    preview.style.backgroundColor = color;
                }}
            }}
            
            textInput.addEventListener('input', function() {{
                updateColor(this.value);
            }});
            
            colorPicker.addEventListener('input', function() {{
                textInput.value = this.value;
                preview.style.backgroundColor = this.value;
            }});
        }})();
        </script>
        '''
        
        return mark_safe(f'<div style="display: flex; align-items: center;">{text_input}{color_input}{preview}</div>{script}')
    
    def _format_attrs(self, attrs):
        return ''.join(f' {key}="{value}"' for key, value in attrs.items())