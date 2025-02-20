from django.contrib import admin
from .models import Category, Test, UserAnswer, MyLearning

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","name")
admin.site.register(Category,CategoryAdmin)


class TestAdmin(admin.ModelAdmin):
    list_display = ("number","category", "question", "aAnswer", "bAnswer", "cAnswer", "dAnswer", "correctAnswer")
    list_filter = ('category',)
admin.site.register(Test,TestAdmin)


class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ("user","category", "number","answerProgresionCorrect","correctAnswerCounterTotal","incorrectAnswerCounterTotal","datetime","lastAnsweredQuestion","questionCircleCounter")
admin.site.register(UserAnswer,UserAnswerAdmin)

class MyLearningAdmin(admin.ModelAdmin):
    list_display = ("user","category","datetime")
admin.site.register(MyLearning,MyLearningAdmin)
