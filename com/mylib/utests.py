# -*- coding: utf-8 -*-
import unittest
from com.mylib.models import get_isplist
import json
class IPGetterTest(unittest.TestCase):
    def runTest(self):
        #for item in get_isplist(['122.11.48.165','122.11.48.70']):
        #    print item
        testjson()
def iprange_test(self):
    ipList=[]
    for i in range(126777218,126777218+3300):
        #print get_ip_test()
        ipList.append(get_ip_str(i))
    for item in get_isplist(ipList):
        print item


def get_ip_test():
    
    return get_ip_str(2294967296)

def get_ip_str(numIp):
    #numIp=1000
    ips=[0,0,0,0]
    newIp=numIp
    ips[3]=newIp%256
    newIp=newIp/256
    ips[2]=newIp%256
    newIp=newIp/256
    ips[1]=newIp%256
    newIp=newIp/256
    ips[0]=newIp%256
    return '.'.join([str(i) for i in ips])

s='''
{
    "http_watch": {
        "abstract": {
            "bytes_received": 0,
            "bytes_sent": 0,
            "dns_start_time": 0,
            "dns_time_used": 0,
            "document_title": "%e7%99%be%e5%ba%a6%e4%b8%80%e4%b8%8b%ef%bc%8c%e4%bd%a0%e5%b0%b1%e7%9f%a5%e9%81%93",
            "download_speed": 57029,
            "end_time": 1407741329,
            "error_code": 100200,
            "first_byte_time": 0,
            "first_screen_time": 0,
            "ip_address": "",
            "is_redirect": false,
            "load_start_time": 11451,
            "page_load_start_time": 13900,
            "redirect_start_time": 0,
            "redirect_time_used": 0,
            "render_start_time": 0,
            "request_count": 10,
            "request_error_count": 0,
            "start_time": 1407741307,
            "status_code": 30,
            "tcp_connection_start_time": 94,
            "tcp_connection_time_used": 47,
            "time_used": 22683
        },
        "elements": [
            {
                "bytes_received": 21070,
                "bytes_sent": 336,
                "content_type": "text/html%3b+charset=utf-8",
                "dns_start_time": 0,
                "dns_time_used": 0,
                "download_speed": 74982,
                "download_time_used": 281,
                "error_code": 100200,
                "ip_address": "",
                "port": 52685,
                "protocol_method": "GET",
                "request_time_used": 172,
                "response_time_used": 0,
                "sequence_number": 1,
                "start_time": 0,
                "status_code": 200,
                "tcp_connection_start_time": 94,
                "tcp_connection_time_used": 47,
                "time_used": 281,
                "url": "www.baidu.com/"
            },
            {
                "bytes_received": 1016,
                "bytes_sent": 467,
                "content_type": "image/gif",
                "dns_start_time": 0,
                "dns_time_used": 0,
                "download_speed": 16387,
                "download_time_used": 62,
                "error_code": 100200,
                "ip_address": "",
                "port": 52685,
                "protocol_method": "GET",
                "request_time_used": 0,
                "response_time_used": 0,
                "sequence_number": 2,
                "start_time": 250,
                "status_code": 200,
                "tcp_connection_start_time": 0,
                "tcp_connection_time_used": 0,
                "time_used": 62,
                "url": "www.baidu.com/img/baidu%5fjgylogo3.gif"
            },
            {
                "bytes_received": 5644,
                "bytes_sent": 459,
                "content_type": "image/png",
                "dns_start_time": 0,
                "dns_time_used": 0,
                "download_speed": 72358,
                "download_time_used": 78,
                "error_code": 100200,
                "ip_address": "",
                "port": 52685,
                "protocol_method": "GET",
                "request_time_used": 0,
                "response_time_used": 16,
                "sequence_number": 3,
                "start_time": 250,
                "status_code": 200,
                "tcp_connection_start_time": 0,
                "tcp_connection_time_used": 0,
                "time_used": 78,
                "url": "www.baidu.com/img/bdlogo.png"
            },
            {
                "bytes_received": 1737,
                "bytes_sent": 415,
                "content_type": "image/gif",
                "dns_start_time": 250,
                "dns_time_used": 62,
                "download_speed": 7423,
                "download_time_used": 234,
                "error_code": 100200,
                "ip_address": "183.61.111.40",
                "port": 52685,
                "protocol_method": "GET",
                "request_time_used": 187,
                "response_time_used": 0,
                "sequence_number": 4,
                "start_time": 250,
                "status_code": 200,
                "tcp_connection_start_time": 312,
                "tcp_connection_time_used": 32,
                "time_used": 234,
                "url": "s1.bdstatic.com/r/www/cache/static/global/img/gs%5f237f015b.gif"
            },
            {
                "bytes_received": 33391,
                "bytes_sent": 425,
                "content_type": "application/javascript",
                "dns_start_time": 0,
                "dns_time_used": 0,
                "download_speed": 133564,
                "download_time_used": 250,
                "error_code": 100200,
                "ip_address": "",
                "port": 52685,
                "protocol_method": "GET",
                "request_time_used": 109,
                "response_time_used": 47,
                "sequence_number": 5,
                "start_time": 250,
                "status_code": 200,
                "tcp_connection_start_time": 312,
                "tcp_connection_time_used": 32,
                "time_used": 250,
                "url": "s1.bdstatic.com/r/www/cache/static/jquery/jquery-1.10.2.min%5ff2fb5194.js"
            },
            {
                "bytes_received": 35792,
                "bytes_sent": 429,
                "content_type": "application/javascript",
                "dns_start_time": 0,
                "dns_time_used": 0,
                "download_speed": 127373,
                "download_time_used": 281,
                "error_code": 100200,
                "ip_address": "",
                "port": 52685,
                "protocol_method": "GET",
                "request_time_used": 156,
                "response_time_used": 0,
                "sequence_number": 6,
                "start_time": 250,
                "status_code": 200,
                "tcp_connection_start_time": 312,
                "tcp_connection_time_used": 32,
                "time_used": 281,
                "url": "s1.bdstatic.com/r/www/cache/static/global/js/all%5fasync%5fpopstate%5fac539be4.js"
            },
            {
                "bytes_received": 2713,
                "bytes_sent": 412,
                "content_type": "application/javascript",
                "dns_start_time": 0,
                "dns_time_used": 0,
                "download_speed": 11594,
                "download_time_used": 234,
                "error_code": 100200,
                "ip_address": "",
                "port": 52685,
                "protocol_method": "GET",
                "request_time_used": 187,
                "response_time_used": 0,
                "sequence_number": 7,
                "start_time": 250,
                "status_code": 200,
                "tcp_connection_start_time": 312,
                "tcp_connection_time_used": 32,
                "time_used": 234,
                "url": "s1.bdstatic.com/r/www/cache/static/home/js/bri%5f7f1fa703.js"
            },
            {
                "bytes_received": 1651,
                "bytes_sent": 500,
                "content_type": "text/javascript",
                "dns_start_time": 3089,
                "dns_time_used": 63,
                "download_speed": 6230,
                "download_time_used": 265,
                "error_code": 100200,
                "ip_address": "180.149.131.210",
                "port": 52685,
                "protocol_method": "GET",
                "request_time_used": 187,
                "response_time_used": 0,
                "sequence_number": 8,
                "start_time": 3089,
                "status_code": 200,
                "tcp_connection_start_time": 3152,
                "tcp_connection_time_used": 78,
                "time_used": 265,
                "url": "passport.baidu.com/passApi/js/uni%5flogin%5fwrapper.js?cdnversion=1407741310122&%5f=1407741310097"
            },
            {
                "bytes_received": 7501,
                "bytes_sent": 413,
                "content_type": "application/javascript",
                "dns_start_time": 0,
                "dns_time_used": 0,
                "download_speed": 119063,
                "download_time_used": 63,
                "error_code": 100200,
                "ip_address": "",
                "port": 52685,
                "protocol_method": "GET",
                "request_time_used": 0,
                "response_time_used": 0,
                "sequence_number": 9,
                "start_time": 3089,
                "status_code": 200,
                "tcp_connection_start_time": 0,
                "tcp_connection_time_used": 0,
                "time_used": 63,
                "url": "s1.bdstatic.com/r/www/cache/static/sug/js/bdsug%5f21bb704a.js"
            },
            {
                "bytes_received": 288,
                "bytes_sent": 627,
                "content_type": "text/javascript%3b+charset=gbk",
                "dns_start_time": 11233,
                "dns_time_used": 46,
                "download_speed": 1321,
                "download_time_used": 218,
                "error_code": 100200,
                "ip_address": "180.97.33.72",
                "port": 52685,
                "protocol_method": "GET",
                "request_time_used": 156,
                "response_time_used": 0,
                "sequence_number": 10,
                "start_time": 11233,
                "status_code": 200,
                "tcp_connection_start_time": 11279,
                "tcp_connection_time_used": 47,
                "time_used": 218,
                "url": "suggestion.baidu.com/su?wd=&zxmode=1&json=1&p=3&sid=7578%5f4398%5f7991%5f1436%5f7801%5f8060%5f8057%5f6505%5f7634%5f6017%5f7825%5f7674%5f7606%5f7798%5f8036%5f7694%5f7962%5f7415%5f7687%5f7791%5f7475&cb=jQuery1102006187518099682232%5f1407741310098&%5f=1407741310099"
            }
        ],
        "url": ""
    },
    "network_info": {
        "adapts": [
            {
                "gateway": [
                    {
                        "gateway": "192.168.0.1"
                    }
                ],
                "ip": [
                    {
                        "ip": "192.168.0.163"
                    }
                ],
                "mac_addr": "F8-0F-41-0B-EB-16",
                "name": "Intel(R) 82579V Gigabit Network Connection",
                "subnetmask": [
                    {
                        "gateway": "192.168.0.1"
                    }
                ],
                "type": "Ethernet"
            },
            {
                "gateway": [
                    {
                        "gateway": "0.0.0.0"
                    }
                ],
                "ip": [
                    {
                        "ip": "192.168.57.1"
                    }
                ],
                "mac_addr": "00-50-56-C0-00-01",
                "name": "VMware Virtual Ethernet Adapter for VMnet1",
                "subnetmask": [
                    {
                        "gateway": "0.0.0.0"
                    }
                ],
                "type": "Ethernet"
            },
            {
                "gateway": [
                    {
                        "gateway": "0.0.0.0"
                    }
                ],
                "ip": [
                    {
                        "ip": "192.168.47.1"
                    }
                ],
                "mac_addr": "00-50-56-C0-00-08",
                "name": "VMware Virtual Ethernet Adapter for VMnet8",
                "subnetmask": [
                    {
                        "gateway": "0.0.0.0"
                    }
                ],
                "type": "Ethernet"
            }
        ],
        "dns_link_info": [
            {
                "delay1": "102",
                "delay2": "53",
                "loss_rate1": "0",
                "loss_rate2": "0",
                "name": "默认DNS : 101.226.4.6",
                "traceroute": [
                    {
                        "IP地址": "116.7.68.1",
                        "IP地址归属地": "广东",
                        "延时(毫秒)": "27",
                        "跳数": "01"
                    },
                    {
                        "IP地址": "219.134.138.157",
                        "IP地址归属地": "广东",
                        "延时(毫秒)": "29",
                        "跳数": "02"
                    },
                    {
                        "IP地址": "183.56.64.177",
                        "IP地址归属地": "广东",
                        "延时(毫秒)": "27",
                        "跳数": "03"
                    },
                    {
                        "IP地址": "119.145.45.189",
                        "IP地址归属地": "广东",
                        "延时(毫秒)": "32",
                        "跳数": "04"
                    },
                    {
                        "IP地址": "61.152.86.205",
                        "IP地址归属地": "上海",
                        "延时(毫秒)": "57",
                        "跳数": "05"
                    },
                    {
                        "IP地址": "61.129.95.2",
                        "IP地址归属地": "其他上海",
                        "延时(毫秒)": "59",
                        "跳数": "06"
                    },
                    {
                        "IP地址": "124.74.233.97",
                        "IP地址归属地": "其他上海",
                        "延时(毫秒)": "53",
                        "跳数": "07"
                    },
                    {
                        "IP地址": "124.74.233.130",
                        "IP地址归属地": "其他上海",
                        "延时(毫秒)": "55",
                        "跳数": "08"
                    },
                    {
                        "IP地址": "0.0.0.0",
                        "延时(毫秒)": "超时",
                        "跳数": "09"
                    },
                    {
                        "IP地址": "101.226.4.6",
                        "IP地址归属地": "上海",
                        "延时(毫秒)": "69",
                        "跳数": "10"
                    }
                ]
            },
            {
                "delay1": "1",
                "delay2": "0",
                "loss_rate1": "0",
                "loss_rate2": "0",
                "name": "默认网关 : 192.168.0.1",
                "traceroute": [
                    {
                        "IP地址": "192.168.0.1",
                        "IP地址归属地": "",
                        "延时(毫秒)": "0",
                        "跳数": "01"
                    }
                ]
            },
            {
                "delay1": "42",
                "delay2": "40",
                "loss_rate1": "0",
                "loss_rate2": "0",
                "name": "电信DNS : 218.85.152.99",
                "traceroute": [
                    {
                        "IP地址": "116.7.68.1",
                        "IP地址归属地": "广东",
                        "延时(毫秒)": "30",
                        "跳数": "01"
                    },
                    {
                        "IP地址": "219.134.138.173",
                        "IP地址归属地": "广东",
                        "延时(毫秒)": "66",
                        "跳数": "02"
                    },
                    {
                        "IP地址": "0.0.0.0",
                        "延时(毫秒)": "超时",
                        "跳数": "03"
                    },
                    {
                        "IP地址": "121.34.242.193",
                        "IP地址归属地": "广东",
                        "延时(毫秒)": "29",
                        "跳数": "04"
                    },
                    {
                        "IP地址": "202.97.66.213",
                        "IP地址归属地": "其他",
                        "延时(毫秒)": "158",
                        "跳数": "05"
                    },
                    {
                        "IP地址": "0.0.0.0",
                        "延时(毫秒)": "超时",
                        "跳数": "06"
                    },
                    {
                        "IP地址": "0.0.0.0",
                        "延时(毫秒)": "超时",
                        "跳数": "07"
                    },
                    {
                        "IP地址": "218.85.152.99",
                        "IP地址归属地": "其他福建",
                        "延时(毫秒)": "66",
                        "跳数": "08"
                    }
                ]
            },
            {
                "delay1": "0",
                "delay2": "0",
                "loss_rate1": "100",
                "loss_rate2": "100",
                "name": "移动DNS : 211.138.151.161",
                "traceroute": [
                ]
            }
        ],
        "public_ip": "116.7.71.183"
    },
    "resolve_domain": {
        "host_name": "www.baidu.com",
        "results": [
            {
                "domain_server": {
                    "alias": "移动",
                    "ip_address": "211.138.151.161"
                },
                "ip_addresses": [
                ]
            },
            {
                "domain_server": {
                    "alias": "铁通",
                    "ip_address": "222.47.29.93"
                },
                "ip_addresses": [
                    "119.75.217.56",
                    "119.75.218.77"
                ]
            },
            {
                "domain_server": {
                    "alias": "google ",
                    "ip_address": "8.8.8.8"
                },
                "ip_addresses": [
                    "180.97.33.108",
                    "180.97.33.107"
                ]
            },
            {
                "domain_server": {
                    "alias": "电信",
                    "ip_address": "218.85.152.99"
                },
                "ip_addresses": [
                ]
            }
        ]
    },
    "telnet": {
        "host_name": "www.baidu.com",
        "port": 80,
        "results": true
    },
    "trace_route": {
        "host_name": "www.baidu.com",
        "results": [
            {
                "delay": 32,
                "ip_address": "116.7.68.1",
                "location": "广东",
                "result": true
            },
            {
                "delay": 24,
                "ip_address": "219.134.138.173",
                "location": "广东",
                "result": true
            },
            {
                "delay": 35,
                "ip_address": "183.56.64.209",
                "location": "广东",
                "result": true
            },
            {
                "delay": 29,
                "ip_address": "119.145.45.185",
                "location": "广东",
                "result": true
            },
            {
                "delay": 48,
                "ip_address": "202.97.49.213",
                "location": "其他",
                "result": true
            },
            {
                "delay": 142,
                "ip_address": "202.102.69.10",
                "location": "江苏",
                "result": true
            },
            {
                "delay": 142,
                "ip_address": "",
                "location": "",
                "result": true
            },
            {
                "delay": 48,
                "ip_address": "180.97.32.22",
                "location": "江苏",
                "result": true
            },
            {
                "delay": 48,
                "ip_address": "",
                "location": "",
                "result": true
            },
            {
                "delay": 59,
                "ip_address": "180.97.33.108",
                "location": "江苏",
                "result": true
            }
        ]
    },
    "user_info": {
        "addr": "--请选择区县--",
        "agent_contact": "",
        "agent_name": "",
        "bandwidth_type": "家庭客户",
        "contact": "",
        "desc": "",
        "name": "",
        "time": "2014/8/11 15:16:04",
        "type": "链路故障"
    }
}
'''
def testjson():
    return json.loads(s)