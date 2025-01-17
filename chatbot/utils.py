import openai
import json
import os
import logging
from django.shortcuts import render
from django.http import JsonResponse
from dotenv import load_dotenv
from django.conf import settings

# Configuração do logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

def carregar_produto():
    try:
        with open(os.path.join(str(settings.BASE_DIR), 'static/pdfs/suvinil-toque-fosco-completo.json'), 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("Arquivo JSON não encontrado.")
        return None  # Retorna None em caso de erro
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON: {e}")
        return None

def consultar_com_ia(pergunta, dados_json):
    if dados_json is None:
        return "Desculpe, não foi possível carregar as informações do produto."

    contexto = f"Informações sobre o produto: {json.dumps(dados_json, ensure_ascii=False)}"
    try:
        resposta_ia = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente útil. E está habilitado a responder somente sobre o produto Toque Fosco Completo, qualquer outra pergunta diga que só pode responder sobre o produto"},
                {"role": "user", "content": f"{contexto}\nPergunta: {pergunta}"}
            ]
        )
        resposta_conteudo = resposta_ia.choices[0].message.content
        return resposta_conteudo.strip()
    except openai.error.OpenAIError as e:
        logger.error(f"Erro na API da OpenAI: {e}")
        return "Desculpe, ocorreu um erro ao processar sua solicitação."
    except Exception as e:
        logger.exception("Um erro inesperado ocorreu:")
        return "Um erro inesperado ocorreu. Por favor, tente novamente mais tarde."

def responder_pergunta(request):
    if request.method == "POST":
        pergunta = request.POST.get('question', '').lower()
        produto_info = carregar_produto()

        if produto_info is None:
            return JsonResponse({'answer': "Erro ao carregar dados do produto."})

        resposta = consultar_com_ia(pergunta, produto_info)
        return JsonResponse({'answer': resposta})

    return JsonResponse({'answer': 'Método inválido.'})