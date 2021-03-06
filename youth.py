#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# 此脚本参考 https://github.com/Sunert/Scripts/blob/master/Task/youth.js

import traceback
import time
import re
import json
import sys
import os
from util import send, requests_session
from datetime import datetime, timezone, timedelta

# YOUTH_HEADER 为对象, 其他参数为字符串，自动提现需要自己抓包
# 选择微信提现30元，立即兑换，在请求包中找到withdraw2的请求，拷贝请求body类型 p=****** 的字符串，放入下面对应参数即可
cookies1 = {
  'YOUTH_HEADER': {"Accept-Encoding":"gzip, deflate, br","Cookie":"sensorsdata2019jssdkcross=%7B%22distinct_id%22%3A%2246315190%22%2C%22%24device_id%22%3A%2217651b5266d30e-0dbb0961dcaf4c8-724c1251-370944-17651b5266e21b%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2217651b5266d30e-0dbb0961dcaf4c8-724c1251-370944-17651b5266e21b%22%7D","Connection":"keep-alive","Referer":"https://kd.youth.cn/html/taskCenter/index.html?uuid=087fceb77b9d62adc6ff5f2ee85d5c3f&sign=88efde8a86280adfe5af83ebe9d60f06&channel_code=80000000&uid=46315190&channel=80000000&access=Wlan&app_version=1.8.2&device_platform=iphone&cookie_id=e1397972d65826957deea9d4fd802100&openudid=087fceb77b9d62adc6ff5f2ee85d5c3f&device_type=1&device_brand=iphone&sm_device_id=2020052418595362894dda63af129647aa5a4ab0b4974801a2e5438b3bd39f&device_id=48679285&version_code=182&os_version=13.5&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWKxzYGxhYx6m66oqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFjKDdrt_MrYKfgW2EY2Ft&device_model=iPhone_6_Plus&subv=1.5.1&&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWKxzYGxhYx6m66oqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFjKDdrt_MrYKfgW2EY2Ft&cookie_id=e1397972d65826957deea9d4fd802100","Accept":"*/*","Host":"kd.youth.cn","User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148","Accept-Language":"zh-cn","X-Requested-With":"XMLHttpRequest"},
  'YOUTH_READBODY': 'p=9NwGV8Ov71o%3DGvDnjwMsu_ld4qx0YVkhCGk95BHaDHeU_TBhaHjQX3Mlq4IPbnLxoaM9tVw1tLB2c_Ry7nBEKRafk5GR1I3FB7Yv10v0gIqD_QgdYPLRZqnKKKjjbcJKT_ppR_rL8zrZOyu-V_GShXZDcuk7r7vOy2W69VMdtAmEuArSicyPlFTYohH76gIKC8YYZ6WSxpZaavXW5VXPRan3heAwQA_kySLxry5KZFc1NUrwVA5I9WBbVFWcaChuGH7Y5xRlkd6KurZhAtRJIWO82pw7ptH4F1UBnIoHOJgoQT5mY1ovfYZA-YtjYrr4xSRqgw9l-_ltZlY2KbNul6-eILTo18QjBa_cgwXVLcxboShD6Ylz6nTZU-_-G0ZKwI2C8QmQse4byXxn0pkh-2yyFraSFGpHrhJJjjiwOERQc-6BMzoA2yUuiJ4Yu1B7U_v46gkQSSGtbPRaEB40NeRSBg7k6PNbtnTOoVQ1Ukjh6jI7uE9AY6xvudpBLepJDVDrR5WadL7VrHVxWplNusXmN3G_6ohysiCdqzyNUwkqfRZFf5VEnv6NrcPLtH8EBEkbN3Gpn0omAVUIfH23tOIFWHciffHUy9ajsNntBTACbtLCryuR5s-KQc7RBGxFCoa3-RmEtR4o-21Kp8hfGn8_EqOL-YMsHNQB-7kRnIObc6ewcJiVo15dwwJHIaNWUUXW-jgoyi6fEHvLIsaSUCgGUazwDE285FilzWkHoDITw4ywsuN1HK-xzIoL3Xvo1GDkzqVJYE3U1gZ9SqaJpEo_fVJSahoJSokNLl3uyZ7w8XnYi7C7jvZqFk_prEdC0xo84WASlHOPC9Gt3ksL-LQ%3D&',
  'YOUTH_REDBODY': 'p=9NwGV8Ov71o%3DGvDnjwMsu_ka-LJ9wnbNzBhA0cz3iHWgEqXEh3bkBC0KSg93aV2LC-S2kpFYl_sQmKPAuBvYw99KKcGdwXnrOIxrdbAcw8RMxAxT0fhhlKbyoLF9JkY0pZZzB4x_MdhOeM1Tr5rb_G8DV3jd2Z7HLwsRvzGAXdj4J9U5F1I3egbmUvWGoxoj0apWLF2jc0fubAq3dyobnwrCtWTFJkRXnKkPDMKcen0xlBGHR2jZF_mX-zkJt0HlAZjyrO48BrfYqkDrr5F2ISwKDy6lKMghhqiaH50ekdCPBxjbM0_-qW-GUpqcyW8ZRQ4oJlesYY4IAvm3qkewqmr-oopwxofpfSv2GkyzwQHqlrhEfPUvivSFniVYBveWKxEd-3fah0nKCoi-UNzF-NAlJbBw_Rd0zyb9l1EWbVkh1MRXwDZFCnY2iFuBgNp_zlxow0d-hXIMRyFJfV3oOfXTLJ5rBg5L3z_kJtl3IZXxmSsNpCxUBhbtpWw3NZpc1oZPCc2rV0j0C8PvZWdodcoVGrNFPSMEIvLY6bKD4gH5QwFtYQOldS9TRSxiEz2zJYq7zeV8r0nFj32lzYlkW0c3nqIf8CiVHufvMa2PTeAag4N5nPy_H_LOEal9Pmvrfo5fwKafyUGgwW5jLCFMsvfSG68nIee9Lb38Df2dO6sYzUNbK30X0hmiHIhTHKcRHM5tPAmoONeIcmwYVjEiQ0HQ48jMk8auEXv067GzKr6pomDdj02F3t8D4HGuvzbRUIjRl-wH2o1QYQgfyoTvyj4kUIkOdF6v2UnPFp0iovgWkdmnI_DvNxchMR-wKDN3o_H4-6KyzuHh2DZPn3m2-0o%3D',
  'YOUTH_READTIMEBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_lgXXENBlMWjgdt2eFsJi4FV71nWDXdXT6C5gioHBTSn7rK0dXFkhDeJIZ5oDXpx9Vt3jnAJ4AwMkOK-OCcx0IflI9Z3ixeEvV284ONFvvktkFa9VEcsPdQR1YwXfcKpDcqzkFTEBdQU2fWKjy0TxL49mKLwT7nCeEWEOqXtxP4qi3Cym3GipOxTBuaEHzPmbUAMPV02OnBqN78U8vXAQPqNLx9aByHORD7D_Kq0Akty-o44-lqaS2KEkkhKB0oksFxiGr4UOFh6SiUJsAzlWeZCVK-QPi_qpJ4PtSe5OiSTqb9jseYatTr8wHLpLRhhZQ46v0OAoirzdKkjl_PAGGAsRGFrpmpdkeRVJyRHFzE_QSNrX5KwAoGOCtJjuvs65F-RdnbXVmTz7e8HWfOlPaCRAvnD0aM0wjypKY26Up5qMwHMu31kBoYv9qNjiCt00_FMhKTVUaZcWE5ZRt_NsKPnog3ojtIbpHfAV9DbgZ3SnSwJ7wicwuWaoYWxvVJqQCzsDxYU16pSGdngTjIxdAiIhTT6Y-jizSjZ7YKN2ieE5ZU4Co-RpXMyE_3e0XTpbjZVfxciH5FZNq77ZsWdHZb6fXMAB8IpyTfrnOQZAYXr5-iCnnDRc16Hd2GZgK_be15jd_4u-S2d2S-841xl4lxbTKBqhdX77KMgK3wtcrDDfvyg0zH2TLH5dkFeZ612lhRe56BtK9aE9NLqKUz6608RJnBDMkccVUndBNjmzqqHzcqr2T2_yFjbAaMxstAXaiU5xmvLIIblxgmLl3pswf5V17hKNaKy9',
  'YOUTH_WITHDRAWBODY': ''
}
cookies2 = {
  'YOUTH_HEADER': {"Accept-Encoding":"gzip, deflate, br","Cookie":"sensorsdata2019jssdkcross=%7B%22distinct_id%22%3A%2247965996%22%2C%22%24device_id%22%3A%22177063b259cb9c-0e7da849c0625e-2a463a35-250125-177063b259da89%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22177063b259cb9c-0e7da849c0625e-2a463a35-250125-177063b259da89%22%7D","Connection":"keep-alive","Referer":"https://kd.youth.cn/html/taskCenter/index.html?uuid=4a7d49020489c2ce01973febf0a0cd4e&sign=13e599c5c6b9eb2f9b1b07def9bb010c&channel_code=80000000&uid=47965996&channel=80000000&access=WIfI&app_version=1.8.2&device_platform=iphone&cookie_id=d600372fa24880e6462aa5843db6316a&openudid=4a7d49020489c2ce01973febf0a0cd4e&device_type=1&device_brand=iphone&sm_device_id=20200709185901e5ff3f3aad74036656370063b495d20a01bcead81641da1b&device_id=49342561&version_code=182&os_version=14.0&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWKx3Z9rhYygm6_OqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonrdr9-mZoGfl7GEY2Ft&device_model=iPad&subv=1.5.1&&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWKx3Z9rhYygm6_OqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonrdr9-mZoGfl7GEY2Ft&cookie_id=d600372fa24880e6462aa5843db6316a","Accept":"*/*","Host":"kd.youth.cn","User-Agent":"Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148","Accept-Language":"zh-cn","X-Requested-With":"XMLHttpRequest"},
  'YOUTH_READBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_kF97hamPuz4ZZk3rmRrVU_m2Z51XN3szZYaCPxNG07BYjyjwYkBVGTfTGYPVecze9u-jGHCQmfvey4yZrPyKR-cA01PbV3h61GBiHFc-skGrpoDK0eliCfJPX7f9_IVT-MEKcW_xpZDbrmsvsu4dMRvrUKKR-WPzCyUg5S61qTfaHyXpHGn2oc65AZMdKswJyuTgLLf3BAEudt8lEJm_CiD9l09-Cg2C0bZ4FPt0eiQfuyent4VXz38jZXqzB-W-JAud5AGgqAu1-dsdy7fEVTYHNYKvVM935_Rl-s-KaJw7wU1J5cFK7wz9m0uTtCJwrnw1iAommSOAhI6poPxd1EUiITFNmxnvmtY8lP4U-nmsWOMHF7iQgnNs5oqleEjMdleJ2PPYvHbPg9aWrymcoXPgHkbanfEGK9fpZKhtIv9CqUpfQOf_6nHbUbGyhj3yg0V8yqrpZSsOl0GNV_J9lbWkkHt5Lbog-evM7n_6rhcXTP4nrxsyHr9psZYFgXz73Gq6s5T4TwsX8jKgU4VEaR-lL5sAD7vSbJxS1tOs0UlnYW7lE7ckc7soKYDS5ezm48HyxEg2TUx_Y5xalCuD66hsV1yN_b3sKtgLGCzLCzSo2lCDiTOaXgg8gi4vbCGrir6vLOZ7L4qiGqdx7KCcchgJZU-RLL2hKgx8pd2uX2WbAH7Br5uZsZW3m4QQgYjCmEDhl5HtP7eOXyu9vmQ5Aqnhjt_R9wZT4shQnCwhyhY%3D',
  'YOUTH_REDBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjazbBlBp4-3VBqIE6FTR2KhfyLVi7Pl1_m0wwPJgXu-Fmh7S-5HqV6o1vMtEls8mPJh514T6M7mT424qvh8QrkxvplMO-SYOVD8eel3ty7vwxe_wa7ZfSZfXdjTiw3cbhIZT-OnIao6ZrF_hSdmQipG4Rvvz3nXQ6gK5CyHYI1D1-baeHBTpn7ijSSnjFXoXswynYfcRFREAFlf3tlH5P3n2IQQPKN4-7ltzqqZsILrKwR-K4sMf3QZpNBJ0yUNoxKwlS9gynhRazoJhK6YsNV4VKiBI0qrt7zhG8IU6D4ee7mczPCSXlwg4h5AGQY7aGanWMTQvRJnRsxK3NtMNJA_R00Zagy6EOPqL_TrG6N_LrEDcf8j_2THLhOkMCU1C6A33_BN6m9tE9SqGL4iAZfv-VIkMqECO9MUbFO26ZropDvQ5FJy-KCRGnJBQSOvgx4Yl68K5hyAFE97BfN3JckCymGJ6rp-I7ZLKm4oqfMsEiA18KS1dipHatReRPNOlT8B2oS9rt-wcNGTSDY-aT4d23CHTplvxXUF0o2zC7I0lM08k9m5H2olpsFYjC6Ys6dJBJgD5a8YYQAGkO4rdZKPPjcs9qJGBZNh0K3kffRYesSBp1tigi4TsRh5aT-39L77qYUW3bGP3OvaOgNj8lEMjcyrXlSzX_c93SkGx3GGjV2Sou_5Ar_SxToKfcrxqml-IzJ67T_K36UFFkXjDI1LUi0EOcRmUle9edu8hM83Ufy66DJDC4jUxVCnh5Sqw1c%3D',
  'YOUTH_READTIMEBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_kF97hamPuz4ZZk3rmRrVU_m2Z51XN3szZYaCPxNG07BYjyjwYkBVGTfTGYPVecze9u-jGHCQmfvey4yZrPyKR-cA01PbV3h61GBiHFc-skGrpoDK0eliCfJPX7f9_IVT-MEKcW_xpZDbrmsvsu4dMRvrUKKR-WPzCyUg5S61qTfaHyXpHGn2oc65AZMdKswJyuTgLLf3BAEudt8lEJm_CiD9l09-Cg2C0bZ4FPt0eiQl1iF8etaAFBHP3_8SFzZ9jgEzVjIVGWjnFgnnYWIwlwLVWhpQYXIVKJdvBBl2_JMPv8nbQDnO5JnaXfKuLncpmF37NGDIdEvzJtcII4-Q0W3iYdOdoX354YPK55kr9EG2uaAKrY6aSiGxZPXvQTEk7UPIA2fefl4qZ7Nzgm-aKyln-VT4oHxpUFAZ0u6D7fV45fQe4yU8ZfPhs2_5srHx9aa_eqWAPxE8bfgv7zZgS2oMyxDBYVrBu4CecGrdszDVmbdbwNniBwr1wjzr7WWGunUQh9_AB8nMcUOdDgPGfPoOS28_zME7qLsxrxmUzkAvuz3QGhQblp5wuIyxHu2tVJ4gZmZ7IDI9h5aiQa22mYSNeCmsDaCK-vwL8thmRebLQf-_m5rtSxNV9feDMusYj2HKC-mDT976XMKfaX4_G2Qvo1iLwIY3ZKFOYrCkcQmvl_VJILjbycxoDJTGHeGCSqc6EPB6Cg477j1eptDLMQ%3D%3D',
  'YOUTH_WITHDRAWBODY': ''
}

