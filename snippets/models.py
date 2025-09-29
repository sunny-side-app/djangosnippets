from django.conf import settings
from django.db import models


class Snippet(models.Model):
    title = models.CharField('タイトル', max_length=128)
    code = models.TextField('コード', blank=True)
    description = models.TextField('説明', blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name="投稿者",
                                   on_delete=models.CASCADE)
    created_at = models.DateTimeField("投稿日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    commented_to = models.ForeignKey(
        Snippet, verbose_name="スニペット", 
        on_delete=models.CASCADE,
        related_name='comments'
        )
    commented_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="投稿者",
        on_delete=models.CASCADE)
    text = models.TextField("本文")
    created_at = models.DateTimeField("投稿日",auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.commented_by} on {self.commented_to}'