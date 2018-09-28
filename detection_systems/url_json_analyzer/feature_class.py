import json
import numpy as np
from tld import get_tld
from tld import get_fld

import sys
sys.path.insert(0, '/home/frenky/PycharmProjects/url_detector/URL-detector/')
# from compute_json import ComputeJson
from detection_systems.url_json_analyzer.compute_json import ComputeJson


class UrlJsonClass(ComputeJson):
    def __init__(self, json_dict):
        super(UrlJsonClass, self).__init__(json_dict)
        self.process_data_features()
    """
    ###################################
    ['lists'] features
    ###################################
    """

    # region ['lists'] features
    def get_1_number_ips(self) -> float:
        try:
            len_ips = len(self.json_dict_lists['ips'])
        except KeyError:
            len_ips = -1
        return float(len_ips)

    def get_2_number_countries(self) -> float:
        try:
            len_countries = len(self.json_dict_lists['countries'])
        except KeyError:
            len_countries = -1
        return float(len_countries)

    def get_3_number_asns(self) -> float:
        try:
            len_asns = len(self.json_dict_lists['asns'])
        except KeyError:
            len_asns = -1
        return float(len_asns)

    def get_4_mean_asns(self) -> float:
        try:
            asns_list = self.json_dict_lists['asns']
            asns_list_int = []
            for item in asns_list:
                try:
                    asns_list_int.append(int(item))
                except:
                    asns_list_int.append(0)
            mean = np.mean(asns_list_int)
        except KeyError:
            mean = float(-1)
        return self.check_nan(mean)

    def get_5_std_asns(self) -> float:
        try:
            asns_list = self.json_dict_lists['asns']
            asns_list_int = []
            for item in asns_list:
                try:
                    asns_list_int.append(int(item))
                except:
                    asns_list_int.append(0)
            std = np.std(asns_list_int)
        except KeyError:
            std = -1
        return self.check_nan(std)

    def get_6_number_domains(self) -> float:
        try:
            len_domains = len(self.json_dict_lists['domains'])
        except KeyError:
            len_domains = -1
        return float(len_domains)

    def get_7_diff_domains(self) -> float:
        tld_dict = {}
        try:
            domains_list = self.json_dict_lists['domains']
            for domain in domains_list:
                try:
                    top_level_domain = get_tld(domain, fix_protocol=True)
                except:
                    top_level_domain = "unknowntlddomain"
                tld_dict[top_level_domain] = 1
        except KeyError:
            return float(-1)
        try:
            return len(tld_dict.keys()) / float(len(domains_list))
        except ZeroDivisionError:
            return float(-1)

    def get_8_servers(self) -> float:
        try:
            len_servers = len(self.json_dict_lists['servers'])
        except KeyError:
            len_servers = -1
        return float(len_servers)

    def get_9_urls(self) -> float:
        try:
            len_urls = len(self.json_dict_lists['urls'])
        except KeyError:
            len_urls = -1
        return float(len_urls)

    def get_10_diff_urls(self) -> float:
        tld_dict = {}
        try:
            domains_list = self.json_dict_lists['urls']
            for domain in domains_list:
                try:
                    top_level_domain = get_tld(domain, fix_protocol=True)
                except:
                    top_level_domain = "unknowntlddomain"
                tld_dict[top_level_domain] = 1
        except KeyError:
            return float(-1)
        try:
            return len(tld_dict.keys()) / float(len(domains_list))
        except ZeroDivisionError:
            return float(-1)

    def get_11_https_in_url(self) -> float:
        try:
            domains_list = self.json_dict_lists['urls']
            https_urls = [url for url in domains_list if 'https' in url]
        except KeyError:
            return float(-1)
        try:
            return len(https_urls) / float(len(domains_list))
        except ZeroDivisionError:
            return float(-1)

    def get_12_domain_in_url(self) -> float:
        try:
            domains_list = self.json_dict_lists['urls']
            # domain_urls = [url for url in domains_list if get_fld(url) in self.main_domain]
            domain_urls = []
            for url in domains_list:
                try:
                    if get_fld(url) in self.main_domain:
                        domain_urls.append(url)
                except:
                    pass
        except KeyError:
            return float(-1)
        try:
            return len(domain_urls) / float(len(domains_list))
        except ZeroDivisionError:
            return float(-1)

    def get_13_image_in_url(self) -> float:
        images_end = ['.jpeg', '.png', '.jpg', '.gif']
        try:
            hit = 0
            domains_list = self.json_dict_lists['urls']
            for domain in domains_list:
                for ext in images_end:
                    if ext.lower() in domain.lower():
                        hit += 1
            try:
                return hit / float(len(domains_list))
            except ZeroDivisionError:
                return float(-1)
        except KeyError:
            return float(-1)

    def get_14_sizemean_url(self) -> float:
        try:
            domains_list = self.json_dict_lists['urls']
            url_lenghts = [len(url) if url is not None else 0 for url in domains_list]
            return self.check_nan(np.mean(url_lenghts))
        except KeyError:
            return float(-1)

    def get_15_sizestd_url(self) -> float:
        try:
            domains_list = self.json_dict_lists['urls']
            url_lenghts = [len(url) if url is not None else 0 for url in domains_list]
            return self.check_nan(np.std(url_lenghts))
        except KeyError:
            return float(-1)

    def get_16_javascript_url(self) -> float:
        try:
            domains_list = self.json_dict_lists['urls']
            javascript_lenghts = [url for url in domains_list if '.js' in url]
            try:
                return len(javascript_lenghts) / float(len(domains_list))
            except ZeroDivisionError:
                return float(-1)
        except :
            return float(-1)

    def get_17_javascript_url(self) -> float:
        try:
            domains_list = self.json_dict_lists['urls']
            javascript_lenghts = [url for url in domains_list if 'cookie' in url]
            try:
                return len(javascript_lenghts) / float(len(domains_list))
            except ZeroDivisionError:
                return float(-1)
        except :
            return float(-1)

    def get_18_length_linkdomains(self) -> float:
        try:
            domains_list = self.json_dict_lists['linkDomains']
            return float(len(domains_list))
        except :
            return float(-1)

    def get_19_difftld_linkdomains(self) -> float:
        tld_dict = {}
        try:
            domains_list = self.json_dict_lists['linkDomains']
            for domain in domains_list:
                try:
                    top_level_domain = get_tld(domain, fix_protocol=True)
                except:
                    top_level_domain = "unknowntlddomain"
                tld_dict[top_level_domain] = 1
            try:
                return len(tld_dict.keys()) / float(len(domains_list))
            except ZeroDivisionError:
                return float(-1)
        except :
            return float(-1)

    def get_20_numsubdomainmean_linkdomains(self) -> float:
        try:
            subdomains_list = []
            domains_list = self.json_dict_lists['linkDomains']
            for domain in domains_list:
                domain = domain.replace('www.', '')
                subdomains_list.append(len(domain.split('.')))
            return self.check_nan(np.mean(subdomains_list))
        except :
            return float(-1)

    def get_21_numsubdomainstd_linkdomains(self) -> float:
        try:
            subdomains_list = []
            domains_list = self.json_dict_lists['linkDomains']
            for domain in domains_list:
                domain = domain.replace('www.', '')
                subdomains_list.append(len(domain.split('.')))
            return self.check_nan(np.std(subdomains_list))
        except :
            return float(-1)

    def get_22_numcertificates_linkdomains(self) -> float:
        try:
            cert_list = self.json_dict_lists['certificates']
            return float(len(cert_list))
        except :
            return float(-1)

    def get_23_certicatevalidationmean_linkdomains(self) -> float:
        try:
            cert_list = self.json_dict_lists['certificates']
            cert_valid_list = []
            for cert in cert_list:
                valid_from = float(cert['validFrom'])
                valid_to = float(cert['validTo'])
                cert_valid_list.append(valid_to - valid_from)
            return self.check_nan(np.mean(cert_valid_list))
        except :
            return float(-1)

    def get_24_certicatevalidationstd_linkdomains(self) -> float:
        try:
            cert_list = self.json_dict_lists['certificates']
            cert_valid_list = []
            for cert in cert_list:
                valid_from = float(cert['validFrom'])
                valid_to = float(cert['validTo'])
                cert_valid_list.append(valid_to - valid_from)
            return self.check_nan(np.std(cert_valid_list))
        except :
            return float(-1)

    def get_25_certicatevalidation2mean_linkdomains(self) -> float:
        try:
            cert_list = self.json_dict_lists['certificates']
            cert_valid_list = []
            for cert in cert_list:
                valid_from = float(cert['validFrom'])
                valid_to = float(cert['validTo'])
                entire_time = valid_to - valid_from
                from_now_to_start = self.timestamp - valid_from
                try:
                    cert_valid_list.append(from_now_to_start / float(entire_time))
                except ZeroDivisionError:
                    cert_valid_list.append(-1)
            return self.check_nan(np.mean(cert_valid_list))
        except :
            return float(-1)

    def get_26_certicatevalidation2std_linkdomains(self) -> float:
        try:
            cert_list = self.json_dict_lists['certificates']
            cert_valid_list = []
            for cert in cert_list:
                valid_from = float(cert['validFrom'])
                valid_to = float(cert['validTo'])
                entire_time = valid_to - valid_from
                from_now_to_start = self.timestamp - valid_from
                try:
                    cert_valid_list.append(from_now_to_start / float(entire_time))
                except KeyError:
                    cert_valid_list.append(-1)
            return self.check_nan(np.std(cert_valid_list))
        except :
            return float(-1)

    # endregion

    """
    ###################################
    ['meta'] features
    ###################################
    """

    # region ['meta'] features
    def get_27_diff_countries(self) -> float:
        d = {}
        try:
            geo_ip_list = self.json_dict_meta['processors']['geoip']['data']
            for geo_ip in geo_ip_list:
                country = geo_ip['geoip']['country_name']
                d[country] = 1
            return float(len(d.keys()))
        except:
            return float(-1)

    def get_28_confidence_mean(self) -> float:
        try:
            l = []
            wappa_data_list = self.json_dict_meta['processors']['wappa']['data']
            for data in wappa_data_list:
                conf = data['confidenceTotal']
                l.append(conf)
            return self.check_nan(np.mean(l))
        except :
            return float(-1)

    def get_29_confidence_std(self) -> float:
        try:
            l = []
            wappa_data_list = self.json_dict_meta['processors']['wappa']['data']
            for data in wappa_data_list:
                conf = data['confidenceTotal']
                l.append(conf)
            return self.check_nan(np.std(l))
        except:
            return float(-1)

    def get_30_priority_mean(self) -> float:
        try:
            l = []
            wappa_data_list = self.json_dict_meta['processors']['wappa']['data']
            for data in wappa_data_list:
                k = [int(priority['priority']) if priority['priority'] is not None else 0 for priority in data['categories']]
                l.append(self.check_nan(np.mean(k)))
            return self.check_nan(np.mean(l))
        except KeyError:
            return float(-1)

    def get_31_priority_std(self) -> float:
        try:
            l = []
            wappa_data_list = self.json_dict_meta['processors']['wappa']['data']
            for data in wappa_data_list:
                k = [int(priority['priority']) if priority['priority'] is not None else 0 for priority in data['categories']]
                l.append(self.check_nan(np.mean(k)))
            return self.check_nan(np.std(l))
        except KeyError:
            return float(-1)

    def get_32_abp_len(self) -> float:
        try:
            # l = [item for item in self.json_dict_meta['processors']['abp']['data']]
            l = self.json_dict_meta['processors']['abp']['data']
            return float(len(l))
        except KeyError:
            return float(-1)

    def get_33_js_len(self) -> float:
        try:
            l = [item for item in self.json_dict_meta['processors']['abp']['data'] if item['url'] is not None and '.js' in item['url']]
            try:
                return len(l) / float(self.get_32_abp_len())
            except ZeroDivisionError:
                return float(-1)
        except KeyError:
            return float(-1)

    def get_34_cookie_len(self) -> float:
        try:
            l = [item for item in self.json_dict_meta['processors']['abp']['data'] if item['url'] is not None and 'cookie' in item['url']]
            try:
                return len(l) / float(self.get_32_abp_len())
            except ZeroDivisionError:
                return float(-1)
        except KeyError:
            return float(-1)

    def get_35_url_mean(self) -> float:
        try:
            l = [len(item['url']) if item['url'] is not None else 0 for item in self.json_dict_meta['processors']['abp']['data']]
            return self.check_nan(np.mean(l))
        except KeyError:
            return float(-1)

    def get_36_url_std(self) -> float:
        try:
            l = [len(item['url']) if item['url'] is not None else 0 for item in self.json_dict_meta['processors']['abp']['data']]
            return self.check_nan(np.std(l))
        except KeyError:
            return float(-1)
    # endregion

    """
    ###################################
    ['stats'] features
    ###################################
    """
    # region ['stats'] features
    # resourceStats
    def get_37_count_mean(self) -> float:
        try:
            count_list = [stat['count'] if stat['count'] is not None else 0 for stat in self.json_dict_stats['resourceStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_38_count_std(self) -> float:
        try:
            count_list = [stat['count'] if stat['count'] is not None else 0 for stat in self.json_dict_stats['resourceStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_39_size_mean(self) -> float:
        try:
            count_list = [stat['size'] if stat['size'] is not None else 0 for stat in self.json_dict_stats['resourceStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_40_size_std(self) -> float:
        try:
            count_list = [stat['size'] if stat['size'] is not None else 0 for stat in self.json_dict_stats['resourceStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_41_ensize_mean(self) -> float:
        try:
            count_list = [stat['encodedSize'] if stat['encodedSize'] is not None else 0 for stat in self.json_dict_stats['resourceStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_42_ensize_std(self) -> float:
        try:
            count_list = [stat['encodedSize'] if stat['encodedSize'] is not None else 0 for stat in self.json_dict_stats['resourceStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_43_latency_mean(self) -> float:
        try:
            count_list = [stat['latency'] if stat['latency'] is not None else 0 for stat in self.json_dict_stats['resourceStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_44_latency_std(self) -> float:
        try:
            count_list = [stat['latency'] if stat['latency'] is not None else 0 for stat in self.json_dict_stats['resourceStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_45_compression_mean(self) -> float:
        try:
            try:
                count_list = [float(stat['compression']) if stat['compression'] is not None else 0 for stat in self.json_dict_stats['resourceStats']]
            except ValueError:
                return float(-1)
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_46_compression_std(self) -> float:
        try:
            try:
                count_list = [float(stat['compression']) if stat['compression'] is not None else 0 for stat in self.json_dict_stats['resourceStats']]
            except ValueError:
                return float(-1)
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_47_ips_mean(self) -> float:
        try:
            count_list = [len(stat['ips']) if stat['ips'] is not None else 0 for stat in self.json_dict_stats['resourceStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_48_ips_std(self) -> float:
        try:
            count_list = [len(stat['ips']) if stat['ips'] is not None else 0 for stat in self.json_dict_stats['resourceStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_49_countries_mean(self) -> float:
        try:
            count_list = [len(stat['countries']) if stat['countries'] is not None else 0 for stat in self.json_dict_stats['resourceStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_50_countries_std(self) -> float:
        try:
            count_list = [len(stat['countries']) if stat['countries'] is not None else 0 for stat in self.json_dict_stats['resourceStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)



    # protocolStats
    def get_51_count_mean(self) -> float:
        try:
            count_list = [stat['count'] if stat['count'] is not None else 0 for stat in self.json_dict_stats['protocolStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_52_count_std(self) -> float:
        try:
            count_list = [stat['count'] if stat['count'] is not None else 0 for stat in self.json_dict_stats['protocolStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_53_size_mean(self) -> float:
        try:
            count_list = [stat['size'] if stat['size'] is not None else 0 for stat in self.json_dict_stats['protocolStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_54_size_std(self) -> float:
        try:
            count_list = [stat['size'] if stat['size'] is not None else 0 for stat in self.json_dict_stats['protocolStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_55_ensize_mean(self) -> float:
        try:
            count_list = [stat['encodedSize'] if stat['encodedSize'] is not None else 0 for stat in self.json_dict_stats['protocolStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_56_ensize_std(self) -> float:
        try:
            count_list = [stat['encodedSize'] if stat['encodedSize'] is not None else 0 for stat in self.json_dict_stats['protocolStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_57_ips_mean(self) -> float:
        try:
            count_list = [len(stat['ips']) if stat['ips'] is not None else 0 for stat in self.json_dict_stats['protocolStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_58_ips_std(self) -> float:
        try:
            count_list = [len(stat['ips']) if stat['ips'] is not None else 0 for stat in self.json_dict_stats['protocolStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_59_countries_mean(self) -> float:
        try:
            count_list = [len(stat['countries']) if stat['countries'] is not None else 0 for stat in self.json_dict_stats['protocolStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_60_countries_std(self) -> float:
        try:
            count_list = [len(stat['countries']) if stat['countries'] is not None else 0 for stat in self.json_dict_stats['protocolStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)



    # tlsStats
    def get_61_count_mean(self) -> float:
        try:
            count_list = [stat['count'] if stat['count'] is not None else 0 for stat in self.json_dict_stats['tlsStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_62_count_std(self) -> float:
        try:
            count_list = [stat['count'] if stat['count'] is not None else 0 for stat in self.json_dict_stats['tlsStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_63_size_mean(self) -> float:
        try:
            count_list = [stat['size'] if stat['size'] is not None else 0 for stat in self.json_dict_stats['tlsStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_64_size_std(self) -> float:
        try:
            count_list = [stat['size'] if stat['size'] is not None else 0 for stat in self.json_dict_stats['tlsStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_65_ensize_mean(self) -> float:
        try:
            count_list = [stat['encodedSize'] if stat['encodedSize'] is not None else 0 for stat in self.json_dict_stats['tlsStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_66_ensize_std(self) -> float:
        try:
            count_list = [stat['encodedSize'] if stat['encodedSize'] is not None else 0 for stat in self.json_dict_stats['tlsStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_67_ips_mean(self) -> float:
        try:
            count_list = [len(stat['ips']) if stat['ips'] is not None else 0 for stat in self.json_dict_stats['tlsStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_68_ips_std(self) -> float:
        try:
            count_list = [len(stat['ips']) if stat['ips'] is not None else 0 for stat in self.json_dict_stats['tlsStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_69_countries_mean(self) -> float:
        try:
            count_list = [len(stat['countries']) if stat['countries'] is not None else 0 for stat in self.json_dict_stats['tlsStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_70_countries_std(self) -> float:
        try:
            count_list = [len(stat['countries']) if stat['countries'] is not None else 0 for stat in self.json_dict_stats['tlsStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_71_protocols_mean(self) -> float:
        try:
            count_list = [len(stat['protocols']) if stat['protocols'] is not None else 0 for stat in self.json_dict_stats['tlsStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_72_protocols_std(self) -> float:
        try:
            count_list = [len(stat['protocols']) if stat['protocols'] is not None else 0 for stat in self.json_dict_stats['tlsStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)



    # serverStats
    def get_73_count_mean(self) -> float:
        try:
            count_list = [stat['count'] if stat['count'] is not None else 0 for stat in self.json_dict_stats['serverStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_74_count_std(self) -> float:
        try:
            count_list = [stat['count'] if stat['count'] is not None else 0 for stat in self.json_dict_stats['serverStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_75_size_mean(self) -> float:
        try:
            count_list = [stat['size'] if stat['size'] is not None else 0 for stat in self.json_dict_stats['serverStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_76_size_std(self) -> float:
        try:
            count_list = [stat['size'] if stat['size'] is not None else 0 for stat in self.json_dict_stats['serverStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_77_ensize_mean(self) -> float:
        try:
            count_list = [stat['encodedSize'] if stat['encodedSize'] is not None else 0 for stat in self.json_dict_stats['serverStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_78_ensize_std(self) -> float:
        try:
            count_list = [stat['encodedSize'] if stat['encodedSize'] is not None else 0 for stat in self.json_dict_stats['serverStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_79_ips_mean(self) -> float:
        try:
            count_list = [len(stat['ips']) if stat['ips'] is not None else 0 for stat in self.json_dict_stats['serverStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_80_ips_std(self) -> float:
        try:
            count_list = [len(stat['ips']) if stat['ips'] is not None else 0 for stat in self.json_dict_stats['serverStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_81_countries_mean(self) -> float:
        try:
            count_list = [len(stat['countries']) if stat['countries'] is not None else 0 for stat in self.json_dict_stats['serverStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_82_countries_std(self) -> float:
        try:
            count_list = [len(stat['countries']) if stat['countries'] is not None else 0 for stat in self.json_dict_stats['serverStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)



    # domainStats
    def get_83_count_mean(self) -> float:
        try:
            count_list = [stat['count'] if stat['count'] is not None else 0 for stat in self.json_dict_stats['domainStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_84_count_std(self) -> float:
        try:
            count_list = [stat['count'] if stat['count'] is not None else 0 for stat in self.json_dict_stats['domainStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_85_size_mean(self) -> float:
        try:
            count_list = [stat['size'] if stat['size'] is not None else 0 for stat in self.json_dict_stats['domainStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_86_size_std(self) -> float:
        try:
            count_list = [stat['size'] if stat['size'] is not None else 0 for stat in self.json_dict_stats['domainStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_87_ensize_mean(self) -> float:
        try:
            count_list = [stat['encodedSize'] if stat['encodedSize'] is not None else 0 for stat in self.json_dict_stats['domainStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_88_ensize_std(self) -> float:
        try:
            count_list = [stat['encodedSize'] if stat['encodedSize'] is not None else 0 for stat in self.json_dict_stats['domainStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_89_ips_mean(self) -> float:
        try:
            count_list = [len(stat['ips']) if stat['ips'] is not None else 0 for stat in self.json_dict_stats['domainStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_90_ips_std(self) -> float:
        try:
            count_list = [len(stat['ips']) if stat['ips'] is not None else 0 for stat in self.json_dict_stats['domainStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_91_countries_mean(self) -> float:
        try:
            count_list = [len(stat['countries']) if stat['countries'] is not None else 0 for stat in self.json_dict_stats['domainStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_92_countries_std(self) -> float:
        try:
            count_list = [len(stat['countries']) if stat['countries'] is not None else 0 for stat in self.json_dict_stats['domainStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_93_redirects_mean(self) -> float:
        try:
            count_list = [stat['redirects'] if stat['redirects'] is not None else 0 for stat in self.json_dict_stats['domainStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_94_redirects_std(self) -> float:
        try:
            count_list = [stat['redirects'] if stat['redirects'] is not None else 0 for stat in self.json_dict_stats['domainStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_95_initiators_mean(self) -> float:
        try:
            count_list = [len(stat['initiators']) if stat['initiators'] is not None else 0 for stat in self.json_dict_stats['domainStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_96_initiators_std(self) -> float:
        try:
            count_list = [len(stat['initiators']) if stat['initiators'] is not None else 0 for stat in self.json_dict_stats['domainStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_97_domain_in_initiators_mean(self) -> float:
        try:
            count_list = [1 for stat in self.json_dict_stats['domainStats'] if stat['domain'] in stat['initiators']]
            return self.check_nan(np.mean(count_list))
        except:
            return float(-1)

    def get_98_domain_in_initiators_std(self) -> float:
        try:
            count_list = [1 for stat in self.json_dict_stats['domainStats'] if stat['domain'] in stat['initiators']]
            return self.check_nan(np.std(count_list))
        except:
            return float(-1)

    # regDomainStats
    def get_99_count_mean(self) -> float:
        try:
            count_list = [stat['count'] if stat['count'] is not None else 0 for stat in self.json_dict_stats['regDomainStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_100_count_std(self) -> float:
        try:
            count_list = [stat['count'] if stat['count'] is not None else 0 for stat in self.json_dict_stats['regDomainStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_101_size_mean(self) -> float:
        try:
            count_list = [stat['size'] if stat['size'] is not None else 0 for stat in self.json_dict_stats['regDomainStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_102_size_std(self) -> float:
        try:
            count_list = [stat['size'] if stat['size'] is not None else 0 for stat in self.json_dict_stats['regDomainStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_103_ensize_mean(self) -> float:
        try:
            count_list = [stat['encodedSize'] if stat['encodedSize'] is not None else 0 for stat in self.json_dict_stats['regDomainStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_104_ensize_std(self) -> float:
        try:
            count_list = [stat['encodedSize'] if stat['encodedSize'] is not None else 0 for stat in self.json_dict_stats['regDomainStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_105_ips_mean(self) -> float:
        try:
            count_list = [len(stat['ips'])  if stat['ips'] is not None else 0 for stat in self.json_dict_stats['regDomainStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_106_ips_std(self) -> float:
        try:
            count_list = [len(stat['ips']) if stat['ips'] is not None else 0 for stat in self.json_dict_stats['regDomainStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_107_countries_mean(self) -> float:
        try:
            count_list = [len(stat['countries']) if stat['countries'] is not None else 0 for stat in self.json_dict_stats['regDomainStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_108_countries_std(self) -> float:
        try:
            count_list = [len(stat['countries']) if stat['countries'] is not None else 0 for stat in self.json_dict_stats['regDomainStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_109_redirects_mean(self) -> float:
        try:
            count_list = [stat['redirects'] if stat['redirects'] is not None else 0 for stat in self.json_dict_stats['regDomainStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_110_redirects_std(self) -> float:
        try:
            count_list = [stat['redirects'] if stat['redirects'] is not None else 0 for stat in self.json_dict_stats['regDomainStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_111_subDomains_mean(self) -> float:
        try:
            count_list = [len(stat['subDomains']) if stat['subDomains'] is not None else 0  for stat in self.json_dict_stats['regDomainStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_112_subDomains_std(self) -> float:
        try:
            count_list = [len(stat['subDomains']) if stat['subDomains'] is not None else 0 for stat in self.json_dict_stats['regDomainStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    # ipStats
    def get_113_size_mean(self) -> float:
        try:
            count_list = [stat['size'] if stat['size'] is not None else 0 for stat in self.json_dict_stats['ipStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_114_size_std(self) -> float:
        try:
            count_list = [stat['size'] if stat['size'] is not None else 0 for stat in self.json_dict_stats['ipStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_115_ensize_mean(self) -> float:
        try:
            count_list = [stat['encodedSize'] if stat['encodedSize'] is not None else 0 for stat in self.json_dict_stats['ipStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_116_ensize_std(self) -> float:
        try:
            count_list = [stat['encodedSize'] if stat['encodedSize'] is not None else 0 for stat in self.json_dict_stats['ipStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_117_countries_mean(self) -> float:
        try:
            count_list = [len(stat['countries']) if stat['countries'] is not None else 0 for stat in self.json_dict_stats['ipStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_118_countries_std(self) -> float:
        try:
            count_list = [len(stat['countries']) if stat['countries'] is not None else 0 for stat in self.json_dict_stats['ipStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_119_redirects_mean(self) -> float:
        try:
            count_list = [stat['redirects'] if stat['redirects'] is not None else 0 for stat in self.json_dict_stats['ipStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_120_redirects_std(self) -> float:
        try:
            count_list = [stat['redirects'] if stat['redirects'] is not None else 0 for stat in self.json_dict_stats['ipStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_121_ipv6_mean(self) -> float:
        try:
            count_list = [1 for stat in self.json_dict_stats['ipStats'] if stat['ipv6'] is True]
            return self.check_nan(np.mean(count_list))
        except:
            return float(-1)

    def get_122_ipv6_std(self) -> float:
        try:
            count_list = [1 for stat in self.json_dict_stats['ipStats'] if stat['ipv6'] is True]
            return self.check_nan(np.std(count_list))
        except :
            return float(-1)

    def get_123_ipv6_mean(self) -> float:
        try:
            count_list = [stat['requests'] if stat['requests'] is not None else 0 for stat in self.json_dict_stats['ipStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_124_ipv6_std(self) -> float:
        try:
            count_list = [stat['requests']  if stat['requests'] is not None else 0 for stat in self.json_dict_stats['ipStats'] ]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    def get_125_domains_mean(self) -> float:
        try:
            count_list = [len(stat['domains']) if stat['domains'] is not None else 0 for stat in self.json_dict_stats['ipStats']]
            return self.check_nan(np.mean(count_list))
        except KeyError:
            return float(-1)

    def get_126_domains_std(self) -> float:
        try:
            count_list = [len(stat['domains']) if stat['domains'] is not None else 0 for stat in self.json_dict_stats['ipStats']]
            return self.check_nan(np.std(count_list))
        except KeyError:
            return float(-1)

    # general
    def get_127_secureRequests(self) -> float:
        try:
            return float(self.json_dict_stats['secureRequests'])
        except KeyError:
            return float(-1)

    def get_128_securePercentage(self) -> float:
        try:
            return float(self.json_dict_stats['securePercentage'])
        except KeyError:
            return float(-1)

    def get_129_IPv6Percentage(self) -> float:
        try:
            return float(self.json_dict_stats['IPv6Percentage'])
        except:
            return float(-1)

    def get_130_uniqCountries(self) -> float:
        try:
            return float(self.json_dict_stats['uniqCountries'])
        except KeyError:
            return float(-1)

    def get_131_totalLinks(self) -> float:
        try:
            return float(self.json_dict_stats['totalLinks'])
        except KeyError:
            return float(-1)

    def get_132_adBlocked(self) -> float:
        try:
            return float(self.json_dict_stats['adBlocked'])
        except KeyError:
            return float(-1)

    # endregion


    def get_133_len_request(self) -> float:
        return float(self.len_main_requests)

    def get_134_domain_in_docuurl_list_mean(self) -> float:
        return self.check_nan(np.mean(self.domain_in_docuurl_list))

    def get_135_domain_in_docuurl_list_std(self) -> float:
        return self.check_nan(np.std(self.domain_in_docuurl_list))

    def get_136_upgrade_insecure_requests_mean(self) -> float:
        return self.check_nan(np.mean(self.upgrade_insecure_requests))

    def get_137_upgrade_insecure_requests_std(self) -> float:
        return self.check_nan(np.std(self.upgrade_insecure_requests))

    def get_138_status_list_mean(self) -> float:
        return self.check_nan(np.mean(self.status_list))

    def get_139_status_list_std(self) -> float:
        return self.check_nan(np.std(self.status_list))

    def get_140_content_length_mean(self) -> float:
        return self.check_nan(np.mean(self.content_length))

    def get_141_content_length_std(self) -> float:
        return self.check_nan(np.std(self.content_length))

    def get_142_encodedDataLength_mean(self) -> float:
        return self.check_nan(np.mean(self.encodedDataLength))

    def get_143_encodedDataLength_std(self) -> float:
        return self.check_nan(np.std(self.encodedDataLength))

    def get_144_requestTime_mean(self) -> float:
        return self.check_nan(np.mean(self.requestTime))

    def get_145_requestTime_std(self) -> float:
        return self.check_nan(np.std(self.requestTime))

    def get_146_proxyStart_mean(self) -> float:
        return self.check_nan(np.mean(self.proxyStart))

    def get_147_proxyStart_std(self) -> float:
        return self.check_nan(np.std(self.proxyStart))

    def get_148_proxyEnd_mean(self) -> float:
        return self.check_nan(np.mean(self.proxyEnd))

    def get_149_proxyEnd_std(self) -> float:
        return self.check_nan(np.std(self.proxyEnd))

    def get_150_dnsStart_mean(self) -> float:
        return self.check_nan(np.mean(self.dnsStart))

    def get_151_dnsStart_std(self) -> float:
        return self.check_nan(np.std(self.dnsStart))

    def get_152_dnsEnd_mean(self) -> float:
        return self.check_nan(np.mean(self.dnsEnd))

    def get_153_dnsEnd_std(self) -> float:
        return self.check_nan(np.std(self.dnsEnd))

    def get_154_connectStart_mean(self) -> float:
        return self.check_nan(np.mean(self.connectStart))

    def get_155_connectStart_std(self) -> float:
        return self.check_nan(np.std(self.connectStart))

    def get_156_connectEnd_mean(self) -> float:
        return self.check_nan(np.mean(self.connectEnd))

    def get_157_connectEnd_std(self) -> float:
        return self.check_nan(np.std(self.connectEnd))

    def get_158_sslStart_mean(self) -> float:
        return self.check_nan(np.mean(self.sslStart))

    def get_159_sslStart_std(self) -> float:
        return self.check_nan(np.std(self.sslStart))

    def get_160_sslEnd_mean(self) -> float:
        return self.check_nan(np.mean(self.sslEnd))

    def get_161_sslEnd_std(self) -> float:
        return self.check_nan(np.std(self.sslEnd))

    def get_162_workerStart_mean(self) -> float:
        return self.check_nan(np.mean(self.workerStart))

    def get_163_workerStart_std(self) -> float:
        return self.check_nan(np.std(self.workerStart))

    def get_164_workerReady_mean(self) -> float:
        return self.check_nan(np.mean(self.workerReady))

    def get_165_workerReady_std(self) -> float:
        return self.check_nan(np.std(self.workerReady))

    def get_166_sendStart_mean(self) -> float:
        return self.check_nan(np.mean(self.sendStart))

    def get_167_sendStart_std(self) -> float:
        return self.check_nan(np.std(self.sendStart))

    def get_168_sendEnd_mean(self) -> float:
        return self.check_nan(np.mean(self.sendEnd))

    def get_169_sendEnd_std(self) -> float:
        return self.check_nan(np.std(self.sendEnd))

    def get_170_pushStart_mean(self) -> float:
        return self.check_nan(np.mean(self.pushStart))

    def get_171_pushStart_std(self) -> float:
        return self.check_nan(np.std(self.pushStart))

    def get_172_pushEnd_mean(self) -> float:
        return self.check_nan(np.mean(self.pushEnd))

    def get_173_pushEnd_std(self) -> float:
        return self.check_nan(np.std(self.pushEnd))

    def get_174_receiveHeadersEnd_mean(self) -> float:
        return self.check_nan(np.mean(self.receiveHeadersEnd))

    def get_175_receiveHeadersEnd_std(self) -> float:
        return self.check_nan(np.std(self.receiveHeadersEnd))

    def get_176_len_request_list_mean(self) -> float:
        return self.check_nan(np.mean(self.len_request_list))

    def get_177_len_request_list_std(self) -> float:
        return self.check_nan(np.std(self.len_request_list))

    def get_178_response_encodedDataLength_mean(self) -> float:
        return self.check_nan(np.mean(self.response_encodedDataLength))

    def get_179_response_encodedDataLength_std(self) -> float:
        return self.check_nan(np.std(self.response_encodedDataLength))

    def get_180_response_dataLength_mean(self) -> float:
        return self.check_nan(np.mean(self.response_dataLength))

    def get_181_response_dataLength_std(self) -> float:
        return self.check_nan(np.std(self.response_dataLength))

    def get_182_response_respo_encodedDataLength_mean(self) -> float:
        return self.check_nan(np.mean(self.response_respo_encodedDataLength))

    def get_183_response_respo_encodedDataLength_std(self) -> float:
        return self.check_nan(np.std(self.response_respo_encodedDataLength))

    def get_184_response_requestTime_mean(self) -> float:
        return self.check_nan(np.mean(self.response_requestTime))

    def get_185_response_requestTime_std(self) -> float:
        return self.check_nan(np.std(self.response_requestTime))

    def get_186_response_proxyStart_mean(self) -> float:
        return self.check_nan(np.mean(self.response_proxyStart))

    def get_187_response_proxyStart_std(self) -> float:
        return self.check_nan(np.std(self.response_proxyStart))

    def get_188_response_proxyEnd_mean(self) -> float:
        return self.check_nan(np.mean(self.response_proxyEnd))

    def get_189_response_proxyEnd_std(self) -> float:
        return self.check_nan(np.std(self.response_proxyEnd))

    def get_190_response_dnsStart_mean(self) -> float:
        return self.check_nan(np.mean(self.response_dnsStart))

    def get_191_response_dnsStart_std(self) -> float:
        return self.check_nan(np.std(self.response_dnsStart))

    def get_192_response_dnsEnd_mean(self) -> float:
        return self.check_nan(np.mean(self.response_dnsEnd))

    def get_193_response_dnsEnd_std(self) -> float:
        return self.check_nan(np.std(self.response_dnsEnd))

    def get_194_response_connectStart_mean(self) -> float:
        return self.check_nan(np.mean(self.response_connectStart))

    def get_195_response_connectStart_std(self) -> float:
        return self.check_nan(np.std(self.response_connectStart))

    def get_196_response_connectEnd_mean(self) -> float:
        return self.check_nan(np.mean(self.response_connectEnd))

    def get_197_response_connectEnd_std(self) -> float:
        return self.check_nan(np.std(self.response_connectEnd))

    def get_198_response_sslStart_mean(self) -> float:
        return self.check_nan(np.mean(self.response_sslStart))

    def get_199_response_sslStart_std(self) -> float:
        return self.check_nan(np.std(self.response_sslStart))

    def get_200_response_sslEnd_mean(self) -> float:
        return self.check_nan(np.mean(self.response_sslEnd))

    def get_201_response_sslEnd_std(self) -> float:
        return self.check_nan(np.std(self.response_sslEnd))

    def get_202_response_workerStart_mean(self) -> float:
        return self.check_nan(np.mean(self.response_workerStart))

    def get_203_response_workerStart_std(self) -> float:
        return self.check_nan(np.std(self.response_workerStart))

    def get_204_response_workerReady_mean(self) -> float:
        return self.check_nan(np.mean(self.response_workerReady))

    def get_205_response_workerReady_std(self) -> float:
        return self.check_nan(np.std(self.response_workerReady))

    def get_206_response_sendStart_mean(self) -> float:
        return self.check_nan(np.mean(self.response_sendStart))

    def get_207_response_sendStart_std(self) -> float:
        return self.check_nan(np.std(self.response_sendStart))

    def get_208_response_sendEnd_mean(self) -> float:
        return self.check_nan(np.mean(self.response_sendEnd))

    def get_209_response_sendEnd_std(self) -> float:
        return self.check_nan(np.std(self.response_sendEnd))

    def get_210_response_pushStart_mean(self) -> float:
        return self.check_nan(np.mean(self.response_pushStart))

    def get_211_response_pushStart_std(self) -> float:
        return self.check_nan(np.std(self.response_pushStart))

    def get_212_response_pushEnd_mean(self) -> float:
        return self.check_nan(np.mean(self.response_pushEnd))

    def get_213_response_pushEnd_std(self) -> float:
        return self.check_nan(np.std(self.response_pushEnd))

    def get_214_response_receiveHeadersEnd_mean(self) -> float:
        return self.check_nan(np.mean(self.response_receiveHeadersEnd))

    def get_215_response_receiveHeadersEnd_std(self) -> float:
        return self.check_nan(np.std(self.response_receiveHeadersEnd))

    # ['reponse']['security']
    def get_216_securityState_mean(self) -> float:
        return self.check_nan(np.mean(self.securityState))

    def get_217_securityState_std(self) -> float:
        return self.check_nan(np.std(self.securityState))

    def get_218_sanList_mean(self) -> float:
        return self.check_nan(np.mean(self.sanList))

    def get_219_sanList_std(self) -> float:
        return self.check_nan(np.std(self.sanList))

    def get_220_subject_name_in_san_list_mean(self) -> float:
        return self.check_nan(np.mean(self.subject_name_in_san_list))

    def get_221_subject_name_in_san_list_std(self) -> float:
        return self.check_nan(np.std(self.subject_name_in_san_list))

    def get_222_cert_valid_mean(self) -> float:
        return self.check_nan(np.mean(self.cert_valid))

    def get_223_cert_valid_std(self) -> float:
        return self.check_nan(np.std(self.cert_valid))

    def get_224_cert_valid_now_mean(self) -> float:
        return self.check_nan(np.mean(self.cert_valid_now))

    def get_225_cert_valid_now_std(self) -> float:
        return self.check_nan(np.std(self.cert_valid_now))

    def get_226_hashes_list_mean(self) -> float:
        return self.check_nan(np.mean(self.hashes_list))

    def get_227_hashes_list_std(self) -> float:
        return self.check_nan(np.std(self.hashes_list))

    # ----------  cookies --------------
    def get_228_hashes_list_mean(self) -> float:
        return float(self.len_coookies)

    def get_229_cookie_expires_mean(self) -> float:
        return self.check_nan(np.mean(self.cookie_expires))

    def get_230_cookie_expires_std(self) -> float:
        return self.check_nan(np.std(self.cookie_expires))

    def get_231_cookie_expires_now_mean(self) -> float:
        return self.check_nan(np.mean(self.cookie_expires_now))

    def get_232_cookie_expires_now_std(self) -> float:
        return self.check_nan(np.std(self.cookie_expires_now))

    def get_233_cookies_sizes_mean(self) -> float:
        return self.check_nan(np.mean(self.cookies_sizes))

    def get_234_cookies_sizes_std(self) -> float:
        return self.check_nan(np.std(self.cookies_sizes))

    def get_235_cookie_http_only_mean(self) -> float:
        return self.check_nan(np.mean(self.cookie_http_only))

    def get_236_cookie_http_only_std(self) -> float:
        return self.check_nan(np.std(self.cookie_http_only))

    def get_237_cookie_secure_mean(self) -> float:
        return self.check_nan(np.mean(self.cookie_secure))

    def get_238_cookie_secure_std(self) -> float:
        return self.check_nan(np.std(self.cookie_secure))

    def get_239_cookie_session_mean(self) -> float:
        return self.check_nan(np.mean(self.cookie_session))

    def get_240_cookie_session_std(self) -> float:
        return self.check_nan(np.std(self.cookie_session))

    # ----------  links --------------
    def get_241_len_links(self) -> float:
        return float(self.len_links)

    def get_242_links_domain_in_url_mean(self) -> float:
        return self.check_nan(np.mean(self.links_domain_in_url))

    def get_243_links_domain_in_url_std(self) -> float:
        return self.check_nan(np.std(self.links_domain_in_url))

    def get_244_diff_tld(self) -> float:
        return float(self.diff_tld)

    # ---------- globals -------------------
    def get_245_diff_tld(self) -> float:
        return float(self.len_globals)

    def get_246_diff_globals(self) -> float:
        return float(self.diff_globals)

    def temp(self):
        pass

