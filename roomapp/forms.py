from django import forms
from django.contrib.auth.forms import UserCreationForm
from roomapp.models import Profile, Room
from django.contrib.auth import get_user_model
User = get_user_model()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    username = None

    class Meta:
        model = User
        fields = ( 'email', 'password1', 'password2', 'first_name', 'last_name')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('mobile', 'occupation', 'birth_date', 'zipcode')

class RoomCreateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('room_name', 'room_address')

class ItemForm(forms.ModelForm):
    custom_queryset = User.objects.filter(has_room_admin=)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'] = forms.ChoiceField(choices=((student.id, student.username) for student in custom_queryset))
    # my_field = forms.MultipleChoiceField(choices=SOME_CHOICES, widget=forms.CheckboxSelectMultiple())

    def clean_my_field(self):
        if len(self.cleaned_data['my_field']) > 3:
            raise forms.ValidationError('Select no more than 3.')
        return self.cleaned_data['my_field']
    class Meta:
        model = Room
        fields = ('room_name', 'room_address')