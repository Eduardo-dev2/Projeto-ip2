import customtkinter as ctk
from config import configuracoes_usuario, calcular_lembretes, mostrar_notificacao, esperando, dados_usuario, iniciar_lembretes
from PIL import Image
from customtkinter import CTkImage, CTkLabel

nome=None
button2=None
button3=None
litros=None
intervalo=None
horario_ini=None
horario_fin=None
titulo2=None
alfredo=None


ctk.set_default_color_theme("blue")

janela=ctk.CTk()
janela.title("Monitorador De Hidratação")
janela.geometry("1024x680")

fundo=Image.open("assets/fundo1.png")
fundo2=Image.open("assets/fundo2.png")
alfredo_img=Image.open("assets/alfredo.png")


img_ctk = CTkImage(light_image=fundo, dark_image=fundo, size=(1024, 800))
img_ctk2 = CTkImage(light_image=fundo2, dark_image=fundo2, size=(1024, 800))
alfredo_ctk=CTkImage(light_image=fundo2, dark_image=fundo2, size=(500, 500))


fundo_label = CTkLabel(janela, image=img_ctk, text="")
fundo_label.place(x=0, y=0, relwidth=1, relheight=1)


titulo = ctk.CTkLabel(janela, text="Monitorador de Hidratação",font=ctk.CTkFont(size=50, weight="bold"), fg_color='#f3f3f3')
titulo.place(relx=0.67, rely=0.3, anchor="center")
erro=None







def button_acao():
    global nome,button2, titulo2
    titulo.place_forget()
    button.place_forget()
    fundo_label.configure(image=img_ctk2)
   
    titulo2=ctk.CTkLabel(janela, text="olá, eu me chamo alfredo, vou ser seu assistente para lhe lembrar de beber água",font=ctk.CTkFont(size=20, weight="bold"), fg_color='#f3f3f3')
    titulo2.place(relx=0.52, rely=0.1, anchor="center")
   
    alfredo = ctk.CTkLabel(janela, image=alfredo_ctk, text="") 
    alfredo.place(relx=0.2, rely=0.5, anchor="center") 


    nome=ctk.CTkEntry(janela,placeholder_text="Como devo te chamar? :)", width=400, height=120, fg_color='white', corner_radius=15)
    nome.configure(font=ctk.CTkFont(size=30))
    nome.place(relx=0.52, rely=0.25, anchor="center")

    button2=ctk.CTkButton(janela, text="Clique para começar",font=ctk.CTkFont(family="Arial", size=18, 
    weight="bold"), width=115, height=70, command=button2_acao, fg_color='#4682B4',corner_radius=50)
    button2.place(relx=0.52,rely=0.45, anchor="center")

def button2_acao():
    global nome, button2, litros, intervalo, horario_ini, horario_fin, button3,erro,qtd_lembretes, qtd_por_lembrete,usuario,titulo2

    usuario=nome.get()
    nome.place_forget()
    button2.place_forget()
    titulo2.place_forget()
    texto=ctk.CTkLabel(janela, text=f"Olá {usuario} vamos começar?", font=ctk.CTkFont(size=18, weight="bold"))
    texto.place(relx=0.5, rely=0.10, anchor="center")

    litros = ctk.CTkEntry(janela, placeholder_text="Quantos litros deseja beber hoje?", width=300, height=40)
    litros.place(relx=0.5, rely=0.20, anchor="center")

    intervalo = ctk.CTkEntry(janela, placeholder_text="Tempo dos lembretes (minutos)", width=300, height=40)
    intervalo.place(relx=0.5, rely=0.30, anchor="center")

    horario_ini = ctk.CTkEntry(janela, placeholder_text="Horário de início dos lembretes", width=300, height=40)
    horario_ini.place(relx=0.5, rely=0.40, anchor="center")

    horario_fin = ctk.CTkEntry(janela, placeholder_text="Horário final dos lembretes", width=300, height=40)
    horario_fin.place(relx=0.5, rely=0.50, anchor="center")

    button3 = ctk.CTkButton(janela, text="Confirmar", command=button3_acao)
    button3.place(relx=0.5, rely=0.60, anchor="center")


def button3_acao():
    global nome, button2, litros, intervalo, horario_ini, horario_fin, button3,erro,qtd_lembretes, qtd_por_lembrete,usuario,titulo2

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
        erro = ctk.CTkLabel(janela, text=resultado, text_color="red",font=ctk.CTkFont(size=15, weight="bold"), fg_color='#f3f3f3')
        erro.place(relx=0.8, rely=0.80, anchor="center",)

    else:
        l,i,ini,fim=resultado 
        print("litros", l)
        print('intervalo',i)
        print('inicio',ini)
        print('fim',fim)
        

    calculo=calcular_lembretes(l,i,ini,fim)
        
    qtd_lembretes, qtd_por_lembrete = calculo

    print(qtd_lembretes)
    print(qtd_por_lembrete)

    intervalo_int=int(intervalo.get())
    dados_usuario(usuario, qtd_por_lembrete)

    def iniciar_agora():
        iniciar_lembretes(qtd_lembretes, intervalo_int, janela)

    esperando(ini, iniciar_agora, janela)





button=ctk.CTkButton(janela, text="Clique para começar",font=ctk.CTkFont(family="Arial", size=18, weight="bold"), 
                     width=200, height=100, command=button_acao, fg_color='#4682B4',corner_radius=50)
button.place(relx=0.67, rely=0.5, anchor="center")








janela.mainloop()