
feature_names= [    'get_1_number_ips()',
    'get_2_number_countries()',
    'get_3_number_asns()',
    'get_4_mean_asns()',
    'get_5_std_asns()',
    'get_6_number_domains()',
    'get_7_diff_domains()',
    'get_8_servers()',
    'get_9_urls()',
    'get_10_diff_urls()',
    'get_11_https_in_url()',
    'get_12_domain_in_url()',
    'get_13_image_in_url()',
    'get_14_sizemean_url()',
    'get_15_sizestd_url()',
    'get_16_javascript_url()',
    'get_17_javascript_url()',
    'get_18_length_linkdomains()',
    'get_19_difftld_linkdomains()',
    'get_20_numsubdomainmean_linkdomains()',
    'get_21_numsubdomainstd_linkdomains()',
    'get_22_numcertificates_linkdomains()',
    'get_23_certicatevalidationmean_linkdomains()',
    'get_24_certicatevalidationstd_linkdomains()',
    'get_25_certicatevalidation2mean_linkdomains()',
    'get_26_certicatevalidation2std_linkdomains()',
    'get_27_diff_countries()',
    'get_28_confidence_mean()',
    'get_29_confidence_std()',
    'get_30_priority_mean()',
    'get_31_priority_std()',
    'get_32_abp_len()',
    'get_33_js_len()',
    'get_34_cookie_len()',
    'get_35_url_mean()',
    'get_36_url_std()',
    'get_37_count_mean()',
    'get_38_count_std()',
    'get_39_size_mean()',
    'get_40_size_std()',
    'get_41_ensize_mean()',
    'get_42_ensize_std()',
    'get_43_latency_mean()',
    'get_44_latency_std()',
    'get_45_compression_mean()',
    'get_46_compression_std()',
    'get_47_ips_mean()',
    'get_48_ips_std()',
    'get_49_countries_mean()',
    'get_50_countries_std()',
    'get_51_count_mean()',
    'get_52_count_std()',
    'get_53_size_mean()',
    'get_54_size_std()',
    'get_55_ensize_mean()',
    'get_56_ensize_std()',
    'get_57_ips_mean()',
    'get_58_ips_std()',
    'get_59_countries_mean()',
    'get_60_countries_std()',
    'get_61_count_mean()',
    'get_62_count_std()',
    'get_63_size_mean()',
    'get_64_size_std()',
    'get_65_ensize_mean()',
    'get_66_ensize_std()',
    'get_67_ips_mean()',
    'get_68_ips_std()',
    'get_69_countries_mean()',
    'get_70_countries_std()',
    'get_71_protocols_mean()',
    'get_72_protocols_std()',
    'get_73_count_mean()',
    'get_74_count_std()',
    'get_75_size_mean()',
    'get_76_size_std()',
    'get_77_ensize_mean()',
    'get_78_ensize_std()',
    'get_79_ips_mean()',
    'get_80_ips_std()',
    'get_81_countries_mean()',
    'get_82_countries_std()',
    'get_83_count_mean()',
    'get_84_count_std()',
    'get_85_size_mean()',
    'get_86_size_std()',
    'get_87_ensize_mean()',
    'get_88_ensize_std()',
    'get_89_ips_mean()',
    'get_90_ips_std()',
    'get_91_countries_mean()',
    'get_92_countries_std()',
    'get_93_redirects_mean()',
    'get_94_redirects_std()',
    'get_95_initiators_mean()',
    'get_96_initiators_std()',
    'get_97_domain_in_initiators_mean()',
    'get_98_domain_in_initiators_std()',
    'get_99_count_mean()',
    'get_100_count_std()',
    'get_101_size_mean()',
    'get_102_size_std()',
    'get_103_ensize_mean()',
    'get_104_ensize_std()',
    'get_105_ips_mean()',
    'get_106_ips_std()',
    'get_107_countries_mean()',
    'get_108_countries_std()',
    'get_109_redirects_mean()',
    'get_110_redirects_std()',
    'get_111_subDomains_mean()',
    'get_112_subDomains_std()',
    'get_113_size_mean()',
    'get_114_size_std()',
    'get_115_ensize_mean()',
    'get_116_ensize_std()',
    'get_117_countries_mean()',
    'get_118_countries_std()',
    'get_119_redirects_mean()',
    'get_120_redirects_std()',
    'get_121_ipv6_mean()',
    'get_122_ipv6_std()',
    'get_123_ipv6_mean()',
    'get_124_ipv6_std()',
    'get_125_domains_mean()',
    'get_126_domains_std()',
    'get_127_secureRequests()',
    'get_128_securePercentage()',
    'get_129_IPv6Percentage()',
    'get_130_uniqCountries()',
    'get_131_totalLinks()',
    'get_132_adBlocked()',
    'get_133_len_request()',
    'get_134_domain_in_docuurl_list_mean()',
    'get_135_domain_in_docuurl_list_std()',
    'get_136_upgrade_insecure_requests_mean()',
    'get_137_upgrade_insecure_requests_std()',
    'get_138_status_list_mean()',
    'get_139_status_list_std()',
    'get_140_content_length_mean()',
    'get_141_content_length_std()',
    'get_142_encodedDataLength_mean()',
    'get_143_encodedDataLength_std()',
    'get_144_requestTime_mean()',
    'get_145_requestTime_std()',
    'get_146_proxyStart_mean()',
    'get_147_proxyStart_std()',
    'get_148_proxyEnd_mean()',
    'get_149_proxyEnd_std()',
    'get_150_dnsStart_mean()',
    'get_151_dnsStart_std()',
    'get_152_dnsEnd_mean()',
    'get_153_dnsEnd_std()',
    'get_154_connectStart_mean()',
    'get_155_connectStart_std()',
    'get_156_connectEnd_mean()',
    'get_157_connectEnd_std()',
    'get_158_sslStart_mean()',
    'get_159_sslStart_std()',
    'get_160_sslEnd_mean()',
    'get_161_sslEnd_std()',
    'get_162_workerStart_mean()',
    'get_163_workerStart_std()',
    'get_164_workerReady_mean()',
    'get_165_workerReady_std()',
    'get_166_sendStart_mean()',
    'get_167_sendStart_std()',
    'get_168_sendEnd_mean()',
    'get_169_sendEnd_std()',
    'get_170_pushStart_mean()',
    'get_171_pushStart_std()',
    'get_172_pushEnd_mean()',
    'get_173_pushEnd_std()',
    'get_174_receiveHeadersEnd_mean()',
    'get_175_receiveHeadersEnd_std()',
    'get_176_len_request_list_mean()',
    'get_177_len_request_list_std()',
    'get_178_response_encodedDataLength_mean()',
    'get_179_response_encodedDataLength_std()',
    'get_180_response_dataLength_mean()',
    'get_181_response_dataLength_std()',
    'get_182_response_respo_encodedDataLength_mean()',
    'get_183_response_respo_encodedDataLength_std()',
    'get_184_response_requestTime_mean()',
    'get_185_response_requestTime_std()',
    'get_186_response_proxyStart_mean()',
    'get_187_response_proxyStart_std()',
    'get_188_response_proxyEnd_mean()',
    'get_189_response_proxyEnd_std()',
    'get_190_response_dnsStart_mean()',
    'get_191_response_dnsStart_std()',
    'get_192_response_dnsEnd_mean()',
    'get_193_response_dnsEnd_std()',
    'get_194_response_connectStart_mean()',
    'get_195_response_connectStart_std()',
    'get_196_response_connectEnd_mean()',
    'get_197_response_connectEnd_std()',
    'get_198_response_sslStart_mean()',
    'get_199_response_sslStart_std()',
    'get_200_response_sslEnd_mean()',
    'get_201_response_sslEnd_std()',
    'get_202_response_workerStart_mean()',
    'get_203_response_workerStart_std()',
    'get_204_response_workerReady_mean()',
    'get_205_response_workerReady_std()',
    'get_206_response_sendStart_mean()',
    'get_207_response_sendStart_std()',
    'get_208_response_sendEnd_mean()',
    'get_209_response_sendEnd_std()',
    'get_210_response_pushStart_mean()',
    'get_211_response_pushStart_std()',
    'get_212_response_pushEnd_mean()',
    'get_213_response_pushEnd_std()',
    'get_214_response_receiveHeadersEnd_mean()',
    'get_215_response_receiveHeadersEnd_std()',
    'get_216_securityState_mean()',
    'get_217_securityState_std()',
    'get_218_sanList_mean()',
    'get_219_sanList_std()',
    'get_220_subject_name_in_san_list_mean()',
    'get_221_subject_name_in_san_list_std()',
    'get_222_cert_valid_mean()',
    'get_223_cert_valid_std()',
    'get_224_cert_valid_now_mean()',
    'get_225_cert_valid_now_std()',
    'get_226_hashes_list_mean()',
    'get_227_hashes_list_std()',
    'get_228_hashes_list_mean()',
    'get_229_cookie_expires_mean()',
    'get_230_cookie_expires_std()',
    'get_231_cookie_expires_now_mean()',
    'get_232_cookie_expires_now_std()',
    'get_233_cookies_sizes_mean()',
    'get_234_cookies_sizes_std()',
    'get_235_cookie_http_only_mean()',
    'get_236_cookie_http_only_std()',
    'get_237_cookie_secure_mean()',
    'get_238_cookie_secure_std()',
    'get_239_cookie_session_mean()',
    'get_240_cookie_session_std()',
    'get_241_len_links()',
    'get_242_links_domain_in_url_mean()',
    'get_243_links_domain_in_url_std()',
    'get_244_diff_tld()',
    'get_245_diff_tld()',
    'get_246_diff_globals()',

]
















