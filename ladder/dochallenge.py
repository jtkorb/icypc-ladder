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

import logging

logger = logging.getLogger(__name__)

LOG_FILENAME = TRACES_DIR + '/ladder.log'
logging.basicConfig(filename=LOG_FILENAME, 
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='[%d-%m-%Y %H:%M:%S]',
                    level=logging.DEBUG,
                    )

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
#
## create formatter
formatter = logging.Formatter("%(asctime)s %(name)s: %(levelname)s - %(message)s", '[%d/%b/%Y %H:%M:%S]')

## add formatter to ch
ch.setFormatter(formatter)

## add ch to logger
logger.addHandler(ch)


runtemplate = 'java -jar %s -player pipe 1 %s -player pipe 1 %s -view trace %s/trace.txt'

def script(userid, player):
    return expanduser('~' + userid) + '/icypc/' + player

def scriptRunnable(userid, player):
    s = script(userid, player)
    try:
        mode = stat(s).st_mode  # get mode bits of script file
    except OSError:
        logger.error("script %s not found" % s)
        return False
    if (mode & 5) != 5: # check for +rx bit set for world
        logger.error('script %s is not executable (r+x) for world' % s)
        return False
    return True

S_IFDIR = 0040000        

def makeTraceDir():
    try:
        mode = stat(TRACES_DIR).st_mode
        if (mode & S_IFDIR == 0):
            logger.critical('%s is not a directory or not accessible -- tell a friend' % TRACES_DIR)
    except OSError:
        print 'making', TRACES_DIR
        try:
            makedirs(TRACES_DIR)
        except:
            logger.critical('could not create %s == tell a friend' % TRACES_DIR)

output_pattern = re.compile(r'.*Winner: (\d+)\sScore: (\d+) \((\d+) (\d+)\) (\d+) \((\d+) (\d+)\)', re.DOTALL)

def runMatch(red, blue):
    (redUser, redPlayer) = red
    (blueUser, bluePlayer) = blue

    rname = redUser + '/' + redPlayer
    bname = blueUser + '/' + bluePlayer
    logger.info('playing %s vs. %s' % (rname, bname))
    
    makeTraceDir()
    command = (runtemplate % (ICYPC_JAR, script(redUser, redPlayer), script(blueUser, bluePlayer), TRACES_DIR)).split()
    logger.info('running: "%s"' % command)
    
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, stderr) = p.communicate();
    m = output_pattern.match(output)
    
    (winner, loser) = (red, blue) # default
    if m:
        logger.info('winner is %s' % m.group(1))
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
        
        try:
            f = open('%s/%s-stdout.txt' % (TRACES_DIR, r.pk), 'w'); f.write(output); f.close()
            f = open('%s/%s-stderr.txt' % (TRACES_DIR, r.pk), 'w'); f.write(stderr); f.close()
        except:
            logger.critical('could not write std out/err files in %s--tell a friend' % TRACES_DIR)
    else:
        logger.error('no winner found in stdout; probably a script was not executable; stdout and stderr follow')
        logger.error('===== begin stdout =====\n%s\n===== end stdout' % output)
        logger.error('===== begin stderr =====\n%s\n===== end stderr' % stderr)
        
        
    return (winner, loser)

def runLadder(userid, player):
    logger.info('running the ladder for %s/%s' % (userid, player))
    challenger = (userid, player)
    
    if Result.objects.count() == 0:  # hack to handle empty ladder
        (winner, loser) = runMatch(challenger, challenger)
        return
    
    ladder = buildLadder()
    if challenger not in ladder:
        ladder.append(challenger)

    while (True):
        i = ladder.index(challenger)
        if i == 0:
            return
        (winner, loser) = runMatch(ladder[i-1], ladder[i])
        if adjustLadder(ladder, winner, loser):  # returns True if challenger lost
            return    