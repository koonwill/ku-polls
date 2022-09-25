import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question, Vote, User


def create_question(question_text, pub_days, end_days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    pub_time = timezone.localtime() + datetime.timedelta(days=pub_days)
    end_time = timezone.localtime() + datetime.timedelta(days=end_days)

    return Question.objects.create(question_text=question_text,
                                   pub_date=pub_time, end_date=end_time)


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.localtime() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.localtime() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.localtime() - datetime.timedelta(
            hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """is_published() returns False for question that not published yet."""
        time = timezone.localtime() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_is_published_with_past_question(self):
        """is_published() return True for question that already published."""
        time = timezone.localtime() - datetime.timedelta(days=1, seconds=1)
        past_question = Question(pub_date=time)
        self.assertIs(past_question.is_published(), True)

    def test_can_vote_within_voting_period(self):
        """If Question in voting period return True. if not return False."""
        votable = create_question('', -1, 5)  # Published
        unvotable = create_question('', 5, 3)  # Not Published
        self.assertIs(votable.can_vote(), True)
        self.assertIs(unvotable.can_vote(), False)

    def test_can_vote_without_end_day(self):
        """If end days didn't set can_vote() still return True(Can vote)."""
        time = timezone.localtime() - datetime.timedelta(days=1)
        question = Question(pub_date=time)
        self.assertIs(question.can_vote(), True)

    def test_can_vote_after_end_day(self):
        """can_vote() returns False for question that passing end day."""
        end_question = create_question('', pub_days=-2, end_days=-1)
        self.assertIs(end_question.can_vote(), False)

    def test_can_vote_current_time_with_pub_day(self):
        """can_vote() returns True if voting in the same time as pub_day"""
        question = create_question('', 0, 5)
        self.assertIs(question.can_vote(), True)

    def test_can_vote_current_time_with_end_day(self):
        """can_vote() returns True if voting in the same time as end_day
        (Sometime fail if running test took a long time. due to datetime)
        """
        question = create_question('', -1, 0)
        self.assertIs(question.can_vote(), True)


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
        question = create_question(
            question_text="Past question.", pub_days=-5, end_days=-3)
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
        create_question(question_text="Future question.",
                        pub_days=3, end_days=5)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(
            question_text="Past question.", pub_days=-5, end_days=-3)
        create_question(question_text="Future question.",
                        pub_days=3, end_days=5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(
            question_text="Past question 1.", pub_days=-5, end_days=-3)
        question2 = create_question(
            question_text="Past question 2.", pub_days=-4, end_days=-3)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def setUp(self) -> None:
        """Initialize user for test"""
        self.user = User.objects.create_user('Test1', password='password')
        self.user.save()
        self.client.login(username='Test1', password='password')

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 302 not found.
        """
        future_question = create_question(
            question_text='Future question.', pub_days=3, end_days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(
            question_text='Past Question.', pub_days=-5, end_days=5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class VoteViewTests(TestCase):
    def setUp(self) -> None:
        """Initialize user for test"""
        self.user = User.objects.create_user('Test2', password='password')
        self.user.save()
        self.client.login(username='Test2', password='password')

    def test_vote_count(self):
        """Check vote count for in question Test1."""
        question = create_question(
            question_text='Test1', pub_days=-1, end_days=3)
        choice = question.choice_set.create(choice_text='Test')
        Vote.objects.create(user=self.user, choice=choice)
        self.assertIs(1, choice.votes())

    def test_vote_two_question(self):
        """Vote more than one question and check."""
        # Vote for question 1
        question1 = create_question(
            question_text='Test 1', pub_days=-1, end_days=3)
        choice1 = question1.choice_set.create(choice_text='Test1')
        Vote.objects.create(user=self.user, choice=choice1)
        self.assertIs(1, choice1.votes())
        # Vote for question 2
        question2 = create_question(
            question_text='Test 2', pub_days=-1, end_days=3)
        choice2 = question2.choice_set.create(choice_text='Test2')
        Vote.objects.create(user=self.user, choice=choice2)
        self.assertIs(1, choice2.votes())

    def test_only_authenticated_user_can_vote(self):
        """Only authenticated user can vote"""
        question = create_question(
            question_text='Test 1', pub_days=-1, end_days=3)
        response1 = self.client.post(
            reverse('polls:vote', args=(question.id,)))
        self.assertEqual(response1.status_code, 200)
        self.client.logout()
        response2 = self.client.post(
            reverse('polls:vote', args=(question.id,)))
        self.assertEqual(response2.status_code, 302)

    def test_one_vote_one_question(self):
        """One user can vote only one choice for each question."""
        ques = create_question(
            question_text='Test 1', pub_days=-1, end_days=3)
        choice1 = ques.choice_set.create(choice_text='choice1')
        choice2 = ques.choice_set.create(choice_text='choice2')
        self.client.post(reverse('polls:vote', args=(
            ques.id,)), {'choice': choice1.id})
        self.assertEqual(Vote.objects.get(
            user=self.user, choice__in=ques.choice_set.all()).choice, choice1)
        self.assertEqual(Vote.objects.all().count(), 1)
        self.client.post(reverse('polls:vote', args=(
            ques.id,)), {'choice': choice2.id})
        self.assertEqual(Vote.objects.get(
            user=self.user, choice__in=ques.choice_set.all()).choice, choice2)
        self.assertEqual(Vote.objects.all().count(), 1)
