from django import forms
from .models import Comuna, Distribuidora, Region

class FormularioCotizacion(forms.Form):
    nom_person = forms.CharField(label='nombrePersona',
                                 min_length=4, max_length=50,
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control',
                                     'placeholder': '* Su Nombre',
                                     'id': 'nombrePersona'}),
                                 required=True)
    
    nom_emp = forms.CharField(label='nombreEmpresa',
                              min_length=7, max_length=100,
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control',
                                  'placeholder': '* Empresa',
                                  'style': 'height: 55px;',
                                  'id': 'nombreEmpresa'}),
                              required=True)
    
    correo = forms.EmailField(label='correoElectronico',
                             min_length=12, max_length=100,
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control',
                                 'placeholder': '* Su Correo Electrónico',
                                 'style': 'height: 55px;',
                                 'id': 'correoElectronico'}),
                             required=True)
    
    telefono = forms.IntegerField(label='numTelefono',
                               widget=forms.NumberInput(attrs={
                                   'class': 'form-control',
                                   'style': 'height: 55px;',
                                   'placeholder': '* Su Telefono',
                                   'type': 'number',
                                   'id': 'numTelefono'}),
                               required=True)
    
    region = forms.ModelChoiceField(label='regions',
                                    queryset=Region.objects.all(),
                                    empty_label='* Región',
                                    widget=forms.Select(attrs={
                                        'class': 'form-selec border-0',
                                        'style': 'height: 55px;',
                                        'required': 'required',
                                        'id': 'id_region'    
                                    }),
                                    required=True)
    
    comuna = forms.ModelChoiceField(label='comunas',
                                    queryset=Comuna.objects.none(),
                                    empty_label='* Comuna',
                                    widget=forms.Select(attrs={
                                        'class': 'form-selec border-0',
                                        'style': 'height: 55px;',
                                        'id': 'id_comuna',
                                        'required': 'required'}),
                                    required=True)
    
    tipo_cliente = forms.ChoiceField(label='tip_cliente',
                                     choices=[
                                         ('', '* Tipo de Cliente'),
                                         ('REGULADO', 'Regulado'),
                                         ('LIBRE', 'Libre')
                                     ],
                                     widget=forms.Select(attrs={
                                        'class': 'form-selec border-0',
                                        'style': 'height: 55px;',
                                        'aria-placeholder': 'Tipo Cliente',
                                        'required': 'required',
                                        'id': 'id_tip_cli'}),
                                     required=True)
    
    distribuidora = forms.ModelChoiceField(label='dx',
                                           queryset=Distribuidora.objects.all(),
                                           empty_label='* Distribuidora',
                                           widget=forms.Select(attrs={
                                                'class': 'form-select border-0',
                                                'style': 'height: 55px;',
                                                'required': 'required'})
                                           )
    
    direccion = forms.CharField(label='direccion',
                                min_length=12, max_length=255,
                                widget=forms.Textarea(attrs={
                                    'class': 'form-control',
                                    'placeholder': '* Dirección Completa',
                                    'style': 'height: 55px;',
                                    'id': 'direcciones',
                                    'rows': 3}),
                                required=True)