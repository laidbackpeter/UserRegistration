from django.conf.urls import url
from views import RegisterFarmer, RegisterSeedBag

urlpatterns = [
    url(r'register/farmer/?',
        RegisterFarmer.as_view(),
        name='register-farmer'),

    url(r'register/seed-bag/?$',
        RegisterSeedBag.as_view(),
        name='register-seed-bag'),

]
