from io import BytesIO

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from app.utils.wmo import get_weather_data

WIDTH = 1080
HEIGHT = 1350



def get_background_colors(weather_code: int):
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



def render_weather_card(location, weather):
    current = weather['current']
    daily = weather['daily']

    weather_code = current['weather_code']

    _, weather_text = get_weather_data(weather_code)

    color1, color2 = get_background_colors(weather_code)

    image = Image.new('RGB', (WIDTH, HEIGHT), color1)

    draw = ImageDraw.Draw(image)

    draw_gradient(draw, color1, color2)

    image = image.filter(ImageFilter.GaussianBlur(1.2))

    draw = ImageDraw.Draw(image, 'RGBA')

    draw.rounded_rectangle(
        (40, 40, WIDTH - 40, HEIGHT - 40),
        radius=55,
        fill=(255, 255, 255, 28),
    )

    title_font = load_font(54)
    temp_font = load_font(250)
    body_font = load_font(42)
    small_font = load_font(34)

    draw.text(
        (80, 90),
        location['name'],
        fill='white',
        font=title_font,
    )

    draw.text(
        (80, 220),
        f"{round(current['temperature_2m'])}°",
        fill='white',
        font=temp_font,
    )

    draw.text(
        (90, 520),
        weather_text,
        fill='white',
        font=body_font,
    )

    draw.text(
        (90, 590),
        f"Sensação {round(current['apparent_temperature'])}°",
        fill=(240, 240, 240),
        font=small_font,
    )

    panel_y = 760

    draw.rounded_rectangle(
        (60, panel_y, WIDTH - 60, panel_y + 220),
        radius=40,
        fill=(255, 255, 255, 35),
    )

    draw.text(
        (120, panel_y + 45),
        'Mínima',
        fill=(240, 240, 240),
        font=small_font,
    )

    draw.text(
        (120, panel_y + 105),
        f"{round(daily['temperature_2m_min'][0])}°",
        fill='white',
        font=body_font,
    )

    draw.text(
        (430, panel_y + 45),
        'Máxima',
        fill=(240, 240, 240),
        font=small_font,
    )

    draw.text(
        (430, panel_y + 105),
        f"{round(daily['temperature_2m_max'][0])}°",
        fill='white',
        font=body_font,
    )

    draw.text(
        (760, panel_y + 45),
        'Chuva',
        fill=(240, 240, 240),
        font=small_font,
    )

    draw.text(
        (760, panel_y + 105),
        f"{daily['precipitation_probability_max'][0]}%",
        fill='white',
        font=body_font,
    )

    output = BytesIO()

    image.save(output, format='PNG', optimize=True)

    output.seek(0)

    return output
