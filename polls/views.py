from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from .models import Choice, Question


class IndexView(generic.ListView):
    """
    View for displaying a list of the published questions.
    """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """
    View for display detail of each poll question
    including a list of choices.
    """
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """
        Receive the request from the user and catch
        the direct-access attempt to the unpublished polls.
        """
        try:
            self.object = self.get_object()
            if not self.object.can_vote():
                messages.error(request, "This poll is currently closed.")
                return redirect('polls:index')
        except Http404:
            messages.error(request, "This poll is not available.")
            return redirect('polls:index')

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ResultsView(generic.DetailView):
    """View for display result of the poll"""
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    """
    View for handling user votes for a specific poll question.
    """
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
        return HttpResponseRedirect(reverse('polls:results',
                                            args=(question.id,)))
