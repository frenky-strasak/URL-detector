
import json
import numpy as np
from tld import get_tld
from tld import get_fld


class ComputeJson:
    def __init__(self, json_dict):
        self.default = '####################'
        self.json_dict = json_dict
        try:
            self.main_url = self.json_dict['page']['url']  # https://www.seznam.cz/
        except:
            self.main_url = self.default
        try:
            self.main_domain = self.json_dict['page']['domain']  # www.seznam.cz
        except:
            self.main_domain = self.default
        self.timestamp = self.get_unixtime(self.json_dict['task']['time'])
        self.json_dict_lists = self.json_dict['lists']
        self.json_dict_meta = self.json_dict['meta']
        self.json_dict_stats = self.json_dict['stats']
        self.json_dict_data = self.json_dict['data']

        self.check_variables()
        """
        Features for data. Data block can be quite big so in this development version we will process it just once.
        In next verison rest of the features will be processed just once too.
        """
        # data
        self.len_main_requests = 0
        self.len_coookies = 0
        # request
        self.domain_in_docuurl_list = []
        self.upgrade_insecure_requests = []
        self.status_list = []
        self.content_length = []
        self.encodedDataLength = []
        ### timing
        self.requestTime = []
        self.proxyStart = []
        self.proxyEnd = []
        self.dnsStart = []
        self.dnsEnd = []
        self.connectStart = []
        self.connectEnd = []
        self.sslStart = []
        self.sslEnd = []
        self.workerStart = []
        self.workerReady = []
        self.sendStart = []
        self.sendEnd = []
        self.pushStart = []
        self.pushEnd = []
        self.receiveHeadersEnd = []

        self.len_request_list = []

        # response
        self.response_encodedDataLength = []
        self.response_dataLength = []
        self.response_respo_encodedDataLength = []
        ### timing
        self.response_requestTime = []
        self.response_proxyStart = []
        self.response_proxyEnd = []
        self.response_dnsStart = []
        self.response_dnsEnd = []
        self.response_connectStart = []
        self.response_connectEnd = []
        self.response_sslStart = []
        self.response_sslEnd = []
        self.response_workerStart = []
        self.response_workerReady = []
        self.response_sendStart = []
        self.response_sendEnd = []
        self.response_pushStart = []
        self.response_pushEnd = []
        self.response_receiveHeadersEnd = []
        ### security
        self.securityState = []
        self.sanList = []
        self.subject_name_in_san_list = []
        self.cert_valid = []
        self.cert_valid_now = []
        ### hashes
        self.hashes_list = []

        # cookies
        self.cookie_expires = []
        self.cookie_expires_now = []
        self.cookies_sizes = []
        self.cookie_http_only = []
        self.cookie_secure = []
        self.cookie_session = []

        # links
        self.len_links = 0
        self.diff_tld = 0
        self.links_domain_in_url = []

        # global
        self.len_globals = 0
        self.diff_globals = 0

    """
   ###################################
   ['data'] features
   ###################################
   """

    # region ['data'] features
    def process_data_features(self) -> None:
        # print('ahoj more: {}'.format(len(self.json_dict_data['requests'])))
        try:
            self.len_main_requests = len(self.json_dict_data['requests'])
            for request in self.json_dict_data['requests']:
                try:
                    try:
                        res = 1 if self.main_domain in request['request']['documentURL'] else 0
                    except:
                        res = -1
                    self.domain_in_docuurl_list.append(float(res))
                except :
                    self.domain_in_docuurl_list.append(-1)

                try:
                    res = request['request']['request']['headers']['Upgrade-Insecure-Requests']
                    self.upgrade_insecure_requests.append(int(res))
                except :
                    self.upgrade_insecure_requests.append(0)

                try:
                    res = request['request']['redirectResponse']['status']
                    self.status_list.append(float(res))
                except :
                    self.status_list.append(0)

                try:
                    res = request['request']['redirectResponse']['headers']['Content-Length']
                    self.content_length.append(int(res))
                except :
                    self.content_length.append(0)

                try:
                    res = request['request']['redirectResponse']['encodedDataLength']
                    self.encodedDataLength.append(float(res))
                except :
                    self.encodedDataLength.append(0)

                try:
                    res = request['request']['redirectResponse']['timing']['requestTime']
                    self.requestTime.append(float(res))
                except :
                    self.requestTime.append(0)

                try:
                    res = request['request']['redirectResponse']['timing']['proxyStart']
                    self.proxyStart.append(float(res))
                except :
                    self.proxyStart.append(0)

                try:
                    res = request['request']['redirectResponse']['timing']['proxyEnd']
                    self.proxyEnd.append(float(res))
                except :
                    self.proxyEnd.append(0)

                try:
                    res = request['request']['redirectResponse']['timing']['dnsStart']
                    self.dnsStart.append(float(res))
                except :
                    self.dnsStart.append(0)

                try:
                    res = request['request']['redirectResponse']['timing']['dnsEnd']
                    self.dnsEnd.append(float(res))
                except :
                    self.dnsEnd.append(0)

                try:
                    res = request['request']['redirectResponse']['timing']['connectStart']
                    self.connectStart.append(float(res))
                except :
                    self.connectStart.append(0)

                try:
                    res = request['request']['redirectResponse']['timing']['connectEnd']
                    self.connectEnd.append(float(res))
                except :
                    self.connectEnd.append(0)

                try:
                    res = request['request']['redirectResponse']['timing']['sslStart']
                    self.sslStart.append(float(res))
                except :
                    self.sslStart.append(0)

                try:
                    res = request['request']['redirectResponse']['timing']['sslEnd']
                    self.sslEnd.append(float(res))
                except :
                    self.sslEnd.append(0)

                try:
                    res = request['request']['redirectResponse']['timing']['workerStart']
                    self.workerStart.append(float(res))
                except :
                    self.workerStart.append(0)

                try:
                    res = request['request']['redirectResponse']['timing']['workerReady']
                    self.workerReady.append(float(res))
                except :
                    self.workerReady.append(0)

                try:
                    res = request['request']['redirectResponse']['timing']['sendStart']
                    self.sendStart.append(float(res))
                except :
                    self.sendStart.append(0)

                try:
                    res = request['request']['redirectResponse']['timing']['sendEnd']
                    self.sendEnd.append(float(res))
                except :
                    self.sendEnd.append(0)

                try:
                    res = request['request']['redirectResponse']['timing']['pushStart']
                    self.pushStart.append(float(res))
                except :
                    self.pushStart.append(0)

                try:
                    res = request['request']['redirectResponse']['timing']['pushEnd']
                    self.pushEnd.append(float(res))
                except :
                    self.pushEnd.append(0)

                try:
                    res = request['request']['redirectResponse']['timing']['receiveHeadersEnd']
                    self.receiveHeadersEnd.append(float(res))
                except :
                    self.receiveHeadersEnd.append(0)

                # ['requests']
                try:
                    self.len_request_list.append(len(request['requests']))
                except :
                    self.len_request_list.append(-1)

                # ['response']
                try:
                    res = request['response']['encodedDataLength']
                    self.response_encodedDataLength.append(float(res))
                except :
                    self.response_encodedDataLength.append(0)

                try:
                    res = request['response']['dataLength']
                    self.response_dataLength.append(float(res))
                except :
                    self.response_dataLength.append(0)

                try:
                    res = request['response']['response']['encodedDataLength']
                    self.response_respo_encodedDataLength.append(float(res))
                except :
                    self.response_respo_encodedDataLength.append(0)

                # ['response']['timing']
                try:
                    res = request['response']['response']['timing']['requestTime']
                    self.response_requestTime.append(float(res))
                except :
                    self.response_requestTime.append(0)

                try:
                    res = request['response']['response']['timing']['proxyStart']
                    self.response_proxyStart.append(float(res))
                except :
                    self.response_proxyStart.append(0)

                try:
                    res = request['response']['response']['timing']['proxyEnd']
                    self.response_proxyEnd.append(float(res))
                except :
                    self.response_proxyEnd.append(0)

                try:
                    res = request['response']['response']['timing']['dnsStart']
                    self.response_dnsStart.append(float(res))
                except :
                    self.response_dnsStart.append(0)

                try:
                    res = request['response']['response']['timing']['dnsEnd']
                    self.response_dnsEnd.append(float(res))
                except :
                    self.response_dnsEnd.append(0)

                try:
                    res = request['response']['response']['timing']['connectStart']
                    self.response_connectStart.append(float(res))
                except :
                    self.response_connectStart.append(0)

                try:
                    res = request['response']['response']['timing']['connectEnd']
                    self.response_connectEnd.append(float(res))
                except :
                    self.response_connectEnd.append(0)

                try:
                    res = request['response']['response']['timing']['sslStart']
                    self.response_sslStart.append(float(res))
                except :
                    self.response_sslStart.append(0)

                try:
                    res = request['response']['response']['timing']['sslEnd']
                    self.response_sslEnd.append(float(res))
                except :
                    self.response_sslEnd.append(0)

                try:
                    res = request['response']['response']['timing']['workerStart']
                    self.response_workerStart.append(float(res))
                except :
                    self.response_workerStart.append(0)

                try:
                    res = request['response']['response']['timing']['workerReady']
                    self.response_workerReady.append(float(res))
                except :
                    self.response_workerReady.append(0)

                try:
                    res = request['response']['response']['timing']['sendStart']
                    self.response_sendStart.append(float(res))
                except :
                    self.response_sendStart.append(0)

                try:
                    res = request['response']['response']['timing']['sendEnd']
                    self.response_sendEnd.append(float(res))
                except :
                    self.response_sendEnd.append(0)

                try:
                    res = request['response']['response']['timing']['pushStart']
                    self.response_pushStart.append(float(res))
                except :
                    self.response_pushStart.append(0)

                try:
                    res = request['response']['response']['timing']['pushEnd']
                    self.response_pushEnd.append(float(res))
                except :
                    self.response_pushEnd.append(0)

                try:
                    res = request['response']['response']['timing']['receiveHeadersEnd']
                    self.response_receiveHeadersEnd.append(float(res))
                except :
                    self.response_receiveHeadersEnd.append(0)

                # ['reponse']['security']
                try:
                    res = request['response']['response']['securityState']
                    if 'secure' in res:
                        self.securityState.append(0)
                    else:
                        self.securityState.append(1)
                except :
                    self.securityState.append(-1)

                try:
                    res = request['response']['response']['securityDetails']['sanList']
                    self.sanList.append(len(res))
                except :
                    self.sanList.append(-1)

                try:
                    san_list = request['response']['response']['securityDetails']['sanList']
                    subject_name = request['response']['response']['securityDetails']['subjectName']
                    if subject_name in san_list:
                        self.subject_name_in_san_list.append(1)
                    else:
                        self.subject_name_in_san_list.append(0)
                except :
                    self.subject_name_in_san_list.append(-1)

                try:
                    validFrom = request['response']['response']['securityDetails']['validFrom']
                    validTo = request['response']['response']['securityDetails']['validTo']
                    self.cert_valid.append(validTo - validFrom)
                except :
                    self.cert_valid.append(-1)

                try:
                    validFrom = request['response']['response']['securityDetails']['validFrom']
                    validTo = request['response']['response']['securityDetails']['validTo']
                    if validFrom < self.timestamp < validTo:
                        self.cert_valid_now.append(1)
                    else:
                        self.cert_valid_now.append(0)
                except :
                    self.cert_valid_now.append(-1)

                # hash
                try:
                    hash_size = request['response']['size']
                    self.hashes_list.append(hash_size)
                except :
                    self.hashes_list.append(-1)

        except :
            print('Error: data json part (requests and responds) were not proceeds.')

        try:
            # ----------  cookies --------------
            self.len_coookies = len(self.json_dict_data['cookies'])
            for cookie in self.json_dict_data['cookies']:
                try:
                    try:
                        hash_size = float(cookie['expires'])
                    except:
                        hash_size = 0
                    self.cookie_expires.append(hash_size)
                except :
                    self.cookie_expires.append(-1)

                try:
                    try:
                        expire_time = float(cookie['expires'])
                    except:
                        expire_time = 0
                    self.cookie_expires_now.append(expire_time - self.timestamp)
                except :
                    self.cookie_expires_now.append(-1)

                try:
                    try:
                        expire_time = float(cookie['size'])
                    except:
                        expire_time = 0
                    self.cookies_sizes.append(expire_time)
                except :
                    self.cookies_sizes.append(-1)

                try:
                    try:
                        res = bool(cookie['httpOnly'])
                    except:
                        res = False
                    l = 1 if res is False else 2
                    self.cookie_http_only.append(l)
                except :
                    self.cookie_http_only.append(-1)

                try:
                    try:
                        res = bool(cookie['secure'])
                    except:
                        res = False
                    l = 1 if res is False else 2
                    self.cookie_secure.append(l)
                except :
                    self.cookie_secure.append(-1)

                try:
                    try:
                        res = bool(cookie['session'])
                    except:
                        res = False
                    l = 1 if res is False else 2
                    self.cookie_session.append(l)
                except :
                    self.cookie_session.append(-1)

        except :
            print('Error: data json part (cookies) were not proceeds.')

        try:
            # ----------  links --------------
            # get_tld(domain, fix_protocol=True)
            self.len_links = len(self.json_dict_data['links'])
            d = {}
            for link in self.json_dict_data['links']:
                try:
                    url = link['href']
                    try:
                        _tld = get_tld(url, fix_protocol=True)
                    except:
                        _tld = "unknowntlddomain"
                    d[_tld] = 1
                except :
                    pass

                try:
                    url = link['href']
                    if self.main_domain in url:
                        self.links_domain_in_url.append(1)
                    else:
                        self.links_domain_in_url.append(0)
                except :
                    self.links_domain_in_url.append(-1)

            self.diff_tld = len(d.keys())
        except :
            print('Error: data json part (links) were not proceeds.')

        try:
            # ---------- globals -------------------
            self.len_globals = len(self.json_dict_data['globals'])
            d = {}
            for _global in self.json_dict_data['globals']:
                try:
                    type = _global['type']
                    d[type] = 1
                except :
                    pass
            self.diff_globals = len(d.keys())
        except :
            print('Error: data json part (globals) were not proceeds.')

            # endregion

    def check_nan(self, value: float) -> float:
        if np.isnan(value):
            return float(-1)
        return value


    def get_unixtime(self, time_string: str) -> float:
        tmp = np.datetime64(time_string)
        unixtime = tmp.view('<i8') / 1e3
        return unixtime


    def check_variables(self):
        if self.main_domain is None or self.main_domain == '':
            self.main_domain = self.default
        if self.main_url is None or self.main_url == '':
            self.main_url = self.default