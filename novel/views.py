import re
import time
import requests
from requests.adapters import HTTPAdapter
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from .models import Novel, Chapter
from read_statistics.utils import statistics_read_once

s = requests.session()
s.mount('http://', HTTPAdapter(max_retries=3))

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36",
}


def code(res):
    if res.status_code == 200:
        if res.encoding == 'ISO-8859-1':
            encodings = requests.utils.get_encodings_from_content(res.text)
            if encodings:
                res.encoding = encodings[0]
            else:
                res.encoding = res.apparent_encoding


def novel_list(request):
    novels = Novel.objects.all()
    paginator = Paginator(novels, settings.EACH_PAGE_NOVELS_NUMBER, 2)
    page_number = request.GET.get('page', 1)
    page_of_novels = paginator.get_page(page_number)
    current_page_num = page_of_novels.number

    page_range = [i for i in range(current_page_num - 2, current_page_num + 3) if 0 < i < paginator.num_pages]
    if page_range:
        if page_range[0] - 1 >= 2:
            page_range.insert(0, '...')
        if paginator.num_pages - page_range[-1] >= 2:
            page_range.append('...')
        if page_range[0] != 1:
            page_range.insert(0, 1)
        if page_range[-1] != paginator.num_pages:
            page_range.append(paginator.num_pages)
    else:
        page_range.append(1)
    context = {'page_of_novels': page_of_novels, 'page_range': page_range}
    return render(request, 'novel/novel_list.html', context)


def novel_detail(request, novelid):
    context = {'novel_detail': get_object_or_404(Novel, novelid=novelid)}
    key = statistics_read_once(request, context['novel_detail'])
    context['chapter_list'] = Chapter.objects.filter(novelid=novelid)
    response = render(request, 'novel/novel_detail.html', context)
    response.set_cookie(key, 'True', max_age=3600)
    return response


def novel_writer(request, writername):
    novels = Novel.objects.filter(writername=writername)
    paginator = Paginator(novels, settings.EACH_PAGE_NOVELS_NUMBER)
    page_number = request.GET.get('page', 1)
    page_of_novels = paginator.get_page(page_number)
    current_page_num = page_of_novels.number
    page_range = [i for i in range(current_page_num - 2, current_page_num + 3) if 0 < i < paginator.num_pages]
    if page_range:
        if page_range[0] - 1 >= 2:
            page_range.insert(0, '...')
        if paginator.num_pages - page_range[-1] >= 2:
            page_range.append('...')
        if page_range[0] != 1:
            page_range.insert(0, 1)
        if page_range[-1] != paginator.num_pages:
            page_range.append(paginator.num_pages)
    else:
        page_range.append(1)
    context = {'page_of_novels': page_of_novels}
    context['page_of_novels'].writername = writername
    context['page_range'] = page_range
    return render(request, 'novel/novel_writer.html', context)


def chapter_detail(request, chapterid):
    chapter = get_object_or_404(Chapter, chapterid=chapterid)
    try:
        res = s.get(chapter.content, headers=header, timeout=(3, 7))
        code(res)
        res = res.text.encode("utf-8").decode("utf-8")
        pattern = re.compile('id="content">(.*?)<a href="http:', re.S)
        content = re.findall(pattern, res)
        s.close()
        chapter.content = content[0]
    except requests.exceptions.ConnectionError as e:
        print(e)
        time.sleep(5)
        chapter_detail(request, chapterid)
    context = {'chapter': chapter}
    if Chapter.objects.filter(novelid=chapter.novelid, chapterid__lt=chapter.chapterid).last():
        context['previous_chapter'] = Chapter.objects.filter(novelid=chapter.novelid,
                                                             chapterid__lt=chapter.chapterid).last()
    else:
        context['previous_chapter'] = chapter
    if Chapter.objects.filter(novelid=chapter.novelid, chapterid__gt=chapter.chapterid).first():
        context['next_chapter'] = Chapter.objects.filter(novelid=chapter.novelid,
                                                         chapterid__gt=chapter.chapterid).first()
    else:
        context['next_chapter'] = chapter
    return render(request, 'novel/chapter_detail.html', context)
