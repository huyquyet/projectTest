from django.conf.urls import url

from learn.user import views

__author__ = 'FRAMGIA\nguyen.huy.quyet'
urlpatterns = [
    url(r'^$', views.UserListCourseView.as_view(), name='index_user'),

    # User
    url(r'^detail_profile/(?P<pk>[0-9]+)/$', views.UserDetailProfile.as_view(), name='u_profile'),
    url(r'^edit_profile/(?P<pk>[0-9]+)/$', views.UserEditProfileView.as_view(), name='u_edit'),

    # Course
    url(r'^my_course/$',views.MyCourseView.as_view(), name='my_course'),
    url(r'^course/$', views.UserListCourseView.as_view(), name='u_list_course'),
    url(r'^course/detail/(?P<pk>[0-9]+)/$', views.UserDetailCourseView.as_view(), name='u_detail_course'),

    # Subject
    url(r'^subject/detail/(?P<pk>[0-9]+)/$', views.UserDetailSubjectView.as_view(), name='u_detail_subject'),

    # Task
    url(r'^task/detail/(?P<pk>[0-9]+)/$', views.UserDetailTaskView.as_view(), name='u_detail_task'),

]
