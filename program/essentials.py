"""
Video + Music Stream Telegram Bot
Copyright (c) 2022-present levina=lab <https://github.com/levina-lab>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but without any warranty; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/licenses.html>
"""


import asyncio
import traceback

from pyrogram.types import Message
from pyrogram import Client, filters, __version__ as pyrover
from pytgcalls import (__version__ as pytgver)

from program import __version__ as ver
from program.start import __python_version__ as pyver

from driver.core import me_bot
from driver.filters import command
from driver.decorators import bot_creator, sudo_users_only
from driver.database.dbchat import get_served_chats
from driver.database.dbusers import get_served_users
from driver.database.dbpunish import get_gbans_count
from driver.database.dbqueue import get_active_chats

from config import BOT_USERNAME as uname


@Client.on_message(command(["/اذاعه", f"broadcast@{uname}"]) & ~filters.edited)
@bot_creator
async def broadcast_message_nopin(c: Client, message: Message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await c.forward_messages(i, y, x)
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(f"✅ الاذاعه اكتملت في{sent} الكروب.")
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**usage**:\n\n/اذاعه (`رساله`) او (`قم بالرد على الرساله`)/"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await c.send_message(i, text=text)
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(f"✅ الاذاعه اكتملت في{sent} كروب.")


@Client.on_message(command(["/اذاعه تثبيت", f"broadcast_pin@{uname}"]) & ~filters.edited)
@bot_creator
async def broadcast_message_pin(c: Client, message: Message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await c.forward_messages(i, y, x)
                try:
                    await m.pin(disable_notification=True)
                    pin += 1
                except Exception:
                    pass
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(
            f"✅ الاذاعه اكتملت في {sent} كروب.\n📌 تم الارسال معه {pin} مثبت المحادثه."
        )
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**usage**:\n\n/اذاعه تثبيت (`الرساله`) او (`قم بالرد على الرساله`)"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    pin = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await c.send_message(i, text=text)
            try:
                await m.pin(disable_notification=True)
                pin += 1
            except Exception:
                pass
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(
        f"✅ تم الاذاعه في {sent} كروب.\n📌 ارسل معه {pin} تثبت في المحادثه."
    )


@Client.on_message(command(["/الاحصائيات", f"stats@{uname}"]) & ~filters.edited)
@sudo_users_only
async def bot_statistic(c: Client, message: Message):
    name = me_bot.first_name
    chat_id = message.chat.id
    msg = await c.send_message(
        chat_id, "❖ جاري جمع الاحصائيات..."
    )
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    gbans_usertl = await get_gbans_count()
    tgm = f"""
📊 الاحصائيات الحالية لـ -›  [{name}](https://t.me/{uname})`:`

-›  **عدد المجموعات** : `{served_chats}`
-›  **عدد المستخدمين** : `{served_users}`
-›  **عدد المحظورين** : `{gbans_usertl}`

-›  **نسخة بايثون** : `{pyver}`
-›  **نسخة السورس** : `{pytgver.__version__}`
-›  **نسخة بايروجرام** : `{pyrover}`

🎗️ نسخة التحديث: `{ver}`"""
    await msg.edit(tgm, disable_web_page_preview=True)


@Client.on_message(command(["/الاتصالات", f"calls@{uname}"]) & ~filters.edited)
@sudo_users_only
async def active_group_calls(c: Client, message: Message):
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        await message.reply_text(f"🚫 خطأ: `{e}`")
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await c.get_chat(x)).title
        except BaseException:
            title = "Private Group"
        if (await c.get_chat(x)).username:
            data = (await c.get_chat(x)).username
            text += (
                f"**{j + 1}.** [{title}](https://t.me/{data}) [`{x}`]\n"
            )
        else:
            text += f"**{j + 1}.** {title} [`{x}`]\n"
        j += 1
    if not text:
        await message.reply_text("❌ لا يوجد هناك اي اتصال في الكروبات")
    else:
        await message.reply_text(
            f"✏️ **قائمه الكروبات التي فيها اتصال:**\n\n{text}\n❖ هذه هي قائمة بجميع المكالمات الجماعية النشطة الحالية في قاعدة البيانات الخاصة بي.",
            disable_web_page_preview=True,
        )
