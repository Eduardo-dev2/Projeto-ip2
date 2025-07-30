import customtkinter as ctk
from config_ip import configuracoes_usuario, calcular_lembretes, mostrar_notificacao, esperando, dados_usuario, iniciar_lembretes, salvar_credenciais, credenciais_validas
from PIL import Image
from customtkinter import CTkImage, CTkLabel

# Variáveis globais
nome = senha = titulo2 = button2 = erro_login = None
nome2 = senha2 = button_log2 = erro = None
litros = intervalo = horario_ini = horario_fin = button3 = texto = None
usuario = senha_usu = qtd_lembretes = qtd_por_lembrete = None
meta_diaria_ml = 0

# Configuração inicial da janela
ctk.set_default_color_theme("blue")
janela = ctk.CTk()
janela.title("Monitorador De Hidratação")
janela.geometry("1024x800")

# Fundos
fundo = Image.open("assets/tela_loguin.png")
fundo2 = Image.open("assets/fundo2.png")
fundo3 = Image.open("assets/fundo3.png")

img_ctk = CTkImage(light_image=fundo, dark_image=fundo, size=(1024, 800))
img_ctk2 = CTkImage(light_image=fundo2, dark_image=fundo2, size=(1024, 800))
img_ctk3 = CTkImage(light_image=fundo3, dark_image=fundo3, size=(1024, 800))

fundo_label = CTkLabel(janela, image=img_ctk, text="")
fundo_label.place(x=0, y=0, relwidth=1, relheight=1)

def cadastro():
    global nome, senha, titulo2, button2
    button_cad.place_forget()
    button_log.place_forget()
    fundo_label.configure(image=img_ctk2)

    titulo2 = ctk.CTkLabel(janela, text="olá, eu me chamo alfredo, vou ser seu assistente para lhe lembrar de beber água",
                           font=ctk.CTkFont(size=20, weight="bold"), fg_color='#f3f3f3')
    titulo2.place(relx=0.52, rely=0.1, anchor="center")

    nome = ctk.CTkEntry(janela, placeholder_text="Como devo te chamar? :)", width=400, height=80,
                        fg_color='white', corner_radius=15)
    nome.configure(font=ctk.CTkFont(size=30))
    nome.place(relx=0.52, rely=0.25, anchor="center")

    senha = ctk.CTkEntry(janela, placeholder_text="Crie uma senha: ", width=400, height=80,
                         fg_color='white', corner_radius=15)
    senha.configure(font=ctk.CTkFont(size=30))
    senha.place(relx=0.52, rely=0.40, anchor="center")

    button2 = ctk.CTkButton(janela, text="Cadastrar", font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
                            width=115, height=70, command=confirmar_cadastro, fg_color='#4682B4', corner_radius=50)
    button2.place(relx=0.52, rely=0.70, anchor="center")

def confirmar_cadastro():
    global nome, senha, titulo2, button2
    usuario = nome.get()
    senha_usu = senha.get()

    if usuario and senha_usu:
        salvar_credenciais(usuario, senha_usu)
        nome.destroy()
        senha.destroy()
        titulo2.destroy()
        button2.destroy()

        aviso = ctk.CTkLabel(janela, text="Cadastro realizado com sucesso! Faça login para continuar.",
                             text_color="green", font=ctk.CTkFont(size=35, weight="bold"), fg_color='#f3f3f3')
        aviso.place(relx=0.52, rely=0.5, anchor="center")
        janela.after(3000, lambda: [aviso.destroy(), voltar_para_inicio()])
    else:
        erro = ctk.CTkLabel(janela, text="Preencha todos os campos", text_color="red",
                            font=ctk.CTkFont(size=16, weight="bold"), fg_color='#f3f3f3')
        erro.place(relx=0.52, rely=0.60, anchor="center")
        janela.after(2000, erro.destroy)

def voltar_para_inicio():
    fundo_label.configure(image=img_ctk)
    button_cad.place(relx=0.70, rely=0.5, anchor="center")
    button_log.place(relx=0.70, rely=0.72, anchor="center")

def login():
    global nome2, senha2, button_log2
    button_cad.place_forget()
    button_log.place_forget()
    fundo_label.configure(image=img_ctk2)

    nome2 = ctk.CTkEntry(janela, placeholder_text="Usuario", width=400, height=80, fg_color='white', corner_radius=15)
    nome2.configure(font=ctk.CTkFont(size=30))
    nome2.place(relx=0.52, rely=0.25, anchor="center")

    senha2 = ctk.CTkEntry(janela, placeholder_text="Senha ", width=400, height=80, fg_color='white', corner_radius=15)
    senha2.configure(font=ctk.CTkFont(size=30))
    senha2.place(relx=0.52, rely=0.40, anchor="center")

    button_log2 = ctk.CTkButton(janela, text="Loguin", font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
                                width=115, height=70, command=validacao, fg_color='#4682B4', corner_radius=50)
    button_log2.place(relx=0.52, rely=0.70, anchor="center")

