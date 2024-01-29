from django.urls import path
from . import views

urlpatterns = [
    path('', views.timeline),
    path('timeline/', views.timeline, name='timeline'),
    path('timeline/<int:page>', views.timeline, name='timeline'),
    path('timeline/share/', views.share_timeline, name='share_timeline'),
    path('timeline/share/<int:share_id>/', views.share_timeline, name='share_timeline'),
    path('timeline/share/<int:share_id>/<int:page>', views.share_timeline, name='share_timeline'),
    
    path('good/<int:good_id>/', views.good, name='good'),
    path('good/<int:good_id>/<before>', views.good),
    path('good/<int:good_id>/<before>/<user_id>', views.good),

    path('global_TL/', views.global_TL, name='global_TL'),
    path('global_TL/<int:page>', views.global_TL, name='global_TL'),
    path('global_TL/share/', views.share_global_TL, name='share_global_TL'),
    path('global_TL/share/<int:share_id>/', views.share_global_TL, name='share_global_TL'),
    path('global_TL/share/<int:share_id>/<int:page>', views.share_global_TL, name='share_global_TL'),

    path('profile/', views.profile, name='profile'),
    path('profile/<int:target_id>/', views.profile),
    path('profile/<int:target_id>/<int:page>', views.profile),

    path('following/', views.following, name='following'),
    path('following/<int:target_id>', views.following, name='following'),

    path('followed/', views.following, name='followed'),
    path('followed/<int:target_id>', views.followed, name='followed'),

    path('update_profile/', views.update_profile, name='update_profile'),
    path('update_profile/<int:target_id>/', views.update_profile),
    path('update_profile/<int:target_id>/<int:page>', views.update_profile),

    path('create_following/', views.create_following, name='create_following'),
    path('create_following/<int:target_id>', views.create_following),
    path('delete_following/', views.delete_following, name='delete_following'),
    path('delete_following/<int:target_id>', views.delete_following),

    path('delete_message/', views.delete_message, name='delete_message'),
    path('delete_message/<int:message_id>/<before>', views.delete_message),
    path('delete_message/<int:message_id>/<before>/<user_id>', views.delete_message),
]