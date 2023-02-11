import openai
import discord
from discord.ext import commands

class ChatGPT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_keys = {}

    @commands.group(name='chatgpt', help='Generate a response using OpenAI API')
    async def chatgpt(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand")

    @chatgpt.command(name='setapi', help='Set the OpenAI API key')
    @commands.has_permissions(administrator=True)
    async def setapi(self, ctx, api_key: str):
        self.api_keys[ctx.guild.id] = api_key
        await ctx.send(f"OpenAI API key set for guild `{ctx.guild.name}`")

    @chatgpt.command(name='respond', help='Generate a response to the prompt')
    async def respond(self, ctx, *, prompt: str):
        api_key = self.api_keys.get(ctx.guild.id)
        if not api_key:
            return await ctx.send("OpenAI API key not set for this guild")

        openai.api_key = api_key

        completions = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        message = completions.choices[0].text
        await ctx.send(message)

def setup(bot):
    bot.add_cog(ChatGPT(bot))
