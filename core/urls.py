from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Paths for general pages
    path('', views.home, name='home'),
    path('posts/', views.posts_list, name='posts_list'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('posts/<int:pk>/content/', views.get_post_content_ajax, name='get_post_content_ajax'),
    
    # Paths for events
    path('events/', views.events_list, name='events_list'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/edit/', views.edit_event, name='edit_event'),
    path('events/<int:pk>/delete/', views.delete_event, name='delete_event'),
    
    # Paths for FAQs
    path('faqs/', views.faqs_list, name='faqs_list'),
    path('faqs/create/', views.create_faq, name='create_faq'),
    path('faqs/<int:pk>/edit/', views.edit_faq, name='edit_faq'),
    path('faqs/<int:pk>/delete/', views.delete_faq, name='delete_faq'),
    
    # The new dashboard path
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Authentication paths
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
