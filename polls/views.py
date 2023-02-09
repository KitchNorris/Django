from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Topic, Entry, Subscribe, EntrySerializer
from .forms import TopicForm, EntryForm, SubsForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.core.paginator import Paginator


def ind(request):
    return render(request, 'polls/ind.html')


@login_required
def topics(request):
    topicz = Topic.objects.filter(owner=request.user).order_by('-pub_date')
    context = {'topics': topicz}
    return render(request, 'polls/topics.html', context)


@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    #if topic.owner != request.user:
    #    raise Http404

    entries = topic.entry_set.order_by('-pub_date')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'polls/topic.html', context)


@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('polls:topics'))

    context = {'form': form}
    return render(request, 'polls/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('polls:topic', args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'polls/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('polls:topic', args=[topic.id]))

    context = {'topic': topic, 'entry': entry, 'form': form}
    return render(request, 'polls/edit_entry.html', context)


@login_required
def uss(request):
    usz = User.objects.all()
    context = {'uss': usz}
    return render(request, 'polls/uss.html', context)


@login_required
def ussort(request):
    topic_sort = User.objects.annotate(tscore=Count('topic')).order_by('-tscore')
    context = {'uss': topic_sort}
    return render(request, 'polls/uss.html', context)


@login_required
def userstops(request, us):
    topics = Topic.objects.filter(owner=us).order_by('-pub_date')
    name = User.objects.get(id=us)
    proof = Subscribe.objects.filter(subs=name).exists()

    if request.POST.get('subscribe'):
        if proof != True:
            form = SubsForm()
            new_sub = form.save(commit=False)
            new_sub.meown = request.user
            new_sub.subs = name
            new_sub.save()

    elif request.POST.get('unsubscribe'):
        delsub = Subscribe.objects.filter(meown=request.user).get(subs=name)
        delsub.delete()
    context = {'topics': topics, 'username': name, 'proof': proof, 'us': us}
    return render(request, 'polls/userstops.html', context)


@login_required
def lenta(request):
    subs = Subscribe.objects.filter(meown=request.user).all()
    zubz = [zub.subs for zub in subs]
    owners = User.objects.filter(username__in=zubz)
    topicsubs = Topic.objects.filter(owner__in=owners).all()
    entr = Entry.objects.filter(topic__in=topicsubs).order_by('-pub_date')

    filter = request.GET.get('filter', 'all') # Фильтрация на помеченные и все посты

    if filter == 'all':
        entrys = entr
    elif filter == 'flagged':
        entrys = entr.filter(is_read=True)

    paginator = Paginator(entrys, 10) # Пагинация
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'subs': subs, 'entrys': entrys, 'page_obj': page_obj}
    return render(request, 'polls/lenta.html', context)

def mark_as_read(request): # Помечаем прочитанные посты
    if request.method == 'POST':
        entry_id = request.POST.get('entry_id')
        entry = Entry.objects.get(id=entry_id)
        entry.is_read = True
        entry.save()
    return redirect('polls:lenta')