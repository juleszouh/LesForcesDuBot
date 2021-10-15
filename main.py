"""Logs in to phpbb forum, pulls last active threads, and compares with what we have on file"""
import json
from pathlib import Path
from datetime import datetime, timedelta
import time
import requests
from bs4 import BeautifulSoup
from config import GENERAL_CHANNEL, ANNOUNCE_CHANNEL, BOT_NAME
from config import USER_NAME, PASSWORD, LOGIN_URL, FEED_URL, FORUM_URL, ANNOUNCE_URL, TEMP_FILE_NAME

def put_file(content):
    """Dumps list of last 10 posts to file"""
    with open(TEMP_FILE_NAME, 'w') as fil:
        json.dump(content, fil, sort_keys=True, indent=4)

def get_file():
    """Gets list of last 10 posts from file"""
    if Path(TEMP_FILE_NAME).is_file():
        with open(TEMP_FILE_NAME, 'r') as fil:
            return json.load(fil)

def discord_broadcast(content, channel):
    """Writes to discord"""
    to_discord = channel.get('msg').format(**content)
    webhook = {
        'content': to_discord,
        'username': BOT_NAME
    }
    requests.post(channel.get('url'), json=webhook)
    time.sleep(5) #to avoid spam if theres multiple

def scan_post(post):
    """Scans the inner html of a post. Will break if site changes anything in layout"""
    return {
        'href': FORUM_URL + post.select_one('a.topictitle').get('href'),
        'topic': post.select_one('a.topictitle').string[1:],
        'name': post.select_one('a.gensmall').string,
        'section': post.select('a')[3].string,
        'last': FORUM_URL + post.select('dd.lastpost a')[1].get('href')
    }

def get_channel(sess, post):
    """Gets discord channel depending on forum section. Will break if site changes anything in layout"""
    current = sess.get(post.get('href'))
    current_soup = BeautifulSoup(current.text, 'html.parser')

    for nav in current_soup.select('a.nav'):
        nav_href = nav.get('href')
        if nav_href == ANNOUNCE_URL:
            return ANNOUNCE_CHANNEL

    current_href = FORUM_URL + current_soup.select_one('h2.topic-title a').get('href')
    if current_href == post.get('last'):
        return GENERAL_CHANNEL

def auth_and_get_posts(username, password):
    """Logs into forum and gets latest posts"""
    payload = {
        'username': username,
        'password': password,
        'login': 'Login'
    }

    with requests.Session() as sess:
        sess.post(LOGIN_URL, data=payload)

        forum_posts = sess.get(FEED_URL)
        forum_posts_soup = BeautifulSoup(forum_posts.text, 'html.parser')

        raw_posts = forum_posts_soup.select('li.row')

        stored_post_list = get_file()
        current_post_list = []

        for raw_post in raw_posts:
            formatted_post = scan_post(raw_post)
            current_post_list.append(formatted_post)

        if stored_post_list != current_post_list:
            for post in current_post_list:
                if not stored_post_list or stored_post_list.count(post) == 0:
                    channel = get_channel(sess, post)
                    if (channel):
                        discord_broadcast(post, channel)

        put_file(current_post_list)

auth_and_get_posts(USER_NAME, PASSWORD) #init call
