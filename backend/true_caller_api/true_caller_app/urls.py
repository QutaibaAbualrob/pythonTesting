from django.urls import path
from .views import RegisterView, LoginView, SearchView, SpamReportView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # Note: number is passed as a string to handle various formats, though our model cleans it
    path('search/<str:number>/', SearchView.as_view(), name='search'),
    path('spam/', SpamReportView.as_view(), name='spam-report'),
]
