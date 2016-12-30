import datetime
import logging

import googlemaps
from chartit import DataPool, Chart
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render
from django.views.generic import FormView, TemplateView
from folium import folium

from tasks import get_data_from_rpi
from .forms import ChooseAxisForm, ChooseCorrelationForm
from .models import Sensor, Entry

logger = logging.getLogger(__name__)
get_data_from_rpi()


def map_view(request):
    """
    Main page - map of all the sensors
    """
    gmaps = googlemaps.Client(key='AIzaSyCZO9lx7k1gFhU-Fv9hSZ9PUynZb0EjeBg')
    sensors = Sensor.objects.all()
    sensor_map = folium.Map(location=[50.064316, 19.985638], zoom_start=12, tiles='Stamen Terrain')
    for sensor in sensors:
        localisation = sensor.localisation
        sensor_id = sensor.sensor_id
        coordinates = (gmaps.geocode(localisation))[0]['geometry']['location']
        popup = '%s; sensor_id = %i' % (localisation, sensor_id)
        folium.Marker([coordinates['lat'], coordinates['lng']], popup=popup).add_to(sensor_map)
    sensor_map.save('templates/map.html')
    return render_to_response('sensors_map.html')


@login_required(login_url='/login/')
def time_chart_view(request):
    """
    User logged to sensor can see its data represented by charts
    """
    source = Entry.objects.all()
    if request.method == "POST":
        terms = ['date']
        form = ChooseAxisForm(request.POST)
        if form.is_valid():
            # get data from checkboxes
            axis = request.POST.get("axis-checkbox", None)
            if axis in ["temperature"]:
                terms.append('temperature')
            if axis in ["humidity"]:
                terms.append('humidity')
            if axis in ["pm25"]:
                terms.append('pm25')
            if axis in ["pm10"]:
                terms.append('pm10')
            if axis in ["pressure"]:
                terms.append('pressure')
            if axis in ["wind_speed"]:
                terms.append('wind_speed')

            # get data from dropdown
            time = form.data['time']
            if time == 'all':
                source = Entry.objects.filter(user=request.user)
            if time == 'week':
                start_date = datetime.date.today() - datetime.timedelta(days=6)
                end_date = datetime.date.today()
                source = Entry.objects.filter(user=request.user, date__range=[start_date, end_date])
            if time == 'day':
                source = Entry.objects.filter(user=request.user, date=datetime.date.today())
        else:
            terms = ['date', 'temperature', 'humidity', 'pm25', 'pm10', 'pressure', 'wind_speed']
    else:
        form = ChooseAxisForm()
        terms = ['date', 'temperature', 'humidity', 'pm25', 'pm10', 'pressure', 'wind_speed']

    weather_data = DataPool(series=[{'options': {'source': source}, 'terms': terms}])
    time_chart = Chart(datasource=weather_data, series_options=[{'options': {
        'type': 'line',
        'stacking': False},
        'terms': {'date': terms[1:]}}],  # everything but date
                       chart_options={'title': {'text': 'Weather Data'},
                                      'xAxis': {'title': {'text': 'Date'}}})
    return render(request, 'time_chart.html', {'time_chart': time_chart, 'form': form})


@login_required(login_url='/login/')
def correlation_chart_view(request):
    """
    User logged to sensor can see its data represented by charts
    """
    terms = []
    if request.method == 'POST':
        form = ChooseCorrelationForm(request.POST)
        if form.is_valid():
            # get data from dropdown
            axis_x = form.data['axis-x']
            terms.append(axis_x)

            # get data from checkboxes
            axis = request.POST.get("axis-checkbox", None)
            if axis in ["temperature"]:
                terms.append('temperature')
            if axis in ["humidity"]:
                terms.append('humidity')
            if axis in ["pm25"]:
                terms.append('pm25')
            if axis in ["pm10"]:
                terms.append('pm10')
            if axis in ["pressure"]:
                terms.append('pressure')
            if axis in ["wind_speed"]:
                terms.append('wind_speed')
        else:
            terms = ['temperature', 'pm25', 'pm10']
    else:
        form = ChooseCorrelationForm()
        terms = ['temperature', 'pm25', 'pm10']  # some default values

    weather_data = DataPool(series=[{'options': {'source': Entry.objects.all()}, 'terms': terms}])
    correlation_chart = Chart(datasource=weather_data, series_options=[{'options': {
        'type': 'line',
        'stacking': False},
        'terms': {terms[0]: terms[1:]}}],  # category for axis x and multiple values for axis y
                              chart_options={'title': {'text': 'Weather Data'}})
    return render(request, 'correlation_chart.html', {'correlation_chart': correlation_chart, 'form': form})


class LoginView(SuccessMessageMixin, FormView):
    """
    Only logged users can see some of the functionalities.
    """
    template_name = 'login.html'
    form_class = AuthenticationForm

    def get_success_url(self):
        return reverse('index')

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
