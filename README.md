# Sk8DateBot backend
Sk8DateBot is a Telegram Bot used for blasting skate dates from a Telegram group chat to a Telegram Channel.
It is a built with the [Django web framework](https://www.djangoproject.com/) in [Python programming language](https://www.python.org/psf/).


## How to Contribute

This is an open source project. Please continue this README to get set your local env set up, 
fork this repo, and then make pull requests from your fork of this repo.
New features will only be accepted if they include adequate tests, and testing instructions for QA. 
Everything will be formatted by Black before being merged.


## Set Up Your Local Development Environment
From here, `words that looks like this` are commands you are meant to type somewhere, usually into a [terminal](https://itconnect.uw.edu/learn/workshops/online-tutorials/web-publishing/what-is-a-terminal/).

 - Install python on your local machine
    - Google it or go [here](https://www.python.org/psf/).

 - Install ngrok on your local machine
    - Google it or go [here](https://ngrok.com/).

 - From the terminal navigate to the directory you want this code to live and clone this repo by typing the following into a terminal:
    
    `git clone https://github.com/mdaizovi/sk8_bot`
    
 - `cd sk8_bot` into repo
 
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

  - You will be prompted by Django to create a super user, and you can use these credentials to log into the admin interface (more on that later)

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
        
    - While still logged in to your Test account, create a group chat and a channel. Add you bot to both, and make the Bot an admin of the channel. 
         
  - Create a Test Group and Channel for your Test Bot and save the chat ids in the database 
     - Set up Telegram webhooks to your local instance with the following command,
     replacing "<web_hook_address>" with the Forwarding address in the ngrok terminal
     (it will probably be something like 'https://001f796288c4.ngrok.io' but with different numbers/letters )
     Make this command from a terminal in this repo's home directory:
      
        `python manage.py set_hook --address <web_hook_address>`

      - Run the Django server: 
      
        `python manage.py runserver`

    - TODO how to get IDS and put in admin.



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

## FAQ

### Everything should work locally but it doesn't. Why?
 - Try restarting ngrok and re-running the command to set the webhook.