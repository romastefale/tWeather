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
        return ((10, 24, 60), (45, 70, 120))

    if weather_code in [0, 1]:
        return ((55, 120, 235), (100, 170, 255))

    if weather_code in [2, 3, 45, 48]:
        return ((60, 82, 132), (88, 110, 165))

    if weather_code in [61, 63, 65, 80, 81, 82]:
        return ((45, 78, 145), (70, 110, 180))

    return ((55, 120, 235), (100, 170, 255))



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



def draw_glow(draw):
    draw.ellipse(
        (620, -20, 1080, 430),
        fill=(255, 255, 255, 24),
    )



def draw_weather_icon(draw, night: bool):
    if night:
        draw.ellipse((760, 90, 900, 230), fill=(245, 245, 220))
        draw.ellipse((815, 80, 935, 220), fill=(30, 50, 95))
        return

    draw.ellipse((760, 120, 930, 270), fill=(248, 248, 252))
    draw.ellipse((855, 95, 1015, 245), fill=(232, 232, 240))



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

    image = image.filter(ImageFilter.GaussianBlur(1.1))

    overlay = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255, 0))

    overlay_draw = ImageDraw.Draw(overlay)

    draw_glow(overlay_draw)

    overlay_draw.rounded_rectangle(
        (60, 60, WIDTH - 60, HEIGHT - 60),
        radius=46,
        fill=(255, 255, 255, 18),
        outline=(255, 255, 255, 55),
        width=2,
    )

    overlay = overlay.filter(ImageFilter.GaussianBlur(7))

    image = Image.alpha_composite(
        image.convert('RGBA'),
        overlay,
    ).convert('RGB')

    draw = ImageDraw.Draw(image, 'RGBA')

    draw_weather_icon(draw, night)

    title_font = load_font(56)
    temp_font = load_font(205)
    body_font = load_font(34)
    small_font = load_font(24)

    draw.text((95, 82), location['name'], fill='white', font=title_font)

    draw.text((72, 150), f"{round(current['temperature_2m'])}°", fill='white', font=temp_font)

    draw.text((102, 392), weather_text, fill='white', font=body_font)

    draw.text(
        (102, 448),
        f"Sensação {round(current['apparent_temperature'])}°",
        fill=(220, 225, 235),
        font=small_font,
    )

    metrics = [
        ('Vento', f"{round(current['wind_speed_10m'])} km/h", 760),
        ('Umidade', f"{current['relative_humidity_2m']}%", 900),
        ('Chuva', f"{daily['precipitation_probability_max'][0]}%", 1040),
    ]

    divider_color = (255, 255, 255, 42)

    for index, (label, value, x) in enumerate(metrics):
        if index > 0:
            draw.line(
                (x - 70, 360, x - 70, 470),
                fill=divider_color,
                width=2,
            )

        draw.text(
            (x - 48, 360),
            label,
            fill=(220, 225, 235),
            font=small_font,
        )

        draw.text(
            (x - 60, 425),
            value,
            fill='white',
            font=body_font,
        )

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
                (x, 555, x, 655),
                fill=divider_color,
                width=2,
            )

        bbox_label = draw.textbbox((0, 0), label, font=small_font)
        bbox_value = draw.textbbox((0, 0), value, font=body_font)

        label_width = bbox_label[2] - bbox_label[0]
        value_width = bbox_value[2] - bbox_value[0]

        draw.text(
            (center_x - (label_width / 2), 565),
            label,
            fill=(220, 220, 235),
            font=small_font,
        )

        draw.text(
            (center_x - (value_width / 2), 625),
            value,
            fill='white',
            font=body_font,
        )

    output = BytesIO()

    image.save(output, format='PNG', optimize=True)

    output.seek(0)

    return output
