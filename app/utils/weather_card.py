from io import BytesIO

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from app.utils.wmo import get_weather_data

WIDTH = 1080
HEIGHT = 720



def is_night(weather):
    current_hour = int(weather.get('current', {}).get('time', '12:00').split('T')[-1].split(':')[0])
    return current_hour >= 18 or current_hour <= 5



def get_background_colors(weather_code: int, night: bool = False):
    if night:
        return ((14, 24, 58), (60, 78, 120))

    if weather_code in [0, 1]:
        return ((76, 163, 255), (140, 210, 255))

    if weather_code in [2, 3, 45, 48]:
        return ((72, 88, 124), (104, 122, 160))

    if weather_code in [61, 63, 65, 80, 81, 82]:
        return ((50, 80, 140), (90, 120, 180))

    if weather_code == 95:
        return ((55, 45, 90), (100, 90, 140))

    return ((76, 163, 255), (140, 210, 255))



def load_font(size: int):
    try:
        return ImageFont.truetype("assets/fonts/Inter-Regular.ttf", size)
    except Exception:
        return ImageFont.load_default()



def draw_gradient(draw, color1, color2):
    for y in range(HEIGHT):
        ratio = y / HEIGHT

        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)

        draw.line((0, y, WIDTH, y), fill=(r, g, b))



def draw_weather_icon(draw, weather_code: int, night: bool):
    if night:
        draw.ellipse((760, 90, 900, 230), fill=(245, 245, 220))
        draw.ellipse((810, 80, 930, 220), fill=(40, 60, 100))
        return

    if weather_code in [0, 1]:
        draw.ellipse((760, 90, 920, 250), fill=(255, 215, 80))
    else:
        draw.ellipse((740, 110, 900, 220), fill=(240, 240, 245))
        draw.ellipse((810, 90, 960, 210), fill=(225, 225, 235))



def render_weather_card(location, weather):
    current = weather['current']
    daily = weather['daily']

    weather_code = current['weather_code']

    _, weather_text = get_weather_data(weather_code)

    night = is_night(weather)

    color1, color2 = get_background_colors(weather_code, night)

    image = Image.new('RGB', (WIDTH, HEIGHT), color1)

    draw = ImageDraw.Draw(image)

    draw_gradient(draw, color1, color2)

    image = image.filter(ImageFilter.GaussianBlur(1.6))

    draw = ImageDraw.Draw(image, 'RGBA')

    draw.rounded_rectangle((60, 60, WIDTH - 60, HEIGHT - 60), radius=42, fill=(255, 255, 255, 30), outline=(255,255,255,40), width=2)

    draw_weather_icon(draw, weather_code, night)

    title_font = load_font(46)
    temp_font = load_font(170)
    body_font = load_font(34)
    small_font = load_font(28)

    draw.text((100, 95), location['name'], fill='white', font=title_font)
    draw.text((100, 180), f"{round(current['temperature_2m'])}°", fill='white', font=temp_font)
    draw.text((110, 390), weather_text, fill='white', font=body_font)
    draw.text((110, 445), f"Sensação {round(current['apparent_temperature'])}°", fill=(235, 235, 235), font=small_font)

    metrics_y = 520

    metrics = [
        ('Mínima', f"{round(daily['temperature_2m_min'][0])}°", 120),
        ('Máxima', f"{round(daily['temperature_2m_max'][0])}°", 420),
        ('Chuva', f"{daily['precipitation_probability_max'][0]}%", 720),
    ]

    for title, value, x in metrics:
        draw.text((x, metrics_y), title, fill=(220, 220, 235), font=small_font)
        draw.text((x, metrics_y + 48), value, fill='white', font=body_font)

    divider_color = (255, 255, 255, 50)

    draw.line((360, 515, 360, 635), fill=divider_color, width=2)
    draw.line((660, 515, 660, 635), fill=divider_color, width=2)

    mini_days = ['Hoje', 'Amanhã', '3° dia']

    for index, label in enumerate(mini_days):
        x = 520 + (index * 160)

        draw.text((x, 520), label, fill=(220, 220, 235), font=small_font)
        draw.text((x, 575), f"{round(daily['temperature_2m_max'][index])}°", fill='white', font=body_font)

    output = BytesIO()

    image.save(output, format='PNG', optimize=True)

    output.seek(0)

    return output
