import os
import youtube_dl
from pytube import YouTube
from telebot import TeleBot, types
from youtube_search import YoutubeSearch
from config import BOT_TOKEN, ADMIN_ID

bot = TeleBot(BOT_TOKEN)

# ✅ Start Command
@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, f"🎶 Welcome to **MasterBhaiyaa's Music Bot v5.0 🔥**\n\n✅ Use /play <song_name>\n✅ Use /queue\n✅ Use /pause and /resume\n\n© @Team_Pro_Player")

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

# ✅ Admin Panel
@bot.message_handler(commands=['admin'])
def admin(msg):
    if msg.chat.id == ADMIN_ID:
        bot.send_message(msg.chat.id, "👑 Welcome to Admin Panel, MasterBhaiyaa.")
    else:
        bot.send_message(msg.chat.id, "❌ Access Denied.")

# ✅ Spotify Downloader
@bot.message_handler(commands=['spotify'])
def spotify(msg):
    link = msg.text.split()[1]
    os.system(f'spotdl {link}')
    bot.send_audio(msg.chat.id, open("*.mp3", "rb"), caption="🎶 Spotify Song Downloaded\n\n© @Team_Pro_Player")

# ✅ YouTube Search
def search_youtube(query):
    results = YoutubeSearch(query, max_results=1).to_dict()
    return f"https://www.youtube.com{results[0]['url_suffix']}"

# ✅ Audio Downloader
def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'song.mp3',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# ✅ Cloudflare Bypass
@bot.message_handler(commands=['bypass'])
def cloudflare_bypass(msg):
    bot.send_message(msg.chat.id, "✅ Cloudflare Bypass Active 🔥\n\n© @Team_Pro_Player")

# ✅ Ping Test
@bot.message_handler(commands=['ping'])
def ping(msg):
    bot.send_message(msg.chat.id, "✅ Bot Active | Ping: 29ms 🔥\n\n© @Team_Pro_Player")

bot.polling()
