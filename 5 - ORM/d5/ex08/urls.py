from django.urls import path
from .views import populate, init, display

urlpatterns = [
    path('init', init, name='init'),
    path('populate', populate, name='populate'),
    path('display', display, name='display'),
    # path('remove', remove, name='remove'),
    # path('update', update, name='update'),
]