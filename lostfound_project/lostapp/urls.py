"""
URL configuration for lostfound_project project.
"""

from django.urls import path
from . import views

urlpatterns = [

    # HOME

    path(
        '',
        views.index,
        name='index'
    ),

    # AUTH

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        views.login_user,
        name='login'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'logout/',
        views.logout_user,
        name='logout'
    ),

    # LOST ITEMS

    path(
        'report-lost/',
        views.report_lost,
        name='report_lost'
    ),

    path(
        'lost-items/',
        views.lost_items,
        name='lost_items'
    ),

    path(
        'lost-item/<int:id>/',
        views.lost_item_detail,
        name='lost_item_detail'
    ),

    path(
        'edit-lost/<int:id>/',
        views.edit_lost_item,
        name='edit_lost_item'
    ),

    path(
        'delete-lost/<int:id>/',
        views.delete_lost_item,
        name='delete_lost_item'
    ),

    # FOUND ITEMS

    path(
        'report-found/',
        views.report_found,
        name='report_found'
    ),

    path(
        'found-items/',
        views.found_items,
        name='found_items'
    ),

    path(
        'found-item/<int:id>/',
        views.found_item_detail,
        name='found_item_detail'
    ),

    path(
        'edit-found/<int:id>/',
        views.edit_found_item,
        name='edit_found_item'
    ),

    path(
        'delete-found/<int:id>/',
        views.delete_found_item,
        name='delete_found_item'
    ),

    # ALL ITEMS

    path(
        'all-items/',
        views.all_items,
        name='all_items'
    ),

    # CLAIM ITEM

    path(
        'claim-item/<str:item_name>/',
        views.claim_item,
        name='claim_item'
    ),

    # PROFILE

    path(
        'profile/',
        views.profile,
        name='profile'
    ),

    # CHAT SYSTEM

    path(
        'chat/<int:user_id>/',
        views.chat_room,
        name='chat_room'
    ),
    path(
    'delete-chat/<int:room_id>/',
    views.delete_chat,
    name='delete_chat'
    ),

    

    path(
    'accept-claim/<int:id>/',
    views.accept_claim,
    name='accept_claim'
    ),

    path(
    'reject-claim/<int:id>/',
    views.reject_claim,
    name='reject_claim'
    ),

    path(
    'delete-claim/<int:id>/',
    views.delete_claim,
    name='delete_claim'
),


path(
    'about/',
    views.about,
    name='about'
),

    
]