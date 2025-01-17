from django.shortcuts import render
from django.http import JsonResponse
from chatbot.utils import responder_pergunta

# Create your views here.
def index(request):
    return render(request, 'index.html')

# Função para lidar com a requisição de pergunta e resposta
def perguntar_produto(request):
    if request.method == 'POST':
        return responder_pergunta(request)  # Chama a função de responder da utils.py

    return JsonResponse({'answer': 'Método inválido.'})