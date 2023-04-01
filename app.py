from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello"

import threading

threading.Thread(target=lambda: app.run(port=10000)).start()

import discord
import aiohttp
from io import BytesIO

client = discord.Client()
TOKEN = 'your_token_here'

@client.event
async def on_ready():
    print(f'{client.user}がログインしました')

@client.event
async def on_message(message):
    if message.content.startswith('/images '):
        url = message.content.split()[1]
        if 'http' not in url:
            await message.channel.send('URLが無効です')
            return

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if 'image' not in response.headers.get('content-type'):
                    await message.channel.send('指定されたURLには画像がありません')
                    return

                try:
                    image_data = await response.read()
                    image = BytesIO(image_data)
                    await message.channel.send(file=discord.File(image, 'image.png'))
                except OSError:
                    await message.channel.send('画像のフォーマットが正しくありません')
                except discord.errors.HTTPException:
                    await message.channel.send('送信する画像が大きすぎます')
                except Exception as e:
                    await message.channel.send(f'エラーが発生しました: {e}')

client.run(TOKEN)
