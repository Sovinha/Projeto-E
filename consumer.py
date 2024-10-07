import requests

# Função para buscar dados da API
def buscar_dados_api():
    try:
        response = requests.get("http://127.0.0.1:5000/pedidos")  # Altere para a URL correta
        response.raise_for_status()
        return response.json()  # Retorna dados no formato JSON
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        return []

if __name__ == "__main__":
    pedidos = buscar_dados_api()
    for pedido in pedidos:
        print(f"Número do Pedido: {pedido['numero_do_pedido']}, Bairro: {pedido['bairro']}, Rua: {pedido['rua']}")
