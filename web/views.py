from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Article, Document
from django.shortcuts import render
from django.conf import settings
from hurry.filesize import size, alternative
from os.path import getsize, join as os_join
import requests
import json


def captcha(request):
    secretKey = settings.RECAPTCHA_PRIVATE_KEY
    clientKey = request.POST['g-recaptcha-response']
    captchaData = {
        'secret': secretKey,
        'response': clientKey
    }
    try:
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captchaData)
        response = json.loads(r.text)
        verify_status = response['success']
    except:
        verify_status = 'fail'
    return verify_status


def send_email(oggetto, messaggio, nome, email):
    superusers_emails = [i[0] for i in User.objects.filter(is_superuser=True).values_list('email')]
    # allusers_emails = [i[0] for i in User.objects.values_list('email')]
    send_mail(oggetto, f"""Messaggio da {nome}.
                        \n{messaggio}
                        \nRispondere all'indirizzo {email}""", settings.EMAIL_HOST_USER, superusers_emails)
    return None


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')


def news(request):
    if request.method == 'GET':
        try:
            articles = Article.objects.all()
        except:
            articles = None
        return render(request, 'news.html', {'articles': articles})


def article(request, slug):
    if request.method == 'GET':
        try:
            articolo = Article.objects.get(slug=slug)
        except:
            articolo = None
        return render(request, 'article.html', {'articolo': articolo})


def regolamento(request):
    if request.method == 'GET':
        return render(request, 'regolamento.html')


def documenti(request):
    if request.method == 'GET':
        documents = Document.objects.all()
        for d in documents:
            try:
                d.size = size(getsize(os_join(str(settings.BASE_DIR), str(d.file))), system=alternative)
            except:
                d.title += " (Eliminato)"; d.size = "0 bytes"; d.file = None
        return render(request, 'documenti.html', {'documenti': documents})


def amministrazione(request):
    if request.method == 'GET':
        return render(request, 'amministrazione.html')


def avvisi(request):
    if request.method == 'GET':
        return render(request, 'avvisi.html')


def domande(request):
    publicKey = settings.RECAPTCHA_PUBLIC_KEY

    if request.method == 'GET':
        return render(request, 'domande.html', {'publicKey': publicKey})

    if request.method == 'POST':
        success = """
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    <strong>Invio riuscito!</strong> Il messaggio è stato inviato correttamente.
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                """
        fail = """
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <strong>Invio fallito!</strong> Si è verificato un errore durante l'invio del messaggio.
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                """
        complete_captcha = """
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <strong>Invio interrotto!</strong> È necessario completare il captcha per inviare il messaggio.
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                """

        verify = captcha(request)
        if verify == 'fail':
            return render(request, 'domande.html', {'publicKey': publicKey, 'message': fail})
        elif verify:
            try:
                send_email(request.POST['oggetto'], request.POST['messaggio'], request.POST['nome'], request.POST['email'])
                return render(request, 'domande.html', {'publicKey': publicKey, 'message': success})
            except:
                return render(request, 'domande.html', {'publicKey': publicKey, 'message': fail})
        else:
            return render(request, 'domande.html', {'publicKey': publicKey, 'message': complete_captcha})
