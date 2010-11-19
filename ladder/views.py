from django.template import RequestContext
from django.shortcuts import render_to_response 
from django.http import HttpResponseRedirect
#from django.http import HttpResponse
#from django.template import Context, loader
#from django.shortcuts import get_object_or_404 
#from django.http import HttpResponse
#from django.core.urlresolvers import reverse

from models import Result
from ladderadjust import buildLadder, countWinsLosses
from dochallenge import runLadder, scriptRunnable, script, runGauntlet
from settings import logger

def index(request):
    logger.info('in index')
    results_list = Result.objects.order_by('-pk')
    ladder = buildLadder()
    (wins, losses) = countWinsLosses()
    for i in xrange(len(ladder)):
        userid = ladder[i][0]
        player = ladder[i][1]
        upwins = wins.setdefault((userid, player), 0)
        uplosses = losses.setdefault((userid, player), 0)
        ladder[i] = (userid, player, upwins, uplosses)
        
    return render_to_response('ladder/index.html', 
                              {'results_list': results_list,
                               'ladder_list': ladder,},
                              context_instance=RequestContext(request))

def challenge(request):
    userid = request.POST['userid']
    player = request.POST['player']
    if (userid, player) == ('debug', 'reset'):
        Result.objects.all().delete()
        return HttpResponseRedirect('/ladder/index.html')
    else:
        first = Result.objects.count() # get index of first result to be created in this challenge match
        if scriptRunnable(userid, player):
            runLadder(userid, player)
        results_list = Result.objects.all()[first:]
        return render_to_response('ladder/challenge.html',
                                  {'results_list': results_list,
                                   'script': script(userid, player)}, 
                                   context_instance=RequestContext(request))

def rebuild(request):
    logger.info('in rebuild')
    first = Result.objects.count() # get index of first result to be created in this challenge match
    ladderOld = buildLadder()
    ladder = [ladderOld[0]] 
    
    for challenger in ladderOld[1:]:
        runGauntlet(challenger, ladder)
    
    results_list = Result.objects.all()[first:]
    return render_to_response('ladder/challenge.html',
                              {'results_list': results_list,}, 
                               context_instance=RequestContext(request))
