from django.test import TestCase
import datetime
from django.urls import reverse
from django.utils import timezone
from polls.models import Topic, Entry, Subscribe
from polls.forms import TopicForm, EntryForm, SubsForm
from django.contrib.auth.models import User


class TopicFormTest(TestCase):
    def test_topic_form_text_field_label(self):
        form = TopicForm()
        self.assertTrue(form.fields['text'].label == None or form.fields['text'].label == '')

    def test_topic_form_valid_data(self):
        form_data = {'text': 'Test Topic'}
        form = TopicForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_topic_form_no_data(self):
        form_data = {'text': ''}
        form = TopicForm(data=form_data)
        self.assertFalse(form.is_valid())


class EntryFormTest(TestCase):
    def test_entry_form_text_field_label(self):
        form = EntryForm()
        self.assertTrue(form.fields['text'].label == None or form.fields['text'].label == '')

    def test_entry_form_valid_data(self):
        form_data = {'text': 'Test Entry'}
        form = EntryForm(data=form_data)
        self.assertTrue(form.is_valid())


class SubsFormTest(TestCase):
    def test_subs_form_subs_field_label(self):
        form = SubsForm()
        self.assertTrue(form.fields['subs'].label == None or form.fields['subs'].label == '')

    def test_subs_form_valid_data(self):
        form_data = {'subs': 'Test Subscription'}
        form = SubsForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_subs_form_no_data(self):
        form_data = {'subs': ''}
        form = SubsForm(data=form_data)
        self.assertFalse(form.is_valid())
