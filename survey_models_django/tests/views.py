from .models import Answer, Option, Test, Testrun
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin


class TestListView(ListView):
    model = Test
    template_name = 'home.html'


class TestDetailView(DetailView):
    model = Test
    template_name = 'tests/detail.html'


class TestSessionView(DetailView):
    
    model = Test
    template_name = 'tests/start.html'

    def post(self, request, **kwargs):
        test = Test.objects.get(pk=kwargs['pk'])
        self.create_test_session(request, test)
        return redirect('/')

    def create_test_session(self, request, test: Test) -> None:
        points = 0
        instance = Testrun.objects.create(test=test, user=self.get_user(request))
        for question in test.questions.all():
            answer_id = request.POST.get(str(question.id))
            if answer_id is not None:
                user_option = Option.objects.get(id=answer_id)
                instance.answers.add(Answer.objects.create(user_answer=user_option,
                                                        question=question))
                if user_option == question.right_option:
                    points += 1
        instance.points = points
        instance.save()

    def get_user(self, request):
        if request.user.is_authenticated:
            return request.user
        return None


class TestSessionHistoryView(ListView):
    model = Testrun
    template_name = 'tests/history.html'
    def get_queryset(self):
        return Testrun.objects.filter(test__id=self.request.resolver_match.kwargs['pk']).order_by('-finished_at')
    ordering = ['-finished_at']


class TestScoreView(LoginRequiredMixin, ListView):
    login_url = "/auth/login/"
    permission_denied_message = 'To see your scores you should sign in first'
    model = Testrun
    template_name = 'tests/myscores.html'
    context_object_name = 'test_sessions'
    def get_queryset(self):
        return Testrun.objects.filter(user__id=self.request.user.id).order_by('-finished_at')
