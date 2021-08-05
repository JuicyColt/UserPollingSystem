from rest_framework import serializers
from .models import Poll, Question, Answer
from datetime import datetime


class PollSerializer(serializers.ModelSerializer):
    question = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ('id', 'name', 'pub_date', 'expiration_date', 'description')
        extra_kwargs = {
            "name": {"required": True},
            "pub_date": {"required": True},
        }

    def validate(self, data):
        if datetime.now() > data['expiration_date']:
            raise serializers.ValidationError(
                "Error: Survey is already ended"
            )
        return data


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'title', 'answer_type', 'poll')
        extra_kwargs = {
            "title": {"required": True},
            "answer_type": {"required": True},
        }


class AnswerSerializer(serializers.Serializer):
    answers = serializers.JSONField()

    def validate_answers(self, answers):
        if not answers:
            raise serializers.ValidationError(
                "Answers must be not null."
            )
        return answers

    def save(self):
        answers = self.data['answers']
        user = self.context.user  # хз как его поставить еще
        for question_id in answers:
            question = Question.objects.get(pk=question_id)
            polls = answers[question_id]
            for poll_id in polls:
                poll = Poll.objects.get(pk=poll_id)
                Answer(user=user, question=question, poll=poll).save()
                user.save()
