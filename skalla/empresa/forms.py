from django import forms
from .models import Colaborador


class ColaboradorForm(forms.ModelForm):
    # telefone = forms.CharField(max_length=20, verbose_name="Telefone")
    # celular = models.CharField(max_length=20, verbose_name="Celular")
    # contato = models.CharField(max_length=20, verbose_name="Contato")
    # contatoFone = models.CharField(max_length=20, verbose_name="Telefone Contato")
    # dataAdmissao = models.DateField(verbose_name="Data Admissão")
    # PIS = models.CharField(max_length=20)
    # departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='depto_colaborador',
    #                                  verbose_name='Departamento')
    # limiteHorasMes = models.SmallIntegerField(validators=[MinValueValidator(1)],
    #                                           verbose_name="Máximo de horas de trabalho mensal")
    # limiteHorasSemana = models.SmallIntegerField

    # username = models.CharField()
    # first_name = models.CharField(_('first name'), max_length=30, blank=True)
    # last_name = models.CharField(_('last name'), max_length=150, blank=True)
    # email = models.EmailField(_('email address'), blank=True)
    # is_staff = models.BooleanField(  )
    # is_active = models.BooleanField()
    # date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    #password

    class Meta:
        model = Colaborador
        exclude = ['password']
        fields = ['username', 'first_name','last_name', 'email','dataNascimento','departamento','telefone','celular','contato',
                  'contatoFone','limiteHorasSemana','limiteHorasMes','PIS','dataAdmissao']


    # def save(self, commit=True):
    #     print("Tratar")
    #     super.save(self, commit)
