from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from read_statistics.utils import get_weeks_read_num, today_hot, yesterday_hot, week_hot
from novel.models import Nover


def home(request):
    novel_content_type = ContentType.objects.get_for_model(Nover)
    read_nums, dates = get_weeks_read_num(novel_content_type)
    today_hot_data = today_hot()
    yesterday_hot_data = yesterday_hot()
    week_hot_data = cache.get('week_hot_data')
    if week_hot_data is None:
        week_hot_data = week_hot()
        cache.set('week_hot_data', week_hot_data, 3000)
    context = {
        'read_nums': read_nums,
        'dates': dates,
        'today_hot_data': today_hot_data,
        'yesterday_hot_data': yesterday_hot_data,
        'week_hot_data': week_hot(),
    }
    return render(request, 'home.html', context)


