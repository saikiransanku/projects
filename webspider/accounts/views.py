from datetime import datetime
from decimal import Decimal, InvalidOperation
from urllib.parse import quote_plus

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import UsageHistory

SEASON_OPTIONS = [
    ('', 'Select season'),
    ('kharif', 'Kharif'),
    ('rabi', 'Rabi'),
    ('zaid', 'Zaid'),
    ('all_season', 'All Season'),
]

INDIA_STATES_AND_UTS = [
    'Andhra Pradesh',
    'Arunachal Pradesh',
    'Assam',
    'Bihar',
    'Chhattisgarh',
    'Goa',
    'Gujarat',
    'Haryana',
    'Himachal Pradesh',
    'Jharkhand',
    'Karnataka',
    'Kerala',
    'Madhya Pradesh',
    'Maharashtra',
    'Manipur',
    'Meghalaya',
    'Mizoram',
    'Nagaland',
    'Odisha',
    'Punjab',
    'Rajasthan',
    'Sikkim',
    'Tamil Nadu',
    'Telangana',
    'Tripura',
    'Uttar Pradesh',
    'Uttarakhand',
    'West Bengal',
    'Andaman and Nicobar Islands',
    'Chandigarh',
    'Dadra and Nagar Haveli and Daman and Diu',
    'Delhi (NCT)',
    'Jammu and Kashmir',
    'Ladakh',
    'Lakshadweep',
    'Puducherry',
]

