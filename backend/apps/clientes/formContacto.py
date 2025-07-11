from re import A
from django import forms

class FormularioContacto(forms.Form):
    nombre = forms.CharField(label='name', 
                             max_length=40, 
                             widget=forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': '* Su Nombre',
                                'id': 'name'
                             }),
                             required=True)
    email = forms.EmailField(label='email', 
                             max_length=100, 
                             widget=forms.EmailInput(attrs={
                                'class': 'form-control',
                                'placeholder': '* Su Correo Electrónico',
                                'id': 'email' 
                             }),
                             required=True)
    mensaje = forms.CharField(label='message', 
                              widget=forms.Textarea(attrs={
                                'class': 'form-control',
                                'placeholder': '* Deje un mensaje aquí',
                                'id': 'message',
                                'style': 'height: 100px'
                              }), 
                              required=True)
    asunto = forms.CharField(label='subject', 
                             widget=forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': '* Asunto',
                                'id': 'subject'
                              }),
                             max_length=60)