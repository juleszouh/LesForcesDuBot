""" Config file for the webhook bot """
BOT_ID = "this is where you put your webhooks id"
BOT_TOKEN = "this is where you put your webhooks token"
WEB_HOOKER = 'https://discordapp.com/api/webhooks/' + BOT_ID + '/' + BOT_TOKEN
BOT_NAME = 'RR-inc' #Name of the bot as it appears in chat
USER_NAME = 'forum username' #username on the forum
PASSWORD = 'forum password' #password on the forum
FORUM_URL = 'forum url ending with  /forum'
LOGIN_URL = FORUM_URL + '/ucp.php?mode=login'
FEED_URL = FORUM_URL + '/search.php?search_id=active_topics'
TEMP_FILE_NAME = 'post_data.json'
MSG = '"{topic}" by __**{name}**__, was just bumped by __**{bump_name}**__ on {bump_time}. [Open thread]({href})'
