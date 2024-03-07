from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, reverse


def main(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    else:
        return render(request, 'backend/base.html')
