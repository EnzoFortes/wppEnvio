import requests
import time
import os
import shutil
import base64
from datetime import datetime
import mimetypes

# Caminhos das pastas
PASTA_MONITORADA = r"C:\Users\Cliente\Desktop\wppEnvio\checar"
PASTA_ENVIADOS = r"C:\Users\Cliente\Desktop\wppEnvio\checado"

# Função para extrair os dados do arquivo
def extrair_dados(caminho_arquivo):
    dados = {}
    linhas_originais = []
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            linhas_originais = f.readlines()
        
        for linha in linhas_originais:
            if "=" in linha:
                chave, valor = linha.strip().split("=", 1)
                dados[chave.strip().upper()] = valor.strip()
        
        return dados, linhas_originais
    except Exception as e:
        print(f"Erro ao extrair dados do arquivo {caminho_arquivo}: {e}")
        return None, None

# Função para converter arquivo para base64
def converter_para_base64(caminho_anexo):
    try:
        with open(caminho_anexo, "rb") as file:
            encoded = base64.b64encode(file.read()).decode("utf-8")
        return encoded
    except Exception as e:
        print(f"❌ Erro ao converter anexo para base64: {e}")
        return None

# Função para detectar o tipo MIME do arquivo
def detectar_mime_type(caminho_arquivo):
    mime_type, _ = mimetypes.guess_type(caminho_arquivo)
    return mime_type or "application/octet-stream"

# Função para enviar mensagem via API
def enviar_mensagem(numero, mensagem, caminho_anexo=None):
    url = "http://localhost:3000/send"
    data = {"number": f"55{numero}", "message": mensagem}
    
    if caminho_anexo and os.path.exists(caminho_anexo):
        arquivo_base64 = converter_para_base64(caminho_anexo)
        if arquivo_base64:
            data["attachment"] = {
                "filename": os.path.basename(caminho_anexo),
                "mimetype": detectar_mime_type(caminho_anexo),
                "data": arquivo_base64
            }
        
    try:
        response = requests.post(url, json=data)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao enviar mensagem: {e}")
        return {"success": False, "error": str(e)}

# Função para atualizar o arquivo após envio
def atualizar_arquivo(caminho_arquivo, linhas_originais, status_envio, anexo_enviado, numero):
    try:
        data_envio = datetime.now().strftime("%d/%m/%Y")
        hora_envio = datetime.now().strftime("%H:%M:%S")
        novas_linhas = linhas_originais + ["\n"] * 5 + [
            f"STATUS={status_envio}\n",
            f"ANEXO={anexo_enviado}\n",
            f"DATA={data_envio}\n",
            f"HORA={hora_envio}\n",
            f"NUMERO=55{numero}\n"
        ]
        
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            f.writelines(novas_linhas)
        return True
    except Exception as e:
        print(f"⚠️ Erro ao atualizar arquivo {caminho_arquivo}: {e}")
        return False

# Loop para monitorar a pasta
while True:
    arquivos = [f for f in os.listdir(PASTA_MONITORADA) if f.endswith('.txt')]
    for arquivo in arquivos:
        caminho_completo = os.path.join(PASTA_MONITORADA, arquivo)
        dados, linhas_originais = extrair_dados(caminho_completo)
        if not dados:
            continue

        numero = dados.get("TELEFONE")
        mensagem = dados.get("MENSAGEM", "Mensagem padrão")
        anexo = dados.get("ANEXOS", "").strip()

        caminho_anexo = os.path.join(PASTA_MONITORADA, anexo) if anexo else None
        if caminho_anexo and not os.path.exists(caminho_anexo):
            caminho_anexo = None
        
        resposta = enviar_mensagem(numero, mensagem, caminho_anexo)
        status_envio = "ENVIADO" if resposta.get("success") else "FALHA"
        anexo_enviado = "ENVIADO" if caminho_anexo and resposta.get("success") else "FALHA"

        if atualizar_arquivo(caminho_completo, linhas_originais, status_envio, anexo_enviado, numero):
            shutil.move(caminho_completo, os.path.join(PASTA_ENVIADOS, arquivo))
            if caminho_anexo and resposta.get("success"):
                shutil.move(caminho_anexo, os.path.join(PASTA_ENVIADOS, os.path.basename(caminho_anexo)))
    
    time.sleep(60)
