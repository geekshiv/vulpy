import sqlite3

# Deliberately insecure sample used to exercise Rikugan PR Guardrail.
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
DJANGO_SECRET_KEY = "django-insecure-8f3k2j4h5g6f7d8s9a0p1o2i3u4y5t6r7e8w9q0"


def lookup_user(username):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = '" + username + "'")
    return cur.fetchall()
