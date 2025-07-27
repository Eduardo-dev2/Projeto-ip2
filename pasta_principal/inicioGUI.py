import customtkinter as ctk
from config_ip import configuracoes_usuario, calcular_lembretes, mostrar_notificacao, esperando, dados_usuario, iniciar_lembretes, salvar_credenciais, credenciais_validas
from PIL import Image
from customtkinter import CTkImage, CTkLabel, CTkScrollableFrame
from datetime import datetime, timedelta


nome = senha = titulo2 = button2 = erro_login = None
nome2 = senha2 = button_log2 = erro = None
litros = intervalo = horario_ini = horario_fin = button3 = texto = None
usuario = senha_usu = qtd_lembretes = qtd_por_lembrete = None
meta_diaria_ml = 0


figurinha_desbloqueada_label = None
colecao_figurinhas = []
todas_figurinhas = [
    "assets/figurinha1.png",
    "assets/figurinha2.png",
    "assets/figurinha3.png",
    "assets/figurinha4.png",
    "assets/figurinha5.png",
    "assets/figurinha6.png",
    "assets/figurinha7.png"
]
ranking_semanal = {}
dias_consecutivos = 0

copo_canvas = None
progresso_texto = None


ARQUIVO_DADOS_USUARIO = "text/dados_usuario.txt"
ARQUIVO_RANKING = "text/ranking.txt"


ctk.set_default_color_theme("blue")
janela = ctk.CTk()
janela.title("Monitorador De Hidratação")
janela.geometry("1024x800")


fundo = Image.open("assets/tela_loguin.png")
fundo2 = Image.open("assets/fundo2.png")
fundo3 = Image.open("assets/fundo3.png")



img_ctk_fundo = CTkImage(light_image=fundo, dark_image=fundo, size=(1024, 800))
img_ctk = CTkImage(light_image=fundo, dark_image=fundo, size=(1024, 800))
img_ctk2 = CTkImage(light_image=fundo2, dark_image=fundo2, size=(1024, 800))
img_ctk3 = CTkImage(light_image=fundo3, dark_image=fundo3, size=(1024, 800))
img_erro = CTkImage(Image.open("assets/erro_login.png"), size=(800, 600))

fundo_label = CTkLabel(janela, image=img_ctk, text="")
fundo_label.place(x=0, y=0, relwidth=1, relheight=1)

# --- Funções de Salvar/Carregar Dados ---

def carregar_dados_usuario():
    global colecao_figurinhas, dias_consecutivos, meta_diaria_ml

    colecao_figurinhas.clear()
    dias_consecutivos = 0
    progresso_do_dia_carregado = 0.0
    meta_diaria_ml_carregada = 0
    
    try:
        with open(ARQUIVO_DADOS_USUARIO, 'r') as f:
            for line in f:
                parts = line.strip().split(';')
                if len(parts) >= 6 and parts[0] == usuario:
                    colecao_figurinhas.extend(parts[1].split(',') if parts[1] else [])
                    dias_consecutivos = int(parts[2])
                    progresso_do_dia_carregado = float(parts[4])
                    meta_diaria_ml_carregada = int(float(parts[5]))
                    break
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Erro ao carregar dados do usuário do TXT: {e}")

    meta_diaria_ml = meta_diaria_ml_carregada

def salvar_dados_usuario():
    all_users_data = {}
    try:
        with open(ARQUIVO_DADOS_USUARIO, 'r') as f:
            for line in f:
                parts = line.strip().split(';')
                if len(parts) >= 6:
                    all_users_data[parts[0]] = {
                        "figurinhas": parts[1],
                        "dias_consecutivos": parts[2],
                        "ultimo_uso": parts[3],
                        "progresso_dia": parts[4],
                        "meta_diaria_ml": parts[5]
                    }
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Erro ao ler dados existentes do TXT antes de salvar: {e}")

    figurinhas_str = ','.join(colecao_figurinhas)
    ultimo_uso_str = datetime.now().strftime("%Y-%m-%d")

    current_progresso = copo_canvas.progresso if copo_canvas and hasattr(copo_canvas, 'progresso') else 0.0
    current_meta_ml = meta_diaria_ml if meta_diaria_ml else 0

    all_users_data[usuario] = {
        "figurinhas": figurinhas_str,
        "dias_consecutivos": str(dias_consecutivos),
        "ultimo_uso": ultimo_uso_str,
        "progresso_dia": str(current_progresso),
        "meta_diaria_ml": str(current_meta_ml)
    }

    with open(ARQUIVO_DADOS_USUARIO, 'w') as f:
        for user_key, data in all_users_data.items():
            line_to_write = f"{user_key};{data['figurinhas']};{data['dias_consecutivos']};{data['ultimo_uso']};{data['progresso_dia']};{data['meta_diaria_ml']}\n"
            f.write(line_to_write)


