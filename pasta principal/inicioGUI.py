import customtkinter as ctk
from config import configuracoes_usuario

ctk.set_appearance_mode("dark")

ctk.set_default_color_theme("blue")

janela=ctk.CTk()
janela.title("Monitorador De Hidratação")
janela.geometry("1000x500")
titulo=ctk.CTkLabel(janela, text="Bem Vindo ao Monitorador de Hidratação", font=ctk.CTkFont(size=18, weight="bold"))
titulo.configure(font=ctk.CTkFont(size=40))
titulo.pack(pady=40)
erro=None

nome=None
button2=None
button3=None
litros=None
intervalo=None
horario_ini=None
horario_fin=None


def button_acao():
    global nome,button2
    titulo.pack_forget()
    button.pack_forget()

    nome=ctk.CTkEntry(janela,placeholder_text="Como devo te chamar? :)", width=300, height=90)
    nome.configure(font=ctk.CTkFont(size=25))
    nome.pack(pady=100)

    button2=ctk.CTkButton(janela,text="Confirmar", command=button2_acao)
    button2.pack(pady=20)

def button2_acao():
    global nome, button2, litros, intervalo, horario_ini, horario_fin, button3

    usuario=nome.get()
    nome.pack_forget()
    button2.pack_forget()
    texto=ctk.CTkLabel(janela, text=f"Olá {usuario} vamos começar?", font=ctk.CTkFont(size=18, weight="bold"))
    texto.pack(pady=40)

    litros=ctk.CTkEntry(janela,placeholder_text="Quantos litros deseja beber hoje?", width=300, height=40 )
    litros.pack(pady=15)

    intervalo=ctk.CTkEntry(janela, placeholder_text="Tempo dos lembretes (minutos)",width=300, height=40 )
    intervalo.pack(pady=16)

    horario_ini=ctk.CTkEntry(janela, placeholder_text="Horario de inicio dos lembretes",width=300, height=40 )
    horario_ini.pack(pady=16)

    horario_fin=ctk.CTkEntry(janela, placeholder_text="Horario final dos lembretes",width=300, height=40 )
    horario_fin.pack(pady=16)

    button3=ctk.CTkButton(janela, text="Confirmar", command=button3_acao)
    button3.pack(pady=20)

def button3_acao():
    global nome, button2, litros, intervalo, horario_ini, horario_fin, button3,erro

    if erro:
        erro.destroy()
        erro=None


    resultado=configuracoes_usuario(
    litros_str=litros.get(),
    intervalo_str=intervalo.get(),
    inicio_str=horario_ini.get(),
    final_str=horario_fin.get()
    )

    if isinstance(resultado,str):
        erro = ctk.CTkLabel(janela, text=resultado, text_color="red")
        erro.pack(pady=10)

    else:
        l,i,ini,fim=resultado 
        print("litros", l)
        print('intervalo',i)
        print('inicio',ini)
        print('fim',fim)
        






button=ctk.CTkButton(janela, text="Clique para começar", width=200, height=100, command=button_acao)
button.pack(pady=100)








janela.mainloop()