)
        return
    text = message.text.split(None, 1)1]
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
📊 الاحصائيات الحالية لـ -›  [{name}:
-›  عدد المجموعات : {served_chats}
-›  عدد المستخدمين : {served_users}
-›  عدد المحظورين : {gbans_usertl}
-›  نسخة بايثون : {pyver}
-›  نسخة السورس : {pytgver.version}
-›  نسخة بايروجرام : {pyrover}
🎗️ نسخة التحديث: {ver}"""
    await msg.edit(tgm, disable_web_page_preview=True)


@Client.on_message(command("/الاتصالات", f"calls@{uname}"]) & ~filters.edited)
@sudo_users_only
async def active_group_calls(c: Client, message: Message):
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        await message.reply_text(f"🚫 خطأ: {e}")
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
                f"{j + 1}. [{title} [{x}]\n"
            )
        else:
            text += f"{j + 1}. {title} [{x}]\n"
        j += 1
    if not text:
        await message.reply_text("❌ لا يوجد هناك اي اتصال في الكروبات")
    else:
        await message.reply_text(
            f"✏️ قائمه الكروبات التي فيها اتصال:\n\n{text}\n❖ هذه هي قائمة بجميع المكالمات الجماعية النشطة الحالية في قاعدة البيانات الخاصة بي.",
            disable_web_page_preview=True,
        )