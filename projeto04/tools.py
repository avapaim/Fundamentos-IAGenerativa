import datetime


def data_atual():
    return datetime.date.today()


def calcular_imc(peso, altura):
    return peso / (altura ** 2)