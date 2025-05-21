from django.contrib import admin
from .models import Topic, Test, UserAnswer, MyLearning, Ope

# Register your models here.


class TestOpeAdmin(admin.ModelAdmin):
    list_display = ("id","name","entity","dateTime","locality","province")
admin.site.register(Ope,TestOpeAdmin)


class TopicAdmin(admin.ModelAdmin):
    list_display = ("id","name","ope")
admin.site.register(Topic,TopicAdmin)


class TestAdmin(admin.ModelAdmin):
    list_display = ("id", "number","topic", "question", "aAnswer", "bAnswer", "cAnswer", "dAnswer", "correctAnswer")
    list_filter = ('ope',)
admin.site.register(Test,TestAdmin)


class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ("user","ope", "number","answerProgresionCorrect","correctAnswerCounterTotal","incorrectAnswerCounterTotal","datetime","lastAnsweredQuestion","questionCircleCounter")
admin.site.register(UserAnswer,UserAnswerAdmin)

class MyLearningAdmin(admin.ModelAdmin):
    list_display = ("user","ope","datetime")
admin.site.register(MyLearning,MyLearningAdmin)