def carregar_ranking():
    global ranking_semanal
    ranking_semanal = {}
    try:
        with open(ARQUIVO_RANKING, 'r') as f:
            lines = f.readlines()
            if lines:
                if "ultima_reset_semana:" in lines[0]:
                    last_reset_line = lines.pop(0)
                    ranking_semanal["ultima_reset_semana"] = last_reset_line.split(":")[1].strip()
                for line in lines:
                    parts = line.strip().split(';')
                    if len(parts) == 2:
                        ranking_semanal[parts[0]] = int(parts[1])
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Erro ao carregar ranking do TXT: {e}")


def salvar_ranking():
    with open(ARQUIVO_RANKING, 'w') as f:
        if "ultima_reset_semana" in ranking_semanal:
            f.write(f"ultima_reset_semana:{ranking_semanal['ultima_reset_semana']}\n")
            temp_ranking = {k:v for k,v in ranking_semanal.items() if k != "ultima_reset_semana"}
        else:
            temp_ranking = ranking_semanal

        for user, days in temp_ranking.items():
            line_to_write = f"{user};{days}\n"
            f.write(line_to_write)


def resetar_semana_ranking():
    global ranking_semanal
    hoje = datetime.now()
    primeiro_dia_semana = hoje - timedelta(days=hoje.weekday()) 
    data_limite_str = primeiro_dia_semana.strftime("%Y-%m-%d")

    carregar_ranking()

    if "ultima_reset_semana" not in ranking_semanal or ranking_semanal["ultima_reset_semana"] != data_limite_str:
        ranking_semanal = {"ultima_reset_semana": data_limite_str}
        salvar_ranking()


def verificar_e_desbloquear_premio():
    global colecao_figurinhas, dias_consecutivos, figurinha_desbloqueada_label

    if len(colecao_figurinhas) >= len(todas_figurinhas):
        return

    if dias_consecutivos > 0 and dias_consecutivos <= len(todas_figurinhas):
        figurinha_nova_path = todas_figurinhas[dias_consecutivos - 1]
        if figurinha_nova_path not in colecao_figurinhas:
            colecao_figurinhas.append(figurinha_nova_path)
            salvar_dados_usuario()
            mostrar_notificacao("Parabéns!", f"Você desbloqueou uma nova figurinha!")

            try:
                if figurinha_desbloqueada_label:
                    figurinha_desbloqueada_label.destroy()
                
                img_figurinha = Image.open(figurinha_nova_path)
                img_ctk_figurinha = CTkImage(light_image=img_figurinha, dark_image=img_figurinha, size=(150, 150))
                
                figurinha_desbloqueada_label = ctk.CTkLabel(janela, image=img_ctk_figurinha, text="")
                figurinha_desbloqueada_label.place(relx=0.5, rely=0.3, anchor="center")
                
                janela.update_idletasks()
                janela.after(100, lambda: None) # Pequeno atraso para garantir renderização
                janela.after(5000, lambda: figurinha_desbloqueada_label.destroy() if figurinha_desbloqueada_label else None)

            except Exception: # Captura FileNotFoundError e outros erros de imagem
                print(f"Erro ao exibir figurinha temporária: {figurinha_nova_path}")
    
    carregar_ranking()
    ranking_semanal[usuario] = ranking_semanal.get(usuario, 0) + 1
    salvar_ranking()


