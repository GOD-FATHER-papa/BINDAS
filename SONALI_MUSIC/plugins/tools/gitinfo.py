# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

import asyncio, os, time, aiohttp, shutil, git
from SONALI_MUSIC import app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SONALI_MUSIC.misc import SUDOERS
from pyrogram import Client, filters
from concurrent.futures import ThreadPoolExecutor
import requests

executor = ThreadPoolExecutor(max_workers=3)


@app.on_message(filters.command(["github", "git"]))
async def github(_, message):
    if len(message.command) != 2:
        await message.reply_text("`/git TEAM-ISHA`")
        return

    username = message.text.split(None, 1)[1]
    URL = f'https://api.github.com/users/{username}'

    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await message.reply_text("404")

            result = await request.json()

            try:
                url = result['html_url']
                name = result['name']
                company = result['company']
                bio = result['bio']
                created_at = result['created_at']
                avatar_url = result['avatar_url']
                blog = result['blog']
                location = result['location']
                repositories = result['public_repos']
                followers = result['followers']
                following = result['following']

                caption = f"""ɢɪᴛʜᴜʙ ɪɴғᴏ ᴏғ {name}
                
✿ ᴜsᴇʀɴᴀᴍᴇ: {username}
✿ ʙɪᴏ : {bio}
✿ ʟɪɴᴋ : [ᴄʟɪᴄᴋ ʜᴇʀᴇ]({url})
✿ ᴄᴏᴍᴩᴀɴʏ : {company}
✿ ᴄʀᴇᴀᴛᴇᴅ ᴏɴ : {created_at}
✿ ʀᴇᴩᴏsɪᴛᴏʀɪᴇs : {repositories}
✿ ʙʟᴏɢ : {blog}
✿ ʟᴏᴄᴀᴛɪᴏɴ : {location}
✿ ғᴏʟʟᴏᴡᴇʀs : {followers}
✿ ғᴏʟʟᴏᴡɪɴɢ : {following}"""

            except Exception as e:
                print(str(e))
                pass


    close_button = InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")
    inline_keyboard = InlineKeyboardMarkup([[close_button]])

    await message.reply_photo(photo=avatar_url, caption=caption, reply_markup=inline_keyboard)



@app.on_message(filters.command(["downloadrepo", "dlrepo"]))
async def download_repo(_, message):
    if len(message.command) != 2:
        await message.reply_text("**⋟ ᴘʀᴏᴠɪᴅᴇ ɢɪᴛʜᴜʙ ʀᴇᴘᴏ ᴜʀʟ ᴀꜰᴛᴇʀ ᴄᴏᴍᴍᴀɴᴅ.**\n\n**ᴇxᴀᴍᴘʟᴇ :-** `/dlrepo Repo url`")
        return

    repo_url = message.command[1]
    status_msg = await message.reply_text("**⋟ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴀɴᴅ ᴢɪᴘᴘɪɴɢ ᴛʜᴇ ʀᴇᴘᴏꜱɪᴛᴏʀʏ, ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ...**")
    
    try:
        # Run the blocking operation in a separate thread
        loop = asyncio.get_event_loop()
        zip_path = await loop.run_in_executor(executor, download_and_zip_repo, repo_url)
        
        if zip_path and os.path.exists(zip_path):
            await message.reply_document(zip_path, caption=f"**⋟ ʀᴇᴘᴏꜱɪᴛᴏʀʏ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!**\n\n**ʟɪɴᴋ :-** `{repo_url}`")
            await status_msg.delete()
        else:
            await message.reply_text("**⋟ ᴜɴᴀʙʟᴇ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜᴇ ꜱᴘᴇᴄɪꜰɪᴇᴅ ɢɪᴛʜᴜʙ ʀᴇᴘᴏꜱɪᴛᴏʀʏ.**")
    except Exception as e:
        await message.reply_text(f"**⋟ ᴇʀʀᴏʀ: {e}**")
    finally:
        # Clean up
        if 'zip_path' in locals() and zip_path and os.path.exists(zip_path):
            os.remove(zip_path)

def download_and_zip_repo(repo_url):
    repo_path = ""
    try:
        
        if repo_url.endswith('.git'):
            repo_name = repo_url.split('/')[-1][:-4]
        else:
            repo_name = repo_url.split('/')[-1]
        
        repo_path = f"temp_{repo_name}"
        
        
        print(f"Cloning repository: {repo_url}")
        git.Repo.clone_from(repo_url, repo_path, depth=1)
        
        
        print(f"Creating zip archive for: {repo_path}")
        zip_filename = shutil.make_archive(repo_name, 'zip', repo_path)
        print(f"Zip created: {zip_filename}")
        
        return zip_filename
        
    except git.exc.GitCommandError as e:
        print(f"Git error: {e}")
        return None
    except Exception as e:
        print(f"Error downloading and zipping GitHub repository: {e}")
        return None
    finally:

        if repo_path and os.path.exists(repo_path):
            print(f"Cleaning up: {repo_path}")
            shutil.rmtree(repo_path, ignore_errors=True)



def chunk_string(text, chunk_size):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

@app.on_message(filters.command("allrepo"))
async def all_repo_command(client, message):
    try:
        
        if len(message.command) > 1:
            github_username = message.command[1]
            
            repo_info = get_all_repository_info(github_username)
            
            chunked_repo_info = chunk_string(repo_info, 4000)  
         
            for chunk in chunked_repo_info:
                await message.reply_text(chunk)
        else:
            await message.reply_text("**ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴀ ɢɪᴛʜᴜʙ ᴜsᴇʀɴᴀᴍᴇ ᴀғᴛᴇʀ ᴄᴏᴍᴍᴀɴᴅ.**")
    except Exception as e:
        await message.reply_text(f"**ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴜᴅ :-** {str(e)}")

def get_all_repository_info(github_username):
    github_api_url = f"https://api.github.com/users/{github_username}/repos"

    response = requests.get(github_api_url)
    data = response.json()

    repo_info = "\n\n".join([
        f"**ʀᴇᴘᴏsɪᴛᴏʀʏ :-** {repo['full_name']}\n"
        f"**ᴅᴇsᴄʀɪᴘᴛɪᴏɴ :-** {repo['description']}\n"
        f"**sᴛᴀʀs :-** {repo['stargazers_count']}\n"
        f"**ғᴏʀᴋs :-** {repo['forks_count']}\n"
        f"**ʀᴇᴘᴏ ᴜʀʟ :-** {repo['html_url']}"
        for repo in data
    ])

    return repo_info



@app.on_message(filters.command(["eco", "co"], prefixes=["/", "e", "E"]) & filters.reply & filters.user(list(SUDOERS)))
async def eco_reply(client: Client, message):

    if not message.reply_to_message:
        await message.reply("**⋟ ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.**")
        return
      
    command_parts = message.text.split(" ", 1)
    if len(command_parts) < 2:
        await message.reply("**⋟ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴍᴇssᴀɢᴇ ᴀғᴛᴇʀ** `/eco` **ᴄᴏᴍᴍᴀɴᴅ.**")
        return

    reply_text = command_parts[1]

    await message.delete()
    await message.reply_to_message.reply(reply_text)

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Sonali-MusicV2
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
