import json

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from rest_framework.views import APIView

from backend.api.utils.games import update_games

TASK_UPDATE_GAMES = "update_games"

ALLOWED_TASKS = [TASK_UPDATE_GAMES]


class TasksApiView(APIView):
    def post(self, request):
        if not request.body:
            return HttpResponseBadRequest()

        body = json.loads(request.body)
        if "task" not in body or body["task"] not in ALLOWED_TASKS:
            return HttpResponseBadRequest()

        if body["task"] == TASK_UPDATE_GAMES:
            update_games()
            return HttpResponse()
        else:
            return HttpResponseNotFound()
