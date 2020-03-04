# インストールした discord.py を読み込む
import discord, json, os, urllib, shutil
from requests_oauthlib import OAuth1Session
from config import discordpy_token , e_channel_id , e_archive_channel_id, consumer_key, consumer_secret, access_token, access_token_secret

# アクセストークン
TOKEN = discordpy_token

E_CHANNEL_ID = e_channel_id
E_ARCHIVE_CHANNEL_ID = e_archive_channel_id

CK = consumer_key
CS = consumer_secret
AT = access_token
ATS = access_token_secret

# twitterAPI認証
twitter = OAuth1Session(CK, CS, AT, ATS)

# 接続に必要なオブジェクトを生成
client = discord.Client()
location = "~/e-archive"
tmp_name = "/tmp"
dir_name = "/dir"

def dir_check():
    if not os.path.isdir(tmp_name):
        os.mkdir(tmp_name)
    count = 0
    while not os.path.isdir(tmp_name + dir_name + str(count)):
        dir_name = dir_name + str(count)
        os.mkdir(tmp_name + dir_name)
        count += 1

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    global image
    global image_number
    dir_check()
    image_number = 0
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    if message.channel.id == E_CHANNEL_ID:
        # リアクション:ii:をつける
        emoji = client.get_emoji(554315588453924874)
        await message.add_reaction(emoji)

        e_archive_channel = client.get_channel(E_ARCHIVE_CHANNEL_ID)
        if 'twitter.com' in message.content:
            tweetId = '1233407306781429760'
            url = 'https://api.twitter.com/1.1/statuses/show.json?id=' + tweetId
            req = twitter.get(url)
            if req.status_code == 200:
                result = json.loads(req.text)
                archiveText = result['user']['name'] + '\n' + '@' + result['user']['screen_name'] + '\n' + result['text'] + '\n' + result['created_at']
                media_list = result['extended_entities']['media']
                await e_archive_channel.send(archiveText)

                for media in media_list:
                    image = media['media_url']
                    filepath = tmp_name + dir_name + "/image_" + os.path.basename(image)
                    # 画像をダウンロード
                    with open(filepath, 'wb') as f:
                        img = urllib.request.urlopen(image).read()
                        f.write(img)
                        await e_archive_channel.send(filepath)
                        # 画像をdiscordに送信
                        # await client.send_file(E_CHANNEL_ID, 画像)
                shutil.rmtree(os.path.join(location, tmp_name))
            else:
                await message.channel.send('ツイート取得に失敗しました')

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)

