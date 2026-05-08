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

    draw.ellipse((760, 110, 930, 260), fill=(240, 240, 245))
    draw.ellipse((850, 90, 1000, 230), fill=(225, 225, 235))



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

    image = image.filter(ImageFilter.GaussianBlur(1.4))

    draw = ImageDraw.Draw(image, 'RGBA')

    draw.rounded_rectangle(
        (60, 60, WIDTH - 60, HEIGHT - 60),
        radius=42,
        fill=(255, 255, 255, 28),
        outline=(255, 255, 255, 45),
        width=2,
    )

    draw_weather_icon(draw, weather_code, night)

    title_font = load_font(52)
    temp_font = load_font(190)
    body_font = load_font(30)
    small_font = load_font(24)

    draw.text((95, 90), location['name'], fill='white', font=title_font)

    draw.text((85, 170), f"{round(current['temperature_2m'])}°", fill='white', font=temp_font)

    draw.text((100, 400), weather_text, fill='white', font=body_font)

    draw.text(
        (100, 455),
        f"Sensação {round(current['apparent_temperature'])}°",
        fill=(225, 225, 235),
        font=small_font,
    )

    metrics = [
        ('14 km/h', 760),
        ('76%', 900),
        ('2%', 1040),
    ]

    metrics_icons = ['〰', '◖', '☂']

    for index, (value, x) in enumerate(metrics):
        draw.text((x - 20, 390), metrics_icons[index], fill=(235,235,245), font=body_font)
        draw.text((x - 35, 455), value, fill='white', font=body_font)

    divider_color = (255, 255, 255, 50)

    draw.line((60, 520, WIDTH - 60, 520), fill=divider_color, width=2)

    section_width = (WIDTH - 120) / 5

    bottom_items = [
        ('Mínima', f"{round(daily['temperature_2m_min'][0])}°"),
        ('Máxima', f"{round(daily['temperature_2m_max'][0])}°"),
        ('Hoje', f"{round(daily['temperature_2m_max'][0])}°"),
        ('Amanhã', f"{round(daily['temperature_2m_max'][1])}°"),
        ('3° dia', f"{round(daily['temperature_2m_max'][2])}°"),
    ]

    for index, (label, value) in enumerate(bottom_items):
        x = 60 + (section_width * index)
        center_x = x + (section_width / 2)

        if index > 0:
            draw.line(
                (x, 555, x, 660),
                fill=divider_color,
                width=2,
            )

        draw.text(
            (center_x - 55, 565),
            label,
            fill=(220, 220, 235),
            font=small_font,
        )

        draw.text(
            (center_x - 45, 625),
            value,
            fill='white',
            font=body_font,
        )

    output = BytesIO()

    image.save(output, format='PNG', optimize=True)

    output.seek(0)

    return output
