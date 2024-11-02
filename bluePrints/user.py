import json, operator, requests, string, random, time, re, base64
from datetime import datetime, timedelta
from flask import Blueprint, request, redirect, url_for, session, render_template, g, jsonify
from exts import db, mail
from config import APPID, APPSECRET
from flask_mail import Message
from sqlalchemy import and_, or_, func

bp = Blueprint("user", __name__, url_prefix="/user")


# 字符串编码
def encode(input_string):
    byte_string = input_string.encode('utf-8')
    base64_bytes = base64.b64encode(byte_string)
    encoded_string = base64_bytes.decode()
    return encoded_string


# 字符串解码
def decode(encoded_string):
    base64_bytes = encoded_string.encode('utf-8')
    byte_string = base64.b64decode(base64_bytes)
    decoded_string = byte_string.decode()
    return decoded_string

