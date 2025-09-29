from django.conf import settings
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from snippets.models import Snippet
from snippets.forms import SnippetForm
from snippets.forms import CommentForm


def top(request):
    snippets = Snippet.objects.all() # get all snippets
    context = {'snippets': snippets} # python ooj. to pass to the template
    return render(request, 'snippets/top.html', context=context)

@login_required
def snippet_new(request):
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.created_by = request.user
            snippet.save()
            return redirect(snippet_detail, snippet_id=snippet.pk)
    else:
        form = SnippetForm()
    return render(request, "snippets/snippet_new.html", {'form': form})

@login_required
def snippet_edit(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    if snippet.created_by_id != request.user.id:
        return HttpResponseForbidden("このスニペットの編集は許可されていません。")

    if request.method == "POST":
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return redirect('snippet_detail', snippet_id=snippet_id)
    else:
        form = SnippetForm(instance=snippet)
    return render(request, 'snippets/snippet_edit.html', {'form': form})


def snippet_detail(request, snippet_id):
        # 投稿者も合わせて効率よく取得
    snippet = get_object_or_404(
        Snippet.objects.select_related('created_by'),
        pk=snippet_id
    )

    # 逆参照名: related_name を付けた場合は snippet.comments
    # 付けていないなら snippet.comment_set に置換
    comments_qs = snippet.comments.select_related('commented_by').order_by('-created_at')

    if request.method == 'POST':
        # 未ログイン投稿はログインへ
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.commented_to = snippet
            comment.commented_by = request.user
            comment.save()
            messages.success(request, 'コメントを投稿しました。')
            return redirect('snippet_detail', snippet_id=snippet_id)
    else:
        form = CommentForm()

    context = {
        'snippet': snippet,
        'comments': comments_qs,
        'comment_form': form,  # ← テンプレで描画
    }
    return render(request, 'snippets/snippet_detail.html', context)