from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import PollViewSet, QuestionViewSet


router = DefaultRouter()
router.register('poll', PollViewSet)
router.register(
    r'poll/(?P<poll_id>\d+)/question',
    QuestionViewSet, basename='questions'
)
urlpatterns = [
    path('', include(router.urls)),
]
