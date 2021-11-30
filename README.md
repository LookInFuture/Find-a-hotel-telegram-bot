# Find a hotel telegram bot

The bot has been written on Python language and helps to find a hotel without needing going on the website.
Instead, you can use the bot and find the hotel you need as per your request.

Moreover, once you have found a hotel you are looking for, you simply click on the 
provided link and book a hotel.

## How to use bot
To start the bot you have to have installed Telegram either mobile or desktop version.
Type or copy @Find_your_place_Bot into search bar and follow instructions of the bot.

There are few commands you can use in the bot:
* Lowprice: this command allows you to find a hotel with the filter of lower price.
* Highprice: this command allows you to find a hotel with the filter of high price.
* Bestdeal: this command allows you to find a hotel with additional settings:
    * Minimum and maximum price range;
    * Minimum and maximum distance range from the center of the city.
* History: this command shows you what command you used before and what hotels had been found.
Including *Hotel name, price* and *url* for found hotels.

## Samples 
Here are pictures that should give you an idea what bot looks like.

Beginning:
![link](/pictures/Beginning.png)

Results:
![link](/pictures/Result.png)

## For programmers
If you ever wish to fork and change this bot, simply use this command:

```
$git clone #insert the link to repository
```
In order to start using it you have to have a telegram bot token. 
Use this step-by-step write up to get it: 
[How to get a telegram token][1]

You as well need to get an API token for hotels from [Rapidapi][2].

All needed requirements to install you will find here in [requirements](/requirements.txt)
## Gratitude
With the deep gratitude thanks to [Skillbox](skillbox.ru) team for providing materials
and data to start the journey. Separately to supervisors who helped a lot to clarify 
all questions. 

> Author: Vladislav Mikhaylov

[1]: (https://creativeminds.helpscoutdocs.com/article/2602-telegram-bot-telegram-creating-a-bot)
[2]: (https://rapidapi.com/apidojo/api/hotels4/)