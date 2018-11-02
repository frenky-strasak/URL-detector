


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

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print('host_ip: {}'.format(ip))
    return ip


# Create your views here.
def index(request: object):
    print('##############################')
    print(request)
    print('##############################')
    url_requested = request.GET.get('url', -1)
    url_requested_feedback = request.GET.get('feedback', -1)
    if url_requested != -1:
        """
        Scan url.
        """
        if len(url_requested) > 100:
            return render(request, 'result.html', {'decision': 2, 'url': url_requested, 'feed_back_done': 0})
        print('url to scan: {}'.format(url_requested))
        user_ip = get_client_ip(request)
        decision = detection_manager.get_decision(str(url_requested), user_ip)
        return render(request, 'result.html', {'decision': decision, 'url': url_requested, 'feed_back_done': 0})
    elif url_requested_feedback != -1:
        """
        Send feedback.
        """
        split_argument = str(url_requested_feedback).split(':')
        if len(split_argument) != 3:
            return render(request, 'result.html', {'decision': -1, 'url': 'hello.com', 'feed_back_done': 1})
        url, detection_result, feedack = split_argument
        try:
            detection_result = int(detection_result)
        except:
            return render(request, 'result.html', {'decision': -1, 'url': url, 'feed_back_done': 1})
        try:
            feedack = int(feedack)
        except:
            return render(request, 'result.html', {'decision': -1, 'url': url, 'feed_back_done': 1})
        user_ip = get_client_ip(request)
        detection_manager.save_feedback(str(url), user_ip, detection_result, feedack)
        return render(request, 'result.html', {'decision': detection_result, 'url': url, 'feed_back_done': 1})
    else:
        return render(request, 'home.html')
