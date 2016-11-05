# from django.shortcuts import render
# from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView, TemplateView
from django.contrib.auth import login, logout
from chartit import DataPool, Chart
from .forms import EntryForm
from .models import Sensor, Entry
import logging
logger = logging.getLogger(__name__)


def get_data():
    """
    Get entries data from Raspberry PI
    """
    pass


def map_view(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}
    # return render(request, 'polls/index.html', context)
    """
    Main page - map of all the sensors
    """
    pass


# @login_required
def time_chart_view(request):
    """
    User logged to sensor can see its data represented by charts
    """
    # TODO: to jest to co ma wykrywac czy dana kategoria danych ma byc wyswietlana
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            display_type = request.POST["display_type"]

    # Step 1: Create a DataPool with the data we want to retrieve.
    weatherdata = \
        DataPool(
            series=
            [{'options': {
                'source': Entry.objects.all()}, # TODO: tu jakos filtrowac po czujniku, dacie, tym co chcemy wyswietlac
                                                # (np sama temperatura)
                'terms': [
                    'date',
                    'temperature',
                    'humidity',
                    'pollution']}
            ])

    # Step 2: Create the Chart object
    time_chart = Chart(
        datasource=weatherdata,
        series_options=
        [{'options': {
            'type': 'line',
            'stacking': False},
            'terms': {
                'date': [
                    'temperature',
                    'humidity',
                    'pollution']
            }}],
        chart_options=
        {'title': {
            'text': 'Weather Data'},
            'xAxis': {
                'title': {
                    'text': 'Month number'}}})

    # Step 3: Send the chart object to the template.
    return render_to_response({'time_chart': time_chart})


# @login_required
def correlation_chart_view(request):

    """
    User logged to sensor can see its data represented by charts
    """
    # Step 1: Create a DataPool with the data we want to retrieve.
    weatherdata = \
        DataPool(
            series=
            [{'options': {
                'source': Entry.objects.all()}, # TODO: tu jakos filtrowac po dacie, tym co chcemy wyswietlac (np sama
                                                # temperatura) -> przyjmowac request...
                'terms': [
                    'date',
                    'temperature',
                    'humidity',
                    'pollution']}
            ])

    # Step 2: Create the Chart object
    corelation_chart = Chart(
        datasource=weatherdata,
        series_options=
        [{'options': {
            'type': 'line',
            'stacking': False},
            'terms': {
                'date': [
                    'temperature',
                    'humidity',
                    'pollution']
            }}],
        chart_options=
        {'title': {
            'text': 'Weather Data'},
            'xAxis': {
                'title': {
                    'text': 'Month number'}}})

    # Step 3: Send the chart object to the template.
    return render_to_response({'corelation_chart': corelation_chart})


class LoginView(SuccessMessageMixin, FormView):
    """
    Only logged users can see some of the functionalities.
    """
    template_name = 'login.html'
    form_class = AuthenticationForm

    def get_success_url(self):
        return reverse('config')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "Fill all the fields in form with correct data!")
        return super(LoginView, self).form_invalid(form)

login_view = LoginView.as_view()


class LogoutView(TemplateView):
    """
    Just a simple logout view.
    """
    template_name = 'logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return self.render_to_response(self.get_context_data())

logout_view = LogoutView.as_view()
