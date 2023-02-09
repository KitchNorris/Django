from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from polls.models import Topic, Entry, Subscribe
from polls.forms import TopicForm


class TopicViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.topic = Topic.objects.create(text='Test topic', owner=self.user)

    def test_ind_view(self):
        response = self.client.get(reverse('polls:ind'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/ind.html')

    def test_topics_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('polls:topics'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/topics.html')
        self.assertQuerysetEqual([str(topic) for topic in response.context['topics']], ['Test topic'])

    def test_topic_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('polls:topic', args=[self.topic.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/topic.html')

    def test_new_topic_view_get(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('polls:new_topic'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/new_topic.html')

    def test_new_topic_view_post(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('polls:new_topic'), data={'text': 'New topic'})
        self.assertRedirects(response, reverse('polls:topics'))
        self.assertEqual(Topic.objects.count(), 2)


class EntryViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.topic = Topic.objects.create(text='Test topic', owner=self.user)
        self.entry = Entry.objects.create(topic=self.topic, text='Test entry')

    def test_new_entry_view_with_login(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('polls:new_entry', args=[self.topic.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/new_entry.html')

    def test_new_entry_view_without_login(self):
        response = self.client.get(reverse('polls:new_entry', args=[self.topic.id]))
        self.assertEqual(response.status_code, 302) # Redirect to login page

    def test_edit_entry_view_with_login(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('polls:edit_entry', args=[self.entry.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/edit_entry.html')

    def test_edit_entry_view_without_login(self):
        response = self.client.get(reverse('polls:edit_entry', args=[self.entry.id]))
        self.assertEqual(response.status_code, 302) # Redirect to login page

    def test_edit_entry_view_with_different_user(self):
        other_user = User.objects.create_user(username='otheruser', password='54321')
        self.client.login(username='otheruser', password='54321')
        response = self.client.get(reverse('polls:edit_entry', args=[self.entry.id]))
        self.assertEqual(response.status_code, 404) # Http404 error


class UssViewTests(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.topic = Topic.objects.create(text='Test topic', pub_date='2022-01-01', owner=self.test_user)

    def test_uss_view(self):
        response = self.client.get(reverse('polls:uss'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/uss.html')
        self.assertQuerysetEqual([str(test_user) for test_user in response.context['uss']], ['testuser'])

    def test_ussort_view(self):
        response = self.client.get(reverse('polls:ussort'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/uss.html')
        self.assertQuerysetEqual([str(test_user) for test_user in response.context['uss']], ['testuser'])

    def test_userstops_view(self):
        response = self.client.get(reverse('polls:userstops', args=[self.test_user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/userstops.html')
        self.assertQuerysetEqual([str(topic) for topic in response.context['topics']], ['Test topic'])
        self.assertEqual(response.context['username'], self.test_user)
        self.assertEqual(response.context['proof'], False)
        self.assertEqual(int(response.context['us']), self.test_user.id)


class LentaViewTests(TestCase):
    def setUp(self):
        # create a user and log the user in
        self.test_user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        # create a topic and entry
        self.topic = Topic.objects.create(text='Test topic', pub_date='2022-01-01', owner=self.test_user)
        self.entry = Entry.objects.create(text='Test entry', pub_date='2022-01-02', topic=self.topic)

        # create a subscribe
        self.subscribe = Subscribe.objects.create(meown=self.test_user, subs=self.test_user.username)

    def test_lenta_view(self):
        response = self.client.get(reverse('polls:lenta'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/lenta.html')
        self.assertQuerysetEqual([str(entry) for entry in response.context['entrys']], ['Test entry...'])
        self.assertEqual(list(response.context['subs']), [self.subscribe])

    def test_mark_as_read_view(self):
        response = self.client.post(reverse('polls:mark_as_read'), data={'entry_id': self.entry.id})
        self.assertEqual(response.status_code, 302)
        self.entry.refresh_from_db()
        self.assertTrue(self.entry.is_read)