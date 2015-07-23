# League-of-Legends-most-played-with
Uses Riots API to display most played with users of x number of previous ranked solo/duo queue games

User enters their username and number of of previous games they want to include, optionally 'all' to gather all games.
The application first uses the username to get the users id.
Next it goes through the users match history grabbing x number of match ids
After the match ids are fully gathered they are then used to find and gather all players in the match.
Finally the dictionary of users with number of games played with is sorted and prints top 10 most played with
NOTE: Riot limits 10 requests per 10 seconds, This drastically limits the time to search through games. You may get a Value Error encountered displayed on the screen a couple times because the application is pushing the line of riots rate limit. These should not occur more than 10 time in a row though so just give the application a chance to keep going.

![results](http://i.imgur.com/liTAcDH.png)

To use:

Make sure you are using Python 2.7

If pip is installed (pip comes installed with later versions of python 2.7):

`pip install requests` via the terminal/command line (possibly `sudo pip install requests` if on a mac)

Head over to https://developer.riotgames.com/ and click 'sign in' in the top right to sign in with your league info. After signing in, scroll down to see your key. Copy it.

Open up leagueNumPlays.py in any text editor and replace XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX with your api-key (inside the apostrophes)

You should then be able to head over to the terminal/command line, navigate to the directory and run `python leagueNumPlays.py`
