# インストールした discord.py を読み込む
import discord

from config import discordpy_token , e_channel_id , e_archive_channel_id

# アクセストークン
TOKEN = discordpy_token

# 接続に必要なオブジェクトを生成
client = discord.Client()

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
    # 
    if message.channel.id == e_channel_id:
        # リアクション:ii:をつける
        emoji = client.get_emoji(554315588453924874)
        await message.add_reaction(emoji)

        if 'twitter.com' in message.content:
            e_archive_channel = client.get_channel(e_archive_channel_id)
            msg = ('twitter_良い',message.content)
            await e_archive_channel.send(msg)



# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)