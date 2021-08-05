from django.utils.translation import gettext as _
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Poll(models.Model):
    """Модель опроса
    Атрибуты опроса:
     название, дата старта, дата окончания, описание"""
    name = models.CharField(
        max_length=50, blank=False, verbose_name='Название опроса'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True
    )
    expiration_date = models.DateTimeField(
        verbose_name='Дата окончания', default=None
    )
    description = models.TextField(
        null=True, verbose_name='Описание'
    )

    class Meta:
        ordering = ['-id', ]

    def __str__(self) -> str:
        return f'{self.name}'


class Question(models.Model):
    """Модель вопроса
    Атрибуты вопроса:
         вопрос, ответ, тип ответа"""

    TYPE = (
        ('text', _('text response')),
        ('one', _('response with a choice of one option')),
        ('several', _('response with a choice of several options')),
    )

    title = models.TextField(verbose_name='Наименование вопроса')
    answer_type = models.CharField(
        max_length=32,
        choices=TYPE,
        verbose_name='Тип ответа',
        related_name='answers'
    )
    poll = models.ManyToManyField(
        Poll, related_name='questions', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id', ]

    def __str__(self) -> str:
        return f'{self.question}'


class Answer(models.Model):
    user_id = models.IntegerField()
    question = models.ForeignKey(
        Question, on_delete=models.DO_NOTHING,
        related_name='answers'
    )
    choice = models.ForeignKey(
        Poll, on_delete=models.DO_NOTHING,
        related_name='answers'
    )