COOKIELIST = [cookies1,cookies2,]  # 多账号准备

# ac读取环境变量
if "YOUTH_HEADER1" in os.environ:
  COOKIELIST = []
  for i in range(5):
    headerVar = f'YOUTH_HEADER{str(i+1)}'
    readBodyVar = f'YOUTH_READBODY{str(i+1)}'
    redBodyVar = f'YOUTH_REDBODY{str(i+1)}'
    readTimeBodyVar = f'YOUTH_READTIMEBODY{str(i+1)}'
    withdrawBodyVar = f'YOUTH_WITHDRAWBODY{str(i+1)}'
    if headerVar in os.environ and os.environ[headerVar] and readBodyVar in os.environ and os.environ[readBodyVar] and redBodyVar in os.environ and os.environ[redBodyVar] and readTimeBodyVar in os.environ and os.environ[readTimeBodyVar]:
      globals()['cookies'+str(i + 1)]["YOUTH_HEADER"] = json.loads(os.environ[headerVar])
      globals()['cookies'+str(i + 1)]["YOUTH_READBODY"] = os.environ[readBodyVar]
      globals()['cookies'+str(i + 1)]["YOUTH_REDBODY"] = os.environ[redBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_READTIMEBODY"] = os.environ[readTimeBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_WITHDRAWBODY"] = os.environ[withdrawBodyVar]
      COOKIELIST.append(globals()['cookies'+str(i + 1)])
  print(COOKIELIST)

cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
YOUTH_HOST = "https://kd.youth.cn/WebApi/"

def get_standard_time():
  """
  获取utc时间和北京时间
  :return:
  """
  # <class 'datetime.datetime'>
  utc_datetime = datetime.utcnow().replace(tzinfo=timezone.utc)  # utc时间
  beijing_datetime = utc_datetime.astimezone(timezone(timedelta(hours=8)))  # 北京时间
  return beijing_datetime

def pretty_dict(dict):
    """
    格式化输出 json 或者 dict 格式的变量
    :param dict:
    :return:
    """
    return print(json.dumps(dict, indent=4, ensure_ascii=False))

def sign(headers):
  """
  签到
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/TaskCenter/sign'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('签到')
    print(response)
    if response['status'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def signInfo(headers):
  """
  签到详情
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/TaskCenter/getSign'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('签到详情')
    print(response)
    if response['status'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def punchCard(headers):
  """
  打卡报名
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}PunchCard/signUp'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('打卡报名')
    print(response)
    if response['code'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def doCard(headers):
  """
  早起打卡
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}PunchCard/doCard'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('早起打卡')
    print(response)
    if response['code'] == 1:
      shareCard(headers=headers)
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def shareCard(headers):
  """
  打卡分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  startUrl = f'{YOUTH_HOST}PunchCard/shareStart'
  endUrl = f'{YOUTH_HOST}PunchCard/shareEnd'
  try:
    response = requests_session().post(url=startUrl, headers=headers, timeout=30).json()
    print('打卡分享')
    print(response)
    if response['code'] == 1:
      time.sleep(0.3)
      responseEnd = requests_session().post(url=endUrl, headers=headers, timeout=30).json()
      if responseEnd['code'] == 1:
        return responseEnd
    else:
      return
  except:
    print(traceback.format_exc())
    return

def luckDraw(headers):
  """
  打卡分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}PunchCard/luckdraw'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('七日签到')
    print(response)
    if response['code'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def shareArticle(headers):
  """
  分享文章
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://focu.youth.cn/article/s?signature=QqvZWbEKpA2yrNR1MnyjPetpZpz2TLdDDw849VGjJl8gXB5keP&uid=52242968&phone_code=4aa0b274198dafebe5c214ea6097d12b&scid=35438728&time=1609414747&app_version=1.8.2&sign=17fe0351fa6378a602c2afd55d6a47c8'
  readUrl = 'https://focus.youth.cn/article/s?signature=QqvZWbEKpA2yrNR1MnyjPetpZpz2TLdDDw849VGjJl8gXB5keP&uid=52242968&phone_code=4aa0b274198dafebe5c214ea6097d12b&scid=35438728&time=1609414747&app_version=1.8.2&sign=17fe0351fa6378a602c2afd55d6a47c8'
  try:
    response1 = requests_session().post(url=url, headers=headers, timeout=30)
    print('分享文章1')
    print(response1)
    time.sleep(0.3)
    response2 = requests_session().post(url=readUrl, headers=headers, timeout=30)
    print('分享文章2')
    print(response2)
    return
  except:
    print(traceback.format_exc())
    return

def openBox(headers):
  """
  开启宝箱
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}invite/openHourRed'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('开启宝箱')
    print(response)
    if response['code'] == 1:
      share_box_res = shareBox(headers=headers)
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def shareBox(headers):
  """
  宝箱分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}invite/shareEnd'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('宝箱分享')
    print(response)
    if response['code'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def friendList(headers):
  """
  好友列表
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}ShareSignNew/getFriendActiveList'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print('好友列表')
    print(response)
    if response['error_code'] == '0':
      if len(response['data']['active_list']) > 0:
        for friend in response['data']['active_list']:
          if friend['button'] == 1:
            time.sleep(1)
            friendSign(headers=headers, uid=friend['uid'])
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def friendSign(headers, uid):
  """
  好友签到
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}ShareSignNew/sendScoreV2?friend_uid={uid}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print('好友签到')
    print(response)
    if response['error_code'] == '0':
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def sendTwentyScore(headers, action):
  """
  每日任务
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}NewTaskIos/sendTwentyScore?{headers["Referer"].split("?")[1]}&action={action}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print(f'每日任务 {action}')
    print(response)
    if response['status'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def watchAdVideo(headers):
  """
  看广告视频
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/taskCenter/getAdVideoReward'
  headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
  try:
    response = requests_session().post(url=url, data="type=taskCenter", headers=headers, timeout=30).json()
    print('看广告视频')
    print(response)
    if response['status'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def watchGameVideo(body):
  """
  激励视频
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/Game/GameVideoReward.json'
  headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
  try:
    response = requests_session().post(url=url, headers=headers, data=body, timeout=30).json()
    print('激励视频')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def visitReward(body):
  """
  回访奖励
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/mission/msgRed.json'
  headers = {
    'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('回访奖励')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def articleRed(body):
  """
  惊喜红包
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/article/red_packet.json'
  headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('惊喜红包')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def readTime(body):
  """
  阅读时长
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/user/stay.json'
  headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('阅读时长')
    print(response)
    if response['error_code'] == '0':
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def rotary(headers, body):
  """
  转盘任务
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/turnRotary?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('转盘任务')
    print(response)
    return response
  except:
    print(traceback.format_exc())
    return

def rotaryChestReward(headers, body):
  """
  转盘宝箱
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/getData?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('转盘宝箱')
    print(response)
    if response['status'] == 1:
      i = 0
      while (i <= 3):
        chest = response['data']['chestOpen'][i]
        if response['data']['opened'] >= int(chest['times']) and chest['received'] != 1:
          time.sleep(1)
          runRotary(headers=headers, body=f'{body}&num={i+1}')
        i += 1
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def runRotary(headers, body):
  """
  转盘宝箱
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/chestReward?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('领取宝箱')
    print(response)
    if response['status'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def doubleRotary(headers, body):
  """
  转盘双倍
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/toTurnDouble?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('转盘双倍')
    print(response)
    if response['status'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def incomeStat(headers):
  """
  收益统计
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'https://kd.youth.cn/wap/user/balance?{headers["Referer"].split("?")[1]}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=50).json()
    print('收益统计')
    print(response)
    if response['status'] == 0:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def withdraw(body):
  """
  自动提现
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/wechat/withdraw2.json'
  headers = {
    'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, headers=headers, data=body, timeout=30).json()
    print('自动提现')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def bereadRed(headers):
  """
  时段红包
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}Task/receiveBereadRed'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('时段红包')
    print(response)
    if response['code'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def run():
  title = f'📚中青看点'
  content = ''
  result = ''
  beijing_datetime = get_standard_time()
  print(f'\n【中青看点】{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")}')
  hour = beijing_datetime.hour
  for i, account in enumerate(COOKIELIST):
    headers = account['YOUTH_HEADER']
    readBody = account['YOUTH_READBODY']
    redBody = account['YOUTH_REDBODY']
    readTimeBody = account['YOUTH_READTIMEBODY']
    withdrawBody = account['YOUTH_WITHDRAWBODY']
    rotaryBody = f'{headers["Referer"].split("&")[15]}&{headers["Referer"].split("&")[8]}'
    sign_res = sign(headers=headers)
    if sign_res and sign_res['status'] == 1:
      content += f'【签到结果】：成功 🎉 明日+{sign_res["nextScore"]}青豆'
    elif sign_res and sign_res['status'] == 2:
      send(title=title, content=f'【账户{i+1}】Cookie已过期，请及时重新获取')
      continue

    sign_info = signInfo(headers=headers)
    if sign_info:
      content += f'\n【账号】：{sign_info["user"]["nickname"]}'
      content += f'\n【签到】：+{sign_info["sign_score"]}青豆 已连签{sign_info["total_sign_days"]}天'
      result += f'【账号】: {sign_info["user"]["nickname"]}'
    friendList(headers=headers)
    if hour > 12:
      punch_card_res = punchCard(headers=headers)
      if punch_card_res:
        content += f'\n【打卡报名】：打卡报名{punch_card_res["msg"]} ✅'
    if hour >= 5 and hour <= 8:
      do_card_res = doCard(headers=headers)
      if do_card_res:
        content += f'\n【早起打卡】：{do_card_res["card_time"]} ✅'
    luck_draw_res = luckDraw(headers=headers)
    if luck_draw_res:
      content += f'\n【七日签到】：+{luck_draw_res["score"]}青豆'
    visit_reward_res = visitReward(body=readBody)
    if visit_reward_res:
      content += f'\n【回访奖励】：+{visit_reward_res["score"]}青豆'
    shareArticle(headers=headers)
    open_box_res = openBox(headers=headers)
    if open_box_res:
      content += f'\n【开启宝箱】：+{open_box_res["score"]}青豆 下次奖励{open_box_res["time"] / 60}分钟'
    watch_ad_video_res = watchAdVideo(headers=headers)
    if watch_ad_video_res:
      content += f'\n【观看视频】：+{watch_ad_video_res["score"]}个青豆'
    watch_game_video_res = watchGameVideo(body=readBody)
    if watch_game_video_res:
      content += f'\n【激励视频】：{watch_game_video_res["score"]}个青豆'
    # article_red_res = articleRed(body=redBody)
    # if article_red_res:
    #   content += f'\n【惊喜红包】：+{article_red_res["score"]}个青豆'
    read_time_res = readTime(body=readTimeBody)
    if read_time_res:
      content += f'\n【阅读时长】：共计{int(read_time_res["time"]) // 60}分钟'
    if (hour >= 6 and hour <= 8) or (hour >= 11 and hour <= 13) or (hour >= 19 and hour <= 21):
      beread_red_res = bereadRed(headers=headers)
      if beread_red_res:
        content += f'\n【时段红包】：+{beread_red_res["score"]}个青豆'
    for i in range(0, 5):
      time.sleep(5)
      rotary_res = rotary(headers=headers, body=rotaryBody)
      if rotary_res:
        if rotary_res['status'] == 0:
          break
        elif rotary_res['status'] == 1:
          content += f'\n【转盘抽奖】：+{rotary_res["data"]["score"]}个青豆 剩余{rotary_res["data"]["remainTurn"]}次'
          if rotary_res['data']['doubleNum'] != 0 and rotary_res['data']['score'] > 0:
            double_rotary_res = doubleRotary(headers=headers, body=rotaryBody)
            if double_rotary_res:
              content += f'\n【转盘双倍】：+{double_rotary_res["score"]}青豆 剩余{double_rotary_res["doubleNum"]}次'

    rotaryChestReward(headers=headers, body=rotaryBody)
    for action in ['watch_article_reward', 'watch_video_reward', 'read_time_two_minutes', 'read_time_sixty_minutes', 'new_fresh_five_video_reward']:
      time.sleep(5)
      sendTwentyScore(headers=headers, action=action)
    stat_res = incomeStat(headers=headers)
    if stat_res['status'] == 0:
      for group in stat_res['history'][0]['group']:
        content += f'\n【{group["name"]}】：+{group["money"]}青豆'
      today_score = int(stat_res["user"]["today_score"])
      score = int(stat_res["user"]["score"])
      total_score = int(stat_res["user"]["total_score"])

      if score >= 300000 and withdrawBody:
        with_draw_res = withdraw(body=withdrawBody)
        if with_draw_res:
          result += f'\n【自动提现】：发起提现30元成功'
          content += f'\n【自动提现】：发起提现30元成功'
          send(title=title, content=f'【账号】: {sign_info["user"]["nickname"]} 发起提现30元成功')

      result += f'\n【今日收益】：+{"{:4.2f}".format(today_score / 10000)}'
      content += f'\n【今日收益】：+{"{:4.2f}".format(today_score / 10000)}'
      result += f'\n【账户剩余】：{"{:4.2f}".format(score / 10000)}'
      content += f'\n【账户剩余】：{"{:4.2f}".format(score / 10000)}'
      result += f'\n【历史收益】：{"{:4.2f}".format(total_score / 10000)}\n\n'
      content += f'\n【历史收益】：{"{:4.2f}".format(total_score / 10000)}\n'

  print(content)

  # 每天 23:00 发送消息推送
  if beijing_datetime.hour == 23 and beijing_datetime.minute >= 0 and beijing_datetime.minute < 5:
    send(title=title, content=result)
  elif not beijing_datetime.hour == 23:
    print('未进行消息推送，原因：没到对应的推送时间点\n')
  else:
    print('未在规定的时间范围内\n')

if __name__ == '__main__':
    run()