CENTRAL_FARMER_LAWS = [
    {
        'title': "Protection of Plant Varieties and Farmers' Rights Act",
        'year': '2001',
        'judicial_number': 'Act 53 of 2001',
        'category': "Farmers' rights and seeds",
        'status': 'In force',
    },
    {
        'title': 'Seeds Act',
        'year': '1966',
        'judicial_number': 'Act 54 of 1966',
        'category': 'Seed quality and certification',
        'status': 'In force',
    },
    {
        'title': 'Seed (Control) Order',
        'year': '1983',
        'judicial_number': 'Order, 1983 (under Essential Commodities Act)',
        'category': 'Seed licensing and sale',
        'status': 'In force',
    },
    {
        'title': 'Insecticides Act',
        'year': '1968',
        'judicial_number': 'Act 46 of 1968',
        'category': 'Pesticides and crop protection',
        'status': 'In force',
    },
    {
        'title': 'Insecticides Rules',
        'year': '1971',
        'judicial_number': 'Rules, 1971',
        'category': 'Pesticide registration and dealer compliance',
        'status': 'In force',
    },
    {
        'title': 'Destructive Insects and Pests Act',
        'year': '1914',
        'judicial_number': 'Act 2 of 1914',
        'category': 'Plant quarantine and pest control',
        'status': 'In force',
    },
    {
        'title': 'Fertiliser (Control) Order',
        'year': '1985',
        'judicial_number': 'FCO, 1985 (under Essential Commodities Act)',
        'category': 'Fertilizers and input quality',
        'status': 'In force',
    },
    {
        'title': 'Essential Commodities Act',
        'year': '1955',
        'judicial_number': 'Act 10 of 1955',
        'category': 'Storage, supply and pricing controls',
        'status': 'In force',
    },
    {
        'title': 'Legal Metrology Act',
        'year': '2009',
        'judicial_number': 'Act 1 of 2010',
        'category': 'Input purchase, weights and measures',
        'status': 'In force',
    },
    {
        'title': 'Consumer Protection Act',
        'year': '2019',
        'judicial_number': 'Act 35 of 2019',
        'category': 'Buying equipment and service disputes',
        'status': 'In force',
    },
    {
        'title': 'Sale of Goods Act',
        'year': '1930',
        'judicial_number': 'Act 3 of 1930',
        'category': 'Contracts for farm equipment and inputs',
        'status': 'In force',
    },
    {
        'title': 'Bureau of Indian Standards Act',
        'year': '2016',
        'judicial_number': 'Act 11 of 2016',
        'category': 'Standards for machinery and products',
        'status': 'In force',
    },
    {
        'title': 'Motor Vehicles Act',
        'year': '1988',
        'judicial_number': 'Act 59 of 1988',
        'category': 'Farm vehicle usage and transport compliance',
        'status': 'In force',
    },
    {
        'title': 'Central Goods and Services Tax Act',
        'year': '2017',
        'judicial_number': 'Act 12 of 2017',
        'category': 'Taxation on farm equipment and services',
        'status': 'In force',
    },
    {
        'title': 'Integrated Goods and Services Tax Act',
        'year': '2017',
        'judicial_number': 'Act 13 of 2017',
        'category': 'Inter-state tax on agricultural inputs',
        'status': 'In force',
    },
    {
        'title': 'Warehousing (Development and Regulation) Act',
        'year': '2007',
        'judicial_number': 'Act 37 of 2007',
        'category': 'Warehouse registration and receipts',
        'status': 'In force',
    },
    {
        'title': 'Food Safety and Standards Act',
        'year': '2006',
        'judicial_number': 'Act 34 of 2006',
        'category': 'Food quality and safety',
        'status': 'In force',
    },
    {
        'title': 'Agricultural Produce (Grading and Marking) Act (AGMARK)',
        'year': '1937',
        'judicial_number': 'Act 1 of 1937',
        'category': 'Quality grading and certification',
        'status': 'In force',
    },
    {
        'title': 'National Food Security Act',
        'year': '2013',
        'judicial_number': 'Act 20 of 2013',
        'category': 'Food security and procurement framework',
        'status': 'In force',
    },
    {
        'title': (
            'Right to Fair Compensation and Transparency in Land Acquisition, '
            'Rehabilitation and Resettlement Act'
        ),
        'year': '2013',
        'judicial_number': 'Act 30 of 2013',
        'category': 'Land acquisition and farmer compensation',
        'status': 'In force',
    },
    {
        'title': (
            'Scheduled Tribes and Other Traditional Forest Dwellers '
            '(Recognition of Forest Rights) Act'
        ),
        'year': '2006',
        'judicial_number': 'Act 2 of 2007',
        'category': 'Forest land rights for cultivators',
        'status': 'In force',
    },
    {
        'title': 'Water (Prevention and Control of Pollution) Act',
        'year': '1974',
        'judicial_number': 'Act 6 of 1974',
        'category': 'Water use and pollution control',
        'status': 'In force',
    },
    {
        'title': 'Air (Prevention and Control of Pollution) Act',
        'year': '1981',
        'judicial_number': 'Act 14 of 1981',
        'category': 'Air pollution compliance',
        'status': 'In force',
    },
    {
        'title': 'Environment (Protection) Act',
        'year': '1986',
        'judicial_number': 'Act 29 of 1986',
        'category': 'Environmental compliance in agriculture',
        'status': 'In force',
    },
    {
        'title': 'Biological Diversity Act',
        'year': '2002',
        'judicial_number': 'Act 18 of 2003 (enforced)',
        'category': 'Biodiversity access and benefit sharing',
        'status': 'In force',
    },
    {
        'title': 'Electricity Act',
        'year': '2003',
        'judicial_number': 'Act 36 of 2003',
        'category': 'Agricultural power supply and regulation',
        'status': 'In force',
    },
    {
        'title': 'Mahatma Gandhi National Rural Employment Guarantee Act',
        'year': '2005',
        'judicial_number': 'Act 42 of 2005',
        'category': 'Rural labor support for farm households',
        'status': 'In force',
    },
    {
        'title': 'Micro, Small and Medium Enterprises Development Act',
        'year': '2006',
        'judicial_number': 'Act 27 of 2006',
        'category': 'Agri-processing and small enterprise support',
        'status': 'In force',
    },
    {
        'title': 'Farmers Produce Trade and Commerce (Promotion and Facilitation) Act',
        'year': '2020',
        'judicial_number': 'Act 20 of 2020',
        'category': 'Agricultural marketing reforms',
        'status': 'Repealed in 2021',
    },
    {
        'title': (
            'Farmers (Empowerment and Protection) Agreement on Price Assurance and '
            'Farm Services Act'
        ),
        'year': '2020',
        'judicial_number': 'Act 21 of 2020',
        'category': 'Contract farming framework',
        'status': 'Repealed in 2021',
    },
    {
        'title': 'Essential Commodities (Amendment) Act',
        'year': '2020',
        'judicial_number': 'Act 22 of 2020',
        'category': 'Commodity regulation reform',
        'status': 'Repealed in 2021',
    },
    {
        'title': 'Farm Laws Repeal Act',
        'year': '2021',
        'judicial_number': 'Act 55 of 2021',
        'category': 'Repeal of the 2020 farm laws',
        'status': 'In force',
    },
]

