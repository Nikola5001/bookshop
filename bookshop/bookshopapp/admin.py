from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Zanr
from .models import Artikl
from .models import Recenzija
from .models import Autor

class ArtiklAdmin(admin.ModelAdmin):
    model = Artikl
    list_display = ('naziv',)
    
class ArtiklZanr(admin.ModelAdmin):
    model = Zanr
    list_display = ('naziv',)

class ArtiklAutor(admin.ModelAdmin):
    model = Autor
    list_display = ['ime','prezime',]

class ArtiklRecenzija(admin.ModelAdmin):
    model = Recenzija
    list_display = ['get_artikl','get_clan_ime',]

    def get_artikl(self, obj):
        return obj.artikl.naziv
    get_artikl.short_description = 'Artikl'
    get_artikl.admin_order_field = 'Recenzija__Artikl'

    def get_clan_ime(self, obj):
        return obj.user.username
    get_clan_ime.short_description = 'Korisnik'
    get_clan_ime.admin_order_field = 'Recenzija__Korisnik'

# Register your models here.
admin.site.register(Zanr, ArtiklZanr)
admin.site.register(Artikl, ArtiklAdmin)
admin.site.register(Recenzija, ArtiklRecenzija)
admin.site.register(Autor, ArtiklAutor)

