from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, View

from learn.forms import CreateSubjectForm, EditCourseForm
from learn.models import Course, Subject, Task, UserTask, UserCourse, UserSubject

__author__ = 'FRAMGIA\nguyen.huy.quyet'


# Account

@user_passes_test(lambda u: u.is_staff, login_url='learn:login')
def index_manage(request):
    print(request.user.is_staff)
    # if request.user.is_staff:
    return render(request, 'manage/index_manage.html', '')
    # else:
    #     return HttpResponseRedirect(reverse('learn:index'))


class ProfileManageView(ListView):
    model = User
    template_name = 'manage/account/profile_user.html'
    # context_object_name = 'list_user_profile'

    @method_decorator(user_passes_test)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileManageView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(is_staff=True)

    def get_context_data(self, **kwargs):
        search = self.request.GET.get('search', '')
        context = super(ProfileManageView, self).get_context_data(**kwargs)
        if search != '':
            context['list_user_profile'] = self.model.objects.filter(is_staff=True, username=search)
        else:
            context['list_user_profile'] = self.model.objects.filter(is_staff=True)
        context['staff'] = True
        return context


class ProfileUserView(ListView):
    model = User
    template_name = 'manage/account/profile_user.html'
    # context_object_name = 'list_user_profile'

    @method_decorator(user_passes_test)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileUserView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(is_staff=False)

    def get_context_data(self, **kwargs):
        search = self.request.GET.get('search', '')
        context = super(ProfileUserView, self).get_context_data(**kwargs)
        if search != '':
            context['list_user_profile'] = self.model.objects.filter(is_staff=False, username=search)
        else:
            context['list_user_profile'] = self.model.objects.filter(is_staff=False)
        context['staff'] = False
        return context


class DetailProfileView(DetailView):
    model = User
    template_name = 'manage/account/detail_profile.html'
    context_object_name = 'profile_user'

    @method_decorator(user_passes_test)
    def dispatch(self, request, *args, **kwargs):
        return super(DetailProfileView, self).dispatch(request, *args, **kwargs)


