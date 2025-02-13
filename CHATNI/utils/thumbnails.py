import os, re, random, aiofiles, aiohttp, math
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from youtubesearchpython.__future__ import VideosSearch
from CHATNI import app
from config import YOUTUBE_IMG_URL

arial = ImageFont.truetype("CHATNI/assets/assets/font2.ttf", 30)
font = ImageFont.truetype("CHATNI/assets/assets/font.ttf", 30)
title_font = ImageFont.truetype("CHATNI/assets/assets/font3.ttf", 45)

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    return image.resize((newWidth, newHeight))

def truncate(text):
    words = text.split(" ")
    text1, text2 = "", ""
    for word in words:
        if len(text1) + len(word) < 30:
            text1 += " " + word
        elif len(text2) + len(word) < 30:
            text2 += " " + word
    return [text1.strip(), text2.strip()]

def crop_center_circle(img, output_size, border, crop_scale=1.5):
    half_width, half_height = img.size[0] / 2, img.size[1] / 2
    larger_size = int(output_size * crop_scale)
    img = img.crop((
        half_width - larger_size / 2,
        half_height - larger_size / 2,
        half_width + larger_size / 2,
        half_height + larger_size / 2
    ))
    img = img.resize((output_size - 2 * border, output_size - 2 * border))
    final_img = Image.new("RGBA", (output_size, output_size), "white")
    mask_main = Image.new("L", (output_size - 2 * border, output_size - 2 * border), 0)
    draw_main = ImageDraw.Draw(mask_main)
    draw_main.ellipse((0, 0, output_size - 2 * border, output_size - 2 * border), fill=255)
    final_img.paste(img, (border, border), mask_main)
    mask_border = Image.new("L", (output_size, output_size), 0)
    draw_border = ImageDraw.Draw(mask_border)
    draw_border.ellipse((border, border, output_size - border, output_size - border), fill=255)
    draw_border.ellipse((0, 0, output_size, output_size), outline="white", width=border)
    result = Image.composite(final_img, Image.new("RGBA", final_img.size, (0, 0, 0, 0)), mask_border)
    return result

async def get_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}_v4.png"):
        return f"cache/{videoid}_v4.png"
    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = await VideosSearch(url, limit=1).next()
        if not results or not results.get("result"):
            return YOUTUBE_IMG_URL
        result = results["result"][0]
    except Exception as e:
        print(f"Error fetching YouTube results: {e}")
        return YOUTUBE_IMG_URL
    title = re.sub("\W+", " ", result.get("title", "Unsupported Title")).title()
    duration = result.get("duration", "Unknown Mins")
    thumbnail = result.get("thumbnails", [{}])[0].get("url", "").split("?")[0] or YOUTUBE_IMG_URL
    views = result.get("viewCount", {}).get("short", "Unknown Views")
    channel = result.get("channel", {}).get("name", "Unknown Channel")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                async with aiofiles.open(f"cache/thumb{videoid}.png", mode="wb") as f:
                    await f.write(await resp.read())

    try:
        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(20))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)
        draw = ImageDraw.Draw(background)
        circle_thumbnail = crop_center_circle(youtube, 400, 20)
        circle_thumbnail = circle_thumbnail.resize((400, 400))
        background.paste(circle_thumbnail, (120, 160), circle_thumbnail) 
        title1 = truncate(title)
        draw.text((565, 180), title1[0], fill=(255, 255, 255), font=title_font)
        draw.text((565, 230), title1[1], fill=(255, 255, 255), font=title_font)
        draw.text((565, 320), f"{channel}  |  {views[:23]}", (255, 255, 255), font=arial)
        text_size = draw.textsize("TEAM PURVI BOTS   ", font=font)
        draw.text((1280 - text_size[0] - 10, 10), "TEAM PURVI BOTS   ", fill="yellow", font=font)
        line_length = 580
        red_length = int(line_length * 0.6)
        draw.line([(565, 380), (565 + red_length, 380)], fill="red", width=9)
        draw.line([(565 + red_length, 380), (565 + line_length, 380)], fill="white", width=8)
        draw.ellipse([565 + red_length - 10, 380 - 10, 565 + red_length + 10, 380 + 10], fill="red")
        draw.text((565, 400), "00:00", (255, 255, 255), font=arial)
        draw.text((1080, 400), duration, (255, 255, 255), font=arial)
        play_icons = Image.open("CHATNI/assets/assets/play_icons.png").resize((580, 62))
        background.paste(play_icons, (565, 450), play_icons)
        stroke_width = 15
        stroke_color = (255, 255, 255)
        stroke_image = Image.new("RGBA", (1280 + 2 * stroke_width, 720 + 2 * stroke_width), stroke_color)
        stroke_image.paste(background, (stroke_width, stroke_width))
        os.remove(f"cache/thumb{videoid}.png")
        stroke_image.save(f"cache/{videoid}_v4.png")
        return f"cache/{videoid}_v4.png"

    except Exception as e:
        print(f"Error processing thumbnail: {e}")
        return YOUTUBE_IMG_URL
