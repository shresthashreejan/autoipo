const fs = require('fs');
const puppeteer = require('puppeteer');

const login = async (user) => {
  const browser = await puppeteer.launch({headless: false});
  const page = await browser.newPage();
  await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36');
  await page.setViewport({ width: 1920, height: 1080 });

  let loginPage = await page.goto('https://meroshare.cdsc.com.np/#/login');
  if(loginPage.status() != 404){
    console.log("status: ok");
  }
  await page.waitForSelector('.sign-in');

  const selectDp = await page.$('.select2-selection__placeholder');
  if (selectDp) {
    await selectDp.click();
    await selectDp.type(user.dp);
    await selectDp.press('Enter');
  }

  const username = await page.$('#username');
  if(username) {
    await username.click();
    await username.type(user.username);
  }

  const password = await page.$('#password');
  if(password) {
    await password.click();
    await password.type(user.password);
  }

  const signIn = await page.$('.btn.sign-in');
  if(signIn) {
    await signIn.click();
  }

  await page.waitForSelector('.user-profile-role');
  await page.screenshot({ path: `${user.username}_debug.png` });

  browser.close();
};

const users = JSON.parse(fs.readFileSync('sample.json')).users;

for (const user of users) {
  await login(user);
}