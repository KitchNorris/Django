from django.test import TestCase
import datetime
from django.urls import reverse
from django.utils import timezone
from polls.models import Topic, Subscribe, Entry
from django.contrib.auth.models import User


class TopicModelTest(TestCase):

    def setUp(self): # Создаем пользователя и экземпляр темы, который вызывается перед каждым тестовым методом
        self.user = User.objects.create_user(
            username='testuser', password='secret')
        self.topic = Topic.objects.create(text='Test Topic', owner=self.user)

    def test_topic_str_representation(self): # тестирует __str__метод, чтобы убедиться, что он возвращает
        self.assertEqual(str(self.topic), self.topic.text) # ожидаемое текстовое представление темы

    def test_topic_creation(self): # проверяет, что тема была успешно создана и имеет правильные
        self.assertEqual(Topic.objects.count(), 1) # значения для текстовых полей и полей владельца.
        self.assertEqual(Topic.objects.first().text, 'Test Topic')
        self.assertEqual(Topic.objects.first().owner, self.user)


class EntryModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', password='test_password')
        self.topic = Topic.objects.create(
            text='Test topic', owner=self.user)
        self.entry = Entry.objects.create(
            topic=self.topic, text='Test entry', is_read=False)

    def test_entry_str_representation(self):
        self.assertEqual(str(self.entry), self.entry.text[:50]+'...')

    def test_entry_is_read(self):
        self.assertEqual(self.entry.is_read, False)


class SubscribeModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', password='test_password')
        self.subscribe = Subscribe.objects.create(
            subs='Test subscribe', meown=self.user)

    def test_subscribe_str_representation(self):
        self.assertEqual(str(self.subscribe), self.subscribe.subs)