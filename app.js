require('dotenv').config();
const puppeteer = require('puppeteer');

const DP = process.env.DP;
const USERNAME = process.env.USERNAME;
const PASSWORD = process.env.PASSWORD;

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });

  await page.goto('https://meroshare.cdsc.com.np/#/login');
  await page.waitForSelector('.sign-in');

  const selectDp = await page.$('.select2-selection__placeholder');
  if (selectDp) {
    await selectDp.click();
    await selectDp.type(DP);
    await selectDp.press('Enter');
  }

  const username = await page.$('#username');
  if(username) {
    await username.click();
    await username.type(USERNAME);
  }

  const password = await page.$('#password');
  if(password) {
    await password.click();
    await password.type(PASSWORD);
  }

  const signIn = await page.$('.btn.sign-in');
  if(signIn) {
    await signIn.click();
  }

  await page.waitForSelector('.user-profile-role');
  await page.screenshot({ path: 'debug.png' });

  await browser.close();
})();