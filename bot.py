import discord
from discord.ext import commands
from itertools import permutations, product
from dotenv import load_dotenv
import os


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents=discord.Intents().default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message: discord.Message):
    # print("message received: " + message.content)
    # if client.user.id != message.author.id:
    #     await message.channel.send("I heard you")

    await client.process_commands(message)

@client.command()
async def solve(ctx: commands.Context, number: str):
    if number.isdigit():
        if len(number) > 4:
            await ctx.send("Number must be 4 digits or less")
            return
        answer = make_10(number)
        if (answer is None):
            await ctx.send(f'{number}: No solution found')
        else:
            answer = answer.replace('**', '^')
            await ctx.send(f'{number}: ||{answer[1:-1]}||')
    else:
        await ctx.send("Invalid number")



def make_10(numbers):
    operators = ['+', '-', '*', '/', '**','<<', '>>']

    def generate_parentheses_combinations(remaining_numbers, remaining_ops):
        if len(remaining_numbers) == 1:
            expr = str(remaining_numbers[0])
            return [expr]

        expressions = []
        for i in range(1, len(remaining_numbers)):
            left_nums = remaining_numbers[:i]
            right_nums = remaining_numbers[i:]
            for left_expr in generate_parentheses_combinations(left_nums, remaining_ops):
                for right_expr in generate_parentheses_combinations(right_nums, remaining_ops):
                    for op in remaining_ops:

                        expr = f"({left_expr}{op}{right_expr})"
                        if (expr.count('**') <= 1 and expr.count('<<') == 0) or (expr.count('**') <= 0 and expr.count('<<') == 1) and expr.count('>>') <= 1 :
                            expressions.append(expr)

        return expressions
    print("Starting")
    for perm in permutations(numbers):
        for ops in product(operators, repeat=3):
            expressions = generate_parentheses_combinations(list(perm), ops)
            for expr in expressions:
                try:
                    result = eval(expr)
                    if result == 10:
                        return expr
                except ZeroDivisionError:
                    continue
                except Exception:
                    continue
    return None

client.run(TOKEN)
