from django.contrib import admin
from applications.social.models import TestChat
# Register your models here.


class TestChatAdmin(admin.ModelAdmin):
    list_display = ("user","text","datetime")
admin.site.register(TestChat,TestChatAdmin)