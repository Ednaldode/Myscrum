# Imports do Django
from django import forms
from django.utils.translation import gettext as _

# Imports do mesmo App
from .models import Entrega

# Import Biblioteca Python


class EntregaForms(forms.ModelForm):

    EMPREENDIMENTOS_CHOICES = (
        ('', _("Selecione")),
        ('Belvedere', _("Belvedere")),
        ('Duetto D Mariah', _("Duetto D' Mariah")),
        ('Grand Ville Residencial', _("Grand Ville Residencial")),
        ('Imagine', _("Imagine")),
        ('Le Jardin Residencial ', _("Le Jardin Residencial ")),
        ('Loft Ekko House', _("Loft Ekko House")),
        ('Montis Residence', _("Montis Residence")),
        ('Parque Árvores', _("Parque Árvores")),
        ('Parque Flores ', _("Parque Flores")),
        ('Parque Pássaros', _("Parque Pássaros")),
        ('Terceiro', _("Terceiro")),
        ('Reserva Vista Verde', _("Reserva Vista Verde")),
        ('Residencial Villa Helvétia', _("Residencial Villa Helvétia")),
        ('Villa Unitá Residencial', _("Villa Unitá Residencial")),
        ('Villagio D Amore', _("Villagio D Amore"))
    )

    id_entrega = forms.IntegerField(required=False)
    empreendimento = forms.ChoiceField(choices=EMPREENDIMENTOS_CHOICES)
    bloco = forms.CharField(label='Bloco', max_length=10, required=False, widget=forms.Textarea)
    apto = forms.IntegerField(required=False)
    data_entrega = forms.DateField(widget=forms.DateInput(attrs={'class': 'input--style-4 js-datepicker'}))
    data_assin = forms.DateField(widget=forms.DateInput(attrs={'class': 'input--style-4 js-datepicker'}))
    proprietario1 = forms.CharField(label='Proprietário 1', max_length=50, required=False, widget=forms.Textarea)
    proprietario2 = forms.CharField(label='Proprietário 2', max_length=50, required=False, widget=forms.Textarea)
    testemunha1 = forms.CharField(label='Testemunha 1', max_length=50, required=False, widget=forms.Textarea)
    testemunha2 = forms.CharField(label='Testemunha 2', max_length=50, required=False, widget=forms.Textarea)
    rg_proprietario1 = forms.CharField(label='RG Propriotário 1', max_length=20, required=False, widget=forms.Textarea)
    rg_proprietario2 = forms.CharField(label='RG Propriotário 2', max_length=20, required=False, widget=forms.Textarea)
    rg_testemunha1 = forms.CharField(label='RG Testemunha 1', max_length=20, required=False, widget=forms.Textarea)
    rg_testemunha2 = forms.CharField(label='RG Testemunha 2', max_length=20, required=False, widget=forms.Textarea)
    cpf_proprietario1 = forms.CharField(label='CPF Propriotário 1', max_length=15, required=False, widget=forms.Textarea)
    cpf_proprietario2 = forms.CharField(label='CPF Propriotário 2', max_length=15, required=False, widget=forms.Textarea)
    cpf_testemunha1 = forms.CharField(label='CPF Testemunha 1', max_length=15, required=False, widget=forms.Textarea)
    cpf_testemunha2 = forms.CharField(label='CPF Testemunha 2', max_length=15, required=False, widget=forms.Textarea)
    
    class Meta:
        model = Entrega
        fields = '__all__'