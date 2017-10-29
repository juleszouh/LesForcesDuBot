"""Logs in to phpbb forum, pulls last active threads, and compares with what we have on file"""
import json
from pathlib import Path
from datetime import datetime, timedelta
import time
import requests
from bs4 import BeautifulSoup
from config import WEB_HOOKER, BOT_NAME, MSG
from config import USER_NAME, PASSWORD, LOGIN_URL, FEED_URL, FORUM_URL, TEMP_FILE_NAME

def put_file(content):
    """Dumps list of last 10 posts to file"""
    with open(TEMP_FILE_NAME, 'w') as fil:
        json.dump(content, fil, sort_keys=True, indent=4)

def get_file():
    """Gets list of last 10 posts from file"""
    if Path(TEMP_FILE_NAME).is_file():
        with open(TEMP_FILE_NAME, 'r') as fil:
            return json.load(fil)

def post_too_old(post):
    """check that a bump is within the last two hours, to avoid old bumps reappearing"""
    check_date = datetime.now()-timedelta(hours=2)
    post_date = datetime.strptime(post.get('bump_time'), '%d %b %Y, %H:%M')
    return check_date > post_date

def discord_broadcast(content):
    """Writes to discord"""
    if post_too_old(content):
        return

    to_discord = MSG.format(**content)
    webhook = {
        'content': to_discord,
        'username': BOT_NAME
    }
    requests.post(WEB_HOOKER, json=webhook)
    time.sleep(5) #to avoid spam if theres multiple

def scan_post(post):
    """Scans the inner html of a post. Will break if site changes anything in layout"""
    return {
        'href': FORUM_URL + post.select_one('a.topictitle').get('href')[1:],
        'topic': post.select_one('dt a.topictitle').string,
        'name': post.select_one('dt a.username-coloured').string,
        'bump_name': post.select_one('dd.lastpost a.username-coloured').string,
        'bump_time': post.select_one('dd.lastpost').contents[0].text.split('\n')[2].strip()
    }

def auth_and_get_posts(username, password):
    """Logs into forum and gets latest posts"""
    payload = {
        'username': username,
        'password': password,
        'redirect': './ucp.php?mode=login',
        'sid': '',
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

        if not stored_post_list: #nullcheck the list (i.e first run of the script)
            stored_post_list = current_post_list

        if stored_post_list != current_post_list:
            for post in current_post_list:
                if stored_post_list.count(post) == 0:
                    discord_broadcast(post)

        put_file(current_post_list)

auth_and_get_posts(USER_NAME, PASSWORD) #init call
