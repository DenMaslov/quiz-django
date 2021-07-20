from django.urls import path
from .views import (TestListView,
                    TestDetailView,
                    TestSessionView,
                    TestSessionHistoryView,
                    TestScoreView,
                    )


urlpatterns = [
    
    path('', TestListView.as_view(), name='tests_list'),
    path('myscores/', TestScoreView.as_view(), name='myscores'),
    path('<int:pk>/', TestDetailView.as_view(), name='post_detail'),
    path('start/<int:pk>/', TestSessionView.as_view(), name='start'),
    path('history/<int:pk>/', TestSessionHistoryView.as_view(), name='history'),
    
]
