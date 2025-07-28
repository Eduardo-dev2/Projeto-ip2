from datetime import datetime, timedelta
from notifypy import Notify
import time

_usuario = None
_qtd_por_lembrete = None
senha_usu=None


def configuracoes_usuario(litros_str, intervalo_str, inicio_str, final_str):

    try:
        litros = float(litros_str)
        if litros <= 0:
            return "Erro: litros deve ser maior que zero."
    except ValueError:
        return "Erro: litros inválido, digite um número."

    try:
        intervalo = int(intervalo_str)
       # if intervalo < 10:
     #       return "Erro: intervalo mínimo é 10 minutos."
    except ValueError:
        return "Erro: intervalo inválido, digite um número inteiro."

    hoje = datetime.now()

    try:
        horario_ini = datetime.strptime(inicio_str, "%H:%M").replace(
            year=hoje.year, month=hoje.month, day=hoje.day
        )
    except ValueError:
        return "Erro: formato horário início inválido, use HH:MM."

    try:
        horario_fin = datetime.strptime(final_str, "%H:%M").replace(
            year=hoje.year, month=hoje.month, day=hoje.day
        )
        
        if horario_fin <= horario_ini:
            horario_fin += timedelta(days=1)
    except ValueError:
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
    print(f"Verificando hora: Agora={agora.strftime('%H:%M:%S')}, Início={hr_ini.strftime('%H:%M:%S')}")
    if agora>=hr_ini:
        print("Horário de início alcançado, iniciando lembretes...")
        ini_apos()
    else:
        print("Aguardando horário de início...")
        janela.after(1000, lambda: esperando(hr_ini,ini_apos,janela))



def dados_usuario(usuario, qtd_por_lembrete):
    global _usuario, _qtd_por_lembrete
    _usuario = usuario
    _qtd_por_lembrete = qtd_por_lembrete



def iniciar_lembretes(lembretes_total, intervalo_min, janela):

    def ciclo(lembretes_restantes):
        if lembretes_restantes == 0:
            print("Ciclo de lembretes concluído.") 
            return
        
        print(f"Enviando notificação: Restam {lembretes_restantes} lembretes. Hora: {datetime.now().strftime('%H:%M:%S')}")
        mostrar_notificacao("Hora de beber Água", f"olá {_usuario} beba {_qtd_por_lembrete}ml")
        
        proximo_agendamento_em_ms = intervalo_min * 60 * 1000
        print(f"Próximo lembrete agendado para daqui a {intervalo_min} minutos.") 
        janela.after(proximo_agendamento_em_ms, lambda: ciclo(lembretes_restantes - 1))

    ciclo(lembretes_total)


def salvar_credenciais(usuario,senha):
    with open("text/credenciais.txt", "a") as arquivo:
        arquivo.write(f"Usuario: {usuario}\n")
        arquivo.write(f"Senha: {senha}\n")
        arquivo.write("---\n") # Separador para futuras entradas
    print("Credenciais salvas com sucesso!")

def credenciais_validas(usuario, senha):
    try:
        with open("text/credenciais.txt", "r") as arquivo:
            linhas = arquivo.readlines()
            for i in range(0, len(linhas), 3):  # cada registo tem 3 linhas
                usuario_salvo = linhas[i].strip().replace("Usuario: ", "")
                senha_salva = linhas[i + 1].strip().replace("Senha: ", "")
                if usuario == usuario_salvo and senha == senha_salva:
                    return True
        return False
    except FileNotFoundError:
        print("Arquivo 'credenciais.txt' não encontrado.")
        return False
