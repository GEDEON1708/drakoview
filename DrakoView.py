import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


# Classe Dragão
class Dragao:
    def __init__(self, nome, imagem_url, descricao, idade, peso, montador, casa):
        self.nome = nome
        self.imagem_url = imagem_url
        self.descricao = descricao
        self.idade = idade
        self.peso = peso
        self.montador = montador
        self.casa = casa

    def get_nome(self):
        return self.nome

    def get_imagem_url(self):
        return self.imagem_url

    def get_descricao(self):
        return self.descricao

    def get_idade(self):
        return self.idade

    def get_peso(self):
        return self.peso

    def get_montador(self):
        return self.montador

    def get_casa(self):
        return self.casa


# Classe ColecaoDragoes
class ColecaoDragoes:
    def __init__(self):
        self.dragoes = []

    def adicionar_dragao(self, dragao):
        self.dragoes.append(dragao)

    def buscar_dragao(self, nome):
        for dragao in self.dragoes:
            if dragao.get_nome().lower() == nome.lower():  # Verificação exata para correspondência
                return dragao
        raise Exception(f"Dragão '{nome}' não encontrado.")  # Mensagem clara se não encontrar


# Classe Buscador
class Buscador:
    def __init__(self, colecao):
        self.colecao = colecao

    def busca(self, criterio_nome=None):
        resultados = []
        for dragao in self.colecao.dragoes:
            if criterio_nome and criterio_nome.lower() == dragao.get_nome().lower():  # Verificação exata
                resultados.append(dragao)
        return resultados


# Classe MenuPrincipal (interface gráfica)
class MenuPrincipal:
    def __init__(self, colecao):
        self.colecao = colecao
        self.root = tk.Tk()
        self.root.title("Visualizador de Dragões")
        self.root.geometry("800x600")  # Tamanho padrão da janela

        # Carrega a imagem de fundo
        self.fundo = Image.open("imagens/img-fundo.jpg")

        # Label com imagem de fundo
        self.label_fundo = tk.Label(self.root)
        self.label_fundo.place(x=0, y=0)

        self.criar_interface()
        self.redimensionar_fundo()  # Ajuste da imagem de fundo ao iniciar

        # Ligação do evento de redimensionamento da janela
        self.root.bind("<Configure>", self.redimensionar_fundo)

    def criar_interface(self):
        # Mensagem de boas-vindas
        tk.Label(self.root, text="Bem-vindo ao Dragon View!", font=("Helvetica", 20, "bold"), bg='black',
                 fg='white').pack(pady=10)

        tk.Label(self.root, text="Procure um Dragão por Nome", font=("Helvetica", 16), bg='black', fg='white').pack(
            pady=5)

        # Caixa de entrada para o nome do dragão
        self.entry_nome = tk.Entry(self.root, font=("Helvetica", 16))
        self.entry_nome.pack(pady=10, padx=10)
        self.entry_nome.insert(0, "Digite o Nome do Dragão")
        self.entry_nome.bind("<FocusIn>", self.limpar_campo)  # Limpa o campo ao clicar

        # Botão para pesquisar
        botao = tk.Button(self.root, text="Pesquisar", command=self.pesquisar_dragao, font=("Helvetica", 16))
        botao.pack(pady=5)

        # Área para mostrar a imagem do dragão
        self.imagem_label = tk.Label(self.root)
        self.imagem_label.pack(pady=10)

        # Área para mostrar informações
        self.info_frame = tk.Frame(self.root, bg='black')
        self.info_frame.pack(pady=10)

        # Labels para exibir informações, alinhadas de forma consistente
        self.nome_label = tk.Label(self.info_frame, text="", font=("Helvetica", 16), bg='black', fg='white')
        self.nome_label.pack(anchor='w', padx=10)

        self.descricao_label = tk.Label(self.info_frame, text="", wraplength=400, font=("Helvetica", 14), bg='black',
                                        fg='white')
        self.descricao_label.pack(anchor='w', padx=10)

        self.idade_label = tk.Label(self.info_frame, text="", font=("Helvetica", 14), bg='black', fg='white')
        self.idade_label.pack(anchor='w', padx=10)

        self.peso_label = tk.Label(self.info_frame, text="", font=("Helvetica", 14), bg='black', fg='white')
        self.peso_label.pack(anchor='w', padx=10)

        self.montador_label = tk.Label(self.info_frame, text="", font=("Helvetica", 14), bg='black', fg='white')
        self.montador_label.pack(anchor='w', padx=10)

        self.casa_label = tk.Label(self.info_frame, text="", font=("Helvetica", 14), bg='black', fg='white')
        self.casa_label.pack(anchor='w', padx=10)

    def limpar_campo(self, event):
        self.entry_nome.delete(0, tk.END)  # Limpa o campo de entrada
        self.entry_nome.insert(0, "")  # Insere um texto vazio

    def redimensionar_fundo(self, event=None):
        # Ajusta a imagem de fundo de acordo com o tamanho da janela
        largura = self.root.winfo_width()
        altura = self.root.winfo_height()
        fundo_redimensionado = self.fundo.resize((largura, altura))
        self.fundo_tk = ImageTk.PhotoImage(fundo_redimensionado)
        self.label_fundo.config(image=self.fundo_tk)
        self.label_fundo.image = self.fundo_tk  # Evita coleta de lixo

    def pesquisar_dragao(self):
        # Obtém os valores dos campos de entrada
        nome_dragao = self.entry_nome.get().strip()

        # Verifica se o campo foi preenchido
        if not nome_dragao:
            messagebox.showinfo("Erro", "Por favor, insira um nome de dragão.")
            return

        buscador = Buscador(self.colecao)
        try:
            resultados = buscador.busca(criterio_nome=nome_dragao)
            if resultados:
                # Exibe as informações do dragão encontrado
                dragao = resultados[0]
                self.atualizar_interface(dragao)
                self.entry_nome.delete(0, tk.END)  # Limpa o campo de entrada
            else:
                messagebox.showinfo("Resultado",
                                    f"Nenhum dragão encontrado com o nome '{nome_dragao}'.")  # Mensagem específica
                self.entry_nome.delete(0, tk.END)  # Limpa o campo de entrada
        except Exception as e:
            messagebox.showinfo("Erro", str(e))

    def atualizar_interface(self, dragao):
        # Tente carregar a imagem local
        try:
            imagem = Image.open(dragao.get_imagem_url())
            imagem = imagem.resize((400, 300))
            imagem_tk = ImageTk.PhotoImage(imagem)

            # Atualiza a label com a nova imagem
            self.imagem_label.config(image=imagem_tk)
            self.imagem_label.image = imagem_tk

            # Atualiza as informações do dragão
            self.nome_label.config(text=f"Nome: {dragao.get_nome()}")
            self.descricao_label.config(text=f"Descrição: {dragao.get_descricao()}")
            self.idade_label.config(text=f"Idade: {dragao.get_idade()} anos")
            self.peso_label.config(text=f"Peso: {dragao.get_peso()} kg")
            self.montador_label.config(text=f"Montador: {dragao.get_montador()}")
            self.casa_label.config(text=f"Casa: {dragao.get_casa()}")
        except Exception as e:
            print(f"Erro ao tentar carregar a imagem: {e}")
            self.descricao_label.config(text="Erro ao carregar a imagem.")


