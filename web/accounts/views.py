from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.utils.html import strip_tags
from django.contrib import messages
from django.http import Http404
from .forms import *


# Регистрация. Все стандартно, кроме кастомной верификации
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            key = Verification.set(user, Verification.REG)
            user.save()

            #confirm_url = request.scheme + '://' + request.get_host() + reverse('register-confirm', kwargs={'key': key})
            #html_content = render_to_string('accounts/register_html_mail.html', context={'url': confirm_url})
            template_name = 'register_html_mail'
            #text_content = strip_tags(html_content)
            user.send_mail(request, template_name)
            return render(request, 'accounts/verify_sent.html', locals())
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', locals())


# Запрос на восстановление аккаунта. Аналогично регистрации, основное веселье в форме
def restore(request):
    if request.method == 'POST':
        form = UserRestoreForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            key = Verification.set(user, Verification.PASS)
            user.save()

            template_name = 'restore_html_mail'
            user.send_mail(request, template_name)
            return render(request, 'accounts/verify_sent.html', locals())
    else:
        form = UserRestoreForm()
    return render(request, 'accounts/restore.html', locals())


# Универсальная (почти) вьюха подтверждения/восстановления
# Проверяет ключик, в случае неудачи кидает на 404, в удачном - на установку пароля
def confirm(request, key, vn_action=None, template=None):
    user = Verification.check(key, vn_action)
    if not user: raise Http404
    if request.method == 'POST':
        form = PasswordSetForm(request.user, request.POST)
        if form.is_valid():
            Verification.reset(user)
            user.set_password(form.cleaned_data['new_password1'])
            user.is_active = True
            user.save()

            return render(request, template, locals())
    else:
        form = PasswordSetForm(request.user)
    return render(request, 'accounts/password_set.html', locals())


# Вьюха для личного кабинета, в качестве обратной связи - фреймворк messages (при желании можно убрать)
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профиль успешно обновлен')
        else:
            messages.error(request, 'Ошибка при обновлении профиля')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', locals())


# Изменение пароля, фреймворк messages
@login_required
def edit_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # Чтобы не выкидывать пользователя из сессии
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Пароль успешно обновлен')
        else:
            messages.error(request, 'Ошибка при обновлении пароля')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'accounts/password_edit.html', locals())