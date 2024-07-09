from django.shortcuts import render
from django.shortcuts import get_object_or_404, render


# Create your views here.

from django.http import HttpResponse

from .models import Question
from smart_sql import smart_sql_query_v2

# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     output = ", ".join([q.question_text for q in latest_question_list])
#     return HttpResponse(output)

# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     template = loader.get_template("polls/index.html")
#     context = {
#         "latest_question_list": latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)


def voice(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/voice.html", context)

def smart_query(request, input):
    # latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # context = {"latest_question_list": latest_question_list}
    res = []
    try:
        res = smart_sql_query_v2.query_demo(input)
    except Exception as e:
        print(e)

    response = "smart query: input {input} ********************  result: {res}".format(input = input, res = res)

    return HttpResponse(response)

    # return HttpResponse("smart query: res %s" %res)


# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)


# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, "./detail.html", {"question": question})


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "detail.html", {"question": question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)