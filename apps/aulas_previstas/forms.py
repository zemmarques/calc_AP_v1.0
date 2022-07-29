from django.forms import ModelForm
from django import forms
from django.forms.models import ModelChoiceField

from apps.aulas_previstas.models import AnoLetivo, Periodo, Feriado


TEMPOS_LETIVOS = (
    (0, "Sem aula"),
    (1, "Um"),
    (2, "Dois"),
    (3, "Três"),
    (4, "Quatro"),
    (5, "Cinco"),
)

GRADE_OPTIONS = (
    ("3p_pre", "Pré-escolar e 1º ciclo"),
    ("3p_ciclo", "5º, 6º, 7º, 8º e 10º Anos"),
    ("3p_fim_ciclo", "9º, 11º e 12º Anos"),
)

DISCIPLINA_OPTION = (
    ("anual", "Disciplina anual"),
    ("semestral", "Disciplina semestral"),
)


class AnoLetivoForm(ModelForm):

    name = ModelChoiceField(
        queryset=AnoLetivo.objects.all(),
        required=True,
        help_text="Ano_letivo",
        empty_label="Ano Letivo"
    )
    grade = forms.ChoiceField(
        choices=GRADE_OPTIONS,
    )
    disciplina = forms.ChoiceField(
        choices=DISCIPLINA_OPTION,
        widget=forms.RadioSelect(),
        initial='anual'
    )
    inicio_ano = forms.DateField(
        label="Data de início do ano letivo",
    )
    fim_ano = forms.DateField(
        label="Data de fim do ano letivo",
    )
    fim_1s = forms.DateField(
        label="FIM do 1ºSemestre",
    )
    inicio_2s = forms.DateField(
        label="Início do 2ºSemestre",
    )
    feriado_movel = ModelChoiceField(
        queryset=Feriado.objects.filter(tipo="municipal"),
        required=True,
        help_text="Feriado Municipal",
    )
    segunda = forms.ChoiceField(
        choices=TEMPOS_LETIVOS,
    )
    terca = forms.ChoiceField(
        choices=TEMPOS_LETIVOS,
    )
    quarta = forms.ChoiceField(
        choices=TEMPOS_LETIVOS,
    )
    quinta = forms.ChoiceField(
        choices=TEMPOS_LETIVOS,
    )
    sexta = forms.ChoiceField(
        choices=TEMPOS_LETIVOS,
    )

    class Meta:
        model = AnoLetivo
        fields = [
            'name', 'grade', 'disciplina', 'inicio_ano', 'fim_ano', 'fim_1s', 'inicio_2s', 'feriado_movel', 'segunda',
            'terca', 'quarta', 'quinta', 'sexta',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['feriado_movel'].queryset = Feriado.objects.none()

# Links úteis:

# Implement Dynamic Select Options With Django
# https://samiddha99.medium.com/implement-dynamic-select-options-with-django-d04e791f0483

# segui este!! funcionou
# https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