def tela_configuracoes():
    global litros, intervalo, horario_ini, horario_fin, button3, texto
    for widget in janela.winfo_children():
        widget.place_forget()

    fundo_label.configure(image=img_ctk3)

    texto = ctk.CTkLabel(janela, text="Antes de começar, defina seus dados de hidratação:", font=ctk.CTkFont(size=22, weight="bold"))
    texto.place(relx=0.5, rely=0.1, anchor="center")

    litros = ctk.CTkEntry(janela, placeholder_text="Quantos litros por dia?", width=300, height=50, fg_color='white')
    litros.place(relx=0.5, rely=0.25, anchor="center")

    intervalo = ctk.CTkEntry(janela, placeholder_text="Intervalo entre lembretes (min)", width=300, height=50, fg_color='white')
    intervalo.place(relx=0.5, rely=0.35, anchor="center")

    horario_ini = ctk.CTkEntry(janela, placeholder_text="Horário inicial (HH:MM)", width=300, height=50, fg_color='white')
    horario_ini.place(relx=0.5, rely=0.45, anchor="center")

    horario_fin = ctk.CTkEntry(janela, placeholder_text="Horário final (HH:MM)", width=300, height=50, fg_color='white')
    horario_fin.place(relx=0.5, rely=0.55, anchor="center")

    button3 = ctk.CTkButton(janela, text="Confirmar", command=button3_acao, width=150, height=50)
    button3.place(relx=0.5, rely=0.70, anchor="center")

def validacao():
    global erro_login, usuario
    usuario_digitado = nome2.get()
    senha_digitada = senha2.get()

    if credenciais_validas(usuario_digitado, senha_digitada):
        print("Login bem-sucedido!")
        fundo_label.configure(image=img_ctk3)
        senha2.place_forget()
        button_log2.place_forget()
        nome2.place_forget()

        if erro_login:
            erro_login.destroy()
            erro_login = None

        usuario = usuario_digitado
        tela_configuracoes()
    else:
        if erro_login:
            erro_login.destroy()

        erro_login = ctk.CTkLabel(janela, text="Usuário ou senha incorretos", text_color="red",
                                  font=ctk.CTkFont(size=15, weight="bold"), fg_color='#f3f3f3')
        erro_login.place(relx=0.52, rely=0.60, anchor="center")

def tela_principal():
    global litros, intervalo, horario_ini, horario_fin, button3, texto
    global copo_canvas, botao_beber, progresso_texto
    global meta_diaria_ml

    for widget in janela.winfo_children():
        widget.place_forget()

    fundo_label.configure(image=img_ctk3)

    texto = ctk.CTkLabel(janela, text=f"Olá {usuario}, acompanhe sua hidratação diária!", font=ctk.CTkFont(size=24, weight="bold"))
    texto.place(relx=0.5, rely=0.1, anchor="center")

    copo_canvas = ctk.CTkCanvas(janela, width=200, height=400, bg="#f3f3f3", highlightthickness=0)
    copo_canvas.place(relx=0.5, rely=0.55, anchor="center")
    copo_canvas.create_rectangle(50, 20, 150, 380, outline="#000", width=3)
    copo_canvas.progresso = 0

    def atualizar_copo():
        copo_canvas.delete("agua")
        altura_total = 360
        altura_agua = int((copo_canvas.progresso / meta_diaria_ml) * altura_total)
        if altura_agua > altura_total:
            altura_agua = altura_total
        copo_canvas.create_rectangle(51, 380 - altura_agua, 149, 380, fill="#00bfff", width=0, tags="agua")
        progresso_texto.configure(text=f"{copo_canvas.progresso} ml / {meta_diaria_ml} ml")

    def beber_agua():
        copo_canvas.progresso += (qtd_por_lembrete * 1000)
        if copo_canvas.progresso > meta_diaria_ml:
            copo_canvas.progresso = meta_diaria_ml
        atualizar_copo()

    botao_beber = ctk.CTkButton(janela, text=f'Beber {qtd_por_lembrete}L', command=beber_agua, width=150, height=50)
    botao_beber.place(relx=0.5, rely=0.9, anchor="center")

    progresso_texto = ctk.CTkLabel(janela, text=f"0 ml / {meta_diaria_ml} ml", font=ctk.CTkFont(size=16))
    progresso_texto.place(relx=0.5, rely=0.8, anchor="center")

    atualizar_copo()

def button3_acao():
    global erro, qtd_lembretes, qtd_por_lembrete, meta_diaria_ml

    if erro:
        erro.destroy()

    resultado = configuracoes_usuario(
        litros_str=litros.get(),
        intervalo_str=intervalo.get(),
        inicio_str=horario_ini.get(),
        final_str=horario_fin.get()
    )

    if isinstance(resultado, str):
        erro = ctk.CTkLabel(janela, text=resultado, text_color="red",
                            font=ctk.CTkFont(size=15, weight="bold"), fg_color='#f3f3f3')
        erro.place(relx=0.8, rely=0.80, anchor="center")
    else:
        l, i, ini, fim = resultado
        qtd_lembretes, qtd_por_lembrete = calcular_lembretes(l, i, ini, fim)
        intervalo_int = int(intervalo.get())
        dados_usuario(usuario, qtd_por_lembrete)
        meta_diaria_ml = int(float(l) * 1000)

        def iniciar_agora():
            iniciar_lembretes(qtd_lembretes, intervalo_int, janela)

        esperando(ini, iniciar_agora, janela)

        litros.place_forget()
        intervalo.place_forget()
        horario_ini.place_forget()
        horario_fin.place_forget()
        button3.place_forget()
        texto.place_forget()
        fundo_label.configure(image=img_ctk3)
        tela_principal()

# Botões iniciais
button_cad = ctk.CTkButton(janela, text="clique aqui", font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
                           width=100, height=50, command=cadastro, fg_color='#4682B4', corner_radius=50)
button_cad.place(relx=0.70, rely=0.5, anchor="center")

button_log = ctk.CTkButton(janela, text="clique aqui", font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
                           width=100, height=50, command=login, fg_color='#4682B4', corner_radius=50)
button_log.place(relx=0.70, rely=0.72, anchor="center")

janela.mainloop()
