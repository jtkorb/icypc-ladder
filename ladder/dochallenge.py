'''
Created on Nov 6, 2010

@author: jtk
'''
from os.path import expanduser
import subprocess
import re
from settings import ICYPC_JAR, TRACES_DIR
from os import stat, makedirs, rename
from datetime import datetime

from models import Result
from ladderadjust import buildLadder, adjustLadder

runtemplate = 'java -jar %s -player pipe 1 %s -player pipe 1 %s -view trace %s/trace.txt'

def script(userid, player):
    return expanduser('~' + userid) + '/icypc/' + player

def scriptRunnable(userid, player):
    s = script(userid, player)
    try:
        mode = stat(s).st_mode  # get mode bits of script file
    except OSError:
        print 'file', s, 'not found'
        return False
    if (mode & 5) != 5: # check for +rx bit set for world
        print 'file', s, 'is not executable (r+x) for world'
        return False
    return True

S_IFDIR = 0040000        

def makeTraceDir():
    try:
        mode = stat(TRACES_DIR).st_mode
        if (mode & S_IFDIR == 0):
            print 'not a directory or not accessible:', TRACES_DIR, '--tell a friend'
    except OSError:
        print 'making', TRACES_DIR
        try:
            makedirs(TRACES_DIR)
        except:
            print 'could not make', TRACES_DIR, '--tell a friend'

output_pattern = re.compile(r'.*Winner: (\d+)\sScore: (\d+) \((\d+) (\d+)\) (\d+) \((\d+) (\d+)\)', re.DOTALL)

def runMatch(red, blue):
    (redUser, redPlayer) = red
    (blueUser, bluePlayer) = blue

    rname = redUser + '/' + redPlayer
    bname = blueUser + '/' + bluePlayer
    print 'Playing ' + rname + ' vs. ' +  bname
    
    makeTraceDir()
    command = (runtemplate % (ICYPC_JAR, script(redUser, redPlayer), script(blueUser, bluePlayer), TRACES_DIR)).split()
    print command
    
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, stderr) = p.communicate();
    m = output_pattern.match(output)
    
    (winner, loser) = (red, blue) # default
    if m:
        print 'winner is', m.group(1) 
        challengerState = 'loses'
        if m.group(1) == '1':
            challengerState = 'wins'
            (winner, loser) = (blue, red) # challenger won
        log = 'challenger (%s) %s: %s [%s (%s %s)] vs. %s [%s (%s %s)]' % (bname, challengerState,
                                                                          rname, m.group(2), m.group(3), m.group(4),
                                                                          bname, m.group(5), m.group(6), m.group(7))
        r = Result(time=datetime.now(), winnerUser=winner[0], winnerPlayer=winner[1], loserUser=loser[0], loserPlayer=loser[1],
                   output=log)
        r.save()
        rename(TRACES_DIR + '/trace.txt', TRACES_DIR + '/%s.txt' % r.pk)
    else:
        print "no winner found, probably a script was not executable; stdout and stderr follow"
        print '===== begin stdout =====\n' + output + '\n===== end stdout'
        print '===== begin stderr =====\n' + stderr + '\n===== end stderr ====='
        
    return (winner, loser)

def runLadder(userid, player):
    print 'running the ladder for', userid, player
    challenger = (userid, player)
    
    if Result.objects.count() == 0:  # hack to handle empty ladder
        (winner, loser) = runMatch(challenger, challenger)
        return
    
    ladder = buildLadder()
    if challenger not in ladder:
        ladder.append(challenger)

    while (True):
        i = ladder.index(challenger)
        print 'challenger', challenger[1], 'index is', i
        if i == 0:
            return
        (winner, loser) = runMatch(ladder[i-1], ladder[i])
        if adjustLadder(ladder, winner, loser):  # returns True if challenger lost
            return    