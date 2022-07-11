
from django.urls import path

from . import views

urlpatterns = [
    path('tile/<uid>/<z>/<x>/<y>', views.GetTileView.as_view())
]
