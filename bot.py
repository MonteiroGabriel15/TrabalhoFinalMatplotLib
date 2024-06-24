import os
import discord
from discord.ext import commands
import matplotlib.pyplot as plt
import io
from collections import Counter

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')
@bot.command()
async def hello(ctx):
    await ctx.send('Olá! Como posso ajudar você hoje?')

@bot.command()
async def plot(ctx):
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Gráfico de exemplo')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    await ctx.send(file=discord.File(buf, 'plot.png'))

@bot.command()
async def bar(ctx, *args):
    if len(args) % 2 != 0:
        await ctx.send("Por favor, forneça pares de categorias e valores. Exemplo: !bar A 10 B 15 C 7")
        return

    categories = args[0::2]
    values = list(map(float, args[1::2]))

    plt.figure()
    plt.bar(categories, values, alpha=0.7)
    plt.title('Gráfico de Barras')
    plt.xlabel('Categorias')
    plt.ylabel('Valores')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    file = discord.File(buf, filename="bar_chart.png")
    await ctx.send(file=file)

@bot.command()
async def pie(ctx, *args):
    if len(args) % 2 != 0:
        await ctx.send("Por favor, forneça pares de categorias e valores. Exemplo: !pie A 10 B 15 C 7")
        return

    categories = args[0::2]
    values = list(map(float, args[1::2]))

    plt.figure()
    plt.pie(values, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Gráfico de Pizza')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    file = discord.File(buf, filename="pie_chart.png")
    await ctx.send(file=file)

@bot.command()
async def percentual_cargos(ctx):
    guild = ctx.guild
    roles = [role for member in guild.members for role in member.roles if role != guild.default_role]
    role_counts = Counter(roles)
    total_members = len(guild.members)

    if total_members == 0:
        await ctx.send("Não há membros no servidor.")
        return

    role_percentages = {role: (count / total_members) * 100 for role, count in role_counts.items()}

    plt.figure()
    labels = [role.name for role in role_percentages.keys()]
    sizes = [percentage for percentage in role_percentages.values()]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Porcentagem de Cargos')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    file = discord.File(buf, filename='role_percentage.png')
    await ctx.send(file=file)

@bot.command()
async def contar_mensagens(ctx):
    await ctx.send("Calculando o número de mensagens em cada canal. Isso pode levar algum tempo...")

    channel_message_counts = {}

    for channel in ctx.guild.text_channels:
        count = 0
        try:
            async for _ in channel.history(limit=None):
                count += 1
            channel_message_counts[channel.name] = count
        except Exception as e:
            await ctx.send(f"Não foi possível acessar o canal {channel.name}: {e}")

    sorted_channels = dict(sorted(channel_message_counts.items(), key=lambda item: item[1], reverse=True))

    plt.figure(figsize=(10, 8))
    plt.bar(sorted_channels.keys(), sorted_channels.values(), color='purple')
    plt.xlabel('Canais')
    plt.ylabel('Número de Mensagens')
    plt.title('Número de Mensagens em Cada Canal de Texto')
    plt.xticks(rotation=45, ha='right')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    await ctx.send(file=discord.File(buf, 'msg_count.png'))

@bot.command()
async def contar_dias(ctx):
    await ctx.send("Calculando o número de mensagens por dia da semana. Isso pode levar algum tempo...")

    days_of_week = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
    message_counts = Counter()

    for channel in ctx.guild.text_channels:
        try:
            async for message in channel.history(limit=None):
                message_day = message.created_at.weekday()
                message_counts[days_of_week[message_day]] += 1
        except Exception as e:
            await ctx.send(f"Não foi possível acessar o canal {channel.name}: {e}")

    sorted_counts = {day: message_counts[day] for day in days_of_week}

    plt.figure(figsize=(10, 6))
    plt.bar(sorted_counts.keys(), sorted_counts.values(), color='deepskyblue')
    plt.xlabel('Dias da Semana')
    plt.ylabel('Número de Mensagens')
    plt.title('Número de Mensagens por Dia da Semana')
    plt.xticks(rotation=45, ha='right')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    await ctx.send(file=discord.File(buf, 'msg_by_day.png'))

bot.run(TOKEN)