def main():
    colecao = ColecaoDragoes()

    colecao.adicionar_dragao(
        Dragao("Asa Prata", "imagens/Asaprata.jpg", "Dragão Asa Prata lendário.", 200, 1000, "Daenerys Targaryen",
               "Casa Targaryen"))
    colecao.adicionar_dragao(
        Dragao("Caraxes", "imagens/Caraxes.jpg", "Dragão Caraxes majestoso.", 150, 850, "Daemon Targaryen",
               "Casa Targaryen"))
    colecao.adicionar_dragao(
        Dragao("Syrax", "imagens/Syrax.jpg", "Dragão Syrax lendário.", 120, 800, "Rhaenyra Targaryen",
               "Casa Targaryen"))
    colecao.adicionar_dragao(
        Dragao("Vhagar", "imagens/vhagarwar.jpg", "Dragão Vhagar majestoso.", 250, 1100, "Aemond Targaryen",
               "Casa Targaryen"))

    colecao.adicionar_dragao(
        Dragao("Drogon", "imagens/Drogon.jpg", "Drogon, o Sombrio.", None, 1000, "Daenerys Targaryen",
               "Casa Targaryen"))

    colecao.adicionar_dragao(
        Dragao("Meleys", "imagens/Meleys.jpg", "Dragão Meleys, a Sanguinária.", 60, 2500, "A rainha Rhaenys Targaryen",
               "Casa Targaryen"))

    colecao.adicionar_dragao(
        Dragao("Seasmoke", "imagens/Seasmoke.jpg", "O Dragão da Tempestade.", 35, 2000, "Laenor Velaryon",
               "Casa Velaryon"))

    colecao.adicionar_dragao(
        Dragao("Vermithor", "imagens/Vermithor.jpg", "A Fúria de Bronze.", 250, 3000, "Hugh Hammer", "Casa Targaryen"))

    menu = MenuPrincipal(colecao)
    menu.root.mainloop()


if __name__ == "__main__":
    main()
