from django.shortcuts import render

import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from .models import Event

def serialize_event(event):
    return {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "date": event.date.isoformat(),
    }

@csrf_exempt
def events_list_create(request):
    if request.method == 'GET':
        events = [serialize_event(e) for e in Event.objects.all().order_by('date')]
        return JsonResponse(events, safe=False)

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        event = Event.objects.create(
            title=data.get('title', 'Untitled'),
            description=data.get('description', ''),
            date=data['date'],
        )
        return JsonResponse(serialize_event(event), status=201)

    return HttpResponseNotAllowed(['GET', 'POST'])

@csrf_exempt
def event_get_update_delete(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return JsonResponse({"error": "Event not found"}, status=404)

    if request.method == 'GET':
        return JsonResponse(serialize_event(event))

    if request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        event.title = data.get('title', event.title)
        event.description = data.get('description', event.description)
        event.date = data.get('date', event.date)
        event.save()
        return JsonResponse(serialize_event(event))

    if request.method == 'DELETE':
        event.delete()
        return JsonResponse({"message": "Event deleted"}, status=204)

    return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])

def upcoming_events(request):
    upcoming = Event.objects.filter(date__gte=now()).order_by('date')
    data = [serialize_event(e) for e in upcoming]
    return JsonResponse(data, safe=False)

