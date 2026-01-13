from django.contrib import admin
from django.urls import path
from events import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', views.events_list_create),
    path('events/<int:event_id>/', views.event_get_update_delete),
    path('events/upcoming/', views.upcoming_events),
]
