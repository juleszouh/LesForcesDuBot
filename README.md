# phpbb-active-topics-to-discord
Script to post on discord if there is a forum bump on a phpbb forum.

## Running
Right now I'm using a task scheduler (like cron) to run this once a minute.

If you dont have access to that, but instead can leave a process running for a long time, you can wrap the initializing method in a `while 1:` loop.

## Parsing
The soup-parsing is specific to the template of the forum I'm currently using, so you'll have to adapt the **scan_post** method if you want to implement this. Parsing logic is contained within this method, to keep it easy.

## Why not hook into phpbb post event
It would be easier to hook into the event fired when a post is submitted in the backend, or perhaps the DB itself, but for my use, I dont have direct access to the box with phpbb running, so I opted with a login-and-parse strategy, which is a lot more flexible and allows others to adopt this easier.

## Config
config.py contains variables you will want to fill in yourself if you want to run this. It also lets you customize a few things, like botname and string-format.
