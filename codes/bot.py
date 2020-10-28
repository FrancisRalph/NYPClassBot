import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('NzcxMDAyMjkzMzk4OTI5NDA4.X5lx1w.1LVA9IsouULV4ZHCqEMtN8qo0LE')
