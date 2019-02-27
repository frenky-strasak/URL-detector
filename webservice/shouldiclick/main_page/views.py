import os
import sys

sys.path.insert(0, '/'.join(os.getcwd().split('/')[:-2]) + '/')

from webservice.shouldiclick.main_page.manager import detection_manager
from django.shortcuts import render


def get_client_ip(request: object):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Create your views here.
def index(request: object):
    print('########### NEW REQUEST ###################')
    # print(request)
    # print('##############################')

    url_requested = request.GET.get('url', -1)
    if url_requested != -1:
        """
        Scan url.
        """
        if len(url_requested) > 500:
            return render(request, 'result.html', {'decision': 2, 'url': url_requested, 'feed_back_done': 0})
        print('url to scan: {}'.format(url_requested))
        user_ip = get_client_ip(request)
        decision, remaining_time = detection_manager.get_decision(str(url_requested), user_ip)
        if decision != -10:
            """
            The url was in database.
            """
            return render(request, 'result.html', {'decision': decision, 'url': url_requested, 'feed_back_done': 0})
        else:
            """
            The url was NOT in database. Say client to wait for responds and ask for some time latter.
            """
            request_back = 'http://192.168.43.32:8000/?url={}'.format(url_requested)
            return render(request, 'wait.html', {'url_to_request': request_back, 'remaining_time': remaining_time * 1000})

    url_requested_feedback = request.GET.get('feedback', -1)
    if url_requested_feedback != -1:
        """
        Feedback.
        """
        if len(url_requested_feedback) > 500:
            return render(request, 'result.html', {'decision': 2, 'url': 'None', 'feed_back_done': 0})
        split_argument = str(url_requested_feedback).split('<<:')
        print(split_argument)
        if len(split_argument) != 3:
            return render(request, 'result.html', {'decision': -1, 'url': '?', 'feed_back_done': 1})
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
        decision = detection_manager.save_feedback(str(url), user_ip, detection_result, feedack)

        if decision == -11:
            return render(request, 'result.html', {'decision': decision, 'url': 'None', 'feed_back_done': 0})
        return render(request, 'result.html', {'decision': detection_result, 'url': url, 'feed_back_done': 1})


    return render(request, 'home.html')
