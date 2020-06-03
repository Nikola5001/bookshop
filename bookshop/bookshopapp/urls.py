from django.urls import path, include
from . import views
from bookshop.settings import DEBUG, STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT
from bookshopapp.views import ArtiklListView, ArtiklDetailView, signupView, RecenzijaListView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name = 'index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('artikl/<int:pk>/', ArtiklDetailView, name='artikl-detail'),
    path('registration/signup', signupView, name='signup'),
    path('moje_recenzije', RecenzijaListView.as_view(), name='recenzija-list'),
    path('update_recenzija/<int:recenzija_id>', views.RecenzijaUpdate),
    path('delete_recenzija/<int:recenzija_id>', views.RecenzijaDelete),
    path('My_profile/', views.UserDetailView, name='my-profile'),
    path('update_email/<int:user_id>', views.EmailUpdate, name='update-email'),
    path(r'^password/$', views.change_password, name='change-password'),
    path('checkout/', views.kosaricaView, name='checkout-view'),
    path('checkout/add/<int:pk>', views.KosaricaDodaj, name='checkout-add'),
    path('checkout/delete/<int:pk>', views.KosaricaIzbrisi, name='checkout-delete'),
    path('checkout/empty', views.KosaricaIsprazni, name='checkout-empty'),
    path('checkout/success', views.ZavrsetakKupnje, name='checkout-success'),
]
#DataFlair
if DEBUG:
    urlpatterns += static(STATIC_URL, document_root = STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root = MEDIA_ROOT)