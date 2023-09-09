import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_not_published_yet(self):
        """Test if the is_published return False if the question pub_date was set with the future date."""
        future = timezone.now() + datetime.timedelta(days=10)
        question = Question(pub_date=future)
        self.assertFalse(question.is_published())

    def test_default_publish_date(self):
        """Test if the question is publishing if the date is not be manually set."""
        question = Question()
        self.assertTrue(question.is_published())

    def test_past_published_date(self):
        """Test if the question pub_date was set with the past date."""
        past = timezone.now() - datetime.timedelta(days=10)
        question = Question(pub_date=past)
        self.assertTrue(question.is_published())

    def test_cannot_vote_before_published(self):
        """Test that user can't vote in the question that's not published yet."""
        future_1 = timezone.now() + datetime.timedelta(days=10)
        future_2 = timezone.now() + datetime.timedelta(seconds=1)
        future_3 = timezone.now() + datetime.timedelta(days=0.0001)
        question_1 = Question(pub_date=future_1)
        question_2 = Question(pub_date=future_2)
        question_3 = Question(pub_date=future_3)
        self.assertFalse(question_1.can_vote())
        self.assertFalse(question_2.can_vote())
        self.assertFalse(question_3.can_vote())

    def test_can_vote_now(self):
        """Test that user can vote if the question are in the voting period and just published."""
        now = timezone.now()
        future = now + datetime.timedelta(days=10)
        question_1 = Question()
        question_2 = Question(pub_date=now)
        question_3 = Question(pub_date=now, end_date=future)
        self.assertTrue(question_1.can_vote())
        self.assertTrue(question_2.can_vote())
        self.assertTrue(question_3.can_vote())

    def test_can_vote_past(self):
        """Test that user can vote for the vote that has been published and not end yet."""
        now = timezone.now()
        past = now - datetime.timedelta(days=10)
        future = now + datetime.timedelta(days=10)
        near = now + datetime.timedelta(seconds=0.0001)
        question_1 = Question(pub_date=past)
        question_2 = Question(pub_date=past, end_date=near)
        question_3 = Question(pub_date=past, end_date=future)
        self.assertTrue(question_1.can_vote())
        self.assertTrue(question_2.can_vote())
        self.assertTrue(question_3.can_vote())

    def test_end_date(self):
        """Test that user can't vote if the end date passed but can vote if not."""
        now = timezone.now()
        past = now - datetime.timedelta(days=10)
        near = now + datetime.timedelta(seconds=0.0001)
        question_1 = Question(end_date=past)
        question_2 = Question(end_date=now)
        question_3 = Question(end_date=near)
        self.assertFalse(question_1.can_vote())
        self.assertFalse(question_2.can_vote())
        self.assertTrue(question_3.can_vote())


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
