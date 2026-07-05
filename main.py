import discord
from discord.ext import commands
from discord import app_commands
import os
import random
from keep_alive import keep_alive

# インテント設定
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# --- 29番目のコマンド：認証パネル（ロール選択システム）の実装 ---

class RoleSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # 永続的なパネルにする

    @discord.ui.select(
        placeholder="あなたの回線タイプを選んで認証してください",
        options=[
            discord.SelectOption(label="爆速回線民", value="1523194083378598051", description="光回線などの高速な方"),
            discord.SelectOption(label="一般回線民", value="1523193819183583353", description="標準的な回線の方"),
            discord.SelectOption(label="低速回線民", value="1523193624739844246", description="ADSLやモバイル回線の方")
        ],
        custom_id="verify_role_select"
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        role_id = int(select.values[0])
        role = interaction.guild.get_role(role_id)
        
        if role:
            # 既に持っている他の認証用ロールを外す処理（必要なら）
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ {role.name} として認証されました！ゆっくりしていってね！", ephemeral=True)
        else:
            await interaction.response.send_message("❌ ロールが見つかりません。管理者に連絡してください。", ephemeral=True)

@bot.command()
@commands.has_permissions(administrator=True)
async def ninsyo(ctx):
    """29. 認証パネルを表示するコマンド"""
    embed = discord.Embed(
        title="ゆっくり回線鯖 認証パネル",
        description="下のメニューから自分の回線環境に近いものを選んでください。\n選択すると自動的にロールが付与され、チャンネルが解放されます。",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=RoleSelectView())

# --- 残り28個のコマンド ---

@bot.event
async def on_ready():
    print(f'ログイン: {bot.user.name}')
    # 起動時にViewを再登録（ボタンやセレクトメニューを有効化し続けるため）
    bot.add_view(RoleSelectView())

@bot.command()
async def ping(ctx): await ctx.send(f'🏓 Pong! {round(bot.latency * 1000)}ms') # 1

@bot.command()
async def hello(ctx): await ctx.send(f'こんにちは {ctx.author.name} さん！') # 2

@bot.command()
async def yukkuri(ctx): await ctx.send('ゆっくりしていってね！！！') # 3

@bot.command()
async def kaisen(ctx): # 4
    s = random.randint(1, 1000)
    await ctx.send(f'📶 {ctx.author.name}の回線速度: {s}Mbps (理論値)')

@bot.command()
async def serverinfo(ctx): # 5
    await ctx.send(f'サーバー名: {ctx.guild.name}\n人数: {ctx.guild.member_count}')

@bot.command()
async def userinfo(ctx, m: discord.Member = None): # 6
    m = m or ctx.author
    await ctx.send(f'名前: {m.name}\nID: {m.id}')

@bot.command()
async def avatar(ctx, m: discord.Member = None): # 7
    m = m or ctx.author
    await ctx.send(m.display_avatar.url)

@bot.command()
async def dice(ctx): await ctx.send(f'🎲 {random.randint(1,6)}') # 8

@bot.command()
async def coin(ctx): await ctx.send(f'🪙 {random.choice(["表", "裏"])}') # 9

@bot.command()
async def omikuji(ctx): # 10
    await ctx.send(f'⛩️ {random.choice(["大吉", "中吉", "小吉", "末吉", "凶"])}')

@bot.command()
async def rules(ctx): await ctx.send('📜 ルール：荒らさない、煽らない、ゆっくりする！') # 11

@bot.command()
async def invite(ctx): await ctx.send('🔗 招待リンク作成中...') # 12

@bot.command()
async def say(ctx, *, t): # 13
    await ctx.message.delete()
    await ctx.send(t)

@bot.command()
async def choose(ctx, *o): await ctx.send(f'🤔 {random.choice(o)}') # 14

@bot.command()
async def math(ctx, a:int, op, b:int): # 15
    if op=='+': await ctx.send(a+b)
    elif op=='-': await ctx.send(a-b)
    else: await ctx.send('未対応')

@bot.command()
async def botinfo(ctx): await ctx.send('🤖 ゆっくり回線鯖専属。Render産') # 16

@bot.command()
async def weather(ctx): await ctx.send(f'☁️ 天気: {random.choice(["快晴", "曇り", "回線雨"])}') # 17

@bot.command()
async def joke(ctx): await ctx.send('布団が吹っ飛んだ！') # 18

@bot.command()
async def pat(ctx, m:discord.Member): await ctx.send(f'✋ {m.name}をなでなでした。') # 19

@bot.command()
async def hug(ctx, m:discord.Member): await ctx.send(f'🫂 {m.name}をハグした。') # 20

@bot.command()
async def praise(ctx): await ctx.send('あなたは最高！素晴らしい回線だ！') # 21

@bot.command()
async def scold(ctx): await ctx.send('こらー！回線を大切にしなさい！') # 22

@bot.command()
async def status(ctx): await ctx.send('🟢 正常稼働中。') # 23

@bot.command()
async def version(ctx): await ctx.send('v2.0 (認証機能付き)') # 24

@bot.command()
async def echo(ctx, *, t): await ctx.send(t) # 25

@bot.command()
async def member(ctx): await ctx.send(f'現在 {ctx.guild.member_count} 人がゆっくりしています。') # 26

@bot.command()
async def bye(ctx): await ctx.send('またゆっくりしに来てね！') # 27

@bot.command()
async def help_me(ctx): # 28
    await ctx.send('!ninsyo(管理者用), !ping, !hello, !yukkuri, !kaisen, !serverinfo, !userinfo, !avatar, !dice, !coin, !omikuji, !rules, !invite, !say, !choose, !math, !botinfo, !weather, !joke, !pat, !hug, !praise, !scold, !status, !version, !echo, !member, !bye')

# サーバー起動
keep_alive()
# 起動
bot.run(os.getenv('DISCORD_TOKEN'))