import numpy as np

"""
Import features from files to vectors. 
"""
X_malware = np.load('malware_json_features.npy')
X_normal = np.load('normal_json_features.npy')
# X_normal = X_normal[:10258]

print('malware shape {}'.format(X_malware.shape))
print('normal shape {}'.format(X_normal.shape))

"""
Merge vectors and create labels.
"""
X = np.concatenate((X_malware, X_normal), axis=0)
y = np.array([1 for i in range(X_malware.shape[0])] + [0 for j in range(X_normal.shape[0])])


import sys
total = 0
for i, x in enumerate(X):
    for j,_x in enumerate(x):
        if np.isnan(_x):
            print('We found nan {}'.format(_x))

        if np.isinf(_x):
            # print('We found infinity {}'.format(_x))
            total += 1
            X[i][j] = sys.maxsize

print(total)



from sklearn.ensemble import RandomForestClassifier

# from xgboost import XGBClassifier
# model = XGBClassifier(
#     learning_rate=0.1,
#     n_estimators=1000,
#     max_depth=3,
#     min_child_weight=5,
#     gamma=0.1,
#     subsample=0.8,
#     colsample_bytree=0.8,
#     objective='binary:logistic',
#     nthread=4,
#     scale_pos_weight=1,
#     seed=27)

model = RandomForestClassifier(random_state=0)


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=56)

print('training')
model.fit(X_train, y_train)



import eli5
from eli5.sklearn import PermutationImportance

perm = PermutationImportance(model, random_state=1).fit(X_test, y_test)
# eli5.show_weights(perm, feature_names = feature_names)
# imporatnce = eli5.format_as_text(eli5.explain_weights(perm, top=100))
imporatnce = eli5.explain_weights(perm, feature_names=feature_names)

print(imporatnce.importances)
# print(imporatnce)
















