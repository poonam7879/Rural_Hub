from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('main/index.html')

@main.route('/about')
def about():
    return render_template('main/about.html')

@main.route('/mandi')
def mandi():
    # Mock data for Mandi prices
    prices = [
        {'crop': 'Wheat', 'variety': 'Lokwan', 'min_price': 2100, 'max_price': 2350, 'modal': 2200, 'market': 'Indore'},
        {'crop': 'Soyabean', 'variety': 'Yellow', 'min_price': 4500, 'max_price': 4800, 'modal': 4650, 'market': 'Ujjain'},
        {'crop': 'Maize', 'variety': 'Hybrid', 'min_price': 1800, 'max_price': 2100, 'modal': 1950, 'market': 'Ratlam'},
        {'crop': 'Mustard', 'variety': 'Black', 'min_price': 5200, 'max_price': 5500, 'modal': 5350, 'market': 'Neemuch'},
        {'crop': 'Cotton', 'variety': 'Medium Staple', 'min_price': 6800, 'max_price': 7200, 'modal': 7000, 'market': 'Khargone'}
    ]
    return render_template('main/mandi.html', prices=prices)

@main.route('/weather')
def weather():
    # Mock data for Weather
    forecast = [
        {'day': 'Today', 'temp_max': 32, 'temp_min': 22, 'condition': 'Sunny', 'icon': '☀️'},
        {'day': 'Tomorrow', 'temp_max': 33, 'temp_min': 23, 'condition': 'Partly Cloudy', 'icon': '⛅'},
        {'day': 'Wednesday', 'temp_max': 30, 'temp_min': 21, 'condition': 'Rain Showers', 'icon': '🌧️'},
        {'day': 'Thursday', 'temp_max': 28, 'temp_min': 20, 'condition': 'Thunderstorms', 'icon': '⛈️'},
        {'day': 'Friday', 'temp_max': 29, 'temp_min': 19, 'condition': 'Mostly Sunny', 'icon': '🌤️'}
    ]
    return render_template('main/weather.html', forecast=forecast)

@main.route('/forum')
def forum():
    # Mock data for Community Forum
    posts = [
        {'title': 'Best fertilizer for late-sown wheat?', 'author': 'Ramesh', 'replies': 12, 'time': '2 hours ago'},
        {'title': 'Tractor subsidy scheme details 2024', 'author': 'Suresh', 'replies': 45, 'time': '5 hours ago'},
        {'title': 'Anyone has spare water pump for a day?', 'author': 'Mukesh', 'replies': 3, 'time': '1 day ago'},
        {'title': 'New disease affecting tomato crops in our area', 'author': 'Dr. Sharma', 'replies': 28, 'time': '2 days ago'}
    ]
    return render_template('main/forum.html', posts=posts)
