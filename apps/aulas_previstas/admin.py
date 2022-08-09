from django.contrib import admin

from .models import AnoLetivo, Periodo, Feriado


class AnoLetivoAdmin(admin.ModelAdmin):
    """ Definições para entradas de Anos Letivos no Admin"""

    # prepopulated_fields = {'slug': ('name',), }

    list_display = ['name', 'slug', 'created', 'modified']
    search_fields = ['name', 'slug', 'created', 'modified']

    list_filter = ['name', 'slug', 'created', 'modified']


admin.site.register(AnoLetivo, AnoLetivoAdmin)


class PeriodoAdmin(admin.ModelAdmin):
    """ Criação da Tabela do Período no admin """

    list_display = [
        'name', 'get_ano_letivo', 'start_date1', 'start_date2', 'end_date1',
        'end_date2', 'end_date3', 'tipo', 'slug', 'created', 'modified'
    ]
    search_fields = [
        'name', 'start_date1', 'start_date2', 'end_date1', 'end_date2', 'end_date3',
        'tipo', 'slug', 'created', 'modified'
    ]
    list_filter = [
        'name', 'start_date1', 'start_date2', 'end_date1', 'end_date2', 'end_date3',
        'tipo', 'slug', 'created', 'modified'
    ]

    def get_ano_letivo(self, obj):
        """ get AnoLetivo object """
        if obj.ano_letivo:
            return obj.ano_letivo.name
        else:
            return None

    get_ano_letivo.short_description = 'Ano Letivo'


admin.site.register(Periodo, PeriodoAdmin)


class FeriadoAdmin(admin.ModelAdmin):
    """ Criação da Tabela do Feriado no admin """

    # form = FeriadoForm

    list_display = [
        'name', 'data', 'tipo', 'movel', 'concelho', 'distrito', 'get_ano_letivo', 'slug', 'created', 'modified'
    ]
    search_fields = [
        'name', 'data', 'tipo', 'movel', 'concelho', 'distrito',  'slug', 'created', 'modified'
    ]
    list_filter = [
        'name', 'data', 'tipo', 'movel', 'concelho', 'distrito', 'slug', 'created', 'modified'
    ]

    def get_ano_letivo(self, obj):
        """ get AnoLetivo object """
        if obj.ano_letivo:
            return obj.ano_letivo.name
        else:
            return None

    get_ano_letivo.short_description = 'Ano Letivo'

    # class Media:
    #    js = ("static/action_change.js",


admin.site.register(Feriado, FeriadoAdmin)