STATE_SPECIFIC_LAW_TEMPLATES = [
    {
        'title_template': '{state} APMC / Agricultural Produce Marketing Law',
        'year': 'State-wise',
        'judicial_number': 'State Act number (varies)',
        'category': 'Mandi licensing, market fee and agricultural trade',
        'status': 'Varies by state',
    },
    {
        'title_template': '{state} Land Revenue and Land Reforms Laws',
        'year': 'State-wise',
        'judicial_number': 'State Act number (varies)',
        'category': 'Land records, titles and mutation',
        'status': 'In force (state specific)',
    },
    {
        'title_template': '{state} Agricultural Tenancy and Land Ceiling Laws',
        'year': 'State-wise',
        'judicial_number': 'State Act number (varies)',
        'category': 'Tenancy rights and ceiling limits',
        'status': 'In force (state specific)',
    },
    {
        'title_template': '{state} Groundwater and Irrigation Regulation Laws',
        'year': 'State-wise',
        'judicial_number': 'State Act number (varies)',
        'category': 'Irrigation usage and groundwater compliance',
        'status': 'In force (state specific)',
    },
    {
        'title_template': '{state} Cooperative Societies Law (Agriculture Cooperatives)',
        'year': 'State-wise',
        'judicial_number': 'State Act number (varies)',
        'category': 'Cooperative credit, procurement and collective farming',
        'status': 'In force (state specific)',
    },
    {
        'title_template': '{state} Insecticide Dealer Licensing and Control Rules',
        'year': 'State-wise',
        'judicial_number': 'State rule/notification (varies)',
        'category': 'Pesticide retail licensing and compliance',
        'status': 'In force (state specific)',
    },
]


def _build_all_farmer_laws():
    all_laws = []
    for law in CENTRAL_FARMER_LAWS:
        law_item = dict(law)
        law_item['scope'] = 'Central'
        law_item['states'] = ['All India']
        all_laws.append(law_item)

    for state_name in INDIA_STATES_AND_UTS:
        for template in STATE_SPECIFIC_LAW_TEMPLATES:
            all_laws.append(
                {
                    'title': template['title_template'].format(state=state_name),
                    'year': template['year'],
                    'judicial_number': template['judicial_number'],
                    'category': template['category'],
                    'status': template['status'],
                    'scope': 'State',
                    'states': [state_name],
                }
            )

    return all_laws


ALL_FARMER_LAWS = _build_all_farmer_laws()


def _build_law_reference_url(title, judicial_number):
    query = quote_plus(f'{title} {judicial_number} India law text')
    return f'https://www.google.com/search?q={query}'


def _format_decimal(value):
    if value is None:
        return ''
    text_value = format(value, 'f').rstrip('0').rstrip('.')
    return text_value or '0'


def _parse_date(value):
    if not value:
        return None
    return datetime.strptime(value, '%Y-%m-%d').date()


def _parse_time(value):
    if not value:
        return None
    return datetime.strptime(value, '%H:%M').time()


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
    search_query = request.GET.get('q', '').strip()
    if search_query:
        UsageHistory.objects.create(user=request.user, activity=f"Searched: {search_query}")
    return render(request, 'accounts/home.html', {'display_name': display_name})


