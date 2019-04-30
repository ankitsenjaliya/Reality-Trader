from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, PermissionType, SysFeatureRole, RoleCode, SysFeature, UserRole, Property, PropertyCategory, \
    PropertySector, PropertyFacing, PropertyImages, Country, City, Province, Advertisement


class Useradmin(admin.ModelAdmin):
    list_display = ['id', 'firstName', 'lastName', 'email']


admin.site.register(User, Useradmin)


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id', 'advUserId', 'advStartDate', 'advEndDate', 'advDescription']


admin.site.register(Advertisement, AdvertisementAdmin)


class Countryadmin(admin.ModelAdmin):
    list_display = ['id', 'countryName']


admin.site.register(Country, Countryadmin)


class Provinceadmin(admin.ModelAdmin):
    list_display = ['id', 'countryName', 'provinceName']


admin.site.register(Province, Provinceadmin)


class Cityadmin(admin.ModelAdmin):
    list_display = ['id', 'countryName', 'provinceName', 'cityName']


admin.site.register(City, Cityadmin)


class Propertyadmin(admin.ModelAdmin):
    list_display = ['id', 'propertyTitle', 'property_category', 'property_sector', 'property_facing', 'property_country',
                    'property_province', 'property_city', 'propertyStreet', 'propertyPostalCode', 'propertyStreetNumber',
                    'propertyConstructionDate', 'propertyRegistrationDate', 'propertyNoOfHalls', 'propertyNoOfBedRooms',
                    'propertyNoOfBathRooms', 'propertyNoOfFloors', 'propertyTotalArea', 'propertyAskingPrice',
                    'propertySellingPrice']


admin.site.register(Property, Propertyadmin)


class PropertyImagesadmin(admin.ModelAdmin):
    list_display = ['propertyImageID', 'propertyID', 'propertyImage', 'propertyImageDescription']


admin.site.register(PropertyImages, PropertyImagesadmin)

admin.site.register(PropertyCategory)
admin.site.register(PropertySector)
admin.site.register(PropertyFacing)
admin.site.register(UserRole)
admin.site.register(SysFeature)
admin.site.register(RoleCode)
admin.site.register(SysFeatureRole)
admin.site.register(PermissionType)
