# Sk8DateBot backend
Sk8DateBot is a Telegram Bot used for blasting skate dates from a Telegram group chat to a Telegram Channel.
It is a built with the [Django web framework](https://www.djangoproject.com/) in [Python programming language](https://www.python.org/psf/).


## How to Contribute

This is an open source project. Please continue this README to get set your local env set up. 
You can then contribute in one of 2 ways:

 - [Fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/about-forks) this repo, and then make [Pull Requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests#:~:text=Pull%20requests%20let%20you%20tell,merged%20into%20the%20base%20branch.) from your fork of this repo.
 - [Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository#:~:text=When%20you%20clone%20a%20repository,and%20folder%20for%20the%20project.) this repo and make [Merge Requests](https://stackoverflow.com/questions/23076923/what-is-a-merge-request) from a [feature branch](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow).
 
New features will only be accepted if they include ~~adequate tests, and~~ testing instructions for QA *(ie tell me what you did and how it should work so I can test it)*. 
Everything will be formatted by Black before being merged *(I'll take care of that, don't worry)*.


## Set Up Your Local Development Environment
From here, `words that looks like this` are commands you are meant to type somewhere, usually into a [terminal](https://itconnect.uw.edu/learn/workshops/online-tutorials/web-publishing/what-is-a-terminal/).

 - Install python on your local machine
    - Google it or go [here](https://www.python.org/psf/).

 - Install ngrok on your local machine
    - Google it or go [here](https://ngrok.com/).
    
    **NOTE** this installation will only work on a mac >= 10.13, and on a mac, for me it was easier to install with `brew install ngrok/ngrok/ngrok` and then [follow these instructions](https://dashboard.ngrok.com/get-started/setup) to conect my account.

 - From the terminal navigate to the directory you want this code to live and clone this repo by typing the following into a terminal:
    
    `git clone https://github.com/mdaizovi/sk8_bot`
    
 - `cd sk8_bot` to get into repo. `cd` is how you change folders from the command line.
 
 - Make a Virtual Environment:
  
    `python -m venv venv`
  
 - Activate virtual environment:
  
    `source venv/bin/activate`

 -  Copy `sk8_bot/.env.example` to `.env`. 
    You can do this by typing `cp sk8_bot/.env.example sk8_bot/.env` in the terminal.

 - Install backend requirements (make sure you are in your virtual environment first):
  
    `pip install -r requirements.txt`

- Run initial migrations, to prepare database:
  
    `python manage.py migrate`

- Make yourself a super user:
  
    `python manage.py createsuperuser`

  - You will be prompted by Django to create a super user, and you can use these credentials to log into the Admin interface (more on that later. We're going to take a pause on this subject here and come back to it.)

- Import starter data into the database:
  
    `python manage.py loaddata fixtures/db.json`

 - Get a Telegram API ID and Save Credenitals
    - Get a Telegram API ID [here](https://my.telegram.org/auth)
    - From there, choose “API development tools”. If it is your first time doing so, it will ask you for an app name and a short name, 
        you can change both of them later if you need to. Submit the form when you have completed it.
    - You will then see the api_id and api_hash for your app. These are unique to your app, and not revocable.
        Put those in the .env file that you copied. Replace "dummy" for TELEGRAM_APP_API_ID and TELEGRAM_APP_API_HASH with your new api_id and api_hash.
        Depending on your system, you might not be able to see the .env file. You will still be able to access it by typing
        `nano sk8_bot/.env` into the terminal, or by using an IDE, like PyCharm, what will show it in the directory.
        Don't forget to save your changes!
        
 - Create a Test Account on the Telegram Test Server 
    - Make an account for yourself on Telegram's Test server by following [these instructions](https://medium.com/@blueset/how-to-write-integration-tests-for-a-telegram-bot-1a23-blog-a82960d7d3ce#a39e).
    
 - Create Your Own Test Bot on the Telegram Test Server 
    - While logged in to your test account on Telegram, [make a bot](https://medium.com/shibinco/create-a-telegram-bot-using-botfather-and-get-the-api-token-900ba00e0f39)
    - BotFather will give you an API Key. Put that in your .env file under TELEGRAM_BOT_TOKEN
    - Set the privacy of your Bot so it can read chat messages. To do this, in your conversation with BotFather type
    
        `/setprivacy`
        
        and then after BotFather has you choose your bot, simple type
        
        `Disable`
        
    - While still logged in to your Test account, create a group chat and a channel. Add your bot to both, and make the Bot an admin of the channel. 
         
  - Create a Test Group and Channel for your Test Bot and save the chat ids in the database 
     - Set up Telegram webhooks to your local instance with the following command,
     replacing "<web_hook_address>" with the Forwarding address in the ngrok terminal
     (it will probably be something like 'https://001f796288c4.ngrok.io' but with different numbers/letters )
     Make this command from a terminal in this repo's home directory:
      
        `python manage.py set_hook --address <web_hook_address>`

      - Run the Django server: 
      
        `python manage.py runserver`

  - Navigate to the Admin by typing "http://127.0.0.1:8000/admin/" into your browser. On the login screen, enter the username and password you made awhile go, when you typed  `python manage.py createsuperuser` *(I told you we'd come back to this.)*
  - Go to "http://127.0.0.1:8000/admin/webhooks_consumer/inputsource/". These are your input sources; basically conversatinos where the bot commands come from. TODO GET ID AND PUT HERE, ALSO FOR OUTPUT. THEN TEST.


## Running Your Local Development Environment While You Work
   - Run ngrok by navigating in the terminal to the directory where you installed it, and typing:
  
    `./ngrok http 8000`
    
  - In another terminal, activate your virtual environment:
    
    `source venv/bin/activate`
    
 - Set up Telegram webhooks to your local instance with the following command,
 replacing "<web_hook_address>" with the Forwarding address in the ngrok terminal
 (it will probably be something like 'https://001f796288c4.ngrok.io' but with different numbers/letters )
 Make this command from a terminal in this repo's home directory:
  
    `python manage.py set_hook --address <web_hook_address>`
    
 - Run the local django server
  
    `python manage.py runserver`

## Running the tests
The tests often work and sometimes don't. Adequate testing is a work in progress.


- In one terminal, run ngrok 
    `./ngrok http 8000 `
- In another terminal:
  - Activate your virtual environment:
    
    `source venv/bin/activate`
  - Run pytest: 
  
      `pytest "-s" --reuse-db`



# How Does it Work?
## How Messages are Received
Posting messages works both from a Telegram chat as well as from the CiB Slack workspace. 
In `sk8_bot/webhooks_consumer/views.py `, there are 2 classes:
 - TelegramBotView
 - SlackBotView

I bet you can guess which one handles which.

For Telegram, every time a message is posted in a group that the skatebot is in, that message gets sent to this backend as JSON, looking something like this:
```
{'update_id': 944746271, 
 'message': {
   'message_id': 32726, 
   'from': 
     {'id': 531519657, 'is_bot': False, 'first_name': 'SABA', 'username': 'SABAloops'
     }, 
   'chat': {
     'id': -1001258758865, 'title': 'Berlin Quadsk8ing on Ramps/Bowls/Skateparks Chatter', 'type': 'supergroup'
    },
   'date': 1658575957, 'text': 'Who is in the parade?! :) we’re coming!! :)'
  }
}
```

In TelegramBotView there is a function called `post`, which parses this json. It checks to see if the message contains a command (if it starts with a /) and of so, if takes the word (for example, "/sk8") and checks the database to see if there is a saved commant for that command and chat combination. This will be explained a little more below, in **Database Models**.

In `sk8_bot/webhooks_consumer/factory.py` you'll see several simple functions, like 
  - `_get_compliment`
  - `_get_doggo`
 etc
Those are the functions that dictate what happens for their respective commands that trigger them. sk8 is not there because all it does is take input and put it somewhere else, which willl make more sense in **Database Models**. Thwe only thing from "/sk8" command that is in this file is the function `_get_broadcast_message`, which formats the message posted to the skate bulletin and CiB Slack. 

## Database Models
In `sk8_bot/webhooks_consumer/models.py` there are definitions of the database models (aka tables).

`InputSource` is where the messages come from, such as a Telegram chat or Slack channel.
`OutputChannel`Is the same, but they are generally different Telegram chats/Slack channels.

For example, for a /sk8 bulletin to go from the "Berlin Quadsk8ing on Ramps/Bowls/Skateparks Chatter" to the CiB Slack channel and skate bulletin channel, the chat where the message originated is the `InputSource`, then the Slack channel and Sk8Date Bulletin are both `OutputChannel`. Because something (pictures of dogs, cats, or sloths) gets posted back to the "Berlin Quadsk8ing on Ramps/Bowls/Skateparks Chatter", it is also an `OutputChannel`. The "Berlin Skate Crew" chat doesn't get animal pictures, so it is not an `OutputChannel`, just an `InputSource`.

`BotOutput` is what the Bot actually returns. For exmample, for the simple command `/doggo` that returns a picture of a dog in "Berlin Quadsk8ing on Ramps/Bowls/Skateparks Chatter", it looks like this:
 - `output_function` is `_get_doggo`
 - `output_platform` is Telegram
 - `output_channel` is the same chat the command came from, "Berlin Quadsk8ing on Ramps/Bowls/Skateparks Chatter"

`BotAction` brings this all together.
 - `command` the actual text that triggers this sequence, like "sk8" or "doggo"
 - `content_required` True or False of whether content is required. For example, /sk8 requires text or else it does nothing, but doggo doesn't.
 - `output`is an instance of `BotOutput` 


## FAQ

### Everything should work locally but it doesn't. Why?
 - Try restarting ngrok and re-running the command to set the webhook.
