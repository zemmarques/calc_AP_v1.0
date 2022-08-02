from django.db import models
from django.core.validators import RegexValidator
from datetime import date

from apps.aulas_previstas.feriadosBackup import feriados, FeriadoBakup, get_dia_pascoa, \
    atualiza_feriados_pela_pascoa, atualiza_feriados_por_data


class AnoLetivo(models.Model):
    """ Um modelo para o ano letivo """

    # regex for name validation
    name_message = 'Formato "aaaa/aaaa". Exemplo: 2020/2021'
    name_regex = RegexValidator(
        regex=r'^\d{4}\/\d{4}$',
        message=name_message,
    )
    name = models.CharField(
        'Designação',
        validators=[name_regex],
        max_length=12,
        unique=False,
        blank=False,
        help_text='Insira um ano letivo com o formato "aaaa/aaaa". Exemplo: 2020/2021'
    )
    slug = models.SlugField(
        max_length=20,
        unique=True,
        blank=True,
        help_text="Deixar em branco para criar um slug automático e único.",
    )
    created = models.DateTimeField(
        'Criado em',
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        'Modificado em',
        auto_now=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ano Letivo'
        verbose_name_plural = 'Anos Letivos'
        ordering = ['created']

    def save(self, *args, **kwargs):
        """set automatic and unique slug from name."""

        is_new = not self.pk

        super(AnoLetivo, self).save(*args, **kwargs)

        if not self.slug:
            self.slug = self.name.replace("/", "-") + '_' + str(self.id)
            self.save()

        # Cálculo e definição de todos os feriados para este ano letivo

        # feriados é um dicionário com todos os objetos FeriadosBackup

        if is_new:
            # lista com os anos do ano letivo separados
            anos = self.name.split('/')

            # calcula e retorna o dia de Páscoa
            pascoa = get_dia_pascoa(int(anos[1]))
            feriados.update({
                "Páscoa": FeriadoBakup("Páscoa", pascoa, True, 'nacional', '-', '-')
                # Corpo de Deus ocorre 60 dias depois da páscoa
                # "Corpo de Deus": date(int(anos[1]), month, day) + datetime.timedelta(days=60)
            })

            # atualiza os feriados pelo dia de Páscoa
            atualiza_feriados_pela_pascoa("Corpo de Deus", pascoa, 60)
            atualiza_feriados_pela_pascoa("Loulé - Feriado Municipal de Loulé", pascoa, 39)
            atualiza_feriados_pela_pascoa("Monchique - Quinta-Feira da Ascenção", pascoa, 39)

            atualiza_feriados_por_data("Alcoutim - Feriado Municipal de Alcoutim", date(int(anos[0]), 9, 1), 2,
                                       "sexta-feira")

            # feriados é um dicionário com todos os objetos FeriadosBackup
            for f in feriados:
                if feriados[f].data.month > 7:
                    nova_data = date(int(anos[0]), feriados[f].data.month, feriados[f].data.day)
                else:
                    nova_data = date(int(anos[1]), feriados[f].data.month, feriados[f].data.day)

                if feriados[f].tipo == "nacional":
                    Feriado.objects.create(
                        ano_letivo=self,
                        name=feriados[f].nome,
                        data=nova_data,
                        tipo=feriados[f].tipo,
                        movel=feriados[f].movel,
                        concelho="pt",
                        distrito="pt",
                    )

                if feriados[f].tipo == "municipal":
                    Feriado.objects.create(
                        ano_letivo=self,
                        name=feriados[f].nome,
                        data=nova_data,
                        tipo=feriados[f].tipo,
                        movel=feriados[f].movel,
                        concelho=feriados[f].concelho,
                        distrito=feriados[f].distrito,
                    )


class Periodo(models.Model):
    """ Um modelo para os períodos do ano letivo """

    ano_letivo = models.ForeignKey(
        'aulas_previstas.AnoLetivo',
        verbose_name='Ano Letivo',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        'Designação',
        max_length=12,
        unique=False,
        blank=False,
    )
    TIPO_OPTIONS = (
        ("1p", "1º Período"),
        ("2p", "2º Período"),
        ("3p_pre", "3ºP - Pré-escolar e 1º ciclo"),
        ("3p_ciclo", "3ºP - 5º, 6º, 7º, 8º e 10º Anos"),
        ("3p_fim_ciclo", "3ºP - 9º, 11ª e 12º Anos"),
        ("natal", "Natal"),
        ("carnaval", "Carnaval"),
        ("pascoa", "Páscoa"),
        ("outro", "Outro"),
    )
    tipo = models.CharField(
        'Tipo',
        blank=False,
        null=False,
        choices=TIPO_OPTIONS,
        max_length=100,
    )
    periodo_letivo = models.BooleanField(
        default=True,
        verbose_name="Período letivo",
    )
    slug = models.SlugField(
        max_length=20,
        unique=True,
        blank=True,
        help_text="Deixar em branco para criar um slug automático e único.",
    )
    start_date1 = models.DateField(
        'Início 1',
        blank=False,
        null=False,
    )
    start_date2 = models.DateField(
        'Início 2',
        blank=True,
        null=True,
    )
    end_date = models.DateField(
        'Fim',
        blank=False,
        null=False,
    )
    created = models.DateTimeField(
        'Criado em',
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        'Modificado em',
        auto_now=True,
    )

    def __str__(self):
        return self.name + "_" + str(self.tipo) + "_" + str(self.ano_letivo)

    def save(self, *args, **kwargs):
        """set automatic and unique slug from name."""

        super(Periodo, self).save(*args, **kwargs)

        if not self.slug:
            self.slug = self.ano_letivo.name.replace("/", "-") + '_' + self.tipo
            self.save()

    class Meta:
        verbose_name = 'Período'
        verbose_name_plural = 'Períodos'
        ordering = ['created']

        """ Makes unique periodo.tipo for the current ano_letivo"""
        unique_together = ("ano_letivo", "tipo")


class Feriado(models.Model):
    """ Um modelo para os feriados """

    ano_letivo = models.ForeignKey(
        'aulas_previstas.AnoLetivo',
        verbose_name='Ano Letivo',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        'Designação',
        max_length=200,
        unique=False,
        blank=False,
    )
    data = models.DateField(
        'Data',
        blank=False,
        null=False,
    )
    concelho = models.CharField(
        'Concelho',
        blank=True,
        null=True,
        max_length=100,
    )
    distrito = models.CharField(
        'Distrito',
        blank=True,
        null=True,
        max_length=100,
    )
    movel = models.BooleanField(
        default=True,
        verbose_name="Data móvel",
    )
    FERIADO_OPTIONS = (
        ("nacional", "Nacional"),
        ("municipal", "Municipal"),
    )
    tipo = models.CharField(
        'Tipo',
        blank=False,
        null=False,
        choices=FERIADO_OPTIONS,
        max_length=100,
        default="nacional",
    )
    slug = models.SlugField(
        max_length=20,
        unique=True,
        blank=True,
        help_text="Deixar em branco para criar um slug automático e único.",
    )
    created = models.DateTimeField(
        'Criado em',
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        'Modificado em',
        auto_now=True,
    )

    def __str__(self):
        return self.concelho + " (" + str(self.data) + ")"

    class Meta:
        verbose_name = 'Feriado'
        verbose_name_plural = 'Feriados'
        ordering = ['data']

    def save(self, *args, **kwargs):
        """set automatic and unique slug from name."""

        super(Feriado, self).save(*args, **kwargs)

        if not self.slug:
            self.slug = self.name + '_' + str(self.concelho).replace(" ", "_") + '_' + \
                        self.ano_letivo.name.replace("/", "-")
            self.save()

            # para remover acentos do self.concelho
            # https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string

    # Links de Apoio:

    # feriados municipais
    # https://www.visitarportugal.pt/listas-ordenadas/feriados-municipais?concelho=4

    # datepicker ... introduzir datas utilizador
    # https://stackoverflow.com/questions/3367091/whats-the-cleanest-simplest-to-get-running-datepicker-in-django

    # para remover acentos do self.concelho na função def save - ainda não implementado, não sei se será necessário
    # https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string

    # contador de visitas da página
    # https://developer.mozilla.org/pt-BR/docs/Learn/Server-side/Django/Sessions
