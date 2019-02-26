import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Count, Sum
from .models import ReadNum, ReadNumDetail
from novel.models import Nover


def statistics_read_once(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "{}_{}_read".format(ct.model, obj.pk)
    if not request.COOKIES.get(key):
        # 总阅读数
        readnum, create = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()
        # 天阅读数
        date = timezone.now().date()
        readnumdetail, create = ReadNumDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readnumdetail.read_num += 1
        readnumdetail.save()
    return key


def get_weeks_read_num(content_type):
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(6, -1, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        readnumdetail = ReadNumDetail.objects.filter(content_type=content_type, date=date)
        result = readnumdetail.annotate(read_num_sum=Count('read_num'))
        sum = 0
        for item in result:
            sum += item.read_num
        read_nums.append(sum)
    return read_nums, dates


def today_hot():
    today = timezone.now().date()
    novels = Nover.objects \
        .filter(read_detail__date=today) \
        .values('noverid', 'novername') \
        .annotate(read_num_sum=Sum('read_detail__read_num')) \
        .order_by('-read_num_sum')
    return novels[:10]


def yesterday_hot():
    yesterday = timezone.now().date() - datetime.timedelta(days=1)
    novels = Nover.objects \
        .filter(read_detail__date=yesterday) \
        .values('noverid', 'novername') \
        .annotate(read_num_sum=Sum('read_detail__read_num')) \
        .order_by('-read_num_sum')
    return novels[:10]


def week_hot():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    novels = Nover.objects \
        .filter(read_detail__date__lt=today, read_detail__date__gte=date) \
        .values('noverid', 'novername') \
        .annotate(read_num_sum=Sum('read_detail__read_num')) \
        .order_by('-read_num_sum')
    return novels[:10]
