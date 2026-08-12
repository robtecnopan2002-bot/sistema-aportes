import customtkinter as ctk

# Configuração global do tema visual (Passo 4)
ctk.set_appearance_mode("dark")  # Ativa o modo escuro nativo

class AplicativoRCB(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da Janela
        self.title("RCB Aportes - FIN-APORT-2026-OK")
        self.geometry("850x600")
        self.configure(fg_color="#031430")  # Azul Marinho Escuro do fundo do logo

        # Cores Oficiais da Identidade Visual (RCB)
        self.cor_dourado = "#B59453"       # Tom da seta de crescimento
        self.cor_card_fundo = "#081F42"    # Azul ligeiramente mais claro para contraste
        self.cor_texto = "#FFFFFF"         # Branco do logotipo

        self.criar_layout()

    def criar_layout(self):
        # 1. CABEÇALHO (Header)
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=25, padx=40, fill="x")

        self.label_logo = ctk.CTkLabel(
            self.header_frame, 
            text="RCB", 
            font=ctk.CTkFont(family="Georgia", size=42, weight="bold"),
            text_color=self.cor_texto
        )
        self.label_logo.pack(side="left")

        self.label_subtitulo = ctk.CTkLabel(
            self.header_frame, 
            text="  A P O R T E S", 
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            text_color=self.cor_dourado
        )
        self.label_subtitulo.pack(side="left", pady=15)

        # 2. CARD DE RESUMO (Métricas Principais)
        self.card_resumo = ctk.CTkFrame(self, fg_color=self.cor_card_fundo, corner_radius=12, border_color=self.cor_dourado, border_width=1)
        self.card_resumo.pack(pady=10, padx=40, fill="x")

        self.lbl_titulo_card = ctk.CTkLabel(self.card_resumo, text="TOTAL APORTADO", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.cor_dourado)
        self.lbl_titulo_card.pack(pady=(15, 5), padx=20, anchor="w")

        self.lbl_valor_card = ctk.CTkLabel(self.card_resumo, text="R$ 150.000,00", font=ctk.CTkFont(size=32, weight="bold"), text_color=self.cor_texto)
        self.lbl_valor_card.pack(pady=(0, 15), padx=20, anchor="w")

        # 3. FORMULÁRIO DE ENTRADA (Onde o usuário digita os dados)
        self.form_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.form_frame.pack(pady=30, padx=40, fill="x")

        # Campo: Valor do Aporte
        self.lbl_valor = ctk.CTkLabel(self.form_frame, text="Valor do Aporte (R$):", text_color=self.cor_texto, font=ctk.CTkFont(size=14))
        self.lbl_valor.grid(row=0, column=0, padx=(0, 20), sticky="w")
        
        self.entry_valor = ctk.CTkEntry(self.form_frame, width=200, fg_color=self.cor_card_fundo, border_color=self.cor_dourado, text_color=self.cor_texto)
        self.entry_valor.grid(row=1, column=0, padx=(0, 20), pady=(5, 0), sticky="w")

        # Campo: Descrição/Cliente
        self.lbl_cliente = ctk.CTkLabel(self.form_frame, text="Identificação do Cliente / Teste:", text_color=self.cor_texto, font=ctk.CTkFont(size=14))
        self.lbl_cliente.grid(row=0, column=1, sticky="w")

        self.entry_cliente = ctk.CTkEntry(self.form_frame, width=300, fg_color=self.cor_card_fundo, border_color=self.cor_dourado, text_color=self.cor_texto)
        self.entry_cliente.grid(row=1, column=1, pady=(5, 0), sticky="w")

        # 4. BOTÃO DE AÇÃO (Estilizado em Dourado)
        self.btn_salvar = ctk.CTkButton(
            self, 
            text="CONFIRMAR APORTE", 
            fg_color=self.cor_dourado, 
            text_color="#031430",  # Texto escuro para dar contraste no botão dourado
            hover_color="#94763E", 
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            corner_radius=8,
            command=self.acao_salvar_aporte
        )
        self.btn_salvar.pack(pady=20, padx=40, fill="x")

        def acao_salvar_aporte(self):
        import pandas as pd
        from tkinter import messagebox
        import os

        # 1. Captura e limpa espaços extras do texto digitado
        cliente_procurado = self.entry_cliente.get().strip()
        valor_aporte = self.entry_valor.get().strip()

        if not cliente_procurado:
            messagebox.showwarning("Aviso", "Por favor, digite o nome do cliente!")
            return

        caminho_planilha = "clientes_cadastro.xlsx"  # Ajuste para o seu arquivo real

        try:
            if not os.path.exists(caminho_planilha):
                messagebox.showerror("Erro", f"Planilha '{caminho_planilha}' não encontrada!")
                return

            # 2. Carrega a planilha
            df = pd.read_excel(caminho_planilha)

            # 3. NORMALIZAÇÃO PARA VALIDAÇÃO (Garante que espaços ou maiúsculas não quebrem a busca)
            # Cria cópias temporárias em minúsculo e sem espaços para comparar com segurança
            cliente_busca_limpo = cliente_procurado.lower()
            coluna_cliente_limpa = df['Cliente'].astype(str).str.strip().str.lower()

            # 4. Procura o cliente na lista normalizada
            if cliente_busca_limpo in coluna_cliente_limpa.values:
                
                # Encontra a posição (índice) exata da linha na planilha
                indice_cliente = coluna_cliente_limpa[coluna_cliente_limpa == cliente_busca_limpo].index

                # 5. GRAVAÇÃO FORÇADA (Usa o índice localizado para garantir a alteração)
                df.loc[indice_cliente, 'Status'] = 'Aprovado'
                
                if valor_aporte:
                    df.loc[indice_cliente, 'Valor'] = valor_aporte

                # 6. Salva o arquivo de volta
                df.to_excel(caminho_planilha, index=False)

                messagebox.showinfo("Sucesso", f"Validação Concluída!\nCliente '{cliente_procurado}' agora é um CLIENTE APROVADO.")
                
                # Limpa os campos
                self.entry_valor.delete(0, "end")
                self.entry_cliente.delete(0, "end")
            
            else:
                # Se cair aqui, o nome digitado realmente não existe igual na planilha
                messagebox.showwarning("Não Encontrado", f"O cliente '{cliente_procurado}' não foi localizado.\nVerifique a grafia exata na planilha.")

        except PermissionError:
            messagebox.showerror("Erro de Permissão", "Feche o arquivo Excel antes de dar o aceite!")
        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Falha na validação: {e}")
