from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from .models import Choice, Question, Vote


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
        ).order_by('-pub_date')


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
            question = get_object_or_404(Question, pk=kwargs["pk"])
        except Http404:
            messages.error(request, f"Poll {kwargs['pk']} is not available.")
            return redirect('polls:index')

        try:
            vote = Vote.objects.get(user=request.user, choice__in=question.choice_set.all())
            previously_selected = vote.choice
        except (Vote.DoesNotExist, TypeError):
            previously_selected = None

        if not question.can_vote():
            messages.error(request, "This poll is currently closed.")
            return redirect('polls:index')

        return render(request, self.template_name, {"question": question, "previously_selected": previously_selected})


class ResultsView(generic.DetailView):
    """View for display result of the poll"""
    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    """
    View for handling user votes for a specific poll question.
    """
    question = get_object_or_404(Question, pk=question_id)

    if not question.can_vote():
        messages.error(request, f"This poll does not allow to vote.")
        return redirect("polls:index")

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        messages.error(request, "Please select choice before submit the vote.")
        return redirect("polls:detail", pk=question_id)

    this_user = request.user

    try:
        # find a vote for this user and this question
        vote = Vote.objects.get(user=this_user, choice__question=question)
        # update his vote
        vote.choice = selected_choice
    except Vote.DoesNotExist:
        # no matching vote - create a new Vote
        vote = Vote(user=this_user, choice=selected_choice)

    vote.save()

    messages.success(request, f"Your vote for '{vote.choice}' has been saved.")

    return HttpResponseRedirect(
        reverse('polls:results', args=(question_id,))
    )


def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # get named fields from the form data
            username = form.cleaned_data.get('username')
            # password input field is named 'password1'
            raw_passwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_passwd)
            login(request, user)
            return redirect('polls:index')
        # what if form is not valid?
        # we should display a message in signup.html
    else:
        # create a user form and display it the signup page
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
