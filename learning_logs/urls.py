"""Defines URL patterns for learning_logs"""

from django.urls import path

from . import views

app_name = 'learning_logs'

urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page that shows all topics. E.g. /topics
    path('topics/', views.topic_list, name='topics'),
    # Detail page for a single topic. E.g. /topics/5
    path('topics/<int:topic_id>/', views.topic_detail, name='topic'),
    # Form page to add a new topic. E.g. /new_topic
    path('new_topic/', views.new_topic, name='new_topic'),
    # Form page for adding a new entry for a topic. E.g. /new_entry/2
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # Form page to edit an existing entry. /edit_entry. E.g. /edit_entry/4
    path('edit_entry/<int:entry_id>', views.edit_entry, name='edit_entry')
]