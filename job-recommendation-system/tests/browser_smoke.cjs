/* Optional end-to-end UI test. Run against a disposable demo instance only.
   npm install --no-save playwright@1.51.1
   npx playwright install chromium
   RESUME_FIXTURE=/absolute/path/resume.docx node tests/browser_smoke.cjs
*/
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

(async () => {
  const base = process.env.TEST_BASE_URL || 'http://127.0.0.1:5000';
  assert.ok(new URL(base).hostname === '127.0.0.1' || new URL(base).hostname === 'localhost', 'Use a local disposable instance.');
  const output = process.env.SCREENSHOT_DIR || path.resolve('docs/screenshots');
  fs.mkdirSync(output, {recursive:true});
  const browser = await chromium.launch({headless:true, args:['--no-sandbox']});
  const context = await browser.newContext({viewport:{width:1440,height:1050}, reducedMotion:'reduce'});
  const page = await context.newPage();
  const errors = [], external = [], failures = [], reports = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('response', response => { if (response.status() >= 400) failures.push(`${response.status()} ${response.url()}`); });
  await context.route('**/*', route => {
    const url = new URL(route.request().url());
    if (['http:', 'https:'].includes(url.protocol) && !['127.0.0.1','localhost'].includes(url.hostname)) {
      external.push(url.href); return route.abort();
    }
    return route.continue();
  });
  async function go(url) {
    const response = await page.goto(base + url, {waitUntil:'networkidle'});
    assert.equal(response.status(),200,`GET ${url}`);
  }
  async function screenshot(name) {
    await page.screenshot({path:path.join(output,name),fullPage:true});
  }
  async function checkWidth(label) {
    const geometry = await page.evaluate(() => ({viewport:innerWidth,width:document.documentElement.scrollWidth}));
    assert.ok(geometry.width <= geometry.viewport + 1, `${label} horizontal overflow: ${JSON.stringify(geometry)}`);
    reports.push({page:label,...geometry});
  }
  await go('/');
  await page.evaluate(() => document.fonts.ready);
  assert.ok(await page.evaluate(() => document.fonts.check('600 16px Manrope') && document.fonts.check('italic 400 40px Fraunces')), 'Bundled fonts load offline');
  assert.equal(await page.evaluate(() => document.getAnimations().filter(a => a.playState === 'running').length), 0, 'Reduced-motion preference disables decorative animation');
  await screenshot('landing-desktop.png');
  for (const width of [1024,768,390]) {
    await page.setViewportSize({width,height:900});
    await checkWidth(`landing-${width}`);
  }
  await page.setViewportSize({width:1440,height:1050});
  await page.emulateMedia({reducedMotion:'no-preference'});
  await page.reload({waitUntil:'domcontentloaded'});
  assert.ok(await page.evaluate(() => document.getAnimations().some(a => a.playState === 'running')), 'Entrances run with normal motion preference');
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.waitForFunction(() => document.getAnimations().every(a => a.playState !== 'running'));
  assert.ok(await page.getByRole('link',{name:'Find my matches'}).isVisible(), 'Motion cancellation preserves usable content');
  const noScript = await browser.newContext({javaScriptEnabled:false,reducedMotion:'reduce'});
  const plainPage = await noScript.newPage();
  await plainPage.goto(base + '/');
  assert.ok(await plainPage.getByRole('link',{name:'Find my matches'}).isVisible(), 'Content is available without JavaScript');
  await noScript.close();
  await go('/login');
  await page.getByLabel('Email address').fill('demo@jobmatch.com');
  await page.getByLabel('Password',{exact:true}).fill('Demo@123');
  await page.getByRole('button',{name:'Sign in',exact:true}).click();
  await page.waitForURL('**/dashboard');
  await screenshot('dashboard-desktop.png');
  const firstJob = await page.locator('.job-title-row h3 a').first().getAttribute('href');
  await go(firstJob);
  assert.ok(await page.getByText('It is more than a percentage.').isVisible());
  await screenshot('job-match-desktop.png');
  await go('/insights');
  assert.equal(await page.locator('canvas[data-chart]').count(),8);
  assert.equal(await page.evaluate(() => Object.keys(Chart.instances).length),8);
  await screenshot('insights-desktop.png');
  for (const width of [1366,1024,768,390]) {
    await page.setViewportSize({width,height:900});
    await go('/dashboard');
    await checkWidth(`dashboard-${width}`);
    if (width === 390) await screenshot('dashboard-mobile.png');
  }
  for (const url of ['/jobs','/profile','/skills','/simulator','/insights','/applications','/history']) {
    await go(url); await checkWidth(`${url}-390`);
  }
  await page.setViewportSize({width:1440,height:1050});
  await page.getByRole('button',{name:'Sign out',exact:true}).click();
  await page.waitForURL(base + '/');
  await go('/register');
  await page.getByLabel('Full name',{exact:true}).fill('Aarav Sharma');
  await page.getByLabel('Email address').fill(`browser-${Date.now()}@example.com`);
  await page.getByLabel('Password',{exact:true}).fill('Browsertest123');
  await page.getByLabel('Confirm password').fill('Browsertest123');
  await page.getByRole('button',{name:'Create account'}).click();
  await page.waitForURL('**/profile');
  await page.locator('#city').fill('Kolkata');
  await page.locator('#state').fill('West Bengal');
  await page.locator('#education').fill('B.Tech Computer Science');
  await page.locator('#experience_years').fill('1');
  await page.locator('#preferred_role').fill('Data Analyst');
  await page.locator('#preferred_location').fill('Kolkata / Remote');
  await page.locator('#expected_salary').fill('500000');
  await page.locator('#skills-input-entry').fill('Python, SQL, Excel, Power BI, Statistics');
  await page.locator('#skills-input-entry').press('Enter');
  await page.getByRole('button',{name:'Save my profile'}).click();
  await page.waitForLoadState('networkidle');
  assert.ok(await page.getByText('Profile saved and recommendations recalculated.').isVisible());
  if (process.env.RESUME_FIXTURE) {
    await page.locator('#resume').setInputFiles(process.env.RESUME_FIXTURE);
    await page.getByRole('button',{name:'Extract & review'}).click();
    await page.waitForURL('**/resume/review/*');
    await page.locator('input[name=education]').fill('BTech Computer Science');
    await page.getByRole('button',{name:'Confirm reviewed details'}).click();
    await page.waitForURL('**/profile');
    assert.ok(await page.getByText('Reviewed resume details saved.',{exact:false}).isVisible());
  }
  await go('/recommendations');
  const jobLink = await page.locator('.job-title-row h3 a').first().getAttribute('href');
  await go(jobLink);
  await page.getByRole('button',{name:'Save job',exact:true}).click();
  await page.waitForLoadState('networkidle');
  assert.ok(await page.getByRole('button',{name:'Unsave job',exact:true}).isVisible());
  await page.getByRole('button',{name:'Apply · Track locally',exact:false}).click();
  await page.waitForURL('**/applications');
  await page.locator('.inline-form select').first().selectOption('Interview');
  await page.getByRole('button',{name:'Update',exact:true}).first().click();
  await page.waitForLoadState('networkidle');
  assert.equal(await page.locator('.status-interview').count(),1);
  await go('/simulator');
  await page.locator('#simulation-skills-entry').fill('Tableau,DAX');
  await page.locator('#simulation-skills-entry').press('Enter');
  await page.getByRole('button',{name:'Simulate my next move'}).click();
  await page.waitForLoadState('networkidle');
  assert.equal(await page.locator('.simulation-card').count(),12);
  await screenshot('simulator-desktop.png');
  await go('/history');
  assert.ok(await page.locator('.timeline .panel').count() >= 2);
  await page.getByRole('button',{name:'Sign out',exact:true}).click();
  await page.waitForURL(base + '/');
  await go('/admin/login');
  await page.getByLabel('Email address').fill('admin@jobmatch.com');
  await page.getByLabel('Password',{exact:true}).fill('Admin@123');
  await page.getByRole('button',{name:'Sign in',exact:true}).click();
  await page.waitForURL('**/admin/');
  await go('/admin/jobs/new');
  const jobTitle = `Browser QA Analyst ${Date.now()}`;
  await page.getByLabel('Job title *',{exact:true}).fill(jobTitle);
  await page.getByLabel('Company name *',{exact:true}).fill('Browser Test Labs');
  await page.getByLabel('Location',{exact:true}).fill('Remote');
  await page.getByLabel('Job description *',{exact:true}).fill('Analyze QA data using Python and SQL to validate test coverage and report product quality.');
  await page.getByLabel('Required skills',{exact:true}).fill('Python, SQL');
  await page.getByRole('button',{name:'Save opportunity'}).click();
  await page.waitForURL('**/admin/jobs');
  let row = page.getByRole('row').filter({hasText:jobTitle});
  await row.getByRole('link',{name:'Edit',exact:true}).click();
  await page.getByLabel('Job title *',{exact:true}).fill(jobTitle + ' Updated');
  await page.getByRole('button',{name:'Save opportunity'}).click();
  await page.waitForURL('**/admin/jobs');
  row = page.getByRole('row').filter({hasText:jobTitle + ' Updated'});
  page.once('dialog',dialog=>dialog.accept());
  await row.getByRole('button',{name:'Remove',exact:true}).click();
  await page.waitForLoadState('networkidle');
  assert.ok(await page.getByRole('row').filter({hasText:jobTitle + ' Updated'}).getByText('Removed',{exact:true}).isVisible());
  assert.deepEqual(errors, [], 'No browser JavaScript errors');
  assert.deepEqual(external, [], 'No requests to external services');
  assert.deepEqual(failures, [], 'No failed HTTP resources');
  const report = {status:'passed',browser:await browser.version(),viewportChecks:reports,jsErrors:errors,externalRequests:external,failedResources:failures,
    workflow:['landing','offline fonts','normal motion','live reduced-motion cancellation','JavaScript-disabled landing','demo dashboard','job explanation','8 charts','responsive layouts','registration','profile save','resume review','recommendations','save','apply locally','Interview status','what-if simulation','history','logout','admin login','admin create/edit/delete']};
  fs.writeFileSync(path.join(output,'browser-results.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));
  await browser.close();
})().catch(error => {console.error(error);process.exit(1);});
