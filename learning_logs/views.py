""" learning_logs/views"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .forms import TopicForm, EntryForm
from .models import Topic, Entry


# Create your views here.
def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')


@login_required
def topic_list(request):
    """Show all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic_detail(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    # Make sure that the topic is owned by the current user
    check_topic_owner(request, topic)

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Add a new topic"""
    if request.method != 'POST':
        # No data submitted; create a blank form. If method is not 'POST' it will be GET by default.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)

        if form.is_valid():
            current_topic = form.save(commit=False)
            current_topic.owner = request.user
            current_topic.save()
            form.save()
            return redirect('learning_logs:topics')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic"""
    topic = Topic.objects.get(id=topic_id)
    # Check that the topic owner is the current user.
    check_topic_owner(request, topic)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            current_entry = form.save(commit=False)
            current_entry.topic = topic
            current_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    # Display a blank or invalid form
    context = {'topic': topic,
               'form': form,
               }
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # Check that the topic owner is the current user.
    check_topic_owner(request, topic)

    if request.method != 'POST':
        # No data submitted; show existing entry
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; update the entry
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    # Display form with existing entry in html page
    context = {'entry': entry,
               'topic': topic,
               'form': form,
               }
    return render(request, 'learning_logs/edit_entry.html', context)


def check_topic_owner(request, topic):
    # Check the owner of a topic is the current logged-in user. If not raise an Http 404 error.
    if topic.owner != request.user:
        raise Http404
