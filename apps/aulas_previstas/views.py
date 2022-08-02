from django.shortcuts import render, get_object_or_404
import datetime
from datetime import timedelta
from django.contrib import messages

from apps.aulas_previstas.models import AnoLetivo, Periodo, Feriado
from apps.aulas_previstas.forms import AnoLetivoForm
from apps.aulas_previstas.tabela_aulas_previstas import *


def daterange(start_date, end_date):
    """ Função geradora e iteradora de dias entre
    a start_date e a end_date """

    for n in range(int((end_date + datetime.timedelta(days=1) - start_date).days)):
        yield start_date + timedelta(n)


def imprime_dias(msg, dicionario):
    """ Função para imprimir os dias de um dicionário """

    print(msg)
    for i in dicionario:
        print("\n    ª {0} -> {1} dias".format(i, len(dicionario[i])))

        # para debug — imprime todos os dias
        # for d in dicionario[k]:
        #    print("      ", d)

    print()


def load_feriados(request):
    try:
        name_id = request.GET.get('ano_letivo')
        print(request)
        feriados = Feriado.objects.filter(ano_letivo_id=name_id, tipo="municipal").order_by('concelho')
        print(feriados)
    except (ValueError, Feriado.DoesNotExist):
        feriados = Feriado.objects.none()

    return render(
        request,
        'aulas_previstas/feriado_dropdown_list_options.html',
        {'feriados': feriados}
    )


def load_fim_ano(request):
    try:
        name_id = request.GET.get('ano_letivo')
        grade = request.GET.get('grade')
        periodo = Periodo.objects.get(ano_letivo_id=name_id, tipo=grade)
        p_data = periodo.end_date.__format__("%d/%m/%Y")
        print(p_data)
    except (ValueError, Periodo.DoesNotExist):
        p_data = 'Campo automático'

    return render(
        request,
        'aulas_previstas/data_fim_ano.html',
        {'fim_ano': p_data}
    )


def load_inicio_ano(request):
    try:
        name_id = request.GET.get('ano_letivo')
        periodo = Periodo.objects.get(ano_letivo_id=name_id, tipo="1p")
        start_date1 = periodo.start_date1
        print(start_date1)
        start_date2 = periodo.start_date2
        print(start_date2)
    except (ValueError, Periodo.DoesNotExist):
        start_date1 = None
        start_date2 = None

    return render(
        request,
        'aulas_previstas/data_inicio_ano.html',
        {
            'inicio_ano_1': start_date1,
            'inicio_ano_2': start_date2,
         }
    )


