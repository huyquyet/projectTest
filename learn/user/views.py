# -*- coding: utf-8 -*-
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, UpdateView

from learn.models import Course, Subject, UserCourse, UserSubject, Task, UserTask

__author__ = 'FRAMGIA\nguyen.huy.quyet'


# User
class UserDetailProfile(DetailView):
    model = User
    context_object_name = 'detail_profile'
    template_name = 'user/account/u_detail_profile.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserDetailProfile, self).dispatch(request, *args, **kwargs)


class UserEditProfileView(UpdateView):
    model = User
    template_name = 'user/account/u_edit_profile.html'
    fields = ['first_name', 'last_name', 'email']
    context_object_name = 'user_obj'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != request.user:
            raise PermissionDenied
        return super(UserEditProfileView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('learn:index')


# Course
class UserListCourseView(ListView):
    model = Course
    template_name = 'user/course/u_index_course.html'
    # context_object_name = 'list_course'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserListCourseView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        search = self.request.GET.get('search', '')
        ctx = super(UserListCourseView, self).get_context_data(**kwargs)
        if search == '':
            ctx['list_course'] = self.model.objects.all()
        else:
            ctx['list_course'] = self.model.objects.filter(name__contains=search)
        return ctx


class UserDetailCourseView(DetailView):
    def get(self, request, *args, **kwargs):
        view = UserDetailCourseView_1.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get('hidden_join') == 'True':
            return user_unjoin_course(request, *args, **kwargs)
        else:
            return user_join_course(request, *args, **kwargs)


class UserDetailCourseView_1(DetailView):
    model = Course
    template_name = 'user/course/u_detail_course.html'
    context_object_name = 'detail_course'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserDetailCourseView_1, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserDetailCourseView_1, self).get_context_data(**kwargs)
        context['list_subject'] = self.object.subjects.all()
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        joined = UserCourse.objects.filter(course_id=course, user_id=self.request.user, status=True).exists()
        if joined:
            context['join_course'] = True
        else:
            context['join_course'] = False

        list_user = UserCourse.objects.filter(course_id=course, status=True)
        context['list_user'] = [User.objects.get(pk=i.user_id.pk) for i in list_user]

        list_user_sub = UserSubject.objects.filter(user_id=self.request.user, status=True)
        list_sub_of_my = [Subject.objects.get(pk=i.subject_id.pk) for i in list_user_sub]
        context['list_sub_in_cou'] = set(list_sub_of_my).intersection(context['list_subject'])
        return context


@login_required()
def user_join_course(request, pk):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=pk)
        usercourse, created = UserCourse.objects.get_or_create(course_id=course, user_id=request.user)
        usercourse.status = True
        usercourse.save()
        return HttpResponseRedirect(reverse('learn:u_detail_course', kwargs={'pk': pk}))


@login_required()
def user_unjoin_course(request, pk):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=pk)
        usercourse = UserCourse.objects.get(course_id=course, user_id=request.user)
        usercourse.status = False
        usercourse.save()
        return HttpResponseRedirect(reverse('learn:u_detail_course', kwargs={'pk': pk}))


class UserDetailSubjectView(DetailView):
    def get(self, request, *args, **kwargs):
        view = UserDetailSubjectView_1.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get('hidden_join') == 'True':
            return user_join_subject(request, *args, **kwargs)
        else:
            return user_unjoin_subject(request, *args, **kwargs)


