#!/usr/bin/env python3

# Copyright (c) 2022 myl7
# SPDX-License-Identifier: Apache-2.0

import os
import logging
import json
import sys
from typing import Dict, Union

import requests

if sys.version_info.minor >= 9:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(asctime)s:%(message)s', encoding='utf-8')
else:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(asctime)s:%(message)s')

EXIT_CODE_INVALID_CONFIG = 1
EXIT_CODE_FAILED = 2
EXIT_CODE_DUP = 3

AUTH = os.getenv('AUTH')
if not AUTH:
    logging.critical('环境变量 AUTH 未提供')
    exit(EXIT_CODE_INVALID_CONFIG)
elif not AUTH.startswith('Bearer '):
    AUTH = 'Bearer ' + AUTH

UA = os.getenv('UA')

LOGIN_URL = 'https://www.vikacg.com/wp-json/b2/v1/userMission'


def app_format_err(msg: str, ctx: Dict):
    ctx_s = ', '.join([f'{k} = {v}' for k, v in ctx.items()])
    return f'{msg}：{ctx_s}'


def app_failed(exit_code: int, err_msg: str, err_ctx: Dict):
    """失败 hook"""
    pass


def app_ok(this_credit: int, total_credit: int):
    """成功 hook"""
    pass


headers = {'Authorization': AUTH}
if UA:
    headers['User-Agent'] = UA
res = requests.post(LOGIN_URL, headers=headers)

if res.status_code != 200:
    exit_code = EXIT_CODE_FAILED
    err_msg = '签到失败'
    err_ctx = {'status code': res.status_code, 'body': res.content.decode()}
    logging.error(app_format_err(err_msg, err_ctx))
    app_failed(exit_code, err_msg, err_ctx)
    exit(exit_code)
res_body: Union[Dict, str] = res.json()
if isinstance(res_body, str):
    exit_code = EXIT_CODE_FAILED
    err_msg = f'签到失败，今天已经签到过了，获得积分 {res_body}'
    err_ctx = {'body': res.content.decode()}
    logging.error(app_format_err(err_msg, err_ctx))
    app_failed(exit_code, err_msg, err_ctx)
    exit(exit_code)
mission: Dict = res_body.get('mission', None)
if not mission:
    exit_code = EXIT_CODE_FAILED
    err_msg = '签到失败，缺少 mission 字段'
    err_ctx = {'body': json.dumps(res_body)}
    logging.error(app_format_err(err_msg, err_ctx))
    app_failed(exit_code, err_msg, err_ctx)
    exit(exit_code)
this_credit = mission.get('credit')
if not this_credit:
    exit_code = EXIT_CODE_FAILED
    err_msg = '签到失败，缺少 mission.credit 字段'
    err_ctx = {'body': json.dumps(res_body)}
    logging.error(app_format_err(err_msg, err_ctx))
    app_failed(exit_code, err_msg, err_ctx)
    exit(exit_code)
total_credit = mission.get('my_credit')
if not total_credit:
    exit_code = EXIT_CODE_FAILED
    err_msg = '签到失败，缺少 mission.my_credit 字段'
    err_ctx = {'body': json.dumps(res_body)}
    logging.error(app_format_err(err_msg, err_ctx))
    app_failed(exit_code, err_msg, err_ctx)
    exit(exit_code)
app_ok(this_credit, total_credit)
logging.info(f'签到成功，获得积分 {this_credit}，当前总积分 {total_credit}')
