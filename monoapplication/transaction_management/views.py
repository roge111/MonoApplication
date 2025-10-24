from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_start=True, set_cookie=True)
def main_user(request):
    return render(request, 'transaction_management/main_page.html', locals())


@main_auth(on_cookies=True)
def page(request):
    return render(request, 'transaction_management/page.html', locals())
# Create your views here.
