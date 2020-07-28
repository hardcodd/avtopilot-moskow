from django.urls import path

from builder.views import case_initial, mate_initial, case, mate

urlpatterns = [
    path('case/', case, name='case_builder'),
    path('mate/', mate, name='mate_builder'),
    path('case-initial/', case_initial),
    path('mate-initial/', mate_initial),
]
