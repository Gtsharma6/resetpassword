from django.shortcuts import render,redirect
from django.views.generic import ListView,CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Country,State,Person,Document

from .forms import PersonForm,DocumentForm
from django.core.files.storage import FileSystemStorage

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



def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'country/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'country/simple_upload.html')





def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'country/model_form_upload.html', {
        'form': form
    })