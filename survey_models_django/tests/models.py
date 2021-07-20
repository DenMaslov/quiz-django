from django.db import models
from django.contrib.auth.models import User


class Option(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text 


class Question(models.Model):
    text = models.TextField()
    options = models.ManyToManyField(Option, related_name='question_set')
    right_option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='question')

    def __str__(self):
        return self.text


class Answer(models.Model):
    user_answer = models.ForeignKey(Option, on_delete=models.CASCADE, default=None, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class Test(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, unique=True)
    questions = models.ManyToManyField(Question, related_name="test", blank=True)
    description = models.CharField(max_length=280, blank=True)
    image_src = models.CharField(max_length=120, blank=True, default="https://source.unsplash.com/random")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    

class Testrun(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    answers = models.ManyToManyField(Answer, related_name="answers", blank=True)
    points = models.PositiveIntegerField(default=0, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=None, null=True)
    finished_at = models.DateTimeField(auto_now_add=True)

