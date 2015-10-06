from django.utils.translation import ugettext_lazy as _

from django import forms
# from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.forms import Textarea, DateInput

from learn.models import Subject, Course

__author__ = 'FRAMGIA\nguyen.huy.quyet'


class CreateSubjectForm(forms.ModelForm):
    courses = forms.ModelMultipleChoiceField(queryset=Course.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Subject
        fields = ['name', 'description', 'begin_at', 'end_at', 'status', 'courses']
        widgets = {
            'name': Textarea(attrs={'cols': 30, 'rows': 1}),
            'description': Textarea(attrs={'cols': 30, 'rows': 3}),
            'begin_at': DateInput(),
            'end_at': DateInput(),

        }

        # def __init__(self, *args, **kwargs):
        #     if 'instance' in kwargs:
        #         initial = kwargs.setdefault('initial', {})
        #         initial['courses'] = [t.pk for t in kwargs['instance'].course_set.all()]
        #     forms.ModelForm.__init__(self, *args, **kwargs)

        # def __init__(self, *args, **kwargs):
        #     qs = kwargs.pop('courses')
        #     super(CreateSubjectForm, self).__init__(*args, **kwargs)
        #     self.fields['courses'].queryset = qs


class EditCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'begin_at', 'end_at']
        widgets = {
            'name': Textarea(attrs={'cols': 30, 'rows': 1}),
            'description': Textarea(attrs={'cols': 30, 'rows': 3}),
        }


class PasswordResetForm(forms.Form):
    password1 = forms.CharField(
        label=_('New password'),
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_('New password (confirm)'),
        widget=forms.PasswordInput,
    )

    error_messages = {
        'password_mismatch': _("The two passwords didn't match."),
    }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data['password2']
        if not password1 == password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch')
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['password1'])
        if commit:
            get_user_model()._default_manager.filter(pk=self.user.pk).update(password=self.user.password, )
        return self.user
