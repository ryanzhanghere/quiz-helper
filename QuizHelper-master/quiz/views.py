from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
import itertools
from copy import deepcopy
from django.contrib.auth.decorators import login_required
from question.models import EssayQuestion
from question.models import MultipleChoiceQuestion
from question.models import MultipleChoiceAnswer
from quiz.models import Quiz
from document.models import Document
from comment.models import Comment
from django.http import Http404

import xml.etree.ElementTree as ET
from xml.dom.minidom import parse
import xml.dom.minidom

CHOICE_LIMIT = 4


# Create your views here.
@login_required
def index(request):
    """
    Home page for a quiz.
    :param request:
    :return:
    """
    if request.method == 'GET':
        try:
            quiz = Quiz.objects.get(id=request.GET.get("quiz_id"))
        except Quiz.DoesNotExist:
            raise Http404("Quiz does not exist")

        context = fill_in_context(quiz, request)
        context['comment_tree'] = Comment.objects.filter(quiz_id=quiz).order_by('path')
    return render(request, 'quiz/quiz_page.html', context)


@login_required
def create_quiz_from_file(request):
    if request.method == 'POST':
        quiz_file = Document.objects.create(author=request.user, docfile=request.FILES.get('quiz-file'))
        save_as_quiz(quiz_file, request)
    return HttpResponseRedirect('/accounts/profile')


def save_as_quiz(quiz_file, request):
    """
    Parse the file and store the quiz into database
    :param quiz_file:
    :param request:
    :return:
    """
    DOMTree = xml.dom.minidom.parse(quiz_file.docfile.path)

    quiz_node = DOMTree.documentElement
    if quiz_node.tagName == 'quiz':  # root is quiz
        print "root is quiz"
        title = quiz_node.getElementsByTagName("title")[0].childNodes[0].data
        description = quiz_node.getElementsByTagName("description")[0].childNodes[0].data

        # create quiz
        if title:
            quiz = Quiz.objects.create(title=title, description=description, creator=request.user)
        else:
            return HttpResponseRedirect('/accounts/profile')

        create_essay_questions(quiz, quiz_node)

        create_multiple_choice_questions(quiz, quiz_node)


def create_multiple_choice_questions(quiz, quiz_node):
    """
    create multiple choice questions
    :param quiz:
    :param quiz_node:
    :return:
    """
    multiple_choice_questions = quiz_node.getElementsByTagName("multiple-choice-question")
    for mq in multiple_choice_questions:

        question_node = mq.getElementsByTagName('question')[0]
        question_body = question_node.childNodes[0].data
        correct_answer = ''
        if question_node.hasAttribute("correct-answer"):
            correct_answer = question_node.getAttribute("correct-answer")
        if not correct_answer:
            continue
        choices = mq.getElementsByTagName('choice')

        choice_l = []
        for c in choices:
            choice_l.append(c.childNodes[0].data)
        if correct_answer in choice_l:
            question = MultipleChoiceQuestion.objects.create(question_body=question_body, correct_answer=correct_answer,
                                                             quiz=quiz)
            for c in choice_l:
                MultipleChoiceAnswer.objects.create(question=question, answer_body=c)


def create_essay_questions(quiz, quiz_node):
    # create essay questions
    essay_questions = quiz_node.getElementsByTagName("essay-question")
    for e_q in essay_questions:
        question = e_q.getElementsByTagName('question')[0].childNodes[0].data
        answer = e_q.getElementsByTagName('answer')[0].childNodes[0].data
        if question and answer:
            EssayQuestion.objects.create(question_body=question, answer=answer, quiz=quiz)


@login_required
def all_quizzes(request):
    """
    Display all quizzes
    :param request:
    :return:
    """
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/all_quizzes.html', locals())


def fill_in_context(quiz, request):
    """
    Populate context dictionary
    :param quiz: related quiz
    :param request:
    :return: context
    """
    essay_questions = EssayQuestion.objects.filter(quiz=quiz)
    multi_questions = get_organized_multi_questions(quiz)
    context = {'essay_questions': essay_questions}
    iterator = itertools.count(start=1)
    context['iterator'] = iterator
    context['multi_questions'] = multi_questions
    context['quiz'] = quiz
    if quiz.creator != request.user:
        context['can_edit'] = False
    else:
        context['can_edit'] = True
    return context


@csrf_exempt
@login_required
def add_comment(request):
    """
    Add comment
    :param request:
    :return:
    """
    if request.method == 'POST':
        quiz_id = request.POST.get("quiz_id")
        quiz = Quiz.objects.get(id=quiz_id)
        creator = request.user
        parent = request.POST.get("parent")
        comment_body = request.POST.get("content")
        comment = Comment.objects.create(comment_body=comment_body, quiz_id=quiz, creator=creator)
        if parent == '':
            comment.path = str(comment.id)
        else:
            parent_comment = Comment.objects.get(id=parent)
            comment.quote_id = parent_comment
            comment.depth = parent_comment.depth + 1
            comment.path = parent_comment.path + ',' + str(comment.id)
            print comment.path
        comment.save()

    return HttpResponseRedirect('/quiz/?quiz_id=' + quiz_id)


@csrf_exempt
@login_required
def add_question(request):
    """
    Handle adding essay questions request
    :param request:
    :return:
    """
    if request.method == 'POST':
        quiz_id = request.POST.get("quiz_id")
        question_body = request.POST.get("question_body")
        answer = request.POST.get("answer")
        quiz = Quiz.objects.get(id=quiz_id)
        EssayQuestion.objects.create(question_body=question_body, answer=answer, quiz=quiz)

    return HttpResponseRedirect('/quiz/?quiz_id=' + quiz_id)


@csrf_exempt
@login_required
def add_multiple_choice_question(request):
    """
    Handle adding multiple choice questions request.
    :param request:
    :return:
    """
    if request.method == 'POST':
        quiz_id = request.POST.get("quiz_id")
        quiz = Quiz.objects.get(id=quiz_id)
        question_body = request.POST.get("question_body")
        answer_idx = request.POST.get("optionsRadios")
        correct_answer = request.POST.get('answer' + answer_idx)
        store_multi_question_and_ans(correct_answer, question_body, quiz, request)

    return HttpResponseRedirect('/quiz/?quiz_id=' + quiz_id)


def store_multi_question_and_ans(correct_answer, question_body, quiz, request):
    """
    Create multiple choice questions and their corresponding answers, and store them in database.
    :param correct_answer:
    :param question_body:
    :param request:
    :param quiz:
    :return:
    """
    print correct_answer, "is"
    question = MultipleChoiceQuestion.objects.create(question_body=question_body, correct_answer=correct_answer,
                                                     quiz=quiz)
    for i in range(1, 1 + CHOICE_LIMIT):
        answer_body = request.POST.get('answer' + str(i))
        MultipleChoiceAnswer.objects.create(question=question, answer_body=answer_body)


def get_organized_multi_questions(quiz):
    """
    Fetch multiple choice questions from database
    :return: A list of questions, each question is a dictionary.
    """
    multi_questions = MultipleChoiceQuestion.objects.filter(quiz=quiz)
    questions = []
    for q in multi_questions:
        answers = MultipleChoiceAnswer.objects.filter(question=q)
        ans_list = []
        for a in answers:
            ans_list.append(a.answer_body)
        h = {}
        h['question'] = q.question_body
        h['correct_ans'] = q.correct_answer
        h['choices'] = deepcopy(ans_list)
        questions.append(deepcopy(h))
    return questions
