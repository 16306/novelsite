from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from read_statistics.models import GetReadNum, ReadNumDetail
from ckeditor_uploader.fields import RichTextUploadingField


class Chapter(models.Model):
    chapterid = models.AutoField(primary_key=True)
    novelid = models.ForeignKey('Novel', models.DO_NOTHING, db_column='novelid', blank=True, null=True)
    chaptername = models.CharField(max_length=255, blank=True, null=True)
    content = RichTextUploadingField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'chapter'
        ordering = ['chapterid']

    def __str__(self):
        return '<novelid:{}>: {}'.format(self.novelid, self.chaptername)


class Novel(models.Model, GetReadNum):
    novelid = models.AutoField(primary_key=True)
    sort = models.IntegerField(blank=True, null=True)
    novelname = models.CharField(max_length=255, blank=True, null=True)
    writername = models.CharField(max_length=255, blank=True, null=True)
    read_detail = GenericRelation(ReadNumDetail)

    class Meta:
        managed = True
        db_table = 'novel'
        ordering = ['-novelid']

    def __str__(self):
        return str(self.novelid)

