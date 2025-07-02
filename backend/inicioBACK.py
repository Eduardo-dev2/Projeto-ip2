import time
import json
import threading
from datetime import datetime, timedelta
from plyer import notification
from playsound import playsound
import os





###configurações do usuario
def configuracoes_usuario():
    #recebe a meta de litros de agua diaria
    while True:
        try:
            litros_dia=float(input('Quantos litros deseja beber? '))
            if litros_dia<0:
                print('por favor insira um valor positivo: ')
                continue
            break
        except ValueError:
            print('insira um valor valido')
        
    #recebe o intervalo de lembrete
    while True:
        try:
            intervalo=int(input('De quanto em quanto tempo deseja receber lembretes? (em minutos)'))
            if intervalo <10:
                print('é um intervalo muito curto')
                continue
            break
        except ValueError:
            print('insira um valor valido em minutos ')    

    #recebe o inicio das horas ativas
    while True:
        hr_inicio_str=input('Que horas você começa a beber água? (horas e minutos)')
        try:
            datetime.strptime(hr_inicio_str, "%H:%M")
            break
        except ValueError:
            print("Formato de hora inválido. Por favor, use HH:MM (ex: 08:00 ou 18:30).")

    #recebe o final das horas ativas
    while True:
        hr_final_str=input('Que horas você termina de beber água? (horas e minutos) ')
        try:
            datetime.strptime(hr_final_str, "%H:%M")
            break
        except:
            print("Formato de hora inválido. Por favor, use HH:MM (ex: 08:00 ou 18:30).")


