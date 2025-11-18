from flask import Flask, render_template, request, jsonify
import threading, time, os, uuid, json, datetime
from playwright.sync_api import sync_playwright

app = Flask(__name__)

MASTER_PASSWORD = "Axel67"
TASKS_FILE = "tasks.json"
URL = "https://post-axel.onrender.com"   # Your server URL

def log_event(msg):
    with open("restart_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {msg}\n")
    print(msg)

# --------- Playwright Comment Function -------
def fb_comment_playwright(email, password, post_url, comment, task_id):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://www.facebook.com/login")
            page.fill('input[name="email"]', email)
            page.fill('input[name="pass"]', password)
            page.click('button[type="submit"]')
            page.wait_for_timeout(5000)

            page.goto(post_url)
            page.wait_for_timeout(5000)

            # Try Click and Fill comment - Use updated selectors if needed
            page.click('xpath=//div[@aria-label="Write a comment"]')
            page.fill('xpath=//div[@aria-label="Write a comment"]', comment)
            page.keyboard.press("Enter")

            page.wait_for_timeout(3000)
            browser.close()
            log_event(f"[{task_id}] Playwright comment posted: {comment}")
    except Exception as e:
        log_event(f"[{task_id}] Playwright Error: {e}")

# --------- Flask Routes ---------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/auto_comment", methods
