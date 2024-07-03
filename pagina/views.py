from django.shortcuts import render

import requests
from django.shortcuts import render


# Create your views here.
def nav(request):
    return render(request, 'nav.html')

def footer(request):
    return render(request,'footer.html')

def base(request):
    return render(request,'base.html')





def noticias(request):
    api_key = 'cf0b48e7634940da8624ea3bd0865dd6'
    url = f'https://newsapi.org/v2/everything?q=tesla&from=2024-06-01&sortBy=publishedAt&apiKey={api_key}'
    
    response = requests.get(url)
    data = response.json()
    
    articles = data.get('articles', [])
    
    return render(request, 'noticias.html', {'articles': articles})
