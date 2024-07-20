from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()
    page.goto('https://meroshare.cdsc.com.np/#/login')
    page.click('.select2-selection__placeholder')
    page.fill('.select2-search__field', '1')
    page.press('.select2-search__field', 'Enter')
    page.fill('#username', "username")
    page.fill('#password', "password")
    page.click('.btn.sign-in')
    page.is_visible('.msi-asba')
    page.click('.msi-asba')