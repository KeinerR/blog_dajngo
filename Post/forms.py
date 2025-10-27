from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    upload = forms.FileField(
        required=False,
        label='Archivo adjunto',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
        })
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del post',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe el contenido aquí...',
                'rows': 5,
            }),
        }
        error_messages = {
            'title': {
                'required': 'Por favor ingresa un título para tu post.',
                'max_length': 'El título es demasiado largo.',
            },
            'content': {
                'required': 'No puedes dejar el contenido vacío.',
            },
        }
