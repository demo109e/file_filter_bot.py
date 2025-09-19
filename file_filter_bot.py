from pyrogram import Client, filters

# 🔹 Your credentials (edit these)
API_ID = 12345                           # your api_id
API_HASH = "your_api_hash"               # your api_hash
BOT_TOKEN = "your_bot_token"             # from @BotFather

# 🔹 Channel IDs
STORE_CHANNEL = -1001234567890           # your private store channel id
PUBLIC_CHAT = -1009876543210             # your public group/channel id

# Start bot client
bot = Client(
    "FileFilterBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# /start command
@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("👋 Hi! Send me a keyword in the public channel/group and I’ll fetch files from my store channel.")

# File search filter
@bot.on_message(filters.text & filters.chat(PUBLIC_CHAT))
async def filter_file(client, message):
    query = message.text.lower()
    results = []

    # search up to 10 files in store channel
    async for msg in bot.search_messages(STORE_CHANNEL, query, limit=10):
        if msg.document or msg.video or msg.audio:
            results.append(msg)

    if results:
        for msg in results:
            await msg.copy(message.chat.id)
    else:
        await message.reply("❌ No file found for your query!")

print("✅ File Filter Bot is running...")
bot.run()