def inicializar_estado_diario():
    global copo_canvas, meta_diaria_ml, dias_consecutivos

    progresso_do_dia_carregado = 0.0
    meta_salva_do_usuario = 0
    ultimo_uso_str = None
    
    try:
        with open(ARQUIVO_DADOS_USUARIO, 'r') as f:
            for line in f:
                parts = line.strip().split(';')
                if len(parts) >= 6 and parts[0] == usuario:
                    colecao_figurinhas.clear()
                    colecao_figurinhas.extend(parts[1].split(',') if parts[1] else [])
                    dias_consecutivos = int(parts[2])
                    ultimo_uso_str = parts[3]
                    progresso_do_dia_carregado = float(parts[4])
                    meta_salva_do_usuario = int(float(parts[5]))
                    break
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Erro ao ler dados do usuário para inicialização diária: {e}")

    hoje = datetime.now().date()

    if ultimo_uso_str:
        ultimo_uso_data = datetime.strptime(ultimo_uso_str, "%Y-%m-%d").date()
    else:
        ultimo_uso_data = None

    copo_canvas_progresso_para_hoje = 0.0

    if ultimo_uso_data != hoje:
        if ultimo_uso_data and progresso_do_dia_carregado >= meta_salva_do_usuario and meta_salva_do_usuario > 0:
            dias_consecutivos += 1
            verificar_e_desbloquear_premio()
        else:
            dias_consecutivos = 0
        copo_canvas_progresso_para_hoje = 0.0
    else:
        copo_canvas_progresso_para_hoje = progresso_do_dia_carregado

    if copo_canvas is not None:
        copo_canvas.progresso = copo_canvas_progresso_para_hoje
    
    user_data_to_save = {
        "figurinhas": colecao_figurinhas,
        "dias_consecutivos": dias_consecutivos,
        "ultimo_uso": hoje.strftime("%Y-%m-%d"),
        "progresso_dia": copo_canvas_progresso_para_hoje,
        "meta_diaria_ml": meta_diaria_ml
    }

    all_users_data_for_save = {}
    try:
        with open(ARQUIVO_DADOS_USUARIO, 'r') as f:
            for line in f:
                parts = line.strip().split(';')
                if len(parts) >= 6:
                    all_users_data_for_save[parts[0]] = {
                        "figurinhas": parts[1],
                        "dias_consecutivos": parts[2],
                        "ultimo_uso": parts[3],
                        "progresso_dia": parts[4],
                        "meta_diaria_ml": parts[5]
                    }
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Erro ao ler todos os dados para salvar na inicialização diária: {e}")

    all_users_data_for_save[usuario] = {
        "figurinhas": ','.join(user_data_to_save["figurinhas"]),
        "dias_consecutivos": str(user_data_to_save["dias_consecutivos"]),
        "ultimo_uso": user_data_to_save["ultimo_uso"],
        "progresso_dia": str(user_data_to_save["progresso_dia"]),
        "meta_diaria_ml": str(user_data_to_save["meta_diaria_ml"])
    }

    with open(ARQUIVO_DADOS_USUARIO, 'w') as f:
        for user_key, data in all_users_data_for_save.items():
            line_to_write = f"{user_key};{data['figurinhas']};{data['dias_consecutivos']};{data['ultimo_uso']};{data['progresso_dia']};{data['meta_diaria_ml']}\n"
            f.write(line_to_write)


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

    usuario_cad = nome.get()
    senha_cad = senha.get()

    if usuario_cad and senha_cad:
        salvar_credenciais(usuario_cad, senha_cad)

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

    button_log2 = ctk.CTkButton(janela, text="Login", font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
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
        fundo_label.configure(image=img_ctk3)
        senha2.place_forget()
        button_log2.place_forget()
        nome2.place_forget()

        if erro_login:
            erro_login.destroy()
            erro_login = None
        
        usuario = usuario_digitado
        
        carregar_dados_usuario() 
        resetar_semana_ranking() 
        inicializar_estado_diario() 
        
        tela_configuracoes()

    else:
        if erro_login:
            erro_login.destroy()

        erro_login = ctk.CTkLabel(janela, text="Usuário ou senha incorretos", text_color="red",
                                  font=ctk.CTkFont(size=15, weight="bold"), fg_color='#f3f3f3')
        erro_login.place(relx=0.52, rely=0.60, anchor="center")

        imagem_erro = CTkLabel(janela, image=img_erro, text="")
        imagem_erro.place(relx=0.50, rely=0.55, anchor="center")
        janela.after(1500, imagem_erro.destroy)


def tela_principal():
    global litros, intervalo, horario_ini, horario_fin, button3, texto
    global copo_canvas, botao_beber, progresso_texto
    global meta_diaria_ml, dias_consecutivos

    for widget in janela.winfo_children():
        widget.place_forget()

    fundo_label.configure(image=img_ctk3)

    texto = ctk.CTkLabel(janela, text=f"Olá {usuario}, acompanhe sua hidratação diária!", font=ctk.CTkFont(size=24, weight="bold"))
    texto.place(relx=0.5, rely=0.1, anchor="center")

    copo_canvas = ctk.CTkCanvas(janela, width=200, height=400, bg="#f3f3f3", highlightthickness=0)
    copo_canvas.place(relx=0.5, rely=0.55, anchor="center")

    copo_canvas.create_rectangle(50, 20, 150, 380, outline="#000", width=3)

    if not hasattr(copo_canvas, 'progresso'):
        copo_canvas.progresso = 0.0
    
    if meta_diaria_ml == 0:
        carregar_dados_usuario() 
        if meta_diaria_ml == 0:
            meta_diaria_ml = 2000


    def atualizar_copo():
        copo_canvas.delete("agua")

        altura_total = 360
        altura_agua = int((copo_canvas.progresso / meta_diaria_ml) * altura_total)
        if altura_agua > altura_total:
            altura_agua = altura_total

        copo_canvas.create_rectangle(51, 380 - altura_agua, 149, 380, fill="#00bfff", width=0, tags="agua")

        progresso_texto.configure(text=f"{copo_canvas.progresso:.0f} ml / {meta_diaria_ml} ml")

        if copo_canvas.progresso >= meta_diaria_ml:
            progresso_texto.configure(text_color="green", text=f"Meta diária atingida! Parabéns!")
        else:
            progresso_texto.configure(text_color="black")

    def beber_agua():
        copo_canvas.progresso += (qtd_por_lembrete*1000)
        if copo_canvas.progresso > meta_diaria_ml:
            copo_canvas.progresso = meta_diaria_ml
        atualizar_copo()
        salvar_dados_usuario()

    botao_beber = ctk.CTkButton(janela, text=f'beber {qtd_por_lembrete*1000} ml', command=beber_agua, width=150, height=50)
    botao_beber.place(relx=0.5, rely=0.9, anchor="center")

    progresso_texto = ctk.CTkLabel(janela, text=f"{copo_canvas.progresso:.0f} ml / {meta_diaria_ml} ml", font=ctk.CTkFont(size=16))
    progresso_texto.place(relx=0.5, rely=0.8, anchor="center")

    button_ranking = ctk.CTkButton(janela, text="Ver Ranking", command=mostrar_ranking, width=120, height=40)
    button_ranking.place(relx=0.1, rely=0.9, anchor="center")

    button_figurinhas = ctk.CTkButton(janela, text="Minhas Figurinhas", command=mostrar_colecao_figurinhas, width=150, height=40)
    button_figurinhas.place(relx=0.9, rely=0.9, anchor="center")

    atualizar_copo()


def button3_acao():
    global erro, qtd_lembretes, qtd_por_lembrete, meta_diaria_ml

    if erro:
        erro.destroy()
        erro = None

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

        salvar_dados_usuario()

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


def mostrar_ranking():
    carregar_ranking()

    janela_ranking = ctk.CTkToplevel(janela)
    janela_ranking.title("Ranking Semanal de Hidratação")
    janela_ranking.geometry("400x400")
    
    janela_ranking.update_idletasks()
    janela_ranking.grab_set()

    ctk.CTkLabel(janela_ranking, text="Ranking Semanal", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

    ranking_para_exibir = {k: v for k, v in ranking_semanal.items() if k != "ultima_reset_semana"}
    ranking_ordenado = sorted(ranking_para_exibir.items(), key=lambda item: item[1], reverse=True)

    if not ranking_ordenado:
        ctk.CTkLabel(janela_ranking, text="Nenhum dado no ranking ainda.", font=ctk.CTkFont(size=14)).pack(pady=5)
    else:
        for i, (user, dias) in enumerate(ranking_ordenado):
            ctk.CTkLabel(janela_ranking, text=f"{i+1}. {user}: {dias} dias com a meta batida", font=ctk.CTkFont(size=16)).pack(pady=2)

    ctk.CTkButton(janela_ranking, text="Fechar", command=janela_ranking.destroy).pack(pady=20)


def mostrar_colecao_figurinhas():
    carregar_dados_usuario()

    janela_figurinhas = ctk.CTkToplevel(janela)
    janela_figurinhas.title("Minhas Figurinhas")
    janela_figurinhas.geometry("600x600")
    
    janela_figurinhas.update_idletasks()
    janela_figurinhas.grab_set()

    ctk.CTkLabel(janela_figurinhas, text="Sua Coleção de Figurinhas", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

    frame_figurinhas = ctk.CTkScrollableFrame(janela_figurinhas, width=550, height=450)
    frame_figurinhas.pack(pady=10, padx=10, fill="both", expand=True)

    if not colecao_figurinhas:
        ctk.CTkLabel(frame_figurinhas, text="Você ainda não desbloqueou nenhuma figurinha. Continue se hidratando!", font=ctk.CTkFont(size=14)).pack(pady=10)
    
    col = 0
    row = 0
    for i, figurinha_path in enumerate(todas_figurinhas):
        try:
            img_figurinha_preview = Image.open(figurinha_path)
            img_ctk_figurinha_preview = CTkImage(light_image=img_figurinha_preview, dark_image=img_figurinha_preview, size=(100, 100))

            if figurinha_path in colecao_figurinhas:
                label_status = "Desbloqueada"
                text_color = "green"
            else:
                label_status = "Bloqueada"
                text_color = "red"

            frame_item = ctk.CTkFrame(frame_figurinhas)
            frame_item.grid(row=row, column=col, padx=10, pady=10)

            label_img = ctk.CTkLabel(frame_item, image=img_ctk_figurinha_preview, text="")
            label_img.image = img_ctk_figurinha_preview
            label_img.pack()
            
            ctk.CTkLabel(frame_item, text=f"Figurinha {i+1}", font=ctk.CTkFont(size=12)).pack()
            ctk.CTkLabel(frame_item, text=label_status, text_color=text_color, font=ctk.CTkFont(size=12, weight="bold")).pack()

            col += 1
            if col > 3:
                col = 0
                row += 1
        except Exception:
            # Exibe um placeholder genérico se a imagem não puder ser carregada
            frame_item = ctk.CTkFrame(frame_figurinhas)
            frame_item.grid(row=row, column=col, padx=10, pady=10)
            ctk.CTkLabel(frame_item, text="[IMG ERRO]", font=ctk.CTkFont(size=10), text_color="red").pack()
            ctk.CTkLabel(frame_item, text=f"Figurinha {i+1}", font=ctk.CTkFont(size=12)).pack()
            ctk.CTkLabel(frame_item, text="Erro", text_color="red", font=ctk.CTkFont(size=12, weight="bold")).pack()
            col += 1
            if col > 3:
                col = 0
                row += 1

    ctk.CTkButton(janela_figurinhas, text="Fechar", command=janela_figurinhas.destroy).pack(pady=20)


# Botões iniciais
button_cad = ctk.CTkButton(janela, text="clique aqui", font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
                           width=100, height=50, command=cadastro, fg_color='#4682B4', corner_radius=50)
button_cad.place(relx=0.70, rely=0.5, anchor="center")

button_log = ctk.CTkButton(janela, text="clique aqui", font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
                           width=100, height=50, command=login, fg_color='#4682B4', corner_radius=50)
button_log.place(relx=0.70, rely=0.72, anchor="center")


janela.mainloop()