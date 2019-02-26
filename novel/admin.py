from django.contrib import admin
from .models import Nover, Chapter
# Register your models here.


@admin.register(Nover)
class NovelAdmin(admin.ModelAdmin):
    list_display = ('noverid', 'sort', 'novername', 'writername', 'get_read_num')


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('chapterid', 'noverid', 'chaptername')
