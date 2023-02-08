from django.urls import path, re_path
from . import views
from .api import App_api
from .webhook import WebhookApi

urlpatterns = [
    # '''views.py'''                                                Whitelisted urls
    path('', views.login, name='index'),                        # https://python.penveel.com
    path('installation', views.installation),
    path('final', views.final),                                 # https://python.penveel.com/final
    path('about', views.about),                                 # https://python.penveel.com/about
    path('privacy_policy', views.policy),                       # https://python.penveel.com/privacy_policy
    path('instruct', views.instruct),                           # https://python.penveel.com/instruct
    path('price', views.pricing),                               # https://python.penveel.com/price
    path('contact', views.contact),                             # https://python.penveel.com/contact
    path('contact_data', views.contact_detail),                 # https://python.penveel.com/contact_data
    path('home', views.home_page),                              # https://python.penveel.com/home
    path('order', views.order_page),                            # https://python.penveel.com/order
    path('return_approved', views.returnapprove),               # https://python.penveel.com/return_approved
    path('return_reject', views.rejected),                      # https://python.penveel.com/return_reject

    # '''api.py'''
    path('oid', App_api.get_order_detail),                      # https://python.penveel.com/oid
    path('c_order', App_api.get_customer),                      # https://python.penveel.com/c_order
    
    # '''webhook.py'''
    path('uninstall', WebhookApi.webhook_uninstall),            # https://python.penveel.com/uninstall
]