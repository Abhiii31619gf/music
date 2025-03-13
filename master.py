import os
import youtube_dl
from pytube import YouTube
from telebot import TeleBot, types
from config import BOT_TOKEN, ADMIN_ID

bot = TeleBot(BOT_TOKEN)

# ✅ Start Command
@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, "🎶 Welcome to MasterBhaiyaa's Music Bot v4.0 🔥\n\n✅ Use /play <song_name> to play music.\n✅ Use /queue to view playlist.\n✅ Use /pause and /resume for voice chat stream.")

# ✅ Play Music Command
@bot.message_handler(commands=['play'])
def play(msg):
    query = msg.text.split(maxsplit=1)[1]
    video_url = search_youtube(query)
    download_audio(video_url)
    bot.send_audio(msg.chat.id, open("song.mp3", "rb"), caption=f"🎵 Now Playing: {query} 🔥\n\n© @MasterBhaiyaa")

# ✅ Admin Panel
@bot.message_handler(commands=['admin'])
def admin(msg):
    if msg.chat.id == ADMIN_ID:
        bot.send_message(msg.chat.id, "👑 Welcome to Admin Panel, MasterBhaiyaa.")
    else:
        bot.send_message(msg.chat.id, "❌ Access Denied.")

# ✅ YouTube Search
def search_youtube(query):
    from youtube_search import YoutubeSearch
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

bot.polling()