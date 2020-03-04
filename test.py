# インストールした discord.py を読み込む
import discord, json
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

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    # tweetId = '1231419383605420032'
    tweetId = '1233423662415351809'
    url = 'https://api.twitter.com/1.1/statuses/show.json?id=' + tweetId
    req = twitter.get(url)
    if req.status_code == 200:
        result = json.loads(req.text)
        print('icon url\n\n')
        print(result['user']['profile_image_url_https'])
        print('media\n\n')
        print(result['entities']['media'][0])

    

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

        e_archive_channel = client.get_channel(E_ARCHIVE_CHANNEL_ID)
        if 'twitter.com' in message.content:
            tweetId = '1231419383605420032'
            url = 'https://api.twitter.com/1.1/statuses/show.json?id=' + tweetId
            req = twitter.get(url)
            if req.status_code == 200:
                result = json.loads(req.text)
                archiveText = result['user']['name'] + '\n' + '@' + result['user']['screen_name'] + '\n' + result['text'] + '\n' + result['created_at']
                await e_archive_channel.send(archiveText)
            else:
                await message.channel.send('ツイート取得に失敗しました')

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)

