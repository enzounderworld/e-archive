# インストールした discord.py を読み込む
import discord
import json
import re
import os
import shutil
import urllib
import datetime


from requests_oauthlib import OAuth1Session
from config import DISCORDPY_TOKEN , E_CHANNEL_ID , E_ARCHIVE_CHANNEL_ID, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, MEDIA_DIR

# twitterAPI認証
twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# 接続に必要なオブジェクトを生成
client = discord.Client()

def dir_check():
    if not os.path.isdir(MEDIA_DIR):
        os.mkdir(MEDIA_DIR)


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    if message.channel.id == E_CHANNEL_ID:
        # リアクション:ii:をつける
        emoji = client.get_emoji(554315588453924874)
        await message.add_reaction(emoji)

        msg = message.content
        attachments = message.attachments
    
        e_archive_channel = client.get_channel(E_ARCHIVE_CHANNEL_ID)
        if 'twitter.com' in msg:

            pattern = '/status/'
            split_list = re.split(pattern, msg)
            tweetId = re.search(r'\d+', split_list[1]).group()

            url = 'https://api.twitter.com/1.1/statuses/show.json?id=' + tweetId
            req = twitter.get(url)
            if req.status_code == 200:
                result = json.loads(req.text)
                archiveText = result['user']['name'] + '\n' + '@' + result['user']['screen_name'] + '\n' + result['text'] + '\n' + result['created_at']
                await e_archive_channel.send(archiveText)

                media_list = result['extended_entities']['media']
                dir_check()

                for media in media_list:
                    image = media['media_url']
                    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                    filepath = MEDIA_DIR + r"\image_" + timestamp + '.jpg'
                    # 画像をダウンロード
                    with open(filepath, 'wb') as f:
                        img = urllib.request.urlopen(image).read()
                        f.write(img)
                        # 画像をdiscordに送信
                        await e_archive_channel.send(file=discord.File(filepath))

            else:
                await message.channel.send('ツイート取得に失敗しました')
    
        #画像の直貼りの場合
        if attachments:
            for attachment in attachments:
                file_attachment = await attachment.to_file()
                await e_archive_channel.send(file=file_attachment)

# Botの起動とDiscordサーバーへの接続
client.run(DISCORDPY_TOKEN)

