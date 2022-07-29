import datetime
from dataclasses import dataclass
from datetime import date
import calendar


@dataclass
class FeriadoBakup:
    nome: str
    data: date
    movel: bool
    tipo: str
    concelho: str
    distrito: str


feriados = {
    # estrutura: dicionário de objetos 'FeriadoBackup
    # nome : <FeriadoBackup: nome, data, movel, tipo, concelho, distrito>

    # Feriados Nacionais
    "Ano novo": FeriadoBakup("Ano novo", date(2018, 1, 1), False, 'nacional', 'pt', 'pt'),
    "Páscoa": FeriadoBakup("Páscoa", date(2018, 4, 1), True, 'nacional', 'pt', 'pt'),
    "Dia da liberdade": FeriadoBakup("Dia da liberdade", date(2018, 4, 25), False, 'nacional', 'pt', 'pt'),
    "Dia do Trabalhador": FeriadoBakup("Dia do Trabalhador", date(2018, 5, 1), False, 'nacional', 'pt', 'pt'),
    # Corpo de Deus - > Feriado Nacional móvel -> 60 dias depois da Páscoa
    "Corpo de Deus": FeriadoBakup("Corpo de Deus", date(2018, 5, 31), True, 'nacional', 'pt', 'pt'),
    "Dia de Portugal": FeriadoBakup("Dia de Portugal", date(2018, 6, 10), False, 'nacional', 'pt', 'pt'),
    "Assunção de Nossa Senhora": FeriadoBakup("Assunção de Nossa Senhora", date(2018, 8, 15), False, 'nacional', 'pt',
                                              'pt'),
    "Implantação da República": FeriadoBakup("Implantação da República", date(2018, 10, 5), False, 'nacional', 'pt',
                                             'pt'),
    "Dia de Todos os Santos": FeriadoBakup("Dia de Todos os Santos", date(2018, 11, 1), False, 'nacional', 'pt', 'pt'),
    "Restauração da Independência": FeriadoBakup("Restauração da Independência", date(2018, 12, 1), False, 'nacional',
                                                 'pt', 'pt'),
    "Imaculada Conceição": FeriadoBakup("Imaculada Conceição", date(2018, 12, 8), False, 'nacional', 'pt', 'pt'),
    "Natal": FeriadoBakup("Natal", date(2018, 12, 25), False, 'nacional', 'pt', 'pt'),

    # -> Feriados Municipais
    # FARO
    "Albufeira - Criação do concelho": FeriadoBakup("Criação do concelho", date(2018, 8, 20), False, 'municipal',
                                                    'Albufeira', 'Faro'),
    # Alcoutim -> Feriado municipal móvel -> 2.ª 6ªFeira de setembro
    "Alcoutim - Feriado Municipal de Alcoutim": FeriadoBakup("Feriado Municipal de Alcoutim", date(2018, 9, 15), True,
                                                             'municipal', 'Alcoutim', 'Faro'),
    "Aljezur - Tradição do banho Santo": FeriadoBakup("Tradição do banho Santo", date(2018, 8, 29), False, 'municipal',
                                                      'Aljezur', 'Faro'),
    "Castro Marim - Dia de São João": FeriadoBakup("Dia de São João", date(2018, 6, 24), False, 'municipal',
                                                   'Castro Marim', 'Faro'),
    "Faro - Dia de elevação a cidade": FeriadoBakup("Dia de elevação a cidade", date(2018, 9, 7), False, 'municipal',
                                                    'Faro', 'Faro'),
    "Lagoa - Festa da Nossa Senhora da Luz": FeriadoBakup("Festa da Nossa Senhora da Luz", date(2018, 9, 8), False,
                                                          'municipal', 'Lagoa', 'Faro'),
    "Lagos - Festa de São Gonçalo de Lagos": FeriadoBakup("Festa de São Gonçalo de Lagos", date(2018, 10, 27), False,
                                                          'municipal', 'Lagos', 'Faro'),
    # Loulé e Monchique -> Feriados municipais móveis -> 39 dias depois da Páscoa (40 dias a contar com a Páscoa)
    "Loulé - Feriado Municipal de Loulé": FeriadoBakup("Feriado Municipal de Loulé", date(2018, 5, 25), True,
                                                       'municipal', 'Loulé', 'Faro'),
    "Monchique - Quinta-Feira da Ascenção": FeriadoBakup("Quinta-feira da Ascenção", date(2018, 5, 10), True,
                                                         'municipal', 'Monchique', 'Faro'),
    "Olhão - Revolta de Olhão contra dos Franceses": FeriadoBakup("Revolta de Olhão contra os franceses",
                                                                  date(2018, 6, 16), False, 'municipal', 'Olhão',
                                                                  'Faro'),
    "Portimão - Feriado Municipal de Portimão": FeriadoBakup("Feriado Municipal de Portimão", date(2018, 12, 11), False,
                                                             'municipal', 'Portimão', 'Faro'),
    "São Brás de Alportel - Dia de elevação a Município": FeriadoBakup("Dia de elevação a Município", date(2018, 6, 1),
                                                                       False, 'municipal', 'São Brás de Alportel',
                                                                       'Faro'),
    "Silves - Conquista da cidade aos mouros": FeriadoBakup("Conquista da cidade aos mouros", date(2018, 9, 3), False,
                                                            'municipal', 'Silves', 'Faro'),
    "Tavira - Dia de São João": FeriadoBakup("Dia de São João", date(2018, 6, 24), False, 'municipal', 'Tavira',
                                             'Faro'),
    "Vila do Bispo - Festa de São Vicente": FeriadoBakup("Festa de São Vicente", date(2018, 1, 22), False, 'municipal',
                                                         'Vila do Bispo', 'Faro'),
    "Vila Real de Santo António - 13 de maio": FeriadoBakup("13 de maio", date(2018, 5, 13), False, 'municipal',
                                                            'Vila Real de Santo António', 'Faro'),
}


