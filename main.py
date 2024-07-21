import json
from playwright.sync_api import sync_playwright

def main():
    # Load user data from json
    with open('userdata.json', 'r') as f:
        data = json.load(f)
    
    users = data['users']
    
    with sync_playwright() as p:
        try:
            for user in users:
                browser = p.chromium.launch(headless=False, slow_mo=500)
                page = browser.new_page()

                try:
                    page.goto('https://meroshare.cdsc.com.np/#/login')

                    # Login
                    page.locator('.select2-selection__placeholder').click()
                    page.locator('.select2-search__field').fill(user['dp'])
                    page.locator('.select2-search__field').press('Enter')
                    page.locator('#username').fill(user['username'])
                    page.locator('#password').fill(user['password'])
                    page.locator('.btn.sign-in').click()

                    # Navigate to My ASBA 
                    page.wait_for_selector('.msi-asba').click()

                    # Check and apply for any new IPO or FPO
                    try:
                        company_lists = page.query_selector_all('.company-list')
                    except playwright.Error as e:
                        company_lists = []
                        print(f"No new IPO or FPO found.")
                    
                    for company_list in company_lists:
                        share_of_type_element = company_list.query_selector('.share-of-type')
                        if share_of_type_element:
                            share_of_type_text = share_of_type_element.inner_text().strip()
                            if share_of_type_text in ['IPO', 'FPO']:
                                apply_button = company_list.query_selector('xpath=//div[contains(@class, "action-buttons")]//button[contains(@class, "btn-issue") and .//i[contains(text(), "Apply")]]')
                                if apply_button:
                                    apply_button.click()

                                    # Fill application form
                                    form_group = page.query_selector('.form-group:has-text("Minimum Quantity")')
                                    minimum_quantity_value = 0
                                    minimum_quantity_element = form_group.query_selector('.form-value span')
                                    if minimum_quantity_element:
                                        minimum_quantity_value = minimum_quantity_element.inner_text().strip()

                                    page.select_option('#selectBank', index=1)
                                    page.select_option('#accountNumber', index=1)
                                    page.locator('#appliedKitta').fill(str(minimum_quantity_value))
                                    page.locator('#crnNumber').fill(user['crn'])
                                    page.locator('#disclaimer').click()

                                    # PIN confirmation
                                    proceed_button = page.wait_for_selector('.card-footer button.btn-primary:visible')
                                    if proceed_button:
                                        proceed_button.click()
                                        page.locator('#transactionPIN').fill(user['pin'])
                                        page.wait_for_selector('.confirm-page-btn .btn-primary').click()
                            else:
                                print(f"No new IPO or FPO found.")

                except playwright.Error as e:
                    print(f"Playwright error: {e}")

                except Exception as e:
                    print(f"Exception occurred: {str(e)}")

                finally:
                    page.close()
                    browser.close()

        except playwright.Error as e:
            print(f"Playwright error: {e}")

        except Exception as e:
            print(f"Exception occurred: {str(e)}")


if __name__ == "__main__":
    main()