class EditProfileView(UpdateView):
    model = User
    template_name = 'manage/account/edit_profile.html'
    fields = ['first_name', 'last_name', 'email', 'is_staff']

    @method_decorator(user_passes_test)
    def dispatch(self, request, *args, **kwargs):
        return super(EditProfileView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('learn:index_profile')


class DeleteUserView(DeleteView):
    model = User
    template_name = 'manage/account/delete_user.html'
    context_object_name = 'del_user'
    success_url = reverse_lazy('learn:index_profile')

    @method_decorator(user_passes_test)
    def dispatch(self, request, *args, **kwargs):
        return super(DeleteUserView, self).dispatch(request, *args, **kwargs)


class SetPasswordUserView(View):
    pass


# End Account

# Course

class CreateCourseView(CreateView):
    model = Course
    # fields = ['name', 'description', 'begin_at', 'end_at']
    form_class = EditCourseForm
    template_name = 'manage/course/create_course.html'

    @method_decorator(user_passes_test)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateCourseView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('learn:list_course')

    def form_valid(self, form):
        form.save()
        return super(CreateCourseView, self).form_valid(form)


class ListCourseView(ListView):
    model = Course
    template_name = 'manage/course/index_course.html'
    context_object_name = 'list_course'


class DetailCourseView(DetailView):
    model = Course
    template_name = 'manage/course/detail_course.html'
    context_object_name = 'detail_course'

    @method_decorator(user_passes_test)
    def dispatch(self, request, *args, **kwargs):
        return super(DetailCourseView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(DetailCourseView, self).get_context_data(**kwargs)
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        ctx['list_subject'] = self.object.subjects.all()

        list_user = UserCourse.objects.filter(course_id=course, status=True)
        ctx['list_user_of_cou'] = [User.objects.get(pk=i.user_id.pk) for i in list_user]
        return ctx


class EditCourseView(UpdateView):
    model = Course
    template_name = 'manage/course/edit_course.html'
    # fields = ['name', 'description', 'begin_at', 'end_at']
    form_class = EditCourseForm
    context_object_name = 'course'

    @method_decorator(user_passes_test)
    def dispatch(self, request, *args, **kwargs):
        return super(EditCourseView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('learn:list_course')

    def form_valid(self, form):
        form.save()
        return super(EditCourseView, self).form_valid(form)

        # def get_context_data(self, **kwargs):
        #     context = super(EditCourseView, self).get_context_data(**kwargs)
        #     context['data'] = Course
        #     return context


class DeleteCourseView(DeleteView):
    model = Course
    template_name = 'manage/course/delete_course.html'
    context_object_name = 'del_course'
    success_url = reverse_lazy('learn:list_course')


@user_passes_test(lambda u: u.is_staff, login_url='learn:login')
def delete_user_course(request):
    user_id = request.POST.get('user_id')
    course_id = request.POST.get('course_id')
    # Return all Subject of Course
    sub = Course.objects.get(pk=course_id).subjects.all()
    use = UserSubject.objects.filter(subject_id=sub).values_list('user_id', flat=True)
    use1 = User.objects.get(pk=user_id).id
    if use1 in use:
        return render(request, 'manage/course/error_delete.html')
    else:
        result = get_object_or_404(UserCourse, user_id=user_id, course_id=course_id)
        result.delete()
    return HttpResponseRedirect(reverse('learn:detail_course', kwargs={'pk': course_id}))


@user_passes_test(lambda u: u.is_staff, login_url='learn:login')
def add_user_course(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        course_id = request.POST.get('course_id')
        user = User.objects.get(pk=user_id)
        course = Course.objects.get(pk=course_id)
        result, created = UserCourse.objects.get_or_create(course_id=course, user_id=user)
        result.status = True
        result.save()
    return HttpResponseRedirect(reverse_lazy('learn:add_user_course_view', kwargs={'pk': course_id}))


class AddUserCourseView(DetailView):
    model = Course
    template_name = 'manage/course/add_user.html'
    context_object_name = 'detail_course'

    @method_decorator(user_passes_test)
    def dispatch(self, request, *args, **kwargs):
        return super(AddUserCourseView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(AddUserCourseView, self).get_context_data(**kwargs)
        user_course = UserCourse.objects.filter(course_id=self.object).values_list('user_id')
        # ctx['user_course'] = user_course
        ctx['users'] = User.objects.exclude(pk__in=user_course)
        ctx['user_course'] = User.objects.filter(pk__in=user_course)
        # pk__in=usercourse.user.pk)
        return ctx


# End Course

# Subject
class CreateSubjectView(CreateView):
    model = Subject
    form_class = CreateSubjectForm
    template_name = 'manage/subject/create_subject.html'
    # fields = ['name', 'description', 'begin_at', 'end_at', 'status']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateSubjectView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        subject = form.save()
        # subject.save()
        subject.courses = form.cleaned_data['courses']
        # form.save_m2m()
        return super(CreateSubjectView, self).form_valid(form)

    def get_success_url(self):
        return reverse('learn:list_subject')

        # def post(self, request, *args, **kwargs):
        #     course =
        #     return super(CreateSubjectView, self).post(request, *args, *kwargs)
        #
        # def get_context_data(self, **kwargs):
        #     context = super(CreateSubjectView, self).get_context_data(**kwargs)
        #     context['list_course'] = Course.objects.values_list('id')
        #     return context


class ListSubjectView(ListView):
    model = Subject
    template_name = 'manage/subject/index_subject.html'
    # context_object_name = 'list_subject'
    cou_id = ''

    def get_context_data(self, **kwargs):
        cou_id = self.request.GET.get('course_id')
        sub_name = self.request.GET.get('name_sub')
        ctx = super(ListSubjectView, self).get_context_data(**kwargs)
        ctx['list_course'] = Course.objects.all()
        ctx['list_subject'] = []
        if cou_id is None:
            ctx['list_subject'] = Subject.objects.all()
        else:
            if cou_id == '' and sub_name == '':
                ctx['list_subject'] = Subject.objects.all()
            elif sub_name == '' and cou_id != '':
                ctx['list_subject'] = Subject.objects.filter(courses=cou_id)
            elif sub_name != '' and cou_id == '':
                ctx['list_subject'] = Subject.objects.filter(name__contains=sub_name)
            elif sub_name != '' and cou_id != '':
                ctx['list_subject'] = Subject.objects.filter(courses=cou_id, name__contains=sub_name)
        return ctx


class DetailSubjectView(DetailView):
    model = Subject
    template_name = 'manage/subject/detail_subject.html'
    context_object_name = 'detail_subject'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        request.session['id_detail_subject'] = self.kwargs['pk']
        return super(DetailSubjectView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(DetailSubjectView, self).get_context_data(**kwargs)
        sub = get_object_or_404(Subject, pk=self.kwargs['pk'])
        ctx['list_course'] = self.object.courses.all()
        ctx['list_task'] = self.object.task.all()
        list_user = UserSubject.objects.filter(subject_id=sub, status=True)
        ctx['list_user'] = [User.objects.get(pk=i.user_id.pk) for i in list_user]
        return ctx


class EditSubjectView(UpdateView):
    model = Subject
    template_name = 'manage/subject/edit_subject.html'
    context_object_name = 'edit_subject'
    form_class = CreateSubjectForm
    # fields = ['name', 'description', 'created_at', 'updated_at', 'begin_at', 'end_at', 'status']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditSubjectView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(EditSubjectView, self).get_initial()
        if not hasattr(self, 'object'):
            self.object = self.get_object()
        initial['courses'] = Course.objects.filter(pk__in=self.object.courses.values_list('pk'))
        return initial

    def get_success_url(self):
        return reverse('learn:list_subject')

    def form_valid(self, form):
        subject = form.save()
        # subject.save()
        subject.courses = form.cleaned_data['courses']
        return super(EditSubjectView, self).form_valid(form)


def delete_subject(request):
    sub_id = request.POST.get('subject_id')
    sub = get_object_or_404(Subject, pk=sub_id)
    tasks = sub.task.all()
    use = UserTask.objects.filter(task_id=tasks, status=True).exists()

    if use:
        return render(request, 'manage/subject/error_delete.html', '')
    else:
        # delete all row in UserTask with task_id = ...
        UserTask.objects.filter(task_id=tasks).delete()
        # delete all Task of Subject
        sub.task.all().delete()
        # delete Subject
        sub.delete()
    return HttpResponseRedirect(reverse('learn:list_subject'))


def delete_user_subject(request):
    user_id = request.POST.get('user_id')
    subject_id = request.POST.get('subject_id')

    # check exists user in subject
    check_user_sub = UserSubject.objects.filter(user_id=user_id, subject_id=subject_id).exists()
    check = False
    if check_user_sub:
        sub = Subject.objects.get(pk=subject_id)
        all_task_sub = sub.task.all()
        # check user with status of UserTask
        for i in all_task_sub:
            if UserTask.objects.filter(user_id=user_id, task_id=i, status=True).exists():
                check = True
                break
    if check:
        return render(request, 'manage/task/error_delete.html', '')
    else:
        # get Subject
        sub = Subject.objects.get(pk=subject_id)
        all_task_sub = sub.task.all()

        for i in all_task_sub:
            UserTask.objects.filter(user_id=request.user, task_id=i).delete()
        # sub.task.all().delete()
        UserSubject.objects.filter(user_id=user_id, subject_id=subject_id).delete()
        # Subject.objects.get(pk=subject_id).delete()

    return HttpResponseRedirect(reverse('learn:list_subject'))


def add_user_subject(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        subject_id = request.POST.get('subject_id')
        user = User.objects.get(pk=user_id)
        subject = Subject.objects.get(pk=subject_id)
        result, created = UserSubject.objects.get_or_create(subject_id=subject, user_id=user)
        result.status = True
        result.save()

    return HttpResponseRedirect(reverse('learn:add_user_sub_view', kwargs={'pk': subject_id}))


class AddUserSubjectView(DetailView):
    model = Subject
    template_name = 'manage/subject/add_user.html'
    context_object_name = 'detail_subject'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AddUserSubjectView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(AddUserSubjectView, self).get_context_data(**kwargs)
        # tra ve user cua Subject
        user_subject = UserSubject.objects.filter(subject_id=self.object, status=True).values_list('user_id', flat=True)

        # tra ve user cua cac Course
        list_courses = self.object.courses.all().values_list('id', flat=True)
        list_users = UserCourse.objects.filter(course_id__in=list_courses).values_list('user_id', flat=True)
        list_users_1 = set(list_users)

        list = list_users_1.difference(user_subject)
        ctx['users'] = User.objects.filter(pk__in=list)
        ctx['user_course'] = User.objects.filter(pk__in=user_subject)
        return ctx


# Task

class ListTaskView(ListView):
    model = Task
    template_name = 'manage/task/index_task.html'
    # context_object_name = 'list_task'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ListTaskView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        search = self.request.GET.get('search', '')
        ctx = super(ListTaskView, self).get_context_data(**kwargs)
        if search == '':
            ctx['list_task'] = Task.objects.all()
        else:
            ctx['list_task'] = Task.objects.filter(name__contains=search)
        return ctx


class CreateTaskView(CreateView):
    model = Task
    template_name = 'manage/task/create_task.html'
    fields = ['name', 'subject_id', 'content', 'begin_at', 'end_at']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateTaskView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('learn:detail_subject', kwargs={'pk': self.request.session['id_detail_subject']})


class DetailTaskView(DetailView):
    model = Task
    template_name = 'manage/task/detail_task.html'
    context_object_name = 'detail_task'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        request.session['id_detail_task'] = self.kwargs['pk']
        return super(DetailTaskView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(DetailTaskView, self).get_context_data(**kwargs)
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        ctx['subject'] = self.object.subject_id

        list_user = UserTask.objects.filter(task_id=task, status=True)
        ctx['list_user_of_task'] = [User.objects.get(pk=i.user_id.pk) for i in list_user]
        return ctx


class EditTaskView(UpdateView):
    model = Task
    template_name = 'manage/task/edit_task.html'
    fields = ['name', 'subject_id', 'content', 'begin_at', 'end_at']
    context_object_name = 'edit_task'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditTaskView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('learn:detail_task', kwargs={'pk': self.request.session['id_detail_task']})


def delete_task(request):
    task_id = request.POST.get('task_id')
    check = UserTask.objects.filter(task_id=task_id, status=True).exists()
    if check:
        return render(request, 'manage/task/error_delete.html', '')
    else:
        dl = UserTask.objects.filter(task_id=task_id).delete()
        delete = Task.objects.get(pk=task_id)
        delete.delete()
        return HttpResponseRedirect(reverse_lazy('learn:list_task'))


def delete_user_task(request):
    user_id = request.POST.get('user_id')
    task_id = request.POST.get('task_id')
    result = get_object_or_404(UserTask, user_id=user_id, task_id=task_id)
    result.delete()
    return HttpResponseRedirect(reverse('learn:detail_task', kwargs={'pk': task_id}))


def add_user_task(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        task_id = request.POST.get('task_id')
        user = User.objects.get(pk=user_id)
        task = Task.objects.get(pk=task_id)

        result, created = UserTask.objects.get_or_create(task_id=task, user_id=user)
        result.status = True
        result.save()

    return HttpResponseRedirect(reverse('learn:add_user_task_view', kwargs={'pk': task_id}))


class AddUserTaskView(DetailView):
    model = Task
    template_name = 'manage/task/add_user.html'
    context_object_name = 'detail_task'

    # @method_decorator(login_required)
    @permission_required('is_staff')
    def dispatch(self, request, *args, **kwargs):
        return super(AddUserTaskView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(AddUserTaskView, self).get_context_data(**kwargs)
        ctx['subject'] = self.object.subject_id
        # Return user of Subject
        list_user_sub = self.object.subject_id.users.all().values_list('pk', flat=True)
        # Return user of task
        list_user_task = UserTask.objects.filter(task_id=self.object, status=True).values_list('user_id', flat=True)

        list = set(list_user_sub).difference(set(list_user_task))

        ctx['users_not_task'] = User.objects.filter(pk__in=list)
        ctx['user_task'] = User.objects.filter(pk__in=list_user_task)

        return ctx
