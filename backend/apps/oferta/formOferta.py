from django import forms
from .models import Comuna, Distribuidora, TipoCliente

class FormularioCotizacion(forms.Form):
    nom_person = forms.CharField(label='nombrePersona',
                                 min_length=4, max_length=50,
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control',
                                     'placeholder': '* Su Nombre',
                                     'style': 'height: 55px;',
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
    
    rut_emp = forms.CharField(label='rutEmpresa',
                              min_length=7, max_length=100,
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control',
                                  'placeholder': '* RUT',
                                  'style': 'height: 55px;',
                                  'id': 'rutEmpresa'}),
                              required=True)
    
    correo = forms.EmailField(label='correoElectronico',
                             min_length=12, max_length=100,
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control',
                                 'placeholder': '* Su Correo Electrónico',
                                 'style': 'height: 55px;',
                                 'type': 'email',
                                 'id': 'correoElectronico'}),
                             required=True)
    
    telefono = forms.CharField(label='numTelefono',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'style': 'height: 55px;',
                                   'placeholder': '* Su Telefono',
                                   'type': 'number',
                                   'id': 'numTelefono'}),
                               required=True)
    
    comuna = forms.ModelChoiceField(label='comunas',
                                    queryset=Comuna.objects.filter(id_region=7).order_by('nom_comuna'),
                                    empty_label='* Comuna',
                                    widget=forms.Select(attrs={
                                        'class': 'form-select border-0',
                                        'style': 'height: 55px;',
                                        'id': 'id_comuna',
                                        'required': 'required'}),
                                    required=True)
    
    tipo_cliente = forms.ModelChoiceField(label='tip_cliente',
                                     queryset=TipoCliente.objects.all(),
                                     empty_label="* Tipo de Cliente",
                                     widget=forms.Select(attrs={
                                        'class': 'form-select border-0',
                                        'style': 'height: 55px;',
                                        'aria-placeholder': 'Tipo Cliente',
                                        'required': 'required',
                                        'id': 'id_tip_cli'}),
                                     required=True)
    
    distribuidora = forms.ModelChoiceField(label='dx',
                                           queryset=Distribuidora.objects.filter(id_distrib=1).order_by('nombre_fantasia'),
                                           empty_label='Distribuidora',
                                           widget=forms.Select(attrs={
                                                'class': 'form-select border-0',
                                                'style': 'height: 55px;',
                                                'id': 'id_distrib'}),
                                            required=False)
    
    direccion = forms.CharField(label='direccion',
                                min_length=4, max_length=255,
                                widget=forms.Textarea(attrs={
                                    'class': 'form-control',
                                    'placeholder': '* Dirección Completa: (Calle 1234, mi comuna)',
                                    'style': 'height: 55px;',
                                    'id': 'direcciones',
                                    'rows': 3}),
                                required=True)

    archivo = forms.FileField(label="Documento (Factura / Boleta)",
                              widget=forms.FileInput(attrs={
                                'class': 'form-control',
                                'accept':'.pdf',
                                'id':'id_archivo'    
                              }),
                              required=True,
                              help_text="Suba su Factura o Boleta en formato PDF para autocompletar los datos")

    def clean(self):
        cleaned_data = super().clean()
        tipo_cliente = cleaned_data.get('tipo_cliente')
        distribuidora = cleaned_data.get('distribuidora')

        if tipo_cliente and tipo_cliente.nom_tip_cli.upper() == 'REGULADO' and not distribuidora:
            self.add_error('distribuidora', 'Debe seleccionar una distribuidora para clientes regulados.')

