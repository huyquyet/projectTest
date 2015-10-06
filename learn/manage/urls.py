from django.conf.urls import url
from learn.manage import views

__author__ = 'FRAMGIA\nguyen.huy.quyet'
urlpatterns = [
    # Account
    url(r'^$', views.index_manage, name='index_admin'),
    url(r'^profile/$', views.ProfileUserView.as_view(), name='index_profile'),
    url(r'^profile/manage/$', views.ProfileManageView.as_view(), name='profile_manage'),
    url(r'^profile/user/$', views.ProfileUserView.as_view(), name='profile_user'),
    url(r'^detail_profile/(?P<pk>[0-9]+)/$', views.DetailProfileView.as_view(), name='detail_profile'),
    url(r'^edit_profile/(?P<pk>[0-9]+)/$', views.EditProfileView.as_view(), name='edit_profile'),
    url(r'^delete_user/(?P<pk>[0-9]+)/$', views.DeleteUserView.as_view(), name='delete_user'),
    url(r'^set_password/(?P<pk>[0-9]+)/$', views.SetPasswordUserView.as_view(), name='set_pass'),

    # Course
    url(r'^course/create_new/$', views.CreateCourseView.as_view(), name='create_course'),
    url(r'^course/$', views.ListCourseView.as_view(), name='list_course'),
    url(r'^course/detail/(?P<pk>[0-9]+)/$', views.DetailCourseView.as_view(), name='detail_course'),
    url(r'^course/edit/(?P<pk>[0-9]+)/$', views.EditCourseView.as_view(), name='edit_course'),
    url(r'^course/delete/(?P<pk>[0-9]+)/$', views.DeleteCourseView.as_view(), name='delete_course'),
    url(r'^course/re_user/$', views.delete_user_course, name='remover_user_course'),
    url(r'^course/add_user/$', views.add_user_course, name='add_user_course'),
    url(r'^course/(?P<pk>[0-9]+)/add_user/$', views.AddUserCourseView.as_view(), name='add_user_course_view'),

    # Subject
    url(r'^subject/create_new/$', views.CreateSubjectView.as_view(), name='create_subject'),
    url(r'^subject/$', views.ListSubjectView.as_view(), name='list_subject'),
    url(r'^subject/detail/(?P<pk>[0-9]+)/$', views.DetailSubjectView.as_view(), name='detail_subject'),
    url(r'^subject/edit/(?P<pk>[0-9]+)/$', views.EditSubjectView.as_view(), name='edit_subject'),
    url(r'^subject/delete/$', views.delete_subject, name='delete_subject'),
    url(r'^course/add_user/$', views.add_user_course, name='add_user_course'),
    url(r'^subject/(?P<pk>[0-9]+)/add_user/$', views.AddUserSubjectView.as_view(), name='add_user_sub_view'),
    url(r'^subject/add_user/$', views.add_user_subject, name='add_user_subject'),
    url(r'^subject/re_user/$', views.delete_user_subject, name='remover_user_sub'),

    # Task
    url(r'^task/$', views.ListTaskView.as_view(), name='list_task'),
    url(r'^task/create_task/$', views.CreateTaskView.as_view(), name='create_task'),
    url(r'^task/detail_task/(?P<pk>[0-9]+)/$', views.DetailTaskView.as_view(), name='detail_task'),
    url(r'^task/edit_task/(?P<pk>[0-9]+)/$', views.EditTaskView.as_view(), name='edit_task'),
    url(r'^task/delete_task/$', views.delete_task, name='delete_task'),
    url(r'^task/re_user/$', views.delete_user_task, name='remover_user_task'),
    url(r'^task/(?P<pk>[0-9]+)/add_user/$', views.AddUserTaskView.as_view(), name='add_user_task_view'),
    url(r'^task/add_user/$', views.add_user_task, name='add_user_task'),
]
