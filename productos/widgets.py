from django import forms

class ColorPickerWidget(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = '#000000'
        
        html = f'<input type="color" name="{name}" value="{value}" style="width: 50px; height: 40px; border: none; cursor: pointer;">'
        return html