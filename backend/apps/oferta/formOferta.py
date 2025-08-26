from django import forms
from .models import Comuna, Distribuidora, TipoCliente

class FormularioCotizacion(forms.Form):
    nom_person = forms.CharField(label='nombrePersona',
                                 min_length=4, max_length=50,
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control',
                                     'placeholder': 'ej: Esteban Canales',
                                     'id': 'nombrePersona'}),
                                 required=True)
    
    nom_emp = forms.CharField(label='nombreEmpresa',
                              min_length=7, max_length=100,
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control',
                                  'placeholder': 'Safira Energía Chile',
                                  'id': 'nombreEmpresa'}),
                              required=True)
    
    rut_emp = forms.CharField(label='rutEmpresa',
                              min_length=7, max_length=100,
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control',
                                  'placeholder': '11.111.111-1 (con puntos y guión)',
                                  'id': 'rutEmpresa'}),
                              required=True)
    
    correo = forms.EmailField(label='correoElectronico',
                             min_length=12, max_length=100,
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control',
                                 'placeholder': 'tucorreo@empresa.cl',
                                 'type': 'email',
                                 'id': 'correoElectronico'}),
                             required=True)
    
    telefono = forms.CharField(label='numTelefono',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': '9 333111222',
                                   'type': 'number',
                                   'id': 'numTelefono'}),
                               required=True)
    
    direccion = forms.CharField(label='direccion',
                                min_length=4, max_length=255,
                                widget=forms.Textarea(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'ej: Las Rosas 852',
                                    'id': 'direcciones',
                                    'rows': 3}),
                                required=True)
    
    consum_elect = forms.CharField(label='consumElect',
                                   widget=forms.TextInput(attrs={
                                       'class': 'form-control',
                                       'style': 'border-left: none;',
                                       'placeholder': 'Ingrese consumo (kWh)',
                                       'type': 'number',
                                       'id': 'consumoMensual'}),
                                   required=True)
    
    demanda_max = forms.CharField(label='demandaMax',
                                   widget=forms.TextInput(attrs={
                                       'class': 'form-control',
                                       'style': 'border-left: none;',
                                       'placeholder': 'Ingrese la demanda (kWh)',
                                       'type': 'number',
                                       'id': 'demandaMaxima'}),
                                   required=True)
    
    demanda_max_hp = forms.CharField(label='demandaMaxHp',
                                   widget=forms.TextInput(attrs={
                                       'class': 'form-control',
                                       'style': 'border-left: none;',
                                       'placeholder': 'Ingrese la demanda (kWh)',
                                       'type': 'number',
                                       'id': 'demandaMaximaHp'}),
                                   required=True)
    
    comuna = forms.ModelChoiceField(label='comunas',
                                    queryset=Comuna.objects.filter(id_region=7).order_by('nom_comuna'),
                                    empty_label='Seleccionar...',
                                    widget=forms.Select(attrs={
                                        'class': 'form-select',
                                        'style': 'border-left: none;',
                                        'id': 'id_comuna',
                                        'required': 'required'}),
                                    required=True)
    
    tipo_cliente = forms.ModelChoiceField(label='tip_cliente',
                                     queryset=TipoCliente.objects.all(),
                                     empty_label="Seleccionar...",
                                     widget=forms.Select(attrs={
                                        'class': 'form-select',
                                        'style': 'border-left: none;',
                                        'aria-placeholder': 'Tipo Cliente',
                                        'required': 'required',
                                        'id': 'id_tip_cli'}),
                                     required=True)
    
    distribuidora = forms.ModelChoiceField(label='dx',
                                           queryset=Distribuidora.objects.filter(id_distrib__in=[1,3]).order_by('nombre_fantasia'),
                                           empty_label='Seleccionar...',
                                           widget=forms.Select(attrs={
                                                'class': 'form-select',
                                                'style': 'border-left: none;',
                                                'id': 'id_distrib'}),
                                            required=False)

    archivo = forms.FileField(label="Documento (Factura / Boleta)",
                              widget=forms.FileInput(attrs={
                                'class': 'file-input',
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

