from django.contrib import admin
from .models import Novel, Chapter
# Register your models here.


@admin.register(Novel)
class NovelAdmin(admin.ModelAdmin):
    list_display = ('novelid', 'sort', 'novelname', 'writername', 'get_read_num')


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('chapterid', 'novelid', 'chaptername')
