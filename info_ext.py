import discord
from discord.ext import commands
import wolframalpha
from dateutil.relativedelta import relativedelta
import datetime

try:
    import google
except:
    print("Unable to import Google")
from PyDictionary import PyDictionary
import random
import wikipedia


class Info:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def xmas(self):
        """Tells you how long until Christmas.
        As requested by Adam."""
        await self.bot.say(get_time_until_xmas())
    
    @commands.command(pass_context=True)
    async def calc(self, ctx, *, msg):
        """Performs the desired calculation.
        Should look like:
            >calc pic <calculation>
        to get pictures of the result or:
            >calc txt <calculation>
        for test of the result.

        Goes through WolframAlpha."""
        try:
            type = "pic"
            if msg.startswith("txt ") or msg.startswith("pic "):
                type = msg.split()[0]
                msg = " ".join(msg.split()[1:])
            client = wolframalpha.Client("TVYA5X-8E78YXA7JL")
            res = client.query(msg)
            em = discord.Embed(type="rich")
            for pod in res.pods:
                for sub in pod.subpods:
                    if type == "pic":
                        try:
                            em.set_image(url=sub["img"]["@src"])
                            await self.bot.say(embed=em)
                        except:
                            pass
                    else:
                        try:
                            await self.bot.say(sub["plaintext"])
                        except:
                            pass
        except:
            try:
                if res["@success"] == "false":
                    output = "Sorry, I didn't understand you. "
                    try:
                        if int(res["didyoumeans"]["@count"]) > 0:
                            output += "Did you mean: " + res["didyoumeans"]["didyoumean"]["#text"]
                    except:
                        pass
                    try:
                        if int(res["tips"]["@count"]) > 0:
                            output += res["tips"]["tip"]["@text"]
                    except:
                        pass
                    await self.bot.say(output)
            except:
                pass
    
    @commands.command(pass_context=True)
    async def poll(self, ctx, *, msg):
        """Creates a poll.
        The poll should be in the following form:
        >poll question; option1; option2; etc."""
        msg = msg.split(";")
        output = "**" + ctx.message.author.name + "** asked **" + msg[0] + "**\n"
        blanks = 0
        for option in range(1, len(msg)):
            if msg[option] == "":
                blanks += 1
            else:
                output += ":regional_indicator_" + chr(96 + option - blanks) + ": " + msg[option] + "\n"
        poll_msg = await self.bot.say(output + "\n React with your answer!")
        for a in range(len(msg) - blanks - 1):
            await self.bot.add_reaction(poll_msg, eval("\"\\N{REGIONAL INDICATOR SYMBOL LETTER " + chr(65 + a) + "}\""))
        await self.bot.delete_message(ctx.message)
    
    @commands.command()
    async def google(self, *, query):
        """Returns the results of a google search.
        Should be written as:
            >google [no. of results] <query>
        eg.:
            >google 5 cat videos
        or:
            >google cat videos"""
        try:
            no_requested = int(query.split(" ")[0])
            query = " ".join(query.split(" "))[1:]
        except:
            no_requested = 5
        results = google.search(query, start=0, stop=no_requested * 2)
        urls = []
        for url in results:
            urls.append(url)
        
        ignore = []
        for a in range(len(urls)):
            for b in range(len(urls)):
                if a != b and urls[a] in urls[b]:
                    ignore.append(b)
        no_given = 0
        for a in range(len(urls)):
            if not a in ignore:
                no_given += 1
                if no_given <= no_requested:
                    await self.bot.say(urls[a])
                else:
                    break
    
    @commands.command(name="def")
    async def define(self, word):
        """Defines the given word."""
        try:
            d = PyDictionary().meaning(word).items()
            output = ""
            for a in d:
                output += "\n\n**" + a[0] + "**"
                for b in a[1]:
                    output += "\n" + b
        except:
            ouput = "Sorry, something went wrong."
        await self.bot.say(output)
    
    @commands.command()
    async def choose(self, *, choices):
        """Selects a choice at random for you.
        Seperate choices with semi-colons, like:
            >choose choice1; choice2; choice3; etc.
        You can also specify how many options you want to be chosen, like:
            >choose amount: choice1; choice2; etc.
        Note the use of a colon here, not a semi-colon."""
        choices = choices.split(";")
        if ":" in choices[0]:
            try:
                amount = int(choices[0].split(":")[0])
                choices.append(":".join(choices[0].split(":")[1:]))
                startAt = 1
                if amount <= 0 or amount >= len(choices) - 1:
                    NO
            except:
                amount = 1
        else:
            amount = 1
            startAt = 0
        
        chosen = []
        a = ""
        for _ in range(amount):
            while a in chosen or a == "":
                a = random.randint(startAt, len(choices) - 1)
            chosen.append(a)
        output = random.choice(("I choose...", "How about", "I'd go for")) + "\n"
        for a in chosen:
            if not a == "":
                output += choices[a] + "\n"
        await self.bot.say(output)
    
    @commands.command(pass_context=True)
    async def call(self, ctx, *, msg):
        """Changes someone's nickname.
        Should look like:
            >call current_name new_name
        Or if one of the names is 2+ words:
            >call current name; new name"""
        if ";" in msg:
            await self.bot.change_nickname(ctx.message.server.get_member_named(msg.split(";")[0]), msg.split(";")[1])
        else:
            if len(msg.split(" ")) == 2:
                await self.bot.change_nickname(ctx.message.server.get_member_named(msg.split(" ")[0]),
                                               msg.split(" ")[1])
            else:
                NO
    
    @commands.command()
    async def wiki(self, *, query):
        """Gives the summary of the wikipedia article.
        Should look like:
            >wiki {no of sentences] <title>
        if no of sentences not specified default is 3."""
        try:
            sentences = int(query.split(" ")[0])
            query = " ".join(query.split(" ")[1:])
        except:
            sentences = 3
        try:
            output = "<https://en.wikipedia.org/wiki/%s>\n" % "_".join(query.split(" "))
            output += wikipedia.summary(query, sentences=sentences)
            await self.bot.say(output)
        except wikipedia.exceptions.DisambiguationError as e:
            output = "There are multiple pages with that name. Did you mean:"
            for suggestion in e.options:
                if suggestion.lower().startswith(query.lower() + " ("):
                    output += "\n" + suggestion
            await self.bot.say(output)


def get_time_until_xmas(minsec=True):
    today = datetime.date.today()
    nextXMasYear = today.year
    if today.month == 12 and today.day >= 25:
        nextXMasYear += 1
    until = "Christmas is in "
    units = ["years", "months", "days"]
    if minsec:
        rd = relativedelta(datetime.datetime(nextXMasYear, 12, 25), datetime.datetime.today())
        for unit in ("hours", "minutes", "seconds"):
            units.append(unit)
    else:
        rd = relativedelta(datetime.date(nextXMasYear, 12, 25), datetime.date.today())
    for a in units:
        if rd.__dict__[a] != 0:
            if until != "Christmas is in ":
                until += ", "
            until += str(rd.__dict__[a]) + " " + a
    return until


def setup(bot):
    bot.add_cog(Info(bot))