def get_dia_pascoa(ano):
    """Calcula o dia de Páscoa através do Algoritmo de Meeus/Jones/Butcher"""

    a = ano % 19
    b = ano // 100
    c = ano % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = ((19 * a) + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + (2 * e) + (2 * i) - h - k) % 7
    m = (a + (11 * h) + (22 * l)) // 451
    month = (h + l - (7 * m) + (114)) // 31
    day = 1 + ((h + l - (7 * m) + (114)) % 31)

    return date(ano, month, day)


def atualiza_feriados_pela_pascoa(nome, pascoa, dias):
    """Soma dias à Páscoa"""

    feriado = feriados[nome]
    feriado.data = pascoa + datetime.timedelta(days=dias)
    feriados.update({nome: feriado})


def atualiza_feriados_por_data(nome, data_ref, posicao, dia_semana):
    """
        Atualiza feriados por data de referencia
        exemplo: 2.ª sexta-feira de setembro
            atualiza_feriados_por_data("feriado Alcoutim", date(2018, 9, 1), 2, "FRIDAY")
        NOTA: dia_semana em inglês e maiusculas
    """
    dia = {
        "domingo": calendar.SUNDAY,
        "segunda-feira": calendar.MONDAY,
        "terça-feira": calendar.TUESDAY,
        "quarta-feira": calendar.WEDNESDAY,
        "quinta-feira": calendar.THURSDAY,
        "sexta-feira": calendar.FRIDAY,
        "sabado": calendar.SATURDAY,
    }
    c = calendar.Calendar(firstweekday=calendar.SUNDAY)

    ano = data_ref.year
    mes = data_ref.month

    monthcal = c.monthdatescalendar(ano, mes)
    data = [day for week in monthcal for day in week if \
            day.weekday() == dia[dia_semana] and \
            day.month == mes][posicao - 1]

    feriado = feriados[nome]
    feriado.data = data
    feriados.update({nome: feriado})
