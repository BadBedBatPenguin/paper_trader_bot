## Kitty Bot
Telegram bot that gets trading pair given by user, fills form on https://paper-trader.frwd.one/ 
and returns chart from result page.

## How to run
Clone repo and move to its directory:

```Shell
git clone https://github.com/BadBedBatPenguin/paper_trader_bot.git
```

```Shell
cd paper_trader_bot
```

Create and activate virtual environment:

```Shell
python3 -m venv venv
```

```Shell
source venv/bin/activate
```

Install packages from requirements.txt:

```Shell
python3 -m pip install --upgrade pip
```

```Shell
pip install -r requirements.txt
```

Create new bot with BotFather.
Create .env file in current directory and fill it with your telegram token as in example:
```
TOKEN=587*****41:AAH-G4U8k2_D0Hij_x4R*****hSlm_Y_hKo
```

Run project: \
```Shell
python3 paper_trader_bot.py
```
Go to telegram and find your freshly created bot. \
Press or send "/start" to start chat with your bot.  \
Enjoy :)
