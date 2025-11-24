import json
import time
from playwright.sync_api import sync_playwright, TimeoutError

def login(page, user):
    page.goto("https://meroshare.cdsc.com.np/#/login")
    page.locator(".select2-selection__placeholder").click()
    page.locator(".select2-search__field").fill(user["dp"])
    page.locator(".select2-search__field").press("Enter")
    page.fill("#username", user["username"])
    page.fill("#password", user["password"])
    page.click(".btn.sign-in")
    page.wait_for_selector(".msi-asba")

def go_to_asba(page):
    page.click(".msi-asba")
    try:
        page.wait_for_selector(".company-list", timeout=5000)
        return True
    except TimeoutError:
        return False

def get_companies(page):
    try:
        return page.query_selector_all(".company-list")
    except Exception:
        return []

def is_valid_share(company):
    share_type = company.query_selector(".share-of-type")
    if not share_type:
        return False

    st = share_type.inner_text().strip()
    if st not in ["IPO", "FPO", "RESERVED"]:
        return False

    isin = company.query_selector(".isin")
    if not isin:
        return False

    if isin.get_attribute("tooltip") != "Share Group":
        return False

    if isin.inner_text().strip() != "Ordinary Shares":
        return False

    return True

def apply_for_company(page, user):
    try:
        apply_btn = page.locator('//button[contains(@class, "btn-issue") and .//i[contains(text(), "Apply")]]')
        apply_btn.first.click()
    except TimeoutError:
        return False

    page.wait_for_selector(".form-group:has-text('Minimum Quantity')")
    min_qty_el = page.locator('.form-group:has-text("Minimum Quantity") .form-value span')
    min_qty = min_qty_el.inner_text().strip()

    page.select_option("#selectBank", index=1)
    page.select_option("#accountNumber", index=1)
    page.fill("#appliedKitta", min_qty)
    page.fill("#crnNumber", user["crn"])
    page.click("#disclaimer")

    page.locator(".card-footer button.btn-primary").click()
    page.fill("#transactionPIN", user["pin"])
    page.locator(".confirm-page-btn .btn-primary").click()

    return True


def process_user(p, user, first_run=False):
    username = user["username"]
    name = user["name"]

    browser = p.chromium.launch(headless=False, slow_mo=100)
    page = browser.new_page()

    try:
        login(page, user)
        found = go_to_asba(page)
        if not found:
            print(f"No active IPO/FPO entries found. Program terminated.")
            raise SystemExit

        companies = get_companies(page)
        if not companies:
            print(f"No IPO/FPO found for {name} ({username}).")
            return

        applied_any = False
        for company in companies:
            if is_valid_share(company):
                if apply_for_company(page, user):
                    print(f"Applied for {name} ({username}).")
                    applied_any = True
                else:
                    print(f"Already applied or failed for {name} ({username}).")

        if not applied_any:
            print(f"No new applicable IPO/FPO for {name} ({username}).")

    except Exception as e:
        print(f"Error processing {name} ({username}): {e}")

    finally:
        browser.close()

def main():
    with open("userdata.json", "r") as f:
        data = json.load(f)

    users = data["users"]

    with sync_playwright() as p:
        for user in users:
            process_user(p, user)

if __name__ == "__main__":
    main()