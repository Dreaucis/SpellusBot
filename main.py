#!/usr/bin/python3
import os
import sqlite3 as sl
from pathlib import Path
import random

from discord.ext import commands

bot = commands.Bot(command_prefix='$')


def get_token_from_file(file: Path) -> str:
    """ Naively parse a file for a token. Expects the format to be <TOKEN_NAME>=<TOKEN>."""
    with file.open() as f:
        return f.read().split('=')[1]


def add_url_to_database(url: str):
    con = sl.connect('spellus_biggus.db')
    cursor = con.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_website (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            url TEXT
        );
    """)
    cursor.execute("""
        INSERT INTO game_website
        VALUES (NULL, '{URL}')
    """.format(URL=url))
    con.commit()
    con.close()


def list_urls_from_database() -> list:
    con = sl.connect('spellus_biggus.db')
    cursor = con.cursor()
    cursor.execute("""
        SELECT
            url
        FROM game_website
        ORDER BY url
    """)
    urls = cursor.fetchall()
    con.close()
    return urls


@bot.command()
async def save_game_website(ctx: commands.Context, url: str):
    """
    Adds the provided URL to the database

    :param ctx:
    :param url:
    :return:
    """
    add_url_to_database(url)
    await ctx.channel.send('Added {URL} to database.'.format(URL=url))


@bot.command()
async def list_game_websites(ctx: commands.Context):
    """
    Lists all urls in database

    :param ctx:
    :return:
    """
    urls = list_urls_from_database()
    urls = '\n'.join([url[0] for url in urls])
    await ctx.channel.send(urls)


@bot.command()
async def suggest_game_website(ctx: commands.Context):
    """
    Lists all urls in database

    :param ctx:
    :return:
    """
    urls = list_urls_from_database()
    urls = [url[0] for url in urls]
    url = random.choice(urls)
    msg = 'I, Spellus Biggus Bottus suggest that you visit {URL}!'.format(URL=url)
    await ctx.channel.send(msg)


if __name__ == '__main__':
    bot.run(os.getenv('TOKEN') or get_token_from_file(Path(__file__).parent / '.env'))
