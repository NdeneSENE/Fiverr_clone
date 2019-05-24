from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('gigs/<int:gig_id>', views.gig_detail, name='gig_detail'),
    path('profil/<username>/', views.profil, name='profil'),
    path('create_gig', views.create_gig, name='create_gig'),
    path('edit_gig/<int:gig_id>', views.edit_gig, name='edit_gig'),
    path('my_gig', views.my_gig, name='my_gig'),
    path('mes_ventes', views.mes_ventes, name='mes_ventes'),
    path('category/<link>', views.category, name='category'),
    path('mes_achats', views.mes_achats, name='mes_achats'),
    path('search', views.search, name='search'),
    path('create_purchase', views.create_purchase, name="create_purchase")
]