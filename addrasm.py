import telebot
from PIL import Image
import rembg
import io

# Bot tokenini kiriting
API_TOKEN = '6831795124:AAHnp5na6xY0HKkfYGWvbM9DHMKBa9KxIOw'


# Botni yaratish
bot = telebot.TeleBot(API_TOKEN)

# Start komandasi
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Rasm yuboring!")

# Rasm qabul qilganda
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Foydalanuvchi rasmini olish
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Rasmni ochish
    img = Image.open(io.BytesIO(downloaded_file))

    # Orqa fonni olib tashlash
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    input_img = img_bytes.read()

    output_img = rembg.remove(input_img)

    # PNG formatida qayta ochamiz
    img_no_bg = Image.open(io.BytesIO(output_img))

    # Orqa fonni #efefef rangga o'zgartiramiz va o'lchamini 1080x1440 qilamiz
    result_img = Image.new("RGBA", (1080, 1440), "#efefef")
    img_no_bg = img_no_bg.resize((1080, 1440), Image.Resampling.LANCZOS)
    result_img.paste(img_no_bg, (0, 0), img_no_bg)

    # Natijaviy rasmni JPG formatida saqlash
    output = io.BytesIO()
    result_img = result_img.convert("RGB")  # RGB formatga o'tkazish
    result_img.save(output, format='JPEG', quality=100)
    output.seek(0)

    # Tayyor rasmni qaytarib yuborish
    bot.send_photo(message.chat.id, output)

    # Yana yuborishingiz mumkinligini xabar qilish
    bot.send_message(message.chat.id, "Yana rasm yuborsangiz, yana tayyorlab beraman!")

# Botni ishga tushirish
bot.polling()
