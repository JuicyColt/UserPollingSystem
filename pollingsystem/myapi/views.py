from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins

from .serializers import PollSerializer, QuestionSerializer
from .models import Poll, Question


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class PollViewSet(CreateListDestroyViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        poll = get_object_or_404(Poll, pk=self.kwargs.get("poll_id"))
        return poll.questions.all()

    def perform_create(self, serializer):
        poll = get_object_or_404(Poll, pk=self.kwargs.get("poll_id"))
        serializer.save(poll=poll)
