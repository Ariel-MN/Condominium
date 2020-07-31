from django.db import models
from ckeditor.fields import RichTextField


class Article(models.Model):
    created_date = models.DateField("Data di creazione", auto_now=False, auto_now_add=True)
    title = models.CharField("Titolo dell'articolo", max_length=150, unique=True)
    slug = models.SlugField("URL", unique=True)
    description = models.TextField("Descrizione")
    content = RichTextField()


class Document(models.Model):
    title = models.CharField("Nome del documento", max_length=150, unique=True)
    file = models.FileField(upload_to='static/documents/')
