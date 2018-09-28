


# import os,sys,inspect
# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0,parentdir)
#
# import detection_manager

import sys
sys.path.insert(0, '/home/frenky/PycharmProjects/url_detector/URL-detector/')
# sys.path.insert(0, '/')

from manager import detection_manager
from django.shortcuts import render
from django.http import HttpResponse

# if request.method == "POST":


# Create your views here.
def index(request: object):
    url_requested = request.GET.get('url', -1)
    if url_requested != -1:
        print('url in view: {}'.format(url_requested))

        decision = detection_manager.get_decision(url_requested)
        return render(request, 'result.html', {'decision': decision, 'url': url_requested})
    else:
        return render(request, 'home.html')
    # info = 'karel'
    # return HttpResponse('ahoj more bohumila {}'.format(info))