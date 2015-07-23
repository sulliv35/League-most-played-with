# Mark Sullivan
# Created 7/17/15
# process:
# 1)Take username and find they're id
# 2)Use user_id to open match history and gather match id's
# 3)Go through each match by id and store players in dictionary/update times played with
# 4)Use some method to order
import requests
import time
import operator

api_key = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
region = 'na'


"""Goes through match history matches gathering people played with and keeping a count
"""


def get_user_id(user): # Need user id to access match history
    print 'getting user Id'
    while True:
        try:
            response = requests.get('https://' + region + '.api.pvp.net/api/lol/na/v1.4/summoner/by-name/' + user + '?api_key=' + api_key)
            user_info = response.json()
            break
        except ValueError:
            user = raw_input('Invalid username, please enter again: ').lower()
            time.sleep(1)
    user_id = user_info[user]['id']
    print 'User id: ' + str(user_id)
    print 'Waiting 10 seconds before gathering'
    time.sleep(10)
    return user_id


def get_match_history_ids(user_id, by_five=20, start=0, end=5):  # match history id to access match
    print 'getting history IDs'
    match_history_id = []
    for fivReg in range(by_five):
        while True:
            try:
                response = requests.get('https://' + region +
                                        '.api.pvp.net/api/lol/na/v2.2/matchhistory/' + str(user_id)
                                        + '?rankedQueues=RANKED_SOLO_5x5&beginIndex='+str(start) +
                                        '&endIndex='+str(end)+'&api_key=' + api_key)
                match_history = response.json()
                if 'matches' in match_history or match_history == {}:# ends when matches
                    break
            except ValueError:
                print 'encountered a value error, waiting 1 second then trying again'
                time.sleep(1)
        for i in range(5):
            while True:
                try:            #try to
                    match_history_id.append(match_history['matches'][i]['matchId'])
                    print 'gathered match ' + str(i+(fivReg*5)+1)
                    break
                except IndexError:
                    print 'Reached end of match history'
                    print 'Waiting 10 seconds'
                    time.sleep(10)
                    return match_history_id
                except KeyError:
                    if match_history == {}:
                        print 'Reached end of match history'
                        print 'Waiting 10 seconds'
                        time.sleep(10)
                        return match_history_id
                    else:
                        print 'Something went wrong'
                        print match_history
                        time.sleep(1)
        if (((fivReg+1) % 10 == 0) and (fivReg != 0)) or (fivReg+1 == by_five):
            print 'Waiting 10 seconds'
            time.sleep(10)
        start += 5
        end += 5
    return match_history_id


def get_users_in_matches(match_history_id):  # go to matches using match id's and count players
    print 'getting users in history'
    games = len(match_history_id)
    participant_identities = {}
    match = 0
    for game in range(games):
        while True:
            try:
                response = requests.get('https://' + region + '.api.pvp.net/api/lol/na/v2.2/match/'
                                        + str(match_history_id[game]) + '?api_key=' + api_key)
                match = response.json()
                participants = match['participantIdentities']
                break
            except (ValueError, KeyError):
                print 'encountered a value error, waiting 1 second then trying again'
                time.sleep(1)
        for x in range(10):
            if participants[x]['player']['summonerName'] not in participant_identities: # if user NOT listed add them with value 1
                participant_identities[participants[x]['player']['summonerName']] = 1
            else:
                participant_identities[participants[x]['player']['summonerName']] += 1  # if user listed add 1 to curent value
        print 'gathered users from ' + str(game+1) + ' game(s)'
        if ((game+1) % 10 == 0) and (game != 0) and game+1 != games:
            print '10 requests made, waiting 10 seconds'
            time.sleep(10)
    return participant_identities


def print_sorted(username, summonerNames):
    summonerNamesSorted = sorted(summonerNames.items(), key=operator.itemgetter(1)) # sort dictionary into tuples
    length = len(summonerNamesSorted)
    print username + ' top 10 users played with:'
    for i in range(10):#prints top x players
        print str(summonerNamesSorted[length-(i+2)][1]) + ' ' + summonerNamesSorted[length-(i+2)][0]


def get_games_by_five():
    while True:
        games_entered = raw_input('Enter number of games to search\n'
                                  'Note that games are gathered in multiples of 5\n'
                                  "Optionally enter 'all' to gather entire history\n").lower()
        if games_entered == 'all':
            return 10000
        try:
            if int(games_entered)%5 != 0:
                return int(games_entered)/5 + 1
            else:
                return int(games_entered)/5
        except ValueError:
            print'Invalid entry'


def start():
    summoner_names = {}
    username = raw_input('Enter a Username: ').lower()  # asks for username
    games_by_five = get_games_by_five()
    start_time = time.time()
    uid = get_user_id(username)
    match_id = get_match_history_ids(uid, games_by_five)
    summoner_names = get_users_in_matches(match_id)
    print_sorted(username, summoner_names)
    end_time = time.time()
    minutes, seconds = divmod((end_time - start_time), 60)
    print 'Time taken: %02d:%02d' % (minutes, seconds)


if __name__ == "__main__":
    start()

