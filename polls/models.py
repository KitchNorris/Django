from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers


class Topic(models.Model):
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('pub_date', auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Entry(models.Model):
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField('pub_date', auto_now_add=True)

    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.text[:50] + '...'


class Subscribe(models.Model):
    subs = models.CharField('subs', max_length=200)
    meown = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.subs


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'