def calculo_previstas(request, data, ):
    """ Calcula as aulas previstas para um ano letivo """

    # Define o ano letivo
    ano_letivo = AnoLetivo.objects.get(
        name=data['name'],
    )

    # Data de início do ano letivo definida pelo
    # utilizador no formulário
    user_inicio_al = data['inicio_ano']

    # Seleciona, a partir do formulário, a carga semanal da disciplina.
    # Dicionário "carga_semanal" no formato (dia da semana: nºtempos)
    carga_semanal = {}
    for key in data:
        if key == 'segunda' and int(data[key]) != 0:
            carga_semanal.update({0: int(data[key])})
        elif key == 'terca' and int(data[key]) != 0:
            carga_semanal.update({1: int(data[key])})
        elif key == 'quarta' and int(data[key]) != 0:
            carga_semanal.update({2: int(data[key])})
        elif key == 'quinta' and int(data[key]) != 0:
            carga_semanal.update({3: int(data[key])})
        elif key == 'sexta' and int(data[key]) != 0:
            carga_semanal.update({4: int(data[key])})
    print(" - Carga semanal (dia da semana: nºtempos):", carga_semanal)
    if len(carga_semanal) == 0:
        print('     # Erro_1 - Não foram selecionados tempos letivos por dia da semana.')

    # Retorna uma lista com os objetos periodos (1P, 2P e 3P) ou (sem1 e sem2),
    # conforme os dados do formulário - data['grade']
    print(" - disciplina:", data['disciplina'])
    lista_periodos = []
    if data["disciplina"] == 'anual':
        periodo_1 = get_object_or_404(Periodo, ano_letivo=ano_letivo.id, tipo='1p')
        periodo_2 = get_object_or_404(Periodo, ano_letivo=ano_letivo.id, tipo='2p')
        periodo_3 = get_object_or_404(Periodo, ano_letivo=ano_letivo.id, tipo=data['grade'])
        lista_periodos.extend((periodo_1, periodo_2, periodo_3))
        print(" - Periodos selecionados:", lista_periodos)
    if data["disciplina"] == 'semestral':
        semestre_1 = get_object_or_404(Periodo, ano_letivo=ano_letivo.id, tipo='1sem')
        semestre_2 = get_object_or_404(Periodo, ano_letivo=ano_letivo.id, tipo='2sem')
        lista_periodos.extend((semestre_1, semestre_2))
        print(" - Semestres selecionados:", lista_periodos)

    # Recolhe as datas dos feriados nacionais e do feriado municipal
    lista_data_feriados = []
    try:
        # QuerySet com todos os feriados nacionais do ano_letivo
        feriados_nacionais = Feriado.objects.filter(ano_letivo=ano_letivo.id, tipo='nacional')
        # coloca as datas dos feriados nacionais numa lista e ordena a lista
        for f in feriados_nacionais:
            lista_data_feriados.append(f.data)
        lista_data_feriados.sort()
        print(" - Feriados nacionais:", lista_data_feriados)

        # recolhe a data do feriado municipal introduzido pelo
        # user no form e adiciona à lista_data_feriados.
        feriado_municipal = Feriado.objects.get(
            ano_letivo=ano_letivo.id,
            data=data['feriado_movel'].data,
            concelho=data['feriado_movel'].concelho,
        )
        data_feriado_municipal = feriado_municipal.data
        print(" - Feriado municipal:", feriado_municipal)
        lista_data_feriados.append(data_feriado_municipal)

    except():
        print('     # Erro_2 - Não foram definidos feriados para o ano letivo:', ano_letivo)

    # Retorna lista com as datas do Carnaval
    lista_dias_carnaval = []
    try:
        carnaval = Periodo.objects.filter(ano_letivo=ano_letivo.id, tipo="carnaval")
        for c in carnaval:
            for single_date in daterange(c.start_date1, c.end_date):
                lista_dias_carnaval.append(single_date)
        print(" - Dias de Carnaval:", lista_dias_carnaval)
    except():
        print('     # Erro_3 - Não foram definidas as datas do Carnaval:', ano_letivo)

    # Calcula os dias de aulas segundo o formulário inserido pelo utilizador.
    # — dicionário_dias_uteis no formato -> {Periodo: [lista de dias_úteis]}
    # — dicionário_dias_aula no formato -> {Periodo: [lista_de dias_aula]}
    dicionario_dias_uteis = {}
    dicionario_dias_aula = {}
    for p in lista_periodos:
        lista_dias_uteis = []
        lista_dias_aula = []

        # permite utilizar a data de inicio do 1periodo definida pelo user.
        if p.tipo == '1p' and user_inicio_al:
            start_date1 = user_inicio_al
        else:
            start_date1 = p.start_date1
        end_date = p.end_date

        for single_date in daterange(start_date1, end_date):
            # percorre todos os dias do período

            if single_date not in lista_data_feriados and single_date not in lista_dias_carnaval and \
                    single_date.weekday() != 5 and single_date.weekday() != 6:
                # O dia não é feriado, não é carnaval, não é sábado (5) nem domingo (6).
                # Então é dia útil
                lista_dias_uteis.append(single_date)

                if len(carga_semanal) != 0:
                    for da in carga_semanal:
                        if single_date.weekday() == da:
                            lista_dias_aula.append(single_date)
        dicionario_dias_aula.update({p: lista_dias_aula})
        dicionario_dias_uteis.update({p: lista_dias_uteis})

    # imprime os dias úteis do ano letivo, se dicionário não vazio.
    if len(dicionario_dias_uteis) != 0:
        imprime_dias(" - Dias úteis por período:", dicionario_dias_uteis)

    # imprime os dias de aula do ano letivo, se dicionário não vazio.
    if len(dicionario_dias_aula) != 0:
        imprime_dias(" - Dias de aula por período:", dicionario_dias_aula)

    dicionario_tabela_ap = {}
    lista = []
    calendario = [
        '2ªFeira', '3ªFeira', '4ªFeira', '5ªFeira', '6ªFeira'
    ]
    for key in carga_semanal:
        for p in dicionario_dias_aula:
            lista.append(p)
        linha_tabela_ap = TabelaAulasPrevistasPeriodos(
            key,
            carga_semanal[key],
            dicionario_dias_aula[lista[0]],
            dicionario_dias_aula[lista[1]],
            dicionario_dias_aula[lista[2]],
        )
        dicionario_tabela_ap.update({calendario[key]: linha_tabela_ap})

    soma_aulas_1p = 0
    soma_aulas_2p = 0
    soma_aulas_3p = 0
    soma_aulas_total = 0
    soma_previstas_1p = 0
    soma_previstas_2p = 0
    soma_previstas_3p = 0
    soma_previstas_total = 0
    for key, obj in dicionario_tabela_ap.items():
        soma_aulas_1p = soma_aulas_1p + obj.conta_weekdays_1p()
        soma_aulas_2p = soma_aulas_2p + obj.conta_weekdays_2p()
        soma_aulas_3p = soma_aulas_3p + obj.conta_weekdays_3p()
        soma_aulas_total = soma_aulas_total + obj.total_weekdays()
        soma_previstas_1p = soma_previstas_1p + obj.aulas_previstas_1p()
        soma_previstas_2p = soma_previstas_2p + obj.aulas_previstas_2p()
        soma_previstas_3p = soma_previstas_3p + obj.aulas_previstas_3p()
        soma_previstas_total = soma_previstas_total + obj.total_previstas()

    totais_dicionario_tabela_ap = {
        'soma_aulas_1p': soma_aulas_1p,
        'soma_aulas_2p': soma_aulas_2p,
        'soma_aulas_3p': soma_aulas_3p,
        'soma_aulas_total': soma_aulas_total,
        'soma_previstas_1p': soma_previstas_1p,
        'soma_previstas_2p': soma_previstas_2p,
        'soma_previstas_3p': soma_previstas_3p,
        'soma_previstas_total': soma_previstas_total,
    }

    context = {
        'ano_letivo': ano_letivo,  # objeto ano letivo
        'disciplina': data['disciplina'],   # tipo disciplina anual/semestral
        'escolaridade': data['grade'],  # tipo escolaridade (1p, 2p, 3p_pre ...) !!!! todo enviar o objeto Período
        'lista_periodos': lista_periodos,  # lista de objetos periodos (períodos ou semestres)
        'lista_feriados': lista_data_feriados,  # lista de datas
        'lista_carnaval': lista_dias_carnaval,  # lista de datas
        'dias_de_aulas': carga_semanal,  # dicionário com a carga semanal (dia semana: tempos)
        'dicionario_dias_uteis': dicionario_dias_uteis,  # dicionário (periodo: lista de dias uteis)
        'dicionario_dias_aula': dicionario_dias_aula,  # dicionário (periodo: lista de dias de aula)
        'dicionario_tabela_ap': dicionario_tabela_ap,
        'totais_dicionario_tabela_ap': totais_dicionario_tabela_ap,     # dicionário de inteiros
    }

    return context


