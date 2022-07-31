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
        required=False,
        initial="Campo automático",
    )
    fim_1s = forms.DateField(
        label="FIM do 1ºSemestre",
        required=True,

    )
    inicio_2s = forms.DateField(
        label="Início do 2ºSemestre",
        required=True,
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

        if 'name' in self.data:
            try:
                name_id = int(self.data.get('name'))
                self.fields['feriado_movel'].queryset = Feriado.objects.filter(
                    ano_letivo_id=name_id, tipo="municipal").order_by('concelho')

                # para apresentar a data final do ano letivo
                tipo = self.data.get('grade')
                p = Periodo.objects.get(ano_letivo=name_id, tipo=tipo)

                self.fields['fim_ano'].disabled = True
                self.fields['fim_ano'].initial = p.end_date

            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['feriado_movel'].queryset = self.instance.name.feriado_set.order_by('name')

# Links úteis:

# Implement Dynamic Select Options With Django
# https://samiddha99.medium.com/implement-dynamic-select-options-with-django-d04e791f0483

# segui este!! funcionou
# https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
