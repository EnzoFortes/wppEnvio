import requests
import time
import os
import shutil
from datetime import datetime

# Caminhos das pastas
PASTA_MONITORADA = r"C:\Users\Cliente\Desktop\wppEnvio\checar"
PASTA_ENVIADOS = r"C:\Users\Cliente\Desktop\wppEnvio\checado"
PASTA_LOGS = r"C:\Users\Cliente\Desktop\wppEnvio\logs"

# Mensagens pré-configuradas para teste
MENSAGENS = {
    "1": "Olá {nome}, esta é uma mensagem de teste."
}

# Função para registrar logs
def registrar_log(mensagem):
    """Registra mensagens no arquivo de log diário"""
    data_atual = datetime.now().strftime("%Y-%m-%d")
    log_path = os.path.join(PASTA_LOGS, f"log_{data_atual}.txt")
    
    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_mensagem = f"[{horario}] {mensagem}\n"

    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(log_mensagem)

# Função para extrair dados do arquivo
def extrair_dados(linha):
    try:
        nome = ''.join(filter(str.isalpha, linha))
        numero = ''.join(filter(str.isdigit, linha.split('-')[0]))  # Número antes do traço
        mensagem_id = linha.split('-')[1]  # ID da mensagem após o traço
        return nome, numero, mensagem_id
    except Exception as e:
        registrar_log(f"Erro ao extrair dados da linha '{linha}': {e}")
        return None, None, None

# Função para enviar a mensagem via API do servidor Node.js
def enviar_mensagem(numero, mensagem):
    url = "http://localhost:3000/send"
    data = {"number": numero, "message": mensagem}
    registrar_log(f"Enviando mensagem para {numero}... Mensagem: {mensagem}")

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            registrar_log(f"Mensagem enviada com sucesso para {numero}")
        else:
            registrar_log(f"Erro ao enviar mensagem para {numero}: {response.text}")
        return response.json()
    except requests.exceptions.RequestException as e:
        registrar_log(f"Falha na requisição ao enviar mensagem para {numero}: {e}")
        return {"success": False, "error": str(e)}

# Loop para monitorar a pasta
while True:
    registrar_log("Verificando a pasta...")

    arquivos = [f for f in os.listdir(PASTA_MONITORADA) if f.endswith('.txt')]

    if not arquivos:
        registrar_log("Nenhum arquivo encontrado. Aguardando...")

    for arquivo in arquivos:
        registrar_log(f"Processando arquivo: {arquivo}")
        caminho_completo = os.path.join(PASTA_MONITORADA, arquivo)

        try:
            with open(caminho_completo, "r", encoding="utf-8") as f:
                linhas = f.readlines()

            for linha in linhas:
                nome, numero, mensagem_id = extrair_dados(linha.strip())
                if numero and mensagem_id:
                    registrar_log(f"Nome: {nome}, Número: {numero}, ID da mensagem: {mensagem_id}")
                    mensagem = MENSAGENS.get(mensagem_id, "Mensagem padrão").format(nome=nome)
                    resposta = enviar_mensagem(numero, mensagem)
                    registrar_log(f"Resultado do envio para {numero}: {resposta}")

            shutil.move(caminho_completo, os.path.join(PASTA_ENVIADOS, arquivo))
            registrar_log(f"Arquivo {arquivo} movido para a pasta de enviados.")

        except Exception as e:
            registrar_log(f"Erro ao processar arquivo {arquivo}: {e}")

    registrar_log("Verificação concluída. Aguardando próximo ciclo...")
    time.sleep(60)
