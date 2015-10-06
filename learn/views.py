# Create your views here.
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView


def index(request):
    if request.user.is_authenticated():
        if request.user.is_staff:
            return HttpResponseRedirect(reverse('learn:index_admin'))
        else:
            return HttpResponseRedirect(reverse('learn:index_user'))
    else:
        return render(request, 'index.html', '')


def login_view(request):
    return render(request, 'account/login.html')


def singin(request):
    # check request
    if request.method == 'POST':
        user_form = AuthenticationForm(data=request.POST)

        # check valid data
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            # link = user_form.cleaned_data['next']

            # authentication account
            auth_user = authenticate(username=username, password=password)

            if auth_user is not None:

                # check account
                if auth_user.is_active:
                    login(request, auth_user)
                    link = request.POST.get('next', '')
                    if link:
                        return HttpResponseRedirect(link)
                    else:
                        if auth_user.is_staff:
                            return HttpResponseRedirect(reverse('learn:index_admin'))
                        else:
                            return HttpResponseRedirect(reverse('learn:index_user'))

                # Account is ban or lock
                else:
                    return render(request, 'account/login_fail.html', {'error': 'Account is ban or lock'})

            # Account is DoseNotExist
            else:
                return render(request, 'account/login_fail.html', {'error': 'Account is DoseNotExist'})

        # data error
        else:
            return render(request, 'account/login_fail.html', {'error': 'Error login'})

    # method error
    return render(request, 'account/login_fail.html', {'error': 'Error login'})


def singout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('learn:index'))


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.instance.is_staff = True
            form.save()
            return HttpResponseRedirect(reverse('learn:login'))
    else:
        form = UserCreationForm()
    return render(request, 'account/register.html', {'form': form})


class EditProfileView(UpdateView):
    model = User
    template_name = 'account/edit_profile.html'
    fields = ['first_name', 'last_name', 'email']
    context_object_name = 'user_obj'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != request.user:
            raise PermissionDenied
        return super(EditProfileView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('learn:index')


class ProfileView(DetailView):
    model = User
    template_name = 'account/view_profile.html'
    context_object_name = 'profile'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileView, self).dispatch(request, *args, **kwargs)


def changepass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learn:index'))
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'account/change_pass.html', {'form': form})
