from django.test import TestCase
from django.contrib.auth.models import User
from django.test import TestCase
from question.models import EssayQuestion
from question.models import MultipleChoiceAnswer
from question.models import MultipleChoiceQuestion

from .views import get_organized_multi_questions
from .models import Quiz

# Create your tests here.
class QuizTest(TestCase):
    def setUp(self):  # create temporary database for testing.
        self.user1 = User.objects.create(username="test", password="1", email="1@g.com")
        self.quiz1 = Quiz.objects.create(title="quiz1", description="testing", creator=self.user1)

        self.eq1 = EssayQuestion.objects.create(question_body="Is this Final0?", answer="Yes", quiz=self.quiz1)
        self.eq2 = EssayQuestion.objects.create(question_body="Is this Final1?", answer="No", quiz=self.quiz1)

        correct_ans1 = "Today"
        correct_ans2 = "Tomorrow"
        self.mq1 = MultipleChoiceQuestion.objects.create(quiz=self.quiz1, question_body="When is it due?", correct_answer=correct_ans1)
        self.choice1_1 = MultipleChoiceAnswer.objects.create(question=self.mq1, answer_body="IDK")
        self.choice1_2 = MultipleChoiceAnswer.objects.create(question=self.mq1, answer_body="Today")

        self.mq2 = MultipleChoiceQuestion.objects.create(quiz=self.quiz1, question_body="When is the deadline?", correct_answer=correct_ans2)
        self.choice2_1 = MultipleChoiceAnswer.objects.create(question=self.mq2, answer_body="IDK")
        self.choice2_2 = MultipleChoiceAnswer.objects.create(question=self.mq2, answer_body="Tomorrow")

    def test_essay_question_store1(self):
        self.assertEqual("Yes", EssayQuestion.objects.get(question_body="Is this Final0?").answer)

    def test_essay_question_store2(self):
        self.assertEqual("No", EssayQuestion.objects.get(question_body="Is this Final1?").answer)

    def test_multi_question_store1(self):
        self.assertEqual("Today", MultipleChoiceQuestion.objects.get(question_body="When is it due?").correct_answer)

    def test_multi_question_store2(self):
        self.assertEqual("Tomorrow", MultipleChoiceQuestion.objects.get(question_body="When is the deadline?").correct_answer)

    def test_organized_multi_q_a1(self):
        multi_question = get_organized_multi_questions(self.quiz1)
        self.assertEqual('Today', multi_question[0]['correct_ans'])
        self.assertEqual('IDK', multi_question[0]['choices'][0])
        self.assertEqual('Today', multi_question[0]['choices'][1])

    def test_organized_multi_q_a2(self):
        multi_question = get_organized_multi_questions(self.quiz1)
        self.assertEqual('Tomorrow', multi_question[1]['correct_ans'])
        self.assertEqual('IDK', multi_question[1]['choices'][0])
        self.assertEqual('Tomorrow', multi_question[1]['choices'][1])

    def test_quiz_store1(self):
        self.assertEqual('quiz1', Quiz.objects.get(creator=self.user1).title)

