from django.conf.urls import url, include

from learn import views

__author__ = 'FRAMGIA\nguyen.huy.quyet'
urlpatterns = [

    # Account
    url(r'^$', views.index, name='index'),
    url(r'^singin/$', views.singin, name='singin'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^singout/$', views.singout, name='singout'),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.ProfileView.as_view(), name='profile'),
    url(r'^edit_profile/(?P<pk>[0-9]+)/$', views.EditProfileView.as_view(), name='edit'),
    url(r'^change_pass/$', views.changepass, name='change_pass'),

    # Course
    url(r'^course/$', views.changepass, name='change_pass'),

    # Manage
    url(r'^manage/', include('learn.manage.urls')),

    # User
    url(r'^user/', include('learn.user.urls')),

]
