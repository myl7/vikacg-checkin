#!/usr/bin/env python

# Copyright (c) 2022 myl7
# SPDX-License-Identifier: Apache-2.0

import os
import logging
import json
from typing import Dict

import requests

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(asctime)s:%(message)s')

EXIT_CODE_INVALID_CONFIG = 1
EXIT_CODE_FAILED = 2
EXIT_CODE_DUP = 3

AUTH = os.getenv('AUTH')
if AUTH == '':
    logging.critical('环境变量 AUTH 未提供')
    exit(EXIT_CODE_INVALID_CONFIG)
elif not AUTH.startswith('Bearer '):
    AUTH = 'Bearer ' + AUTH

UA = os.getenv('UA')

LOGIN_URL = 'https://www.vikacg.com/wp-json/b2/v1/userMission'

headers = {'Authorization': AUTH}
if UA:
    headers['User-Agent'] = UA
res = requests.post(LOGIN_URL, headers=headers)

if res.status_code != 200:
    logging.error(f'签到失败：status code = {res.status_code}, body = {res.content.decode()}')
    exit(EXIT_CODE_FAILED)
res_body: Dict | str = res.json()
if isinstance(res_body, str):
    logging.error(f'签到失败，今天已经签到过了，获得积分 {res_body}：body = {res.content.decode()}')
    exit(EXIT_CODE_DUP)
mission: Dict = res_body.get('mission', None)
if not mission:
    logging.critical(f'签到失败，缺少 mission 字段：body = {json.dumps(res_body)}')
    exit(EXIT_CODE_FAILED)
this_credit = mission.get('credit')
if not this_credit:
    logging.critical(f'签到失败，缺少 mission.credit 字段：body = {json.dumps(res_body)}')
    exit(EXIT_CODE_FAILED)
total_credit = mission.get('my_credit')
if not total_credit:
    logging.critical(f'签到失败，缺少 mission.my_credit 字段：body = {json.dumps(res_body)}')
    exit(EXIT_CODE_FAILED)
logging.info(f'签到成功，获得积分 {this_credit}，当前总积分 {total_credit}')
