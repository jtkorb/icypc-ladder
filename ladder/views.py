from django.template import RequestContext
from django.shortcuts import render_to_response 
from django.http import HttpResponseRedirect
#from django.http import HttpResponse
#from django.template import Context, loader
#from django.shortcuts import get_object_or_404 
#from django.http import HttpResponse
#from django.core.urlresolvers import reverse

from models import Result
from ladderadjust import buildLadder
from dochallenge import runLadder, scriptRunnable


def index(request):
    results_list = Result.objects.order_by('-pk')
    ladder = buildLadder()
    return render_to_response('ladder/index.html', 
                              {'results_list': results_list,
                               'ladder_list': ladder},
                              context_instance=RequestContext(request))

def challenge(request):
    userid = request.POST['userid']
    player = request.POST['player']
    if scriptRunnable(userid, player):
        runLadder(userid, player)
    return HttpResponseRedirect('/ladder/')
