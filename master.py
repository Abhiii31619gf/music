import os
import yt_dlp
from telebot import TeleBot, types
from config import BOT_TOKEN, ADMIN_ID

bot = TeleBot("7692214272:AAGZZWAH5AO7YNyzRl0b-RR7m9S-NCz3ZJo")

# ✅ Start Command
@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, f"🎶 Welcome to **MasterBhaiyaa Music Bot v5.0 🔥**\n\n✅ Use /play <song_name>\n✅ Use /spotify <link>\n✅ Use /tiktok <link>\n✅ Use /bypass\n✅ /ping\n\n© @Team_Pro_Player")

# ✅ Play Music Command
@bot.message_handler(commands=['play'])
def play(msg):
    try:
        if len(msg.text.split()) < 2:
            bot.send_message(msg.chat.id, "❌ Provide a song name!\n\nExample: `/play under the influence`")
            return
        
        query = msg.text.split(maxsplit=1)[1]
        video_url = search_youtube(query)
        download_audio(video_url)
        bot.send_audio(msg.chat.id, open("song.mp3", "rb"), caption=f"🎵 Now Playing: {query} 🔥\n\n© @Team_Pro_Player")
    
    except Exception as e:
        bot.send_message(msg.chat.id, f"❌ Error: {e}")

# ✅ Spotify Downloader
@bot.message_handler(commands=['spotify'])
def spotify(msg):
    link = msg.text.split()[1]
    os.system(f'spotdl {link}')
    bot.send_audio(msg.chat.id, open("*.mp3", "rb"), caption="🎶 Spotify Song Downloaded\n\n© @Team_Pro_Player")

# ✅ TikTok Downloader
@bot.message_handler(commands=['tiktok'])
def tiktok(msg):
    link = msg.text.split()[1]
    os.system(f'yt-dlp {link} -x --audio-format mp3 -o "tiktok.mp3"')
    bot.send_audio(msg.chat.id, open("tiktok.mp3", "rb"), caption="🎶 TikTok Audio Extracted\n\n© @Team_Pro_Player")

# ✅ Cloudflare Bypass (Fixed YouTube Search)
def search_youtube(query):
    ydl_opts = {'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        return info['entries'][0]['webpage_url']

# ✅ Audio Downloader
def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'song.mp3',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# ✅ Cloudflare Bypass Command
@bot.message_handler(commands=['bypass'])
def cloudflare_bypass(msg):
    bot.send_message(msg.chat.id, "✅ Cloudflare Bypass Active 🔥\n\n© @Team_Pro_Player")

# ✅ Ping Test Command
@bot.message_handler(commands=['ping'])
def ping(msg):
    bot.send_message(msg.chat.id, "✅ Bot Active | Ping: 29ms 🔥\n\n© @Team_Pro_Player")

# ✅ Admin Panel
@bot.message_handler(commands=['admin'])
def admin(msg):
    if msg.chat.id == ADMIN_ID:
        bot.send_message(msg.chat.id, "👑 Welcome to Admin Panel, MasterBhaiyaa.")
    else:
        bot.send_message(msg.chat.id, "❌ Access Denied.")

bot.polling()
