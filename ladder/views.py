from models import Result
#from models import Challenger
#from django.http import HttpResponse
#from django.template import Context, loader
from django.shortcuts import get_object_or_404, render_to_response 
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from datetime import datetime
from ladderadjust import buildLadder

def index(request):
    results_list = Result.objects.all()
    ladder = buildLadder(results_list)
#    challengers_list = Challenger.objects.all()
    return render_to_response('ladder/index.html', 
                              {'results_list': results_list,
#                               'challengers_list': challengers_list,
                               'ladder_list': ladder},
                              context_instance=RequestContext(request))

from dochallenge import runLadder

def challenge(request):
    userid = request.POST['userid']
    player = request.POST['player']
#    c = Challenger(time=datetime.now(), user=userid, player=player)
#    c.save()
    runLadder(userid, player)
    return HttpResponseRedirect('/ladder/')
