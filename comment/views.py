from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from .models import Comment
from .forms import CommentForm
from novel.models import Nover


def comment_views(request, novelid):
    novel = get_object_or_404(Nover, noverid=novelid)
    context = {'novel': novel}
    response = render(request, 'comment/comment.html', context)
    return response


def update_comment(request):
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}
    if comment_form.is_valid():
        # 检查表单是否有效
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        parent = comment_form.cleaned_data['parent']
        if parent is not None:
            comment.root = parent.root if parent.root is not None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()
        comment.send_mail()
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.get_nikename_or_username()
        data['comment_time'] = comment.comment_time.timestamp()
        data['text'] = comment.text
        if parent is not None:
            data['reply_to'] = comment.reply_to.get_nikename_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if comment.root is not None else ''
    else:
        data['status'] = 'ERROR'
        data['massage'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)
