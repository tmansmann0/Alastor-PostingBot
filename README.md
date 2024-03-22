# Alastor-PostingBot
Rewards people with good taste

### Welcome To Alastor-Posting Bot
- This simple discord bot was created in only 2 hours. It is designed to reward discord users when they send gif's and images of Alastor from Hazbin Hotel

### Features
- Machine learning model to identify Alastor in images
- Database to provide scoreboard for keeping track of who has sent most images
- Quote scraping tool to make bot reply with Alastor quotes

### ML Model Info
- Based on EfficientNet trained on 1000 iterations via https://liner.ai
- Trained on images of Alastor, any random image I found on my computer, and images of other HH characters to prevent misclassification based on shared background and color pallete 

### Setup Instructions

To get Alastor-PostingBot up and running, you will need to follow these setup instructions. This guide assumes you have a basic understanding of Python and Discord bot creation.

#### Prerequisites
- Python 3.8 or later
- A Discord account and a bot token (see Discord's developer portal)
- An environment capable of running TensorFlow models

#### Installation
1. Clone the repository:
``` 
git clone https://github.com/tmansmann0/Alastor-PostingBot.git
cd Alastor-PostingBot
```
2. Install required Python packages:
```
pip install -r requirements.txt
```
3. Set up your environment variables:
Create a .env file in the root directory of the project and add the following lines:
```
DISCORD_BOT_TOKEN=your_discord_bot_token_here
DISCORD_GUILD_ID=your_guild_id_here
```
Replace your_discord_bot_token_here and your_guild_id_here with your Discord bot token and the Discord guild ID where you want to deploy the bot, respectively.

### Running the Bot
Execute the following command in the terminal:
```
python bot.py
```
The bot should now set up a database and begin running and listening to messages on your Discord server.

### Acknowledgments
Big thanks to liner.ai for providing the super helpful training GUI and model exporting
Thank you to Collin for beating me to making the bot actually good
Copyright of underlying model data and quotes belongs to Spindlehorse Toons, Amazon, and A24 respsectively

