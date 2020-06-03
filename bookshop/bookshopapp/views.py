from django.shortcuts import render, redirect
from .models import Artikl, Recenzija, Autor, Zanr
from .forms import ArtiklCreate, RecenzijaCreate, SignUpForm, ProfileForm, ArtiklSearchForm
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.template import loader, Context
from django.forms.models import model_to_dict
from django.db.models import Sum
from django.core.mail import send_mail

# Create your views here.

def is_valid_query_param(param):
    return param != '' and param is not None
 
    
def index(request):
    shelf = Artikl.objects.all()
    zanrovi = Zanr.objects.all()
    if 'kosarica' not in request.session:
        request.session['kosarica']=[]

    kosarica = request.session['kosarica']
    SumCijena = sum(artikl['cijena'] for artikl in kosarica)
    CountArtikl = len(kosarica)

    pretraga = request.GET.get('pretraga')
    cijena_min = request.GET.get('cijena_min')
    cijena_max = request.GET.get('cijena_max')
    zanr = request.GET.get('zanr')

    if is_valid_query_param(pretraga):
        shelf=shelf.filter(naziv__icontains=pretraga)

    if is_valid_query_param(cijena_min):
        shelf=shelf.filter(cijena__gte=cijena_min)

    if is_valid_query_param(cijena_max):
        shelf=shelf.filter(cijena__lte=cijena_max)

    if is_valid_query_param(zanr) and zanr != 'zanr...':
       shelf=shelf.filter(zanr__naziv=zanr)

    context = {
        'shelf': shelf, 
        'zanrovi': zanrovi,
        'SumCijena': SumCijena,
        'CountArtikl': CountArtikl,
        'kosarica': kosarica,
    }
    return render(request, 'bookshop/bookshop.html', context)


def kosaricaView(request):
    if 'kosarica' not in request.session:
        request.session['kosarica']=[]
    kosarica = request.session['kosarica']
    SumCijena = sum(artikl['cijena'] for artikl in kosarica)
    CountArtikl = len(kosarica)
    
    context = {
        'kosarica': kosarica,
        'SumCijena': SumCijena,
        'CountArtikl': CountArtikl,
    }
    return render(request, 'bookshop/checkout.html', context)

def ZavrsetakKupnje(request):
    request.session['kosarica'] = []
    kosarica = request.session['kosarica']
    SumCijena = sum(artikl['cijena'] for artikl in kosarica)
    CountArtikl = len(kosarica)

    userEmail = request.POST.get('eracunEmail')
    eracun = request.POST.get('eracun')
    
    if eracun == 'yes':
        send_mail(
            'Bookshop E-racun',
            'test message.',
            'kvarner600@gmail.com',
            [userEmail],
            fail_silently=False,
        ) 

    context = {
        'kosarica': kosarica,
        'SumCijena': SumCijena,
        'CountArtikl': CountArtikl,
        'eracun': eracun,
    }
    return render(request, 'bookshop/checkout_end.html', context)

def KosaricaDodaj(request, pk):
    if 'kosarica' not in request.session:
        request.session['kosarica']=[]
    kosarica = request.session['kosarica']
    kosarica_artikl=Artikl.objects.get(id=pk)
    artikl = {'pk':kosarica_artikl.pk, 'naziv': kosarica_artikl.naziv, 'cijena':kosarica_artikl.cijena}

    kosarica.append(artikl)
    request.session['kosarica']=kosarica

    return redirect(request.META['HTTP_REFERER'])

def KosaricaIzbrisi(request, pk):
    kosarica = request.session['kosarica']
    kosarica_artikl=Artikl.objects.get(id=pk)
    artikl = {'pk': kosarica_artikl.pk, 'naziv': kosarica_artikl.naziv, 'cijena':kosarica_artikl.cijena}

    kosarica.remove(artikl)
    request.session.modified = True
    request.session['kosarica']=kosarica

    return redirect(request.META['HTTP_REFERER'])

def KosaricaIsprazni(request):

    request.session['kosarica'] =[]
    request.session.modified = True

    return redirect(request.META['HTTP_REFERER'])

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

def UserDetailView(request):
    user = request.user
    return render(request, 'accounts/my_profile.html', {'user': user})

def EmailUpdate(request, user_id):
    user_id = int(user_id)
    try:
        user_sel = User.objects.get(id = user_id)
    except User.DoesNotExist:
        return redirect('my-profile')
    user_form = ProfileForm(request.POST or None, instance = user_sel)
    if user_form.is_valid():
       user_form.save()
       return redirect('my-profile')
    return render(request, 'accounts/email_update.html', {'user_form':user_form})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('my-profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })

def ArtiklDetailView(request, pk):
    user = request.user
    recenzije = Recenzija.objects.all()
    kosarica = request.session['kosarica']
    SumCijena = sum(artikl['cijena'] for artikl in kosarica)
    CountArtikl = len(kosarica)
    try:
        artikl = Artikl.objects.get(pk=pk)
    except Artikl.DoesNotExist:
        raise Http404('Artikl does not exist')
    new_recenzija = RecenzijaCreate(initial={'artikl': artikl.pk, 'user': user.pk})
    context = {
        'SumCijena': SumCijena,
        'CountArtikl': CountArtikl,
        'kosarica': kosarica,
        'artikl': artikl, 'recenzije': recenzije, 'new_recenzija': new_recenzija,
    }
    if request.method == 'POST':
        new_recenzija = RecenzijaCreate(request.POST, request.FILES)
        if new_recenzija.is_valid():
            new_recenzija.save()
            #return redirect('artikl_detail')
            return redirect(request, 'bookshop/artikl_detail.html', context={'artikl': artikl, 'recenzije': recenzije, 'new_recenzija': new_recenzija})
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        return render(request, 'bookshop/artikl_detail.html', context)

class RecenzijaListView(ListView):
    model = Recenzija
    template_name = "accounts/recenzija_list.html"
    paginate_by = 50  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def get_queryset(self):
        return Recenzija.objects.filter(user=self.request.user)

def RecenzijaUpdate(request, recenzija_id):
    recenzija_id = int(recenzija_id)
    try:
        recenzija_sel = Recenzija.objects.get(id = recenzija_id)
    except Recenzija.DoesNotExist:
        return redirect('recenzija-list')
    recenzija_form = RecenzijaCreate(request.POST or None, instance = recenzija_sel)
    if recenzija_form.is_valid():
       recenzija_form.save()
       return redirect('recenzija-list')
    return render(request, 'bookshop/recenzija_upload_form.html', {'upload_form':recenzija_form})

def RecenzijaDelete(request, recenzija_id):
    recenzija_id = int(recenzija_id)
    try:
        recenzija_sel = Recenzija.objects.get(id = recenzija_id)
    except Recenzija.DoesNotExist:
        return redirect('recenzija-list')
    recenzija_sel.delete()
    return redirect('recenzija-list')

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
    return render(request, 'bookshop/upload_form.html', {'upload_form':update_artikl})

def delete_artikl(request, artikl_id):
    artikl_id = int(artikl_id)
    try:
        artikl_sel = Artikl.objects.get(id = artikl_id)
    except Artikl.DoesNotExist:
        return redirect('index')
    artikl_sel.delete()
    return redirect('index')