def homepage(request):
    """ Apresenta a página inicial da Calculadora de Aulas Previstas """

    if request.method == "POST":
        form = AnoLetivoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(type(data))
            print(" \n  *** Calculadora de aulas pervistas *** \n")
            print(" - Dados do Formulário:", data)
            context = calculo_previstas(request, data)
            # request.session['data'] = data
            messages.success(request, " @:P Boa!")
            template_name = 'aulas_previstas/results.html'
            return render(request, template_name, context)
        else:
            if form.errors:
                messages.error(request, "Falha na inserção de dados! Verifique os campos do formulário.")
            template_name = "aulas_previstas/homepage.html"
            context = {"form": form}
            return render(request, template_name, context)

    form = AnoLetivoForm
    message = 'Calc @:P'
    template_name = 'aulas_previstas/homepage.html'
    return render(request, template_name, context={"form": form, 'msn': message})


def show_results(request):
    """ Apresenta os resultados do calculo de aulas previstas efetuado """

    template_name = 'aulas_previstas/results.html'
    print("oi")
    # data = request.session.get("data")
    # print(data)
    context = {
        'msn': 'Olá Mundo',
    }

    return render(request, template_name, context)

# TODO validar as datas do formulário ... data de inicio maior que fim etc... etc...
# __FEITO__ todo validar carga semanal... pensar como fazer
# __FEITO__ todo colocar datapicker nos campos data ( início de ano letivo, fim 1S e Inicio 2S )
# __FEITO__ todo corrigir os cálculo de previstas... ver TODOs acima neste ficheiro
# Todo colocar os dados do formulário num cartão nos results
# todo verificar cálculo quando disciplina semestral
# todo homepage.html colocar info nos cartões de ajuda, ao lado do form
# todo results.html preencher outros cartões
