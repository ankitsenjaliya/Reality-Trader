from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, get_object_or_404
import csv
import io

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as dj_login, logout as django_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.db.models import Q
from django.views import generic

from .forms import SignUpForm, RoleCodeForm, UserRoleForm, SysFeatureForm, SysFeatureRoleForm, ActiveStatusForm, \
    PropertyForm, PropertyImagesForm, AdvertisementsForm, UpdateProfileForm
from .models import SysFeature, RoleCode, SysFeatureRole, PermissionType, UserRole, Property, PropertyImages, \
    Advertisement, City

from .tokens import account_activation_token


# Create your views here.
def base(request):
    return render(request, 'home/base.html')


def home(request):
    context = {}
    context['user'] = request.user
    property_item = Property.objects.all() \
        .select_related('property_province', 'property_country', 'property_city')
    return render(request, 'home/home.html', {'user': request.user, 'property_item': property_item})


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.is_staff = True
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate Realty Trader account.'
            message = render_to_string('home/new_acc_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = 'realtytrader1@gmail.com'
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return redirect('registartionDetail')
    else:
        form = SignUpForm()
    return render(request, 'home/register.html', {'form': form})


def registartionDetail(request):
    return render(request, 'home/registartionDetail.html')


def activate_user(request):
    if request.POST:
        user_id = request.POST['user_id']
        status = request.POST['status']
        if user_id and status:
            user = User.objects.filter(id=user_id).first()
            status_form = ActiveStatusForm(request.POST)
            if status_form.is_valid():
                first_time_password = get_random_string(8, allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789')
                user.set_password(first_time_password)
                user.is_active = status

                user.save()

                current_site = get_current_site(request)
                mail_subject = 'Your account for Realty Trader has been activated.'
                message = render_to_string('home/acc_active_email.html', {
                    'user': user,
                    'temporary_password': first_time_password,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                to_email = user.email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
            return redirect('listUnapprovedUser')
        else:
            return redirect('addUser')


def enable_disable_user(request):
    if request.POST:
        user_id = request.POST['user_id']
        status = request.POST['status']
        if user_id and status:
            user = User.objects.filter(id=user_id).first()
            status_form = ActiveStatusForm(request.POST)
            if status_form.is_valid():
                user.is_active = status
                user.save()
            return redirect('listUser')
        else:
            return redirect('addUser')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        dj_login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def about(request):
    return render(request, 'home/about.html')


def contact(request):
    return render(request, 'home/contact.html')


def admin_portal(request):
    return render(request, 'admin_portal/listUser.html')


def login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_staff:
                dj_login(request, user)
                return redirect('changePassword')
            else:
                dj_login(request, user)
                return HttpResponseRedirect(reverse('manageProperty'))
        else:
            context['error'] = 'Provide valid credential'
            return render(request, 'home/login.html', context)

    return render(request, 'home/login.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            dj_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'admin_portal/signup.html', {'form': form})


def changePassword(request):
    messages.success(request, request.method)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = False
            user.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'home/change_password.html', {
            'form': form
        })


def updateProfile(request, pk):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=pk)
        form = UpdateProfileForm(request.POST or None, instance=user)
        if form.is_valid():
            user = form.save()
            user.save()
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UpdateProfileForm(request.user)
        return render(request, 'home/updateProfile.html', {'form': form})


def listUser(request):
    users = User.objects.all()
    return render(request, 'admin_portal/listUser.html', {'users': users})


def listUnapprovedUser(request):
    users = User.objects.all().filter(is_active=False, is_staff=True)
    return render(request, 'admin_portal/listUnapprovedUser.html', {'users': users})


def listUserRole(request):
    userroles = UserRole.objects.all()
    return render(request, 'admin_portal/listUserRole.html', {'userroles': userroles})


def manageRole(request):
    users = User.objects.all()
    roles = RoleCode.objects.all()
    form = UserRoleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('listUserRole')
    return render(request, 'admin_portal/manageRole.html', {'users': users, 'roles': roles})


def addUser(request):
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('listUser')
    return render(request, 'admin_portal/addUser.html', {'form': form})


def editUser(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = SignUpForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('listUser')
    return render(request, 'admin_portal/editUser.html', {'form': form})


def deleteUser(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('listUser')
    return render(request, 'admin_portal/userConfirmDelete.html', {'object': user})


def deleteUserRole(request, pk):
    userrole = get_object_or_404(UserRole, pk=pk)
    if request.method == 'POST':
        userrole.delete()
        return redirect('listUserRole')
    return render(request, 'admin_portal/userroleConfirmDelete.html', {'object': userrole})


def listRole(request):
    roles = RoleCode.objects.all()
    return render(request, 'admin_portal/listRole.html', {'roles': roles})


def addRole(request):
    form = RoleCodeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('listRole')
    return render(request, 'admin_portal/addRole.html', {'form': form})


def editRole(request, pk):
    rolecode = get_object_or_404(RoleCode, pk=pk)
    form = RoleCodeForm(request.POST or None, instance=rolecode)
    if form.is_valid():
        form.save()
        return redirect('listRole')
    return render(request, 'admin_portal/editRole.html', {'form': form})


def deleteRole(request, pk):
    rolecode = get_object_or_404(RoleCode, pk=pk)
    if request.method == 'POST':
        rolecode.delete()
        return redirect('listRole')
    return render(request, 'admin_portal/roleConfirmDelete.html', {'object': rolecode})


def listFeature(request):
    features = SysFeature.objects.all()
    return render(request, 'admin_portal/listFeature.html', {'features': features})


def addFeature(request):
    form = SysFeatureForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('listFeature')
    return render(request, 'admin_portal/addFeature.html', {'form': form})


def importFeature(request):
    template = 'admin_portal/importFeature.html'

    prompt = {
        'order': 'Order of CSV should be name'
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES.get('file')
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not CSV file')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)

    next(io_string)

    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = SysFeature.objects.update_or_create(
            name=column[0]
        )

    features = SysFeature.objects.all()
    return render(request, 'admin_portal/listFeature.html', {'features': features})


def editFeature(request, pk):
    feature = get_object_or_404(SysFeature, pk=pk)
    form = SysFeatureForm(request.POST or None, instance=feature)
    if form.is_valid():
        form.save()
        return redirect('listFeature')
    return render(request, 'admin_portal/editFeature.html', {'form': form})


def deleteFeature(request, pk):
    feature = get_object_or_404(SysFeature, pk=pk)
    if request.method == 'POST':
        feature.delete()
        return redirect('listFeature')
    return render(request, 'admin_portal/featureConfirmDelete.html', {'object': feature})


def deleteAssignFeatures(request, pk):
    assignfeature = get_object_or_404(SysFeatureRole, pk=pk)
    if request.method == 'POST':
        assignfeature.delete()
        return redirect('listAssignFeatures')
    return render(request, 'admin_portal/assignFeatureConfirmDelete.html', {'object': assignfeature})


def listAssignFeatures(request):
    assignfeatures = SysFeatureRole.objects.all()
    return render(request, 'admin_portal/listAssignFeatures.html', {'assignfeatures': assignfeatures})


def assignFeature(request):
    sysfeatures = SysFeature.objects.all()
    roles = RoleCode.objects.all()
    permissiontypes = PermissionType.objects.all()
    form = SysFeatureRoleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('listAssignFeatures')
    return render(request, 'admin_portal/assignFeature.html',
                  {'sysfeatures': sysfeatures, 'roles': roles, 'permissiontypes': permissiontypes})


def logout(request):
    if request.method == "POST":
        django_logout(request)
    return HttpResponseRedirect(reverse('login'))


def view_property(request):
    return render(request, 'view_property.html')


# Property
def listProperty(request):
    properties = Property.objects.all()
    return render(request, 'admin_portal/listProperty.html', {'properties': properties})


def addProperty(request):
    form = PropertyForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('listProperty')
    return render(request, 'admin_portal/addProperty.html', {'form': form})


def editProperty(request, pk):
    property = get_object_or_404(Property, pk=pk)
    form = PropertyForm(request.POST or None, instance=property)
    if form.is_valid():
        form.save()
        return redirect('listProperty')
    return render(request, 'admin_portal/editProperty.html', {'form': form})


def deleteProperty(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        property.delete()
        return redirect('listProperty')
    return render(request, 'admin_portal/propertyConfirmDelete.html', {'object': property})


# user side
def manageProperty(request):
    properties = Property.objects.all()
    return render(request, 'home/manageProperty.html', {'properties': properties})


def useraddProperty(request):
    form = PropertyForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('manageProperty')
    return render(request, 'home/useraddProperty.html', {'form': form})


def usereditProperty(request, pk):
    property = get_object_or_404(Property, pk=pk)
    form = PropertyForm(request.POST or None, instance=property)
    if form.is_valid():
        form.save()
        return redirect('manageProperty')
    return render(request, 'home/usereditProperty.html', {'form': form})


def userdeleteProperty(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        property.delete()
        return redirect('manageProperty')
    return render(request, 'home/userpropertyConfirmDelete.html', {'object': property})


# PropertyImages

def listPropertyImage(request):
    properties_images = PropertyImages.objects.all()
    return render(request, 'admin_portal/listPropertyImage.html', {'properties_images': properties_images})


def addPropertyImage(request):
    form = PropertyImagesForm(request.POST or None, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('listPropertyImage')
    return render(request, 'admin_portal/addPropertyImage.html', {'form': form})


def editPropertyImage(request, pk):
    propertyImage = get_object_or_404(PropertyImages, pk=pk)
    form = PropertyImagesForm(request.POST or None, instance=propertyImage)
    if form.is_valid():
        form.save()
        return redirect('listPropertyImage')
    return render(request, 'admin_portal/editPropertyImage.html', {'form': form})


def deletePropertyImage(request, pk):
    propertyImage = get_object_or_404(PropertyImages, pk=pk)
    if request.method == 'POST':
        propertyImage.delete()
        return redirect('listPropertyImage')
    return render(request, 'admin_portal/propertyImageConfirmDelete.html', {'object': propertyImage})


# Advertisement
def listAdvertisement(request):
    ads = Advertisement.objects.all()
    return render(request, 'admin_portal/listAdvertisement.html', {'ads': ads})


def addAdvertisement(request):
    form = AdvertisementsForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('listAdvertisement')
    return render(request, 'admin_portal/addProperty.html', {'form': form})


def editAdvertisement(request, pk):
    ad = get_object_or_404(Advertisement, pk=pk)
    form = AdvertisementsForm(request.POST or None, instance=ad)
    if form.is_valid():
        form.save()
        return redirect('listAdvertisement')
    return render(request, 'admin_portal/editAdvertisement.html', {'form': form})


def advertisementConfirmDelete(request, pk):
    ad = get_object_or_404(Advertisement, pk=pk)
    if request.method == 'POST':
        ad.delete()
        return redirect('listAdvertisement')
    return render(request, 'admin_portal/advertisementConfirmDelete.html', {'object': ad})


# def propertylisting(request):
#    return render(request, 'home/propertylisting.html')

# def propertylisting(request,cityName, provinceName, countryName):
#
#     if 'search' in request.GET:
#         property_item = \
#             Property.objects.filter(Q(propertyTitle__icontains=request.GET.get('search')) | \
#                                     Q(property_city__cityName__icontains= cityName) | \
#                                     Q(property_province__provinceName__icontains= provinceName) | \
#                                     Q(property_country__countryName__icontains= countryName))\
#                                     .select_related('property_province', 'property_country', 'property_city')
#
#     else:
#         property_item = Property.objects.all() \
#             .select_related('property_province', 'property_country', 'property_city')
#
#     return render(request, 'home/propertylisting.html', {'property_item': property_item})

def propertylisting(request):
    if 'search' in request.GET:
        property_item = \
            Property.objects.filter(Q(propertyTitle__icontains=request.GET.get('search'))) \
                .select_related('property_province', 'property_country', 'property_city')

    elif request.GET.get('search1') != '0' and request.GET.get('search2') == '0' and request.GET.get('search3') == '0':
        property_item = \
            Property.objects.filter(property_country__countryName__icontains=request.GET.get('search1')) \
                .select_related('property_country')

    elif request.GET.get('search1') == '0' and request.GET.get('search2') != '0' and request.GET.get('search3') == '0':
        property_item = \
            Property.objects.filter(property_province__provinceName__icontains=request.GET.get('search2')) \
                .select_related('property_province')

    elif request.GET.get('search1') == '0' and request.GET.get('search2') == '0' and request.GET.get('search3') != '0':
        property_item = \
            Property.objects.filter(property_city__cityName__icontains=request.GET.get('search3')) \
                .select_related('property_city')

    else:
        property_item = Property.objects.all() \
            .select_related('property_province', 'property_country', 'property_city')

    return render(request, 'home/propertylisting.html', \
                  {'property_item': property_item})


def advertisementlisting(request):
    property_item = Property.objects.all()
    return render(request, 'home/propertylisting.html', {'property_item': property_item})


def advertisement(request):
    if request.method == 'POST':
        form = PropertyImagesForm(request.POST or None, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PropertyImagesForm()
        return render(request, 'home/advertisement.html', {'form': form})


def singlePropertyDetails(request, pk):
    property_item = get_object_or_404(Property, pk=pk)
    return render(request, 'home/singlePropertyDetails.html', {'property_item': property_item})


# User PropertyImages

def userlistPropertyImage(request):
    properties_images = PropertyImages.objects.all()
    return render(request, 'home/userlistPropertyImage.html', {'properties_images': properties_images})


def useraddPropertyImage(request):
    form = PropertyImagesForm(request.POST or None, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('userlistPropertyImage')
    return render(request, 'home/useraddPropertyImage.html', {'form': form})


def usereditPropertyImage(request, pk):
    propertyImage = get_object_or_404(PropertyImages, pk=pk)
    form = PropertyImagesForm(request.POST or None, instance=propertyImage)
    if form.is_valid():
        form.save()
        return redirect('userlistPropertyImage')
    return render(request, 'home/usereditPropertyImage.html', {'form': form})


def userdeletePropertyImage(request, pk):
    propertyImage = get_object_or_404(PropertyImages, pk=pk)
    if request.method == 'POST':
        propertyImage.delete()
        return redirect('userlistPropertyImage')
    return render(request, 'home/userpropertyImageConfirmDelete.html', {'object': propertyImage})


# user Advertisement
def userlistAdvertisement(request):
    ads = Advertisement.objects.all().filter(advUserId=request.user.id).order_by('-advStartDate')
    return render(request, 'home/userlistAdvertisement.html', {'ads': ads})


@login_required
def useraddAdvertisement(request):
    form = AdvertisementsForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('userlistAdvertisement')
    return render(request, 'home/useraddAdvertisement.html', {'form': form})


def usereditAdvertisement(request, pk):
    ad = get_object_or_404(Advertisement, pk=pk)
    form = AdvertisementsForm(request.POST or None, instance=ad)
    if form.is_valid():
        form.save()
        return redirect('userlistAdvertisement')
    return render(request, 'home/usereditAdvertisement.html', {'form': form})


def useradvertisementConfirmDelete(request, pk):
    ad = get_object_or_404(Advertisement, pk=pk)
    if request.method == 'POST':
        ad.delete()
        return redirect('userlistAdvertisement')
    return render(request, 'home/useradvertisementConfirmDelete.html', {'object': ad})
