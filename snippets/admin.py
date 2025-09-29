from django.contrib import admin
from snippets.models import Snippet
from snippets.models import Comment

admin.site.register(Snippet)
admin.site.register(Comment)



