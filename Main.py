import discord
import subprocess
import asyncio
import os
from discord.channel import DMChannel
from os.path import join

#config
jarName = "server.jar"#name of the jar file used to start the server (server.jar is the default but can be changed if you're using a mod launcher)
pathtojar = ""#path to the server.jar (currently not in use but in the futrue can be used if you want to manage multiple MC servers)
allocatedRamInMB = "4096" #sets the amount of ram allocated to the MC server in MB
commandSymbol = "$"#sets the symbol that needs to exist at the start of each bot command
startCommand = "$start"#sets the command for starting the MC server
stopCommand = "$stop"#sets the command for stopping the MC server
saveCommand = "$save" #sets the command for saving the word data
shutdownCommand = "$shutdown" #sets the command for shutting down the host machine
shutdownable = False #set to True if you want the bot to be able to shutdown the host machine
role="MC"#sets the role name that's able to execute bot commands("MC" by default)
############################


running = False
client = discord.Client()

def start():
    if running == False:
        global mc_subprocess
        mc_subprocess = subprocess.Popen(["powershell","java -Xmx"+allocatedRamInMB+"M -Xms"+allocatedRamInMB+"M -jar "+jarName+" nogui"], stdin=asyncio.subprocess.PIPE)

def save():
    if running == False:
        mc_subprocess.stdin.write(bytes('save-all' + '\n', 'utf-8'))
        mc_subprocess.stdin.flush()

def stop():
    if running == True:
        mc_subprocess.stdin.write(bytes('save-all' + '\n', 'utf-8'))
        mc_subprocess.stdin.flush()
        mc_subprocess.stdin.write(bytes('stop' + '\n', 'utf-8'))
        mc_subprocess.stdin.flush()

def shutdown():
    #by default this puts the pc in hibernation mode to allow for wake on lan without BIOS support
    #(change the /h to /s if your BIOS supports wake on lan or you don't care about waking the pc up again)
    if shutdownable == True:#a redundant check to see if shutting down is enabled (there is another check before we even call the function)
        os.system("shutdown.exe /h")


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
     
@client.event
async def on_message(message):
    global running
    if message.author == client.user:
        return

    elif message.content.startswith(commandSymbol):#skips checking the message content if the message doesn't start with the commandSymbol
        controlRole = discord.utils.get(message.author.guild.roles, name=role)
        if controlRole in message.author.roles:
            if message.content == startCommand:
                if running == False:
                    await message.channel.send('starting')
                    await message.channel.send('use $stop to stop the server')
                    if shutdownable == True:
                        await message.channel.send('use $shutdown to stop the server and shutdown')
                    start()
                    running = True
                else:
                    await message.channel.send('already running')
                    
            elif message.content == stopCommand:
                if running == True:
                    await message.channel.send('stoping')
                    stop()
                    running = False
                else:
                    await message.channel.send('server is not running')

            elif message.content == saveCommand:
                if running == True:
                    await message.channel.send('saving')
                    save()
                else:
                    await message.channel.send('server is not running')

            elif message.content == shutdownCommand:
                if shutdownable == True:
                    if running == True:
                        await message.channel.send('stoping and shutting down')
                        stop()
                        running = False
                        shutdown()
                    else:
                        await message.channel.send('shutting down')
                        shutdown()
                else:
                    await message.channel.send('the shutdown command is not enabled')
            else:
                return
    else:
        return
            
    
         
client.run('discord token')