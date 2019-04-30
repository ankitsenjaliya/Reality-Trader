from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserRole, SysFeature, RoleCode, SysFeatureRole, Property, PropertyImages, Advertisement
from django.forms import ModelForm
from django.forms.widgets import DateInput


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ActiveStatusForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_active']


class RoleCodeForm(ModelForm):
    class Meta:
        model = RoleCode
        fields = ['name']


class SysFeatureForm(ModelForm):
    class Meta:
        model = SysFeature
        fields = ['name']


class UserRoleForm(ModelForm):
    class Meta:
        model = UserRole
        fields = ['username', 'rolename']


class SysFeatureRoleForm(ModelForm):
    class Meta:
        model = SysFeatureRole
        fields = ['featurename', 'rolename', 'permissiontype']


class PropertyForm(ModelForm):
    class Meta:
        model = Property
        fields = ['id', 'propertyTitle', 'property_sector', 'property_category', 'property_facing', 'property_country',
                  'property_province', 'property_city', 'propertyStreet', 'propertyPostalCode',
                  'propertyStreetNumber', 'propertyConstructionDate', 'propertyRegistrationDate',
                  'propertyNoOfHalls', 'propertyNoOfBedRooms', 'propertyNoOfBathRooms', 'propertyNoOfFloors',
                  'propertyTotalArea', 'propertyAskingPrice', 'propertySellingPrice']
        widgets = {
            'propertyConstructionDate': DateInput(attrs={'type': 'date'}),
            'propertyRegistrationDate': DateInput(attrs={'type': 'date'})
        }


class PropertyImagesForm(ModelForm):
    class Meta:
        model = PropertyImages
        fields = ['propertyID', 'propertyImage', 'propertyImageDescription']


class AdvertisementsForm(ModelForm):
    class Meta:
        model = Advertisement
        fields = ['id', 'advUserId', 'advProperty', 'advStartDate', 'advEndDate', 'advDescription']

        widgets = {
            'advStartDate': DateInput(attrs={'type': 'date'}),
            'advEndDate': DateInput(attrs={'type': 'date'})
        }
