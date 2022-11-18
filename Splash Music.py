import discord
import os
import asyncio
import youtube_dl

token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
client = discord.Client()

voice_clients = {}

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"}


@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")



@client.event
async def on_message(msg):



    if msg.content.startswith("!play"):

        try:
            voice_client = await msg.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        
        except:
            print("error")

        try:
            url = msg.content.split()[1]


            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download = False))

            song = data['url']
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options, executable = "E:\\ffmpeg\\ffmpeg.exe")

            voice_clients[msg.guild.id].play(player)
           
        except Exception as err:
            print(err)

    if msg.content.startswith("!pause"):
        try:
            voice_clients[msg.guild.id].pause()
            await msg.channel.send(f"Player has been paused by {msg.author.display_name}")

        except Exception as err:
            print(err)


    if msg.content.startswith("!resume"):
            try:
                voice_clients[msg.guild.id].resume()
                await msg.channel.send(f"Player has been resumed by {msg.author.display_name}")

            except Exception as err:
                print(err)

    if msg.content.startswith("!repeat"):
            try:
                voice_clients[msg.guild.id].repeat()

            except Exception as err:
                print(err)

    if msg.content.startswith("!stop"):
            try:
                voice_clients[msg.guild.id].stop()
                await voice_clients[msg.guild.id].disconnect()
                await msg.channel.send(f"Player has been stopped by {msg.author.display_name}")

            except Exception as err:
                print(err)


    if msg.content.startswith("!leave"):
        try:
            voice_clients[msg.guild.id].stop()
            await voice_clients[msg.guild.id].disconnect()
            await msg.channel.send(f"{msg.author.display_name} kicked me :(")

        except Exception as err:
            print(err)

   
client.run(token)