class UserDetailSubjectView_1(DetailView):
    # Views Detail of subject
    model = Subject
    template_name = 'user/subject/u_detail_subject.html'
    context_object_name = 'detail_subject'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserDetailSubjectView_1, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserDetailSubjectView_1, self).get_context_data(**kwargs)
        # return context all course of subject
        # subjects = get_object_or_404(Subject, pk=self.kwargs['pk'])
        context['list_course'] = self.object.courses.all()
        context['join_subject'] = []

        # kiem tra xem subject đã kêt thúc chưa
        if self.object.check_time_end_subject(timezone.now()):
            context['time_end'] = True
        else:
            context['time_end'] = False

        # Tim kiem xem user da join vao subject hay chua
        if self.object.joined_user(self.request.user):
            # Đã tồn tại trong UserSubject
            if self.object.joined_user(self.request.user, True):
                # Status = True đang tham gia khóa học
                context['join_subject'] = False
            else:
                # Status = False đã hủy hoặc kết thúc khóa học
                context['join_subject'] = True
        # if user_subject = False
        # Tìm kiếm xem Subject có nằm trong những Course mà User join hay ko
        else:
            # List những Course mà user join vào
            user_course = UserCourse.objects.filter(user_id=self.request.user, status=True)
            for i in user_course:
                if self.object.courses.filter(pk=i.course_id.pk).exists():
                    # Subject thuộc Course mà User đã đăng ký
                    context['join_subject'] = True
                    break
            else:
                # Subject không thuộc Course mà User đã đăng ký
                context['disable'] = True
                context['join_subject'] = False

        # List User of Subject
        list_user_1 = UserSubject.objects.filter(subject_id=self.object, status=True)
        context['list_user'] = [User.objects.get(pk=i.user_id.pk) for i in list_user_1]

        # List Task of Subject
        context['list_task'] = self.object.task.all()
        return context


def user_join_subject(request, pk):
    if request.method == 'POST':
        subject = get_object_or_404(Subject, pk=pk)
        user_subject, created = UserSubject.objects.get_or_create(subject_id=subject, user_id=request.user)
        user_subject.status = True
        user_subject.save()
    return HttpResponseRedirect(reverse('learn:u_detail_subject', kwargs={'pk': pk}))


def user_unjoin_subject(request, pk):
    if request.method == 'POST':
        subject = get_object_or_404(Subject, pk=pk)
        user_subject = UserSubject.objects.get(subject_id=subject, user_id=request.user)
        user_subject.status = False
        user_subject.save()
    return HttpResponseRedirect(reverse('learn:u_detail_subject', kwargs={'pk': pk}))


class MyCourseView(ListView):
    model = Course
    template_name = 'user/course/u_list_my_course.html'
    context_object_name = 'list_course'

    def get_context_data(self, **kwargs):
        context = super(MyCourseView, self).get_context_data(**kwargs)
        context['course_user'] = UserCourse.objects.filter(user_id=self.request.user, status=True)
        context['list_course_of_user'] = []
        for i in context['course_user']:
            context['list_course_of_user'].append(Course.objects.get(pk=i.course_id.pk))
        return context


# Task


class UserDetailTaskView(DetailView):
    model = Task
    template_name = 'user/task/u_detail_task.html'
    context_object_name = 'u_detail_task'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserDetailTaskView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(UserDetailTaskView, self).get_context_data(**kwargs)
        ctx['subject'] = self.object.subject_id

        # return list subject of user
        user_subject = self.request.user.subjects.all()
        joined = Task.objects.filter(subject_id__in=user_subject, pk=self.object.pk).exists()
        if joined:
            ctx['joined'] = joined
            ctx['joined_user'] = []
            if self.object.joined_user_task(self.request.user):
                # User exists in UserTask
                if self.object.joined_user_task(self.request.user, True):
                    ctx['joined_user'] = 'Finish task'
                else:
                    ctx['joined_user'] = 'Completed'
            else:
                # User DoseNotExists in UserTask
                ctx['joined_user'] = 'Join'
        list_user_of_task = UserTask.objects.filter(task_id=self.object, status=True)
        ctx['list_user_of_task'] = [User.objects.get(pk=i.user_id.pk) for i in list_user_of_task]

        return ctx

    def post(self, request, *args, **kwargs):
        if request.POST.get('hidden_join') == "Finish task":
            return user_finish_task(request, *args, **kwargs)
        elif request.POST.get('hidden_join') == "Join":
            return user_join_task(request, *args, **kwargs)
        elif request.POST.get('hidden_join') == "Completed":
            return user_unjoin_task(request, *args, **kwargs)


def user_finish_task(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        user_task, created = UserTask.objects.get_or_create(task_id=task, user_id=request.user)
        user_task.status = False
        user_task.save()
    return HttpResponseRedirect(reverse_lazy('learn:u_detail_task', kwargs={'pk': pk}))


def user_join_task(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        user_task, created = UserTask.objects.get_or_create(task_id=task, user_id=request.user)
        user_task.status = True
        user_task.save()
    return HttpResponseRedirect(reverse_lazy('learn:u_detail_task', kwargs={'pk': pk}))


def user_unjoin_task(request, pk):
    pass
