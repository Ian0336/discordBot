
from PIL import Image
import io
import json

# 導入Discord.py模組
import discord
# 導入commands指令模組
from discord.ext import commands
import requests

API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
headers = {"Authorization": "Bearer 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"}
options = {'use_cache': False}
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)


def query(payload):
    data = json.dumps(payload)
    response = requests.post(API_URL, headers=headers, data=data)
    return response.content


def queryPic(promt):
    image_bytes = query({
        "inputs": promt,
        "options": options,
    })
    # You can access the image with PIL.Image for example
    image_stream = io.BytesIO(image_bytes)

    # Open the image using PIL
    img = Image.open(image_stream)
    img.save("output_image.jpg")


@bot.event
# 當機器人完成啟動
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")


@bot.command()
# 輸入%Hello呼叫指令
async def generate(ctx, *arg):
    # 回覆Hello, world!
    await ctx.send("生成中, ")
    # put the args into str
    prompt = ' '.join(arg)
    queryPic(prompt)
    await ctx.send("生成完畢!")
    with open('output_image.jpg', 'rb') as image_file:
        image_bytes = image_file.read()
        await ctx.send(file=discord.File(io.BytesIO(image_bytes), filename='output_image.jpg'))


@bot.command()
# 輸入%Hello呼叫指令
async def echo(ctx, *arg):   # 回覆Hello, world!
    prompt = ' '.join(arg)

    await ctx.send(prompt)


@bot.command()
# 輸入%Hello呼叫指令
async def switchCashe(ctx):
    # 回覆Hello, world!
    await ctx.send(f"switch the cashe mode { '[open]' if ~options['use_cache'] else '[close]'}!")
    options["use_cache"] = ~options["use_cache"]


with open('item.json', "r", encoding="utf8") as file:
    data = json.load(file)


bot.run(data['token'])