@login_required(login_url='login')
def agent_dummy_view(request):
    display_name = request.user.get_full_name().strip() or request.user.username
    UsageHistory.objects.create(user=request.user, activity='Opened Farmer (dummy placeholder)')
    return render(request, 'accounts/agent_dummy.html', {'display_name': display_name})


@login_required(login_url='login')
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('home')


@login_required(login_url='login')
def history_view(request):
    display_name = request.user.get_full_name().strip() or request.user.username
    history_entries = request.user.usage_entries.all()[:100]
    return render(
        request,
        'accounts/history.html',
        {
            'display_name': display_name,
            'history_entries': history_entries,
        },
    )


@login_required(login_url='login')
def farmer_laws_view(request):
    display_name = request.user.get_full_name().strip() or request.user.username
    selected_state = request.GET.get('state', '').strip()
    valid_states = set(INDIA_STATES_AND_UTS)
    if selected_state and selected_state not in valid_states:
        selected_state = ''

    laws_with_links = []
    for law in ALL_FARMER_LAWS:
        law_item = dict(law)
        law_item['reference_url'] = _build_law_reference_url(law['title'], law['judicial_number'])
        laws_with_links.append(law_item)

    UsageHistory.objects.create(user=request.user, activity='Opened farmer laws reference')
    return render(
        request,
        'accounts/laws.html',
        {
            'display_name': display_name,
            'laws': laws_with_links,
            'states': INDIA_STATES_AND_UTS,
            'selected_state': selected_state,
        },
    )


