import requests
import tkinter as tk
from tkinter import messagebox, Frame, Scrollbar, ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
# Importa a classe do MotoGrau
from MotoGrau import ExcelImporter  # Ajuste conforme o nome da classe que você deseja importar

def buscar_dados_api():
    try:
        response = requests.get("http://127.0.0.1:5000/pedidos")
        response.raise_for_status()
        return response.json()  # Isso já deve incluir o nome do motoboy
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar dados: {e}")
        return []

def gerar_etiquetas(pedido):
    bairro = pedido.get("bairro")
    numero_pedido = pedido.get("numero_do_pedido")
    rua = pedido.get("rua")
    motoboy = pedido.get("motoboy")  # Capturando o nome do motoboy
    pdf_filename = f"etiqueta_{numero_pedido}.pdf"
    try:
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        c.drawString(100, 750, f"Bairro: {bairro}")
        c.drawString(100, 730, f"Número do Pedido: {numero_pedido}")
        c.drawString(100, 710, f"Rua: {rua}")
        c.drawString(100, 690, f"Motoboy: {motoboy}")  # Adicionando o nome do motoboy
        c.save()

        os.startfile(pdf_filename, "print")  # Envia o PDF para impressão diretamente
        return True
    except Exception as e:
        print(f"Erro na impressão: {e}")
        return False

def gerar_etiquetas_selecionadas():
    global pedidos_impressos
    selecoes = tree.selection()

    if not selecoes:
        messagebox.showwarning("Atenção", "Nenhum pedido selecionado para impressão.")
        return

    for item in selecoes:
        index = tree.index(item)
        if index not in pedidos_impressos:
            pedido = pedidos[index]
            if gerar_etiquetas(pedido):
                pedidos_impressos.append(index)
                tree.item(item, values=(pedido["numero_do_pedido"], pedido["bairro"], pedido["rua"], pedido["motoboy"], "Sim"))

    messagebox.showinfo("Sucesso", "Etiquetas selecionadas geradas e enviadas para impressão!")

def atualizar_lista():
    global pedidos
    novos_pedidos = buscar_dados_api()
    for pedido in novos_pedidos:
        numero_pedido = pedido.get("numero_do_pedido")
        bairro = pedido.get("bairro")
        rua = pedido.get("rua")
        motoboy = pedido.get("motoboy")  # Capturando o nome do motoboy

        if numero_pedido is not None and bairro is not None and rua is not None and motoboy is not None:
            if pedido not in pedidos:
                pedidos.append(pedido)
                tree.insert("", tk.END, values=(numero_pedido, bairro, rua, motoboy, "Não"))  # Incluindo o nome do motoboy

                # Gera e imprime a etiqueta automaticamente
                if gerar_etiquetas(pedido):
                    pedidos_impressos.append(len(pedidos) - 1)
                    tree.item(tree.get_children()[-1], values=(numero_pedido, bairro, rua, motoboy, "Sim"))

def pesquisar_pedido(event=None):
    numero_pedido = entrada_pesquisa.get().strip()
    if not numero_pedido:
        messagebox.showwarning("Atenção", "Por favor, insira um número de pedido para pesquisar.")
        return

    encontrado = False
    for item in tree.get_children():
        tree.item(item, tags=())

    for index, pedido in enumerate(pedidos):
        if str(pedido.get("numero_do_pedido")) == numero_pedido:
            resultado_pesquisa_label.config(text=f"Número do Pedido: {numero_pedido}")
            pedido_info.config(text=f"Bairro: {pedido['bairro']} | Rua: {pedido['rua']} | Motoboy: {pedido['motoboy']}")
            tree.selection_set(tree.get_children()[index])
            tree.see(tree.get_children()[index])
            encontrado = True
            break

    if not encontrado:
        messagebox.showinfo("Resultado", "Nenhum pedido encontrado.")
        resultado_pesquisa_label.config(text="")
        pedido_info.config(text="")

def atualizar_periodicamente():
    atualizar_lista()
    root.after(5000, atualizar_periodicamente)

def abrir_motoboys():
    new_window = tk.Toplevel(root)
    new_window.title("MOTOGRAU")
    new_window.geometry("600x400")
    
    # Instancia a classe do ExcelImporter na nova janela
    app = ExcelImporter(new_window)

root = tk.Tk()
root.title("Gerador de Etiquetas")
root.geometry("850x550")
root.minsize(400, 300)
root.configure(bg="#f0f0f0")

pedidos = []
pedidos_impressos = []

titulo = tk.Label(root, text="Gerador de Etiquetas", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
titulo.grid(row=0, column=0, columnspan=2, pady=10)

frame_pesquisa = Frame(root, bg="#f0f0f0")
frame_pesquisa.grid(row=1, column=0, padx=10, pady=5)

entrada_pesquisa = tk.Entry(frame_pesquisa, font=("Helvetica", 12), width=20)
entrada_pesquisa.pack(side=tk.LEFT, padx=(10, 5))

botao_pesquisar = tk.Button(frame_pesquisa, text="Pesquisar", command=pesquisar_pedido, bg="#2196F3", fg="white", font=("Helvetica", 12))
botao_pesquisar.pack(side=tk.LEFT)

resultado_pesquisa_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#f0f0f0")
resultado_pesquisa_label.grid(row=2, column=0, padx=10, pady=5)

pedido_info = tk.Label(root, text="", font=("Helvetica", 12), bg="#f0f0f0", fg="blue")
pedido_info.grid(row=3, column=0, padx=10, pady=5)

frame = Frame(root, bg="#f0f0f0")
frame.grid(row=4, column=0, padx=10, pady=10)

tree = ttk.Treeview(frame, columns=("Numero do Pedido", "Bairro", "Rua", "Motoboy", "Impressa"), show='headings')
tree.heading("Numero do Pedido", text="Número do Pedido")
tree.heading("Bairro", text="Bairro")
tree.heading("Rua", text="Rua")
tree.heading("Motoboy", text="Motoboy")  # Adicionando cabeçalho para motoboy
tree.heading("Impressa", text="Impressa")
tree.column("Impressa", width=80)
tree.column("Motoboy", width=120)  # Ajustando largura da coluna do motoboy
tree.pack(side=tk.LEFT)

scrollbar = Scrollbar(frame, orient="vertical", command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscrollcommand=scrollbar.set)

botao_imprimir_todas = tk.Button(root, text="Imprimir Todas as Etiquetas", command=lambda: [gerar_etiquetas(p) for p in pedidos if p not in pedidos_impressos], bg="#2196F3", fg="white", font=("Helvetica", 12))
botao_imprimir_todas.grid(row=5, column=0, pady=5)

botao_imprimir_selecionados = tk.Button(root, text="Imprimir Etiquetas Selecionadas", command=gerar_etiquetas_selecionadas, bg="#FFC107", fg="white", font=("Helvetica", 12))
botao_imprimir_selecionados.grid(row=6, column=0, pady=5)

# Botão MOTOBOY'S
botao_motoboys = tk.Button(root, text="MOTOBOY'S", command=abrir_motoboys, bg="#FF5722", fg="white", font=("Helvetica", 12))
botao_motoboys.grid(row=7, column=0, pady=10)

entrada_pesquisa.bind("<Return>", pesquisar_pedido)

atualizar_periodicamente()
root.mainloop()
