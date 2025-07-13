from datetime import datetime, timedelta
from notifypy import Notify
import time

_usuario = None
_qtd_por_lembrete = None





def configuracoes_usuario(litros_str, intervalo_str, inicio_str, final_str):

    try:
        litros = float(litros_str)
        if litros <= 0:
            return "Erro: litros deve ser maior que zero."
    except:
        return "Erro: litros inválido, digite um número."


    try:
        intervalo = int(intervalo_str)
        if intervalo < 10:
            return "Erro: intervalo mínimo é 10 minutos."
    except:
        return "Erro: intervalo inválido, digite um número inteiro."


    try:
        horario_ini = datetime.strptime(inicio_str, "%H:%M")
    except:
        return "Erro: formato horário início inválido, use HH:MM."

   
    try:
        horario_fin = datetime.strptime(final_str, "%H:%M")
        if horario_fin <= horario_ini:
            horario_fin += timedelta(days=1)
    except:
        return "Erro: formato horário final inválido, use HH:MM."

   
    return litros, intervalo, horario_ini, horario_fin




def calcular_lembretes(litros, intervalo, horario_ini, horario_fin):
    
    tempo_ativo = horario_fin - horario_ini
    total_minutos = tempo_ativo.total_seconds() // 60

 
    quantidade_lembretes = int(total_minutos // intervalo)

    if quantidade_lembretes == 0:
        return "Erro: período muito curto para o intervalo escolhido."

 
    quantidade_por_lembrete = round(litros / quantidade_lembretes, 2)

    return quantidade_lembretes, quantidade_por_lembrete




def mostrar_notificacao(titulo, mensagem):
    notification = Notify()
    notification.title = titulo
    notification.message = mensagem
    notification.send()



def esperando(hr_ini,ini_apos,janela):
    agora=datetime.now()
    if agora>=hr_ini:
        ini_apos()
    else:
        janela.after(1000, lambda: esperando(hr_ini,ini_apos,janela))



def dados_usuario(usuario, qtd_por_lembrete):
    global _usuario, _qtd_por_lembrete
    _usuario = usuario
    _qtd_por_lembrete = qtd_por_lembrete



def iniciar_lembretes(lembretes_total,intervalo_min,janela):
    from config import _usuario, _qtd_por_lembrete

    def ciclo(lembretes_restantes):
        if lembretes_restantes==0:
            return
        mostrar_notificacao("Hora de beber Água", f"olá {_usuario} beba {_qtd_por_lembrete}ml")
        janela.after((intervalo_min*60000), lambda:ciclo(lembretes_restantes-1))

    ciclo(lembretes_total)

