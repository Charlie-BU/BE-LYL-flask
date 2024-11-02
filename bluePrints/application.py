import json, operator, string, random, time, re, base64
from datetime import datetime, timedelta
from flask import Blueprint, request, redirect, url_for, session, render_template, g, jsonify, flash
from sqlalchemy import and_, or_
from exts import db
from wxpay import *
from hooks import inform

bp = Blueprint("application", __name__, url_prefix="/application")

# @bp.route('/test', methods=['POST'])
# def test():
