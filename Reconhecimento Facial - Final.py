import os
import cvzone
import pickle
import cv2
import face_recognition
import numpy as np
import openpyxl
import customtkinter
from tkinter import messagebox
from PIL import Image, ImageTk
import webbrowser
import tkinter as tk
import tkinter as Tk
import pandas as pd
from customtkinter import CTkImage

customtkinter.set_appearance_mode("light")

# Utilização da classe
folder_path = 'Pessoas'
excel_file_path = r'C:\Users\Pichau\Desktop\VISAO_COMPUTACIONAL\Dados coletados.xlsx'
background_image = 'Background Safe Vision - Rec. Facial.png'
mode_folder_path = 'Resources/Modes'


# Exemplo de função que mostra a messagebox sem abrir uma janela adicional do Tkinter
def mostrar_messagebox(titulo, mensagem):
    # Cria uma instância de Tk
    root = tk.Tk()

    # Oculta a janela principal
    root.withdraw()

    # Mostra a messagebox
    messagebox.showinfo(titulo, mensagem)

    # Fecha a instância de Tk após a messagebox ser fechada
    root.destroy()

# Exemplo de função que mostra a messagebox sem abrir uma janela adicional do Tkinter
def mostrar_messagebox2(titulo, mensagem):
    # Cria uma instância de Tk
    root = tk.Tk()

    # Oculta a janela principal
    root.withdraw()

    # Mostra a messagebox
    messagebox.showinfo(titulo, mensagem)

    # Fecha a instância de Tk após a messagebox ser fechada
    root.destroy()

# Exemplo de função que mostra a messagebox sem abrir uma janela adicional do Tkinter
def mostrar_messagebox3(titulo, mensagem):
    # Cria uma instância de Tk
    root = tk.Tk()

    # Oculta a janela principal
    root.withdraw()

    # Mostra a messagebox
    messagebox.showinfo(titulo, mensagem)

    # Fecha a instância de Tk após a messagebox ser fechada
    root.destroy()


