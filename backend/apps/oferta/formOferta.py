from django import forms

class FormularioCotizacion(forms.Form):
    nom_person = forms.CharField(label='* Su Nombre',
                                 min_length=4, max_length=50,
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control',
                                     'style': 'height: 55px;',
                                     'id': 'nombrePersona'}),
                                 required=True)
    
    nom_emp = forms.CharField(label='* Empresa',
                              min_length=7, max_length=100,
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control',
                                  'style': 'height: 55px;',
                                  'id': 'nombreEmpresa'}),
                              required=True)
    
    correo = forms.EmailField(label='* Su Correo Electrónico',
                             min_length=12, max_length=100,
                             widget=forms.EmailField(attrs={
                                 'class': 'form-control',
                                 'placeholder': '* Su Correo Electrónico',
                                 'style': 'height: 55px;',
                                 'id': 'correoElectronico'}),
                             required=True)
    
    telefono = forms.CharField(label='* Su Telefono',
                               max_length=20,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'style': 'height: 55px;',
                                   'required': 'required',
                                   'type': 'number',
                                   'id': 'numTelefono'}),
                               required=True)
    
    region = forms.ModelChoiceField(label='* Región',
                                    queryset=Region.objects.all(),
                                    empty_label='* Región',
                                    widget=forms.Select(attrs={
                                        'class': 'form-selec border-0',
                                        'style': 'height: 55px;',
                                        'required': 'required',
                                        'id': 'id_region'    
                                    }),
                                    required=True)
    
    comuna = forms.ModelChoiceField(label='* Comuna',
                                    queryset=Comuna.objects.none(),
                                    empty_label='* Comuna',
                                    widget=forms.Select(attrs={
                                        'class': 'form-selec border-0',
                                        'style': 'height: 55px;',
                                        'id': 'id_comuna',
                                        'required': 'required'}),
                                    required=True)
    
    tipo_cliente = forms.ChoiceField(label='* Tipo de Cliente',
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
    
    distribuidora = forms.ModelChoiceField(label='* Distribuidora',
                                           queryset=Distribuidora.objects.all(),
                                           empty_label='* Distribuidora',
                                           widget=forms.Select(attrs={
                                                'class': 'form-select border-0',
                                                'style': 'height: 55px;',
                                                'required': 'required'})
                                           )
    
    direccion = forms.CharField(label='* Direccion Completa',
                                min_length=12, max_length=255,
                                widget=forms.Textarea(attrs={
                                    'class': 'form-control',
                                    'style': 'height: 55px;',
                                    'id': 'direcciones',
                                    'rows': 3}),
                                required=True)