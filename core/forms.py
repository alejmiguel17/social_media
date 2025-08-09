from django import forms
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    # La clase Meta define el modelo y los campos que se incluirán en el formulario
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio']