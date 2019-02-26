from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from read_statistics.models import GetReadNum, ReadNumDetail
from ckeditor_uploader.fields import RichTextUploadingField


class Chapter(models.Model):
    chapterid = models.AutoField(primary_key=True)
    noverid = models.ForeignKey('Nover', models.DO_NOTHING, db_column='noverid', blank=True, null=True)
    chaptername = models.CharField(max_length=255, blank=True, null=True)
    content = RichTextUploadingField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chapter'
        ordering = ['chapterid']

    def __str__(self):
        return '<novelid:{}>: {}'.format(self.noverid, self.chaptername)


class Nover(models.Model, GetReadNum):
    noverid = models.AutoField(primary_key=True)
    sort = models.IntegerField(blank=True, null=True)
    novername = models.CharField(max_length=255, blank=True, null=True)
    writername = models.CharField(max_length=255, blank=True, null=True)
    read_detail = GenericRelation(ReadNumDetail)
    novelindex = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nover'
        ordering = ['noverid']

    def __str__(self):
        return str(self.noverid)

