"""Views for Polls Application"""
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from .models import Choice, Question


class IndexView(generic.ListView):
    """Index view of index.html"""
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.localtime()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """Detail view of detail.html"""
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(
            pub_date__lte=timezone.localtime())

    def get(self, request, pk):
        """Handle of get request to return correct response to detail view."""
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            messages.error(request, "Poll dosen't exist.")
            return HttpResponseRedirect(reverse('polls:index'))

        if not question.can_vote():
            messages.error(request, "Voting is not allowed on this question")
            return HttpResponseRedirect(reverse('polls:index'))
        return render(request, 'polls/detail.html', {'question': question})


class ResultsView(generic.DetailView):
    """Results view of results.html"""
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    """Vote function for voting button"""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
