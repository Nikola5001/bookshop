from django.shortcuts import render, redirect
from .models import Artikl, Recenzija, Autor, Zanr
from .forms import ArtiklCreate, RecenzijaCreate, SignUpForm
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm


# Create your views here.


#def index(request):
#    shelf = Artikl.objects.all()
#    return render(request, 'musicshop/musicshop.html', {'shelf': shelf})

def index(request):
    shelf = Artikl.objects.all()
    return render(request, 'bookshop/bookshop.html', {'shelf': shelf})

def loginView(request):
    return render(request, 'registraion/login.html')

def signupView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def logout(request):
    return render(request, 'registraion/logout.html')

def ArtiklDetailView(request, pk):
    user = request.user
    recenzije = Recenzija.objects.all()
    try:
        artikl = Artikl.objects.get(pk=pk)
    except Artikl.DoesNotExist:
        raise Http404('Artikl does not exist')
    new_recenzija = RecenzijaCreate(initial={'artikl': artikl.pk, 'user': user.pk})
    if request.method == 'POST':
        new_recenzija = RecenzijaCreate(request.POST, request.FILES)
        if new_recenzija.is_valid():
            new_recenzija.save()
            #return redirect('artikl_detail')
            return redirect(request, 'musicshop/artikl_detail.html', context={'artikl': artikl, 'recenzije': recenzije, 'new_recenzija': new_recenzija})
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        return render(request, 'musicshop/artikl_detail.html', context={'artikl': artikl, 'recenzije': recenzije, 'new_recenzija': new_recenzija})

class RecenzijaListView(ListView):
    model = Recenzija
    template_name = "musicshop/recenzija_list.html"
    paginate_by = 50  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def get_queryset(self):
        return Recenzija.objects.filter(user=self.request.user)


class ArtiklListView(generic.ListView):
    model = Artikl
    paginate_by = 25  # if pagination is desired

def update_artikl(request, artikl_id):
    artikl_id = int(artikl_id)
    try:
        Artikl_sel = Artikl.objects.get(id = artikl_id)
    except Artikl.DoesNotExist:
        return redirect('index')
    Artikl_form = ArtiklCreate(request.POST or None, instance = Artikl_sel)
    if Artikl_form.is_valid():
       Artikl_form.save()
       return redirect('index')
    return render(request, 'musicshopapp/upload_form.html', {'upload_form':update_artikl})

def delete_artikl(request, artikl_id):
    artikl_id = int(artikl_id)
    try:
        artikl_sel = Artikl.objects.get(id = artikl_id)
    except Artikl.DoesNotExist:
        return redirect('index')
    artikl_sel.delete()
    return redirect('index')