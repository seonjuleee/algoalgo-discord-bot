import discord
import os
import algoalgo_member

client = discord.Client()

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    # if this message is sent by bot itself, do nothing.
    if message.author == client.user:
        return
    
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    # adduser function
    if message.content.startswith('!adduser'):
        result = algoalgo_member.adduser(str(message.author), message.content)
        await message.channel.send(result)
    
    # have to add truncate table
    if message.content.startswith('!truncate'):
        result = algoalgo_member.truncate(message.content)
        await message.channel.send(result)
        

token = 'NzQ0MTE0NTUyMDczMDkzMTgy.Xzegrg.9a23S3NbIEyXGq5RHNmEdwxWwnw'
client.run(token)
# client.run(os.environ['discord-token'])