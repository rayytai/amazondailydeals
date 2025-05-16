// deals.js
const fs        = require('fs');
const puppeteer = require('puppeteer');

(async () => {
  // Launch headless Chrome
  const browser = await puppeteer.launch({
    args: ['--no-sandbox','--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  await page.setUserAgent('Mozilla/5.0');
  // Go to Amazon Gold Box deals
  await page.goto('https://www.amazon.com/gp/goldbox', { waitUntil: 'networkidle2' });

  // Wait for deals to render (adjust selector if needed)
  await page.waitForSelector('a.a-link-normal[href*="/dp/"]', { timeout: 10000 });

  // Extract deals
  const deals = await page.$$eval(
    'a.a-link-normal[href*="/dp/"]',
    links => links.map(a => {
      // Title: any span whose class includes "truncate"
      const titleEl = a.querySelector('span[class*="truncate"]');
      // Price: the whole-dollar span
      const priceEl = a.querySelector('span.a-price-whole');
      return {
        title: titleEl ? titleEl.innerText.trim() : null,
        link:  'https://amazon.com' + a.getAttribute('href'),
        price: priceEl ? priceEl.innerText.trim() : null
      };
    }).filter(d => d.title && d.price)
  );

  await browser.close();

  // Save to deals.json
  fs.writeFileSync('deals.json', JSON.stringify(deals, null, 2));
  console.log(`Fetched ${deals.length} deals`);
})().catch(err => {
  console.error(err);
  process.exit(1);
});
