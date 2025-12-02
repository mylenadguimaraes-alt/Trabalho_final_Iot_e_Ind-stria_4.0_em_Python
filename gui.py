import tkinter as tk
from tkinter import messagebox
from auth import validar_codigo, validar_admin, criar_admin
from database import create_user
from arduino_comm import ArduinoController

# Inicializa Arduino (modo simulação se porta ocupada ou desconectada)
arduino = ArduinoController(porta="/dev/ttyACM0")


class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Controle de Acesso")
        self.window.geometry("320x420")

        self.violated = False
        self.system_armed = True

        arduino.callback = self.receber_msg_arduino

        self.show_home()
        self.window.mainloop()

    # ---------------- MENSAGENS DO ARDUINO ----------------
    def receber_msg_arduino(self, msg):
        print("ARDUINO:", msg)

        if msg == "unauthorized_open":
            self.violated = True
            messagebox.showerror("VIOLAÇÃO", "🚨 Porta violada!\nSistema travado!")
        elif msg == "Sistema_armado":
            messagebox.showinfo("OK", "Sistema armado.")
        elif msg == "Sistema_desarmado":
            messagebox.showinfo("OK", "Sistema desarmado.")
        elif msg == "Alarme_parado":
            messagebox.showinfo("OK", "Alarme parado.")
        elif msg == "Autorizacao_recebida":
            messagebox.showinfo("OK", "Acesso autorizado.")
        elif msg == "porta_fechada_apos_autorizacao":
            print("Porta fechada após autorização - aguardando rearmamento automático")
        elif msg == "Sistema_armado_automaticamente":
            self.system_armed = True
            messagebox.showinfo("Sistema Rearmado", "✅ Porta trancada\nSistema rearmado automaticamente!")

    # ---------------- TELA PRINCIPAL ----------------------
    def show_home(self):
        self.clear()

        tk.Label(self.window, text="Digite sua chave:",
                 font=("Arial", 12)).pack(pady=10)

        self.codigo_entry = tk.Entry(self.window, font=("Arial", 18), justify="center")
        self.codigo_entry.pack()

        tk.Button(self.window, text="ENTRAR",
                  font=("Arial", 14),
                  command=self.validar_entrada).pack(pady=20)

        tk.Button(self.window, text="Entrar como Admin",
                  command=self.show_admin_login).pack()

    # ---------------- USUÁRIO ENTRA -----------------------
    def validar_entrada(self):
        if self.violated:
            messagebox.showerror("Bloqueado", "Sistema violado! Só o admin libera.")
            return

        codigo = self.codigo_entry.get().strip()
        user = validar_codigo(codigo)

        if user:
            messagebox.showinfo("OK", f"Bem-vindo {user[0]}")
            arduino.authorize()
        else:
            messagebox.showerror("Erro", "Código inválido.")

    # ---------------- ADMIN LOGIN ------------------------
    def show_admin_login(self):
        self.clear()

        tk.Label(self.window, text="Nome Admin:", font=("Arial", 12)).pack(pady=5)
        self.admin_nome_entry = tk.Entry(self.window)
        self.admin_nome_entry.pack()

        tk.Label(self.window, text="Senha Admin:", font=("Arial", 12)).pack(pady=5)
        self.admin_senha_entry = tk.Entry(self.window, show="*")
        self.admin_senha_entry.pack()

        tk.Button(self.window, text="Entrar", command=self.validar_login_admin).pack(pady=15)
        tk.Button(self.window, text="Voltar", command=self.show_home).pack()

    def validar_login_admin(self):
        nome = self.admin_nome_entry.get().strip()
        senha = self.admin_senha_entry.get().strip()

        if validar_admin(nome, senha):
            self.show_admin_panel()
        else:
            messagebox.showerror("Erro", "Nome ou senha incorretos!")

    # ---------------- PAINEL ADMIN -----------------------
    def show_admin_panel(self):
        self.clear()

        tk.Label(self.window, text="Painel Admin",
                 font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(self.window, text="Criar Usuário",
                  command=self.show_create_user).pack(pady=10)

        tk.Button(self.window, text="Criar Admin",
                  command=self.show_create_admin).pack(pady=10)

        tk.Button(self.window, text="Desativar Alarme",
                  bg="red", fg="white",
                  command=self.parar_alarme).pack(pady=10)

        tk.Button(self.window, text="Armar Sistema",
                  bg="green", fg="white",
                  command=self.armar_sistema).pack(pady=10)

        tk.Button(self.window, text="Desarmar Sistema",
                  bg="orange", fg="black",
                  command=self.desarmar_sistema).pack(pady=10)

        tk.Button(self.window, text="Voltar",
                  command=self.show_home).pack(pady=15)

    def parar_alarme(self):
        arduino.stop_alarm()
        self.violated = False
        messagebox.showinfo("OK", "Alarme parado.")

    def armar_sistema(self):
        arduino.arm_system()
        self.system_armed = True

    def desarmar_sistema(self):
        arduino.disarm_system()
        self.system_armed = False
        self.violated = False

    # ---------------- CRIA USUÁRIOS ----------------------
    def show_create_user(self):
        self.clear()

        tk.Label(self.window, text="Nome:", font=("Arial", 12)).pack()
        self.nome_entry = tk.Entry(self.window)
        self.nome_entry.pack()

        tk.Label(self.window, text="Senha:", font=("Arial", 12)).pack()
        self.senha_entry = tk.Entry(self.window, show="*")
        self.senha_entry.pack()

        tk.Button(self.window, text="Criar", command=self.criar_usuario).pack(pady=10)
        tk.Button(self.window, text="Voltar", command=self.show_admin_panel).pack()

    def criar_usuario(self):
        nome = self.nome_entry.get().strip()
        senha = self.senha_entry.get().strip()

        if not nome or not senha:
            messagebox.showerror("Erro", "Preencha tudo.")
            return

        codigo = create_user(nome, senha)
        messagebox.showinfo("OK", f"Usuário criado!\nCódigo: {codigo}")
        self.show_admin_panel()

    # ---------------- CRIA ADMINS ----------------------
    def show_create_admin(self):
        self.clear()

        tk.Label(self.window, text="Nome Admin:", font=("Arial", 12)).pack()
        self.admin_nome_entry = tk.Entry(self.window)
        self.admin_nome_entry.pack()

        tk.Label(self.window, text="Senha Admin:", font=("Arial", 12)).pack()
        self.admin_senha_entry = tk.Entry(self.window, show="*")
        self.admin_senha_entry.pack()

        tk.Button(self.window, text="Criar", command=self.criar_admin).pack(pady=10)
        tk.Button(self.window, text="Voltar", command=self.show_admin_panel).pack()

    def criar_admin(self):
        nome = self.admin_nome_entry.get().strip()
        senha = self.admin_senha_entry.get().strip()

        if not nome or not senha:
            messagebox.showerror("Erro", "Preencha tudo.")
            return

        if criar_admin(nome, senha):
            messagebox.showinfo("OK", f"Admin criado: {nome}")
        else:
            messagebox.showerror("Erro", "Nome de admin já existe.")

        self.show_admin_panel()

    # ---------------- LIMPAR TELA ------------------------
    def clear(self):
        for widget in self.window.winfo_children():
            widget.destroy()
