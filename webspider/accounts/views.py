from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password')
        country_code = request.POST.get('country_code', '').strip()

        if '@' in username:
            if not username.lower().endswith('@gmail.com'):
                error = 'Please enter a valid Gmail address ending with @gmail.com.'
            else:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    error = 'Invalid credentials. Please try again.'
        elif username.isdigit():
            if not country_code or not country_code.startswith('+') or not country_code[1:].isdigit():
                error = 'Please enter a valid country code (e.g. +1) for your phone number.'
            else:
                phone_username = f"{country_code}{username}"
                user = authenticate(request, username=phone_username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    error = 'Invalid credentials. Please try again.'
        else:
            error = 'Enter a valid Gmail address or phone number.'
    return render(request, 'accounts/login.html', {'error': error})


def signup_view(request):
    error = None
    user_model = get_user_model()

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        gmail = request.POST.get('gmail', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not full_name:
            error = 'Please enter your full name.'
        elif not gmail.endswith('@gmail.com'):
            error = 'Please enter a valid Gmail address ending with @gmail.com.'
        elif password != confirm_password:
            error = 'Password and confirm password do not match.'
        elif user_model.objects.filter(username=gmail).exists():
            error = 'This Gmail account is already registered.'
        else:
            name_parts = full_name.split(maxsplit=1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''

            user_model.objects.create_user(
                username=gmail,
                email=gmail,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            return redirect('login')

    return render(request, 'accounts/signup.html', {'error': error})


@login_required(login_url='login')
def home_view(request):
    display_name = request.user.get_full_name().strip() or request.user.username
    return render(request, 'accounts/home.html', {'display_name': display_name})


@login_required(login_url='login')
def profile_view(request):
    error = None
    success = None
    full_name = request.user.get_full_name().strip()
    if not full_name:
        full_name = request.user.username

    if request.method == 'POST':
        submitted_name = request.POST.get('full_name', '').strip()
        uploaded_image = request.FILES.get('profile_image')
        fields_to_update = []

        if submitted_name:
            name_parts = submitted_name.split(maxsplit=1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            if request.user.first_name != first_name:
                request.user.first_name = first_name
                fields_to_update.append('first_name')
            if request.user.last_name != last_name:
                request.user.last_name = last_name
                fields_to_update.append('last_name')
            full_name = submitted_name

        if uploaded_image:
            request.user.profile_image = uploaded_image
            fields_to_update.append('profile_image')

        if not fields_to_update:
            error = 'Please update your name or choose an image.'
        else:
            request.user.save(update_fields=list(dict.fromkeys(fields_to_update)))
            success = 'Profile updated successfully.'

    display_name = request.user.get_full_name().strip() or request.user.username
    return render(
        request,
        'accounts/profile.html',
        {
            'error': error,
            'success': success,
            'full_name': full_name,
            'display_name': display_name,
        },
    )
