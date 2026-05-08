from io import BytesIO

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from app.utils.wmo import get_weather_data

WIDTH = 1080
HEIGHT = 1350



def is_night(weather):
    current_hour = int(weather.get('current', {}).get('time', '12:00').split('T')[-1].split(':')[0])
    return current_hour >= 18 or current_hour <= 5



def get_background_colors(weather_code: int, night: bool = False):
    if night:
        return ((20, 30, 60), (50, 70, 110))

    if weather_code in [0, 1]:
        return ((76, 163, 255), (140, 210, 255))

    if weather_code in [2, 3, 45, 48]:
        return ((90, 110, 140), (140, 160, 180))

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
        draw.ellipse((780, 170, 930, 320), fill=(245, 245, 220))
        draw.ellipse((830, 160, 950, 310), fill=(40, 60, 100))
        return

    if weather_code in [0, 1]:
        draw.ellipse((760, 170, 930, 340), fill=(255, 215, 80))
    elif weather_code in [2, 3, 45, 48]:
        draw.ellipse((730, 190, 920, 320), fill=(240, 240, 245))
        draw.ellipse((820, 160, 980, 300), fill=(225, 225, 235))
    else:
        draw.ellipse((730, 190, 920, 320), fill=(230, 230, 235))
        draw.ellipse((820, 160, 980, 300), fill=(210, 210, 225))

        for x in [780, 840, 900]:
            draw.line((x, 330, x - 20, 390), fill=(180, 220, 255), width=10)



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

    image = image.filter(ImageFilter.GaussianBlur(1.2))

    draw = ImageDraw.Draw(image, 'RGBA')

    draw.rounded_rectangle((40, 40, WIDTH - 40, HEIGHT - 40), radius=55, fill=(255, 255, 255, 28))

    draw_weather_icon(draw, weather_code, night)

    title_font = load_font(54)
    temp_font = load_font(250)
    body_font = load_font(42)
    small_font = load_font(34)

    draw.text((80, 90), location['name'], fill='white', font=title_font)

    draw.text((80, 220), f"{round(current['temperature_2m'])}°", fill='white', font=temp_font)

    draw.text((90, 520), weather_text, fill='white', font=body_font)

    draw.text((90, 590), f"Sensação {round(current['apparent_temperature'])}°", fill=(240, 240, 240), font=small_font)

    panel_y = 760

    draw.rounded_rectangle((60, panel_y, WIDTH - 60, panel_y + 220), radius=40, fill=(255, 255, 255, 35))

    sections = [
        ('Mínima', f"{round(daily['temperature_2m_min'][0])}°", 120),
        ('Máxima', f"{round(daily['temperature_2m_max'][0])}°", 430),
        ('Chuva', f"{daily['precipitation_probability_max'][0]}%", 760),
    ]

    for title, value, x in sections:
        draw.text((x, panel_y + 45), title, fill=(240, 240, 240), font=small_font)
        draw.text((x, panel_y + 105), value, fill='white', font=body_font)

    mini_days = ['Hoje', 'Amanhã', '3° dia']

    mini_y = 1080

    draw.rounded_rectangle((60, mini_y, WIDTH - 60, mini_y + 170), radius=35, fill=(255, 255, 255, 25))

    for index, label in enumerate(mini_days):
        x = 120 + (index * 300)

        draw.text((x, mini_y + 30), label, fill=(240, 240, 240), font=small_font)
        draw.text((x, mini_y + 90), f"{round(daily['temperature_2m_max'][index])}°", fill='white', font=body_font)

    output = BytesIO()

    image.save(output, format='PNG', optimize=True)

    output.seek(0)

    return output
