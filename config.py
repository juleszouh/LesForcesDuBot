""" Config file for the webhook bot """
GENERAL_HOOK  = 'ICI TU METS L'URL DU WEBHOOK SUR LE CANAL général DU DISCORD'
ANNOUNCE_HOOK = 'ICI TU METS L'URL DU WEBHOOK SUR LE CANAL annonces DU DISCORD'
GENERAL_CHANNEL  = { 'url': GENERAL_HOOK,
                     'msg': ':bell: Nouvelle discussion : [**{topic}**]({href}) par `{name}` dans **{section}**' }
ANNOUNCE_CHANNEL = { 'url': ANNOUNCE_HOOK,
                     'msg': ':star: Nouvelle annonce : [**{topic}**]({last})' }
BOT_NAME       = 'Les Forces Du Bot'
USER_NAME      = 'ICI TU METS LE NOM D'UTILISATEUR SUR LE FORUM'
PASSWORD       = 'ICI TU METS LE MOT DE PASSE DU FORUM'
FORUM_URL      = 'https://lesforcesdumalt.forumactif.org'
LOGIN_URL      = FORUM_URL + '/login'
FEED_URL       = FORUM_URL + '/search?search_id=newposts'
ANNOUNCE_URL   = '/f19-annonces-du-groupe-de-gestion'
TEMP_FILE_NAME = 'post_data.json'
