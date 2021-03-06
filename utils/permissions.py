from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def student_required(function=None,redirect_field_name=REDIRECT_FIELD_NAME,login_url='accounts/login'):

    actual_deco=user_passes_test(
         lambda u:u.is_active and u.is_superuser==False and u.is_superuser==False,
         login_url=login_url,
         redirect_field_name=redirect_field_name
      )
    if function:
        return actual_deco(function)
    return actual_deco
def admin_required(function=None,redirect_field_name=REDIRECT_FIELD_NAME,login_url='accounts/login'):

    actual_deco=user_passes_test(
         lambda u:u.is_active and u.is_superuser,
         login_url=login_url,
         redirect_field_name=redirect_field_name
      )
    if function:
        return actual_deco(function)
    return actual_deco