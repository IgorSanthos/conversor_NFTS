import pandas as pd
import tkinter as tk
from tkinter import filedialog, Tk,  ttk,  Text, Scrollbar, messagebox

def importar_arquivo():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("Arquivos de texto", "*.csv"), ("Todos os arquivos", "*.*")])
    if file_path:
        try:
            # Leitura do arquivo CSV
            df = pd.read_csv(file_path, encoding='latin1', sep=';')
            
            # Manipulações nos dados
            df = df.astype(str)
            df = df.replace('nan', '')
            df['Número do Documento'] = df['Número do Documento'].astype(str).str.replace('.0', '')
            df['Data Hora Emissão NFTS'], df['Data da Prestação de Serviços'] = zip(*df.apply(lambda row: replacement_date(row['Data Hora Emissão NFTS'], row['Data da Prestação de Serviços']), axis=1))
            
            # Adiciona sufixo aos números de documento duplicados
            new_numeracoes = []
            count_dict = {}
            for num in df['Número do Documento']:
                if num in count_dict:
                    count_dict[num] += 1
                else:
                    count_dict[num] = 1
                if count_dict[num] > 1:
                    new_value = f"{num}-{count_dict[num] - 1}"
                else:
                    new_value = str(num)
                new_numeracoes.append(new_value)
            df['Número do Documento'] = new_numeracoes
            
            df.loc[1:,'Nº NFTS'] = df.loc[1:,'Número do Documento']
            
            # Atualizar o widget de texto com os dados processados
            atualizar_texto(df.head().to_string(index=False))           
        except Exception as e:
            messagebox.showinfo('Erro !', f"Erro ao ler o arquivo: {e}")

def salvar_arquivo():
    try:
        if df is not None:
            file_path = get_save_path()
            if file_path:
                # Exporta para arquivo CSV
                df.to_csv(file_path, index=False, sep=';', encoding='latin1')
                messagebox.showinfo('Erro !', f'Dados exportados para {file_path}')
            else:
                messagebox.showinfo('Erro !', 'Nenhum arquivo selecionado. Exportação cancelada.')
            messagebox.showinfo('Aviso !', 'SALVO')
        else:
            messagebox.showinfo('Erro !', 'Nenhum arquivo importado ainda.')
    except Exception as e:
        messagebox.showinfo('Erro !', f"Erro ao salvar o arquivo: {e}")



def replacement_date(x, y):
    x_part = x[:10]
    y_part = y[:10]
    x = y_part + x[10:]
    y = x_part + y[10:]
    return x, y

def get_save_path():
    root = Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Arquivos CSV", "*.csv")])
    root.destroy()  # Destruir a janela após selecionar o arquivo
    return file_path


def fechar_janela_principal():
    root.destroy()  # Destruir a janela principal ao fechar

def atualizar_texto(novo_texto):
    text_box.config(state=tk.NORMAL)  # Habilita a edição do widget de texto
    text_box.delete('1.0', tk.END)  # Limpa o conteúdo atual
    text_box.insert(tk.END, novo_texto)  # Insere os novos dados
    text_box.config(state=tk.DISABLED)  # Desabilita a edição do widget de texto

root = tk.Tk()
root.title("Conversor-NFTS Online")
root.geometry("800x600")
root.configure(bg='#4D9D76')


#DATAFRAME
scrollbar = Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_box = Text(root, wrap=tk.WORD, yscrollcommand=scrollbar.set, width=80, height=15)
text_box.place(relx=0.1, rely=0.50)
scrollbar.config(command=text_box.yview)


# Criando o menu
menu = tk.Menu(root)
root.config(menu=menu)
fonte_menu = ('Helvetica', 12)
# Criando os itens do menu
menu_botoes = tk.Menu(menu, tearoff=0, font=fonte_menu)
menu.add_cascade(label="Arquivos", menu=menu_botoes)
menu_botoes.add_command(label="Importar Arquivo", command=importar_arquivo)
menu_botoes.add_command(label="Salvar Arquivo", command=salvar_arquivo)
menu_botoes.add_separator()
menu_botoes.add_command(label="Sair", command=fechar_janela_principal)


root.mainloop()
