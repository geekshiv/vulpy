"""Deliberately vulnerable module added to test PR-gating behaviour.

Not reachable from the app. Exists only so a pull request contains net-new
SAST findings and a net-new vulnerable dependency at the same time, so a
scanner's PR check can be observed reacting to both.
"""
import os
import sqlite3

from flask import Blueprint, request

mod_report = Blueprint("mod_report", __name__)


@mod_report.route("/report/export")
def export():
    # Command injection: unsanitised request parameter into a shell.
    fmt = request.args.get("format")
    os.system("generate-report --format " + fmt)
    return "exported"


@mod_report.route("/report/lookup")
def lookup():
    # SQL injection: unsanitised request parameter concatenated into a query.
    username = request.args.get("username")
    conn = sqlite3.connect("db_users.sqlite")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = '" + username + "'")
    return str(cur.fetchall())
