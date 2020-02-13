from django.shortcuts import render
from django.views.generic import ListView,CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Country,State,Person
from .forms import PersonForm

# Create your views here.



class PersonListView(ListView):
    model = Person
    context_object_name = 'people'

class PersonCreateView(CreateView):
    model = Person
    form_class = PersonForm
    success_url = reverse_lazy('person_changelist')

class PersonUpdateView(UpdateView):
	model = Person
	form_class = PersonForm
	success_url = reverse_lazy('person_changelist')


def load_cities(request):
    country_id = request.GET.get('country')
    cities = State.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'country/city_dropdown_list_options.html', {'cities': cities})