@login_required(login_url='login')
def profile_view(request):
    error = None
    success = None
    full_name = request.user.get_full_name().strip()
    if not full_name:
        full_name = request.user.username
    address = request.user.address
    land_survey_numbers = request.user.land_survey_numbers
    soil_type = request.user.soil_type
    current_season = request.user.current_season
    land_area_acres = _format_decimal(request.user.land_area_acres)
    farmer_type = request.user.farmer_type
    current_crop = request.user.current_crop
    plantation_date = request.user.plantation_date.isoformat() if request.user.plantation_date else ''
    crop_end_time = request.user.crop_end_time.strftime('%H:%M') if request.user.crop_end_time else ''

    if request.method == 'POST':
        submitted_name = request.POST.get('full_name', '').strip()
        submitted_address = request.POST.get('address', '').strip()
        submitted_land_survey_numbers = request.POST.get('land_survey_numbers', '').strip()
        submitted_land_area_acres = request.POST.get('land_area_acres', '').strip()
        submitted_soil_type = request.POST.get('soil_type', '').strip()
        submitted_current_season = request.POST.get('current_season', '').strip()
        submitted_farmer_type = request.POST.get('farmer_type', '').strip()
        submitted_current_crop = request.POST.get('current_crop', '').strip()
        submitted_plantation_date = request.POST.get('plantation_date', '').strip()
        submitted_crop_end_time = request.POST.get('crop_end_time', '').strip()
        uploaded_image = request.FILES.get('profile_image')
        uploaded_passbook_image = request.FILES.get('passbook_image')
        fields_to_update = []
        parsed_land_area = None
        parsed_plantation_date = None
        parsed_crop_end_time = None

        full_name = submitted_name or full_name
        address = submitted_address
        land_survey_numbers = submitted_land_survey_numbers
        soil_type = submitted_soil_type
        current_season = submitted_current_season
        land_area_acres = submitted_land_area_acres
        farmer_type = submitted_farmer_type
        current_crop = submitted_current_crop
        plantation_date = submitted_plantation_date
        crop_end_time = submitted_crop_end_time

        if submitted_current_season not in {option[0] for option in SEASON_OPTIONS}:
            error = 'Please select a valid current season.'
        elif submitted_land_area_acres:
            try:
                parsed_land_area = Decimal(submitted_land_area_acres)
                if parsed_land_area < 0:
                    error = 'Land area cannot be negative.'
            except InvalidOperation:
                error = 'Please enter a valid number for land area in acres.'

        if not error and submitted_plantation_date:
            try:
                parsed_plantation_date = _parse_date(submitted_plantation_date)
            except ValueError:
                error = 'Please enter a valid plantation date.'

        if not error and submitted_crop_end_time:
            try:
                parsed_crop_end_time = _parse_time(submitted_crop_end_time)
            except ValueError:
                error = 'Please enter a valid crop end time.'

        if not error and submitted_name:
            name_parts = submitted_name.split(maxsplit=1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            if request.user.first_name != first_name:
                request.user.first_name = first_name
                fields_to_update.append('first_name')
            if request.user.last_name != last_name:
                request.user.last_name = last_name
                fields_to_update.append('last_name')

        if not error:
            if request.user.address != submitted_address:
                request.user.address = submitted_address
                fields_to_update.append('address')
            if request.user.land_survey_numbers != submitted_land_survey_numbers:
                request.user.land_survey_numbers = submitted_land_survey_numbers
                fields_to_update.append('land_survey_numbers')
            if request.user.soil_type != submitted_soil_type:
                request.user.soil_type = submitted_soil_type
                fields_to_update.append('soil_type')
            if request.user.current_season != submitted_current_season:
                request.user.current_season = submitted_current_season
                fields_to_update.append('current_season')
            if request.user.farmer_type != submitted_farmer_type:
                request.user.farmer_type = submitted_farmer_type
                fields_to_update.append('farmer_type')
            if request.user.current_crop != submitted_current_crop:
                request.user.current_crop = submitted_current_crop
                fields_to_update.append('current_crop')
            if submitted_plantation_date:
                if request.user.plantation_date != parsed_plantation_date:
                    request.user.plantation_date = parsed_plantation_date
                    fields_to_update.append('plantation_date')
            elif request.user.plantation_date is not None:
                request.user.plantation_date = None
                fields_to_update.append('plantation_date')
            if submitted_crop_end_time:
                if request.user.crop_end_time != parsed_crop_end_time:
                    request.user.crop_end_time = parsed_crop_end_time
                    fields_to_update.append('crop_end_time')
            elif request.user.crop_end_time is not None:
                request.user.crop_end_time = None
                fields_to_update.append('crop_end_time')
            if submitted_land_area_acres:
                if request.user.land_area_acres != parsed_land_area:
                    request.user.land_area_acres = parsed_land_area
                    fields_to_update.append('land_area_acres')
            elif request.user.land_area_acres is not None:
                request.user.land_area_acres = None
                fields_to_update.append('land_area_acres')

        if uploaded_image:
            request.user.profile_image = uploaded_image
            fields_to_update.append('profile_image')
        if uploaded_passbook_image:
            request.user.passbook_image = uploaded_passbook_image
            fields_to_update.append('passbook_image')

        if not error and not fields_to_update:
            error = 'Please update at least one profile field.'
        elif not error:
            request.user.save(update_fields=list(dict.fromkeys(fields_to_update)))
            UsageHistory.objects.create(user=request.user, activity='Updated profile settings')
            success = 'Profile updated successfully.'
            land_area_acres = _format_decimal(request.user.land_area_acres)

    display_name = request.user.get_full_name().strip() or request.user.username
    return render(
        request,
        'accounts/profile.html',
        {
            'error': error,
            'success': success,
            'full_name': full_name,
            'address': address,
            'land_survey_numbers': land_survey_numbers,
            'land_area_acres': land_area_acres,
            'soil_type': soil_type,
            'current_season': current_season,
            'farmer_type': farmer_type,
            'current_crop': current_crop,
            'plantation_date': plantation_date,
            'crop_end_time': crop_end_time,
            'season_options': SEASON_OPTIONS,
            'display_name': display_name,
        },
    )
