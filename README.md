# Hello there , feature users of ECHO Cl Bot by me, Firemix!
There are all information how to fast start the bot, aboute bot, feature plans to bot
1. [Fast start the bot](#fast-start)
2. [Aboute](#aboute)
3. [Future of bot](#future-of-bot)


## Fast start
1. Install and place unpacked folder anywhere
2. Open in VS Code folder with bot
3. Open terminal
4. Execute ```pip install -r requirements.txt```
5. Wait for end of installing
6. Go to ```/Storage/.env.example```
7. Rename file to ```.env```
8. Fill all settings:\
```TOKEN``` = (Token from discord developer portal) \
```GIT_TOKEN``` = (Your token from github for work with github.api)  
```REPO_PATH``` = (Your path to repository, for example: ```ExampleOrganisation/ExampleRepo```) \
```NUMBER_OF_PR```=''(Number of PR that processing now) \
```CHANNEL_DEV_ID```=''(ID of channel in Discord for developer's changelog(contain targeted to developer information aboute Pull Request)) \
```CHANNEL_CL_ID```=''(ID of channel in Discord for public viewers) \
```GUILD_ID```='' (ID of guild where will sending CL)\
(all in '' must be string) \
```EMAIL_SUBJECT```=''(Topic of your latter) \
```EMAIL_OF_BOT``` = ''(Email of bot on which will be password of app) \ 
```EMAIL_OF_RECIEVER``` = '' (Your, for example, email or email of person, that will recieve error logs)
```EMAIL_PASSWORD``` = (Password that can be created on https://myaccount.google.com/apppasswords)

9. Double click on ```run.bat``` (need to be installed from your side python 3.14.3 or younger)

10. All done

## Aboute
This is bot for developers, that need to make changelog in discord for tracking or give to view progress of developing some product by publicating changelog from PR's
-
Pluses:
- Have ready in box system of publicating of changelogs
- Have filters for repacking  text in json format
- Have nice design
- Can send to developer's changelog comments in thread under PR's changelog
- Can from 04.04.26 send emails to developer with error logs

## Future of bot
In future, I plan to add:
- Make possible to customise all messages from bot to discord by adding language packs
- Make possible to working with Pull Request from Discord by leads of project for example
- Make possible to add tags from which will collecting all information in body of PR




### Also you always can write me in Discord(firemix_) to talk 
