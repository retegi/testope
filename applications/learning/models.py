from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

# Create your models here


class Category(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    categoryImage = models.ImageField(upload_to='static/category/images', null=True, blank=True)
    def __str__(self):
        return self.name

correctAnswer = [('A','A'),('B','B'),('C','C'),('D','D'),('No detallado','No detallado')]

class Test(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    number = models.IntegerField(blank=True, null=True)
    question = models.TextField(max_length=500, blank=True, null=True)
    aAnswer = models.CharField(max_length=350, blank=True, null=True)
    bAnswer = models.CharField(max_length=350, blank=True, null=True)
    cAnswer = models.CharField(max_length=350, blank=True, null=True)
    dAnswer = models.CharField(max_length=350, blank=True, null=True)
    correctAnswer = models.CharField(choices=correctAnswer,max_length=15, blank=True, null=True)
    def __str__(self):
        return self.question


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.IntegerField(blank=True, null=True)
    category = models.CharField(max_length=30,blank=True, null=True)
    answerProgresionCorrect = models.IntegerField(blank=True, null=True)
    correctAnswerCounterTotal = models.IntegerField(blank=True, null=True) #Si se redsponde incorrecto se resetea a cero
    incorrectAnswerCounterTotal = models.IntegerField(blank=True, null=True)
    questionCircleCounter = models.IntegerField(blank=True, null=True)
    lastAnsweredQuestion = models.IntegerField(blank=True, null=True)
    datetime = models.DateTimeField(default=timezone.now, null=True)
    def __str__(self):
        return str(self.id)
    
class MyLearning(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    datetime = models.DateTimeField(default=timezone.now, null=True)
    def __str__(self):
        return str(self.category)
    