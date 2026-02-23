from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views


app_name = 'absent'
router = DefaultRouter(trailing_slash=False)
# http://127.0.0.1:8000/absent/absent
router.register('absent',views.AbsentViewSet,basename='absent')


urlpatterns = [
    # http://127.0.0.1:8000/absent/type
    path('type',views.AbsentTypeView.as_view(),name='type'),
    path('responder',views.ResponderView.as_view(),name='getresponder')
] + router.urls