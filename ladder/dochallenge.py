'''
Created on Nov 6, 2010

@author: jtk
'''
from os.path import expanduser
import subprocess
import re
from models import Result

runtemplate = 'java -jar /Users/jtk/icypc/icypc.jar -player pipe 1 %s/icypc/%s -player pipe 1 %s/icypc/%s -view trace trace.txt'

def runMatch(red, blue):
    print 'Playing ' + red[1] + ' vs. ' + blue[1]
    (redUser, redPlayer) = red
    (blueUser, bluePlayer) = blue
    redUser = expanduser('~' + redUser)
    blueUser = expanduser('~' + blueUser)
    command = (runtemplate % (redUser, redPlayer, blueUser, bluePlayer)).split()
    
    print command
    
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    output = p.communicate()[0];
    print '=====\n' + output + '\n====='
    pattern = re.compile(r'Winner: (\d+)')
    match = pattern.match(output)
    
    (winner, loser) = (red, blue) # default
    if match is None:
        print "no winner found"
    else:
        print 'winner is', match.group(1) 
        if match.group(1) == '1':
            (winner, loser) = (blue, red) # challenger won
    r = Result(time=datetime.now(), winnerUser=winner[0], winnerPlayer=winner[1], loserUser=loser[0], loserPlayer=loser[1])
    r.save()
    return (winner, loser)


from models import Result
from ladderadjust import buildLadder, adjustLadder
from datetime import datetime

def runLadder(userid, player):
    print 'running the ladder for', userid, player
    challenger = (userid, player)
    
    if Result.objects.count() == 0:  # hack to handle empty ladder
        (winner, loser) = runMatch(challenger, challenger)
        return
    
    results_list = Result.objects.all()
    ladder = buildLadder(results_list)
    
    if challenger not in ladder:
        ladder.append(challenger)

    while (True):
        i = ladder.index(challenger)
        if i == 0:
            return
        (winner, loser) = runMatch(ladder[i-1], ladder[i])
        if adjustLadder(ladder, winner, loser):  # returns True if challenger lost
            return

    