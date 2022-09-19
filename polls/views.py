"""Views for Polls Application"""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Choice, Question, Vote


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

class EyesOnlyView(LoginRequiredMixin, generic.ListView):
    # this is the default. Same default as in auth_required decorator
    login_url = '/accounts/login/'

class DetailView(LoginRequiredMixin, generic.DetailView):
    """Detail view of detail.html"""
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(
            pub_date__lte=timezone.localtime())

    def get(self, request, pk):
        """Handle of get request to return correct response to detail view."""
        if not request.user.is_authenticated:
            return redirect(to='http://127.0.0.1:8000/accounts/login')
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

@login_required
def vote(request, question_id):
    """Vote function for voting button"""
    question = get_object_or_404(Question, pk=question_id)
    user = request.user
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    try:
        # check this user vote history.
        vote = Vote.objects.get(user=user)
        vote.choice = selected_choice
        vote.save()
    except Vote.DoesNotExist:
        Vote.objects.create(user=user, choice=selected_choice).save()
    # after vote its will redirect to results page.
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
