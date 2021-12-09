from django.urls import path

from recomendation_app import views

app_name='recoms'
urlpatterns = [
    path('import_all_data/', views.import_properties),
    path('add_user_to_recommend/', views.add_user),
    path('add_property_to_recommend/', views.add_property),
    path('property_view_interaction/', views.property_view_interaction),
    path('get_recommendations/', views.get_recommendations),
    path('test/', views.test),
    path('test2/', views.test2),

]
