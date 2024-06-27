from django.shortcuts import render

# Create your views here.
def nav(request):
    return render(request, 'nav.html')

def footer(request):
    return render(request,'footer.html')

def base(request):
    return render(request,'base.html')