from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from polls.models import WeeklyQuestion, WeeklyAnswer


def landing(request):
    if hasattr(request, 'user') and request.user.is_authenticated:
        return HttpResponseRedirect(settings.AFTER_LOGIN_URL)
    return render(request, 'polls/landing.html')


@login_required(login_url=settings.LOGIN_URL)
def index(request):
    context = {}
    wq_qs = WeeklyQuestion.retrieve_wq_qs_for_user(request.user)

    context['weekly_question_count'] = wq_qs.count()
    context['available_survey_count'] = 0

    return render(request, 'polls/index.html', context)


@login_required(login_url=settings.LOGIN_URL)
def settings_page(request):
    return render(request, 'polls/settings_page.html')


def error_page(request):
    return render(request, 'polls/error_page.html')


@login_required(login_url=settings.LOGIN_URL)
def question_types(request):
    return render(request, 'polls/question_types.html')


def meta(request):
    user_count = User.objects.all().count()
    return JsonResponse({'users': user_count})


@login_required(login_url=settings.LOGIN_URL)
def weekly_question(request):
    """ Checks whether there is a weekly question which can be answered by a user else it show no question available """
    context = {}

    # If there is a weekly question that can be answered it will return one
    wq = WeeklyQuestion.retrieve_wq_qs_for_user(request.user)
    context['weekly_question'] = wq.first()
    context['remaining_weekly_question'] = wq.count()

    return render(request, 'polls/weekly_question.html', context)


@login_required(login_url=settings.LOGIN_URL)
def specific_survey(request):
    return HttpResponse("Weekly question")


@login_required(login_url=settings.LOGIN_URL)
def answer_weekly_question(request):
    context = {}

    question_id = request.GET.get('question_id')
    answer_value = request.GET.get('answer_value')

    try:
        question_id = int(question_id)
        answer_value = int(answer_value)

        wq = WeeklyQuestion.objects.get(id=question_id)

        already_answered = WeeklyAnswer.objects.filter(answered_by=request.user, question=wq)\
            .exclude(answer_again_from__lt=timezone.now()).exists()

        if already_answered:
            context['error_message'] = "Question already answered!"
        elif answer_value not in wq.answers.values():
            context['error_message'] = "Answer value not in the possible answers"
        else:
            WeeklyAnswer.answer_question(request.user, answer_value, wq, timezone.now())

            open_weekly_questions = WeeklyQuestion.retrieve_wq_qs_for_user(request.user).count()

            if open_weekly_questions > 0:
                return HttpResponseRedirect(reverse('weekly_question'))
            else:
                return HttpResponseRedirect(reverse('index'))

    except WeeklyQuestion.DoesNotExist:
        context['error_message'] = "Could not find the question you tried to answer!"
    except Exception:
        context['error_message'] = "Some error occurred during recording your answer"
    return render(request, 'polls/error_page.html', context)