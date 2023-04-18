import openai
import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()

bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

openai.api_key = os.getenv("OPEN_AI_KEY")

@bot.event
async def on_ready():
	print("Bot is Up and Ready!")
	try:
		synced = await bot.tree.sync()
		print(f"Synced {len(synced)} command(s)")
	except Exception as e:
		print(e)

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
	await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command!")

@bot.tree.command(name="ask")
@app_commands.describe(prompts = "prompts")
async def ask(interaction: discord.Interaction, prompts: str):
	response = openai.ChatCompletion.create	(
		model="gpt-3.5-turbo",
		messages = [
			{"role":"user","content":prompts}
		]
	)
	
	response_text =  response.choices[0].message.content

	await interaction.response.send_message(f"{interaction.user.mention} {response_text}")

bot.run(os.getenv("TOKEN"))