class Confirmar_id(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x700")
        self.title("Confirmar ID")
        self.attributes('-fullscreen', True)  # Tela cheia
        self.banner_path = "Banner Safe Vision Formulário (1200 x 800 px).png"
        self.banner_image = Image.open(self.banner_path)
        self.motorista_dados = {}  # Dicionário para armazenar dados do motorista
        self.setup_ui()

    def redimensionar_banner(self):
        banner_width, banner_height = self.banner_image.size
        proporcao = banner_width / banner_height
        nova_largura = self.winfo_width()
        nova_altura = int(nova_largura / proporcao)
        return self.banner_image.resize((nova_largura, nova_altura), Image.LANCZOS)

    def setup_ui(self):
        customtkinter.CTkLabel(self, font=("Arial", 30), text="").pack(padx=10, pady=10)
        self.banner_redimensionado = self.redimensionar_banner()
        self.banner_tk = ImageTk.PhotoImage(self.banner_redimensionado)
        banner_label = customtkinter.CTkLabel(self, image=self.banner_tk, text="")
        banner_label.pack(side="top", fill="x")

        customtkinter.CTkLabel(self, font=("Arial", 30), text="").pack(padx=10, pady=5)
        customtkinter.CTkLabel(self, font=("Arial", 30), text="Confirmação de ID do motorista").pack(padx=10, pady=10)
        customtkinter.CTkLabel(self, font=("Arial", 15), text="").pack(padx=10, pady=10)

        customtkinter.CTkLabel(self, font=("Arial", 15),
                               text="Insira abaixo o seu ID novamente, exemplo: joao_silva.jpg").pack(padx=10, pady=0)
        self.id_entry = customtkinter.CTkEntry(self, width=300, placeholder_text="Digite aqui o seu ID")
        self.id_entry.pack(padx=10, pady=0)
        customtkinter.CTkLabel(self, font=("Arial", 15),
                               text="Utilize o ID que foi cadastrado anteriormente\nSomente letras minúsculas\nUtilize o _ entre o seu nome e sobrenome\nDeve conter .jpg no final").pack(
            padx=10, pady=0)
        customtkinter.CTkLabel(self, font=("Arial", 15), text="").pack(padx=10, pady=0)

        frame_botoes = customtkinter.CTkFrame(self, fg_color="transparent")
        frame_botoes.pack(pady=20)

        coluna1 = customtkinter.CTkFrame(frame_botoes, fg_color="transparent")
        coluna1.grid(row=0, column=0, padx=20)

        customtkinter.CTkButton(coluna1, text="Buscar ID", command=self.buscar, fg_color="#0D6AD8").pack(pady=10)
        customtkinter.CTkButton(coluna1, text="Salvar dados temporariamente", command=self.salvar_id, fg_color="#0D6AD8").pack(pady=10)
        customtkinter.CTkButton(coluna1, text="Avançar", command=self.avancar_etapa, fg_color="#0D6AD8").pack(pady=10)
        customtkinter.CTkButton(coluna1, text="Encerrar programa", command=self.encerrar_prog, fg_color="#0D6AD8").pack(pady=10)

    def avancar_etapa(self):
        self.destroy()

    def encerrar_prog(self):
        messagebox.showinfo("Obrigado!", "Agradecemos por usar o sistema Safe Vision.")
        self.destroy()

    def buscar(self):
        id_digitado = self.id_entry.get().strip()
        try:
            df = pd.read_excel(r'C:\Users\Pichau\Desktop\VISAO_COMPUTACIONAL\Dados coletados.xlsx', sheet_name='Sheet1',
                               skiprows=1)
            df.columns = df.columns.str.strip()

            if 'ID Motorista' not in df.columns:
                messagebox.showerror("Erro", "Coluna 'ID Motorista' não encontrada na planilha.")
                return None

            df['ID Motorista'] = df['ID Motorista'].astype(str).str.strip()
            id_digitado = str(id_digitado).strip()

            linha = df[df['ID Motorista'] == id_digitado]

            if linha.empty:
                messagebox.showinfo("ID não encontrado", "ID não encontrado na planilha.")
                return None

            # Puxa os dados do motorista e salva no dicionário
            try:
                self.motorista_dados = {
                    'ID': id_digitado,
                    'Nome': linha['Nome'].values[0],
                    'Sobrenome': linha['Sobrenome'].values[0],
                    'Idade': linha['Idade'].values[0],
                    'Medicamentos': linha['Medicamentos'].values[0],
                    'Doenças': linha['Doenças'].values[0],
                    'Marca': linha['Marca'].values[0],
                    'Modelo': linha['Modelo'].values[0],
                    'Ano': linha['Ano'].values[0],
                    'Cor': linha['Cor'].values[0],
                    'Placa': linha['Placa'].values[0],
                }

                messagebox.showinfo("ID encontrado",
                                    f"ID: {id_digitado}\n\nInformações do Motorista:\n\nNome: {self.motorista_dados['Nome']} \nSobrenome: {self.motorista_dados['Sobrenome']}\nIdade: {self.motorista_dados['Idade']} anos\nMedicamentos: {self.motorista_dados['Medicamentos']}\nDoenças: {self.motorista_dados['Doenças']}\n\nInformações do Veículo:\n\nMarca: {self.motorista_dados['Marca']}\nModelo: {self.motorista_dados['Modelo']}\nAno: {self.motorista_dados['Ano']}\nCor: {self.motorista_dados['Cor']}\nPlaca: {self.motorista_dados['Placa']}")

            except Exception as e:
                print(f"Erro ao puxar informações do motorista: {e}")
                messagebox.showerror("Erro", f"Ocorreu um erro ao puxar as informações do motorista: {e}")

        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo 'Dados coletados.xlsx' não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao buscar o ID: {e}")
            return None

    def salvar_id(self):
        id_digitado = self.id_entry.get().strip()  # Obtém o ID da entrada
        try:
            # Lê a planilha, definindo a segunda linha como cabeçalho
            df = pd.read_excel(r'C:\Users\Pichau\Desktop\VISAO_COMPUTACIONAL\Dados coletados.xlsx', sheet_name='Sheet1',
                               header=1)

            # Verifica se o ID está na coluna 'ID Motorista'
            linha = df[df['ID Motorista'] == id_digitado]

            if not linha.empty:
                # Puxa os dados do motorista nas colunas especificadas
                self.motorista_dados = {
                    "ID": id_digitado,
                    "Nome": linha['Nome'].values[0],
                    "Sobrenome": linha['Sobrenome'].values[0],
                    "Idade": linha['Idade'].values[0],
                    "Medicamentos": linha['Medicamentos'].values[0],
                    "Doenças": linha['Doenças'].values[0],
                    "Marca": linha['Marca'].values[0],
                    "Modelo": linha['Modelo'].values[0],
                    "Ano": linha['Ano'].values[0],
                    "Cor": linha['Cor'].values[0],
                    "Placa": linha['Placa'].values[0],
                }

                # Exibe mensagem de sucesso
                mensagem = (f"Dados do motorista salvos temporariamente com êxito!\n\n"
                            f"Informações do motorista:\n\n"
                            f"ID: {self.motorista_dados['ID']}\n"
                            f"Nome: {self.motorista_dados['Nome']}\n"
                            f"Sobrenome: {self.motorista_dados['Sobrenome']}\n"
                            f"Idade: {self.motorista_dados['Idade']} anos\n"
                            f"Medicamentos: {self.motorista_dados['Medicamentos']}\n"
                            f"Doenças: {self.motorista_dados['Doenças']}\n\n"
                            f"Informações do veículo:\n\n"
                            f"Marca: {self.motorista_dados['Marca']}\n"
                            f"Modelo: {self.motorista_dados['Modelo']}\n"
                            f"Ano: {self.motorista_dados['Ano']}\n"
                            f"Cor: {self.motorista_dados['Cor']}\n"
                            f"Placa: {self.motorista_dados['Placa']}")

                messagebox.showinfo("Dados Salvos", mensagem)  # Exibe mensagem de sucesso

            else:
                messagebox.showerror("Erro", "ID não encontrado na planilha.")

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar os dados do motorista: {e}")


class Sistema_reconhecimento_facial():
    def __init__(self, folder_path, excel_file_path, background_image, mode_folder_path):
        self.folder_path = folder_path
        self.excel_file_path = excel_file_path
        self.background_image = background_image
        self.mode_folder_path = mode_folder_path
        self.img_list = []
        self.motorista_ids = []
        self.encode_list_known = []
        self.encode_list_known_with_ids = []
        self.img_mode_list = []
        self.mode_type = 0
        self.counter = 0
        self.id = -1
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)  # Largura
        self.cap.set(4, 430)  # Altura
        self.img_backgroud_facial = cv2.imread(self.background_image)
        self.load_images_and_ids()
        self.encode_faces()
        self.load_mode_images()
        self.load_encoding_file()

    def load_images_and_ids(self):
        path_list = os.listdir(self.folder_path)
        for path in path_list:
            self.img_list.append(cv2.imread(os.path.join(self.folder_path, path)))
            self.motorista_ids.append(path)
        print(self.motorista_ids)

    def encode_faces(self):
        print("Encoding Started...")
        self.encode_list_known = self.find_encodings(self.img_list)
        self.encode_list_known_with_ids = [self.encode_list_known, self.motorista_ids]
        print("Encoding Completed")
        file = open("EncodeFile.p", 'wb')
        pickle.dump(self.encode_list_known_with_ids, file)
        file.close()
        print("File Saved")

    def find_encodings(self, images_list):
        encode_list = []
        for img in images_list:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encode_list.append(encode)
        return encode_list

    def load_mode_images(self):
        mode_path_list = os.listdir(self.mode_folder_path)
        for path in mode_path_list:
            self.img_mode_list.append(cv2.imread(os.path.join(self.mode_folder_path, path)))

    def load_encoding_file(self):
        print("Loading Encode File...")
        file = open('EncodeFile.p', 'rb')
        self.encode_list_known_with_ids = pickle.load(file)
        file.close()
        self.encode_list_known, self.motorista_ids = self.encode_list_known_with_ids
        print("Encode File Loaded")

    def read_excel_data(self):
        wb = openpyxl.load_workbook(self.excel_file_path)
        sheet = wb['Sheet1']
        return sheet

    def run(self):
        sheet = self.read_excel_data()

        # Definindo a tela para full screen
        cv2.namedWindow("Reconhecimento Facial", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Reconhecimento Facial", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        mostrar_messagebox("Informação", "Quando o sistema fazer o seu reconhecimento facial,\naperte a tecla *c* para concluir.")

        while True:
            success, img = self.cap.read()
            img_s = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            img_s = cv2.cvtColor(img_s, cv2.COLOR_BGR2RGB)

            face_cur_frame = face_recognition.face_locations(img_s)
            encode_cur_frame = face_recognition.face_encodings(img_s, face_cur_frame)

            img_resized = cv2.resize(img, (640, 430))
            self.img_backgroud_facial[176:176 + 430, 46:46 + 640] = img_resized
            self.img_backgroud_facial[40:40 + 640, 756:756 + 306] = self.img_mode_list[self.mode_type]

            for encode_face, face_loc in zip(encode_cur_frame, face_cur_frame):
                matches = face_recognition.compare_faces(self.encode_list_known, encode_face)
                face_dis = face_recognition.face_distance(self.encode_list_known, encode_face)

                match_index = np.argmin(face_dis)

                if matches[match_index]:
                    y1, x2, y2, x1 = face_loc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    bbox = x1, y1, x2, y2

                    cv2.rectangle(img_resized, (x1, y1), (x2, y2), (153, 77, 2), 2)
                    self.img_backgroud_facial[176:176 + 430, 46:46 + 640] = img_resized
                    self.id = self.motorista_ids[match_index]

                    if self.counter == 0:
                        self.counter = 1
                        self.mode_type = 1

            if self.counter != 0:
                if self.counter == 1:
                    id_motorista_com_extensao = self.motorista_ids[match_index]
                    motorista_info = {}
                    for row in sheet.iter_rows(min_row=3, values_only=True):
                        if row[0] == id_motorista_com_extensao:
                            motorista_info = {
                                'ID Motorista': row[0],
                                'Nome': row[2],
                                'Sobrenome': row[3],
                                'Idade': row[4],
                                'Medicamentos': row[5],
                                'Doenças': row[6],
                                'Marca do veículo': row[8],
                                'Modelo do veículo': row[9],
                                'Ano do veículo': row[10],
                                'Cor do veículo': row[11],
                                'Placa do veículo': row[12]
                            }
                            break

                    if motorista_info:
                        id_motorista = f"{motorista_info['ID Motorista']}"
                        veiculo = f"{motorista_info['Modelo do veículo']} {motorista_info['Ano do veículo']}"
                        nome = f"{motorista_info['Nome']}"

                        cv2.putText(self.img_backgroud_facial, f" {id_motorista}", (830, 478), cv2.FONT_HERSHEY_DUPLEX,
                                    0.6,
                                    (255, 255, 255), 1, cv2.LINE_AA)
                        cv2.putText(self.img_backgroud_facial, f" {veiculo}", (876, 538), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                    (255, 255, 255), 2, cv2.LINE_AA)
                        cv2.putText(self.img_backgroud_facial, f"{nome}", (879, 403), cv2.FONT_HERSHEY_DUPLEX, 0.6,
                                    (255, 255, 255), 1, cv2.LINE_AA)

                        img_motorista_path = rf'C:\\Users\\Pichau\\Desktop\\VISAO_COMPUTACIONAL\\Pessoas\\{id_motorista_com_extensao}'
                        img_motorista = cv2.imread(img_motorista_path)

                        if img_motorista is not None:
                            img_motorista_resized = cv2.resize(img_motorista, (640, 480))
                            x_offset, y_offset = 796, 201
                            largura_maxima = 1023 - x_offset
                            altura_maxima = 426 - y_offset

                            img_altura, img_largura = img_motorista.shape[:2]
                            proporcao_final = min(largura_maxima / img_largura, altura_maxima / img_altura)

                            nova_largura = int(img_largura * proporcao_final)
                            nova_altura = int(img_altura * proporcao_final)

                            if y_offset + nova_altura > 426:
                                nova_altura = 426 - y_offset
                            if x_offset + nova_largura > 1023:
                                nova_largura = 1023 - x_offset

                            img_motorista_resized = cv2.resize(img_motorista, (nova_largura, nova_altura))
                            self.img_backgroud_facial[y_offset:y_offset + nova_altura,
                            x_offset:x_offset + nova_largura] = img_motorista_resized

                        else:
                            print(f"Imagem do motorista {id_motorista_com_extensao} não encontrada.")
                    else:
                        print("Informações do motorista não encontradas na planilha.")

            cv2.imshow("Reconhecimento Facial", self.img_backgroud_facial)
            if cv2.waitKey(1) & 0xFF == ord('c'):
                mostrar_messagebox2("Instrução", f"O ID: {id_motorista} foi reconhecido.\nProssiga para confirmar o seu ID.")
                cv2.destroyAllWindows()
                Confirmar_id().mainloop()
                break

        self.cap.release()
        cv2.destroyAllWindows()


class Tela_bem_vindo(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x800")
        self.title("Seja bem-vindo")
        self.attributes('-fullscreen', True)  # Tela cheia
        self.banner_path = "Banner Safe Vision Formulário Bem-vindo Detecção (1200 x 800 px).png"
        self.banner_image = Image.open(self.banner_path)
        self.setup_ui()
        self.foto_capturada = None  # Inicializar variável para a foto capturada

    def redimensionar_banner(self):
        # Mantém o tamanho original do banner
        return self.banner_image

    def setup_ui(self):
        # Configura o layout da tela
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Permite o frame ocupar o espaço verticalmente

        # Redimensiona o banner
        self.banner_redimensionado = self.redimensionar_banner()
        self.banner_tk = ImageTk.PhotoImage(self.banner_redimensionado)

        # Cria um label para exibir o banner à esquerda
        banner_label = tk.Label(self, image=self.banner_tk)
        banner_label.grid(row=0, column=0, sticky="nsew")  # Banner ocupa a coluna da esquerda

        # Cria o frame para os botões e a mensagem à direita
        right_frame = customtkinter.CTkFrame(self, fg_color="transparent")  # Frame sem fundo
        right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Configura o layout do right_frame
        right_frame.grid_rowconfigure(0, weight=1)  # Espaço antes da mensagem
        right_frame.grid_rowconfigure(1, weight=0)  # Mensagem
        right_frame.grid_rowconfigure(2, weight=0)  # Linha dos botões
        right_frame.grid_rowconfigure(3, weight=1)  # Espaço depois dos botões

        # Mensagem "Selecione uma das opções abaixo para prosseguir"
        info_text = customtkinter.CTkLabel(right_frame, font=("Arial", 25),
                                           text="Selecione uma das opções abaixo para prosseguir")
        info_text.grid(row=1, column=0, pady=20, padx=20)

        # Cria o frame para os botões abaixo da mensagem
        button_frame = customtkinter.CTkFrame(right_frame, fg_color="transparent")  # Remove o fundo
        button_frame.grid(row=2, column=0, pady=20, padx=20)

        # Botão "Iniciar Cadastro"
        iniciar_button = customtkinter.CTkButton(button_frame, text="Iniciar Software", command=self.iniciar_deteccao,
                                                 fg_color="#0D6AD8")
        iniciar_button.grid(row=0, column=0, pady=5)

        cadastrado_button = customtkinter.CTkButton(button_frame, text="Não tenho Cadastro",
                                                    command=self.nao_tem_cadastro, fg_color="#0D6AD8")
        cadastrado_button.grid(row=1, column=0, pady=5)

        # Botão "Encerrar Programa"
        encerrar_button = customtkinter.CTkButton(button_frame, text="Encerrar Programa",
                                                  command=self.encerrar_programa, fg_color="#0D6AD8")
        encerrar_button.grid(row=2, column=0, pady=5)

        # Botão "Políticas de Privacidade e LGPD"
        privacidade_button = customtkinter.CTkButton(button_frame, text="Políticas de Privacidade e LGPD",
                                                     command=self.abrir_politicas_privacidade, fg_color="#0D6AD8")
        privacidade_button.grid(row=3, column=0, pady=5)

    def iniciar_deteccao(self):
        self.destroy()
        sistema_reconhecimento = Sistema_reconhecimento_facial(folder_path, excel_file_path, background_image, mode_folder_path)
        sistema_reconhecimento.run()

    def nao_tem_cadastro(self):
        messagebox.showinfo("Usuário não cadastrado",
                            "Realize primeiro o cadastro para fazer a detecção\nProssiga para o programa de cadastro de usuários.")
        self.destroy()

    def encerrar_programa(self):
        # Função para fechar o programa
        mostrar_messagebox3("Obrigado!", "Agradecemos por usar o sistema da Safe Vision.")
        self.destroy()

    def abrir_politicas_privacidade(self):
        # Função para abrir o site de Políticas de Privacidade e LGPD
        webbrowser.open(
            "https://www.gov.br/anpd/pt-br/documentos-e-publicacoes/documentos-de-publicacoes/web-guia-anpd-tratamento-de-dados-para-fins-academicos.pdf")

if __name__ == "__main__":
    app = Tela_bem_vindo()
    app.mainloop()
