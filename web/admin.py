from django.contrib import admin
from .models import Article, Document


@admin.register(Article)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Document)
