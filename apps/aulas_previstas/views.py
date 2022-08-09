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


def funcao_lista_dias_delta_t(epoca):
    """ Função que recebe o objeto deltaT (objeto do tipo periodo -> Natal, semestre, periodo , Páscoa, Carnaval)
    e retorna a lista de dias desse intervalo de tempo"""

    # define o tipo de data final do período escolhido, end_date 1, 2 ou 3
    if epoca.tipo == '3p_meio_ciclo':
        end_date = epoca.end_date2
    elif epoca.tipo == '3p_pre':
        end_date = epoca.end_date3
    else:
        end_date = epoca.end_date1

    lista_dias = []
    for single_date in daterange(epoca.start_date1, end_date):
        lista_dias.append(single_date)
    return lista_dias


def imprime_dias(msg, dicionario):
    """ Função para imprimir os dias de um dicionário """

    print(msg)
    for i in dicionario:
        print("\n    ª {0} -> {1} dias".format(i, len(dicionario[i])))

        # para debug — imprime todos os dias
        # for d in dicionario[i]:
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

    # Seleciona o objeto ano letivo na base de dados
    # a partir do ano letivo inserido pelo user no formulário
    ano_letivo = AnoLetivo.objects.get(
        name=data['name'],
    )

    # seleciona o verbose_name a partir do campo grade do formulário
    grade = data['grade']
    escolaridade = ''
    if grade == '3p_pre':
        escolaridade = "Pré-escolar e 1º ciclo"
    elif grade == '3p_ciclo':
        escolaridade = "5º, 6º, 7º, 8º e 10º Anos"
    elif grade == '3p_fim_ciclo':
        escolaridade = "9º, 11º e 12º Anos"

    # datas definidas pelo user no formulário
    user_inicio_al = data['inicio_ano']  # Data de início do ano letivo
    user_fim_1s = data['fim_1s']  # Data de fim do 1ºSemestre
    user_inicio_2s = data['inicio_2s']  # Data de início do 2ºSemestre

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
    print(" - Disciplina:", data['disciplina'])
    lista_periodos = []
    if data["disciplina"] == 'anual':
        periodo_1 = get_object_or_404(Periodo, ano_letivo=ano_letivo.id, tipo='1p')
        periodo_2 = get_object_or_404(Periodo, ano_letivo=ano_letivo.id, tipo='2p')
        periodo_3 = get_object_or_404(Periodo, ano_letivo=ano_letivo.id, tipo='3p')
        lista_periodos.extend((periodo_1, periodo_2, periodo_3))
        print(" - Periodos selecionados:", lista_periodos)
    if data["disciplina"] == 'semestral':
        # para obter datas iniciais do semestre uso o 1p
        semestre_1 = get_object_or_404(Periodo, ano_letivo=ano_letivo.id, tipo='1p')
        # para obter datas finais do semestre uso o 3p
        semestre_2 = get_object_or_404(Periodo, ano_letivo=ano_letivo.id, tipo='3p')
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
    except Feriado.DoesNotExist:
        feriados_nacionais = None
        print('     # Erro_2 - Não foram definidos feriados nacionais para o ano letivo:', ano_letivo)

    try:
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
        feriado_municipal = None
        print('     # Erro_3 - Não foi definido um feriado municipal:', ano_letivo)

    # Retorna lista com os dias de férias do Natal
    lista_dias_natal = []
    try:
        natal = get_object_or_404(Periodo, ano_letivo=ano_letivo.id, tipo="natal")
        lista_dias_natal = funcao_lista_dias_delta_t(natal)
        print(" - Dias de Natal:", lista_dias_natal)
    except ValueError:
        print('     # Erro_4 - Não foram definidas as datas do Natal:', ano_letivo)

    # Retorna lista com os dias de férias do Carnaval
    lista_dias_carnaval = []
    try:
        carnaval = get_object_or_404(Periodo, ano_letivo=ano_letivo.id, tipo="carnaval")
        lista_dias_carnaval = funcao_lista_dias_delta_t(carnaval)
        print(" - Dias de Carnaval:", lista_dias_carnaval)
    except ValueError:
        print('     # Erro_5 - Não foram definidas as datas do Carnaval:', ano_letivo)

    # Retorna lista com os dias de férias da Páscoa
    lista_dias_pascoa = []
    try:
        pascoa = get_object_or_404(Periodo, ano_letivo=ano_letivo.id, tipo="pascoa")
        lista_dias_pascoa = funcao_lista_dias_delta_t(pascoa)
        print(" - Dias de Páscoa:", lista_dias_pascoa)
    except ValueError:
        print('     # Erro_6 - Não foram definidas as datas do Páscoa:', ano_letivo)

    # Calcula os dias de aulas segundo o formulário inserido pelo utilizador.
    # — dicionário_dias_uteis no formato -> {Periodo: [lista de dias_úteis]}
    # — dicionário_dias_aula no formato -> {Periodo: [lista_de dias_aula]}
    dicionario_dias_uteis = {}
    dicionario_dias_aula = {}
    for p in lista_periodos:
        lista_dias_uteis = []
        lista_dias_aula = []
        # inicialização de variáveis para datas
        start_date = 0
        end_date = 0

        # disciplina anual (com 3 Períodos)
        if data["disciplina"] == 'anual':
            # permite utilizar a data de início do 1periodo inserida pelo user no formulário
            if p.tipo == '1p':
                start_date = user_inicio_al
                end_date = p.end_date1
            elif p.tipo == '3p':
                start_date = p.start_date1
                if grade == '3p_fim_ciclo':
                    end_date = p.end_date1
                elif grade == '3p_meio_ciclo':
                    end_date = p.end_date2
                else:
                    end_date = p.end_date3
            else:
                start_date = p.start_date1
                end_date = p.end_date1

        # disciplina semestral (com 2 Semestres)
        if data["disciplina"] == 'semestral':
            if p.tipo == '1p':
                start_date = user_inicio_al
                end_date = user_fim_1s
            else:
                start_date = user_inicio_2s
                if grade == '3p_fim_ciclo':
                    end_date = p.end_date1
                elif grade == '3p_meio_ciclo':
                    end_date = p.end_date2
                else:
                    end_date = p.end_date3

        for single_date in daterange(start_date, end_date):
            # percorre todos os dias do período

            if single_date not in lista_data_feriados and \
                    single_date not in lista_dias_natal and \
                    single_date not in lista_dias_carnaval and \
                    single_date not in lista_dias_pascoa and \
                    single_date.weekday() != 5 and single_date.weekday() != 6:
                # O dia não é feriado, não é Natal, não é Carnaval, não é Páscoa,
                # não é sábado (5) nem domingo (6)...
                # Então é dia útil
                lista_dias_uteis.append(single_date)

                # verifica se o dia (single_date) é um dia de aula (com carga semanal)
                for da in carga_semanal:
                    if single_date.weekday() == da:
                        lista_dias_aula.append(single_date)
        # Atualiza os dicionários de dias de aula e útil
        # formato: {periodo: lista_dias}
        dicionario_dias_aula.update({p: lista_dias_aula})
        dicionario_dias_uteis.update({p: lista_dias_uteis})

    # imprime os dias úteis do ano letivo, se dicionário não vazio.
    if len(dicionario_dias_uteis) != 0:
        imprime_dias("\n - Dias úteis por período/semestre:", dicionario_dias_uteis)

    # imprime os dias de aula do ano letivo, se dicionário não vazio.
    if len(dicionario_dias_aula) != 0:
        imprime_dias(" - Dias de aula por período/semestre:", dicionario_dias_aula)

    dicionario_tabela_ap = {}
    lista = []
    calendario = [
        '2ªFeira', '3ªFeira', '4ªFeira', '5ªFeira', '6ªFeira'
    ]

    context = {}

    if data["disciplina"] == 'anual':
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
            'ano_letivo': ano_letivo,               # objeto ano letivo
            'disciplina': data['disciplina'],           # tipo disciplina anual/semestral
            'escolaridade': escolaridade,               # tipo escolaridade (1p, 2p, 3p_pre ...) -> verbose name
            'lista_periodos': lista_periodos,           # lista de objetos periodos (períodos ou semestres)
            'lista_feriados': lista_data_feriados,          # lista de datas
            'feriados_nacionais': feriados_nacionais,       # queriset com os objetos feriados nacionais
            'feriado_municipal': feriado_municipal,         # objeto feriado municipal
            'lista_carnaval': lista_dias_carnaval,          # lista de datas
            'dias_de_aulas': carga_semanal,                     # dicionário com a carga semanal (dia semana: tempos)
            'dicionario_dias_uteis': dicionario_dias_uteis,         # dicionário (periodo: lista de dias uteis)
            'dicionario_dias_aula': dicionario_dias_aula,           # dicionário (periodo: lista de dias de aula)
            'dicionario_tabela_ap': dicionario_tabela_ap,                       # dicionário de inteiros
            'totais_dicionario_tabela_ap': totais_dicionario_tabela_ap,         # dicionário de inteiros
        }

    if data["disciplina"] == 'semestral':
        for key in carga_semanal:
            for p in dicionario_dias_aula:
                lista.append(p)
            linha_tabela_ap = TabelaAulasPrevistasSemestres(
                key,
                carga_semanal[key],
                dicionario_dias_aula[lista[0]],
                dicionario_dias_aula[lista[1]],
            )
            dicionario_tabela_ap.update({calendario[key]: linha_tabela_ap})

        soma_aulas_1s = 0
        soma_aulas_2s = 0
        soma_aulas_total = 0
        soma_previstas_1s = 0
        soma_previstas_2s = 0
        soma_previstas_total = 0
        for key, obj in dicionario_tabela_ap.items():
            soma_aulas_1s = soma_aulas_1s + obj.conta_weekdays_1s()
            soma_aulas_2s = soma_aulas_2s + obj.conta_weekdays_2s()
            soma_aulas_total = soma_aulas_total + obj.total_weekdays()
            soma_previstas_1s = soma_previstas_1s + obj.aulas_previstas_1s()
            soma_previstas_2s = soma_previstas_2s + obj.aulas_previstas_2s()
            soma_previstas_total = soma_previstas_total + obj.total_previstas()

        totais_dicionario_tabela_ap = {
            'soma_aulas_1s': soma_aulas_1s,
            'soma_aulas_2s': soma_aulas_2s,
            'soma_aulas_total': soma_aulas_total,
            'soma_previstas_1s': soma_previstas_1s,
            'soma_previstas_2s': soma_previstas_2s,
            'soma_previstas_total': soma_previstas_total,
        }

        context = {
            'ano_letivo': ano_letivo,                   # objeto ano letivo
            'disciplina': data['disciplina'],           # tipo disciplina anual/semestral
            'escolaridade': escolaridade,               # tipo escolaridade (1p, 2p, 3p_pre ...) -> verbose name
            'lista_periodos': lista_periodos,           # lista de objetos periodos (períodos ou semestres)
            'lista_feriados': lista_data_feriados,          # lista de datas
            'feriados_nacionais': feriados_nacionais,       # queriset com os objetos feriados nacionais
            'feriado_municipal': feriado_municipal,         # objeto feriado municipal
            'lista_carnaval': lista_dias_carnaval,          # lista de datas
            'dias_de_aulas': carga_semanal,                        # dicionário com a carga semanal (dia semana: tempos)
            'dicionario_dias_uteis': dicionario_dias_uteis,        # dicionário (periodo: lista de dias uteis)
            'dicionario_dias_aula': dicionario_dias_aula,          # dicionário (periodo: lista de dias de aula)
            'dicionario_tabela_ap': dicionario_tabela_ap,                   # dicionário de inteiros
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
