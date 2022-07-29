from dataclasses import dataclass


@dataclass
class TabelaAulasPrevistasPeriodos:
    dia_da_semana: int
    carga_semanal: int
    lista_dias_aula_1p: list
    lista_dias_aula_2p: list
    lista_dias_aula_3p: list

    def conta_weekdays_1p(self):
        count = 0
        for a in self.lista_dias_aula_1p:
            if a.weekday() == self.dia_da_semana:
                count = count + 1
        return count

    def conta_weekdays_2p(self):
        count = 0
        for a in self.lista_dias_aula_2p:
            if a.weekday() == self.dia_da_semana:
                count = count + 1
        return count

    def conta_weekdays_3p(self):
        count = 0
        for a in self.lista_dias_aula_3p:
            if a.weekday() == self.dia_da_semana:
                count = count + 1
        return count

    def total_weekdays(self):
        count = self.conta_weekdays_1p() + self.conta_weekdays_2p() + self.conta_weekdays_3p()
        return count

    def aulas_previstas_1p(self):
        count = self.conta_weekdays_1p() * self.carga_semanal
        return count

    def aulas_previstas_2p(self):
        count = self.conta_weekdays_2p() * self.carga_semanal
        return count

    def aulas_previstas_3p(self):
        count = self.conta_weekdays_3p() * self.carga_semanal
        return count

    def total_previstas(self):
        count = self.aulas_previstas_1p() + self.aulas_previstas_2p() + self.aulas_previstas_3p()
        return count


@dataclass
class TabelaAulasPrevistasSemestres:
    dia_da_semana: int
    carga_semanal: int
    da_1sem_count: int
    da_2sem_count: int
    da_total_count: int
    ap_1sem_count: int
    ap_2sem_count: int
    ap_total_count: int

