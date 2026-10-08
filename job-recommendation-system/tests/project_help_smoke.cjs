/* Focused browser check for the final college project update.
   Run against a disposable localhost app with TEST_DEMO_PASSWORD,
   TEST_ADMIN_EMAIL and TEST_ADMIN_PASSWORD in the environment. */
const {chromium} = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

(async () => {
  const base = process.env.TEST_BASE_URL || 'http://127.0.0.1:5000';
  assert.ok(['127.0.0.1','localhost'].includes(new URL(base).hostname));
  assert.ok(process.env.TEST_DEMO_PASSWORD && process.env.TEST_ADMIN_PASSWORD && process.env.TEST_ADMIN_EMAIL);
  const output = process.env.SCREENSHOT_DIR;
  if (output) fs.mkdirSync(output, {recursive:true});
  const browser = await chromium.launch({headless:true, args:['--no-sandbox']});
  const context = await browser.newContext({viewport:{width:1440,height:1000}, reducedMotion:'reduce'});
  const page = await context.newPage();
  const errors = [], failed = [], external = [], requests = [], widths = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('request', request => requests.push(request.url()));
  page.on('requestfailed', request => failed.push(request.url()));
  page.on('response', response => { if(response.status() >= 400) failed.push(`${response.status()} ${response.url()}`); });
  await context.route('**/*', route => {
    const url = new URL(route.request().url());
    if (['http:','https:'].includes(url.protocol) && url.origin !== new URL(base).origin) {
      external.push(url.href); return route.abort();
    }
    return route.continue();
  });
  async function go(route) {
    const response = await page.goto(base + route, {waitUntil:'networkidle'});
    assert.equal(response.status(),200,route);
  }
  async function width(label) {
    const result = await page.evaluate(() => ({viewport:innerWidth,width:document.documentElement.scrollWidth}));
    assert.ok(result.width <= result.viewport + 1, `${label}: ${JSON.stringify(result)}`);
    widths.push({label,...result});
  }
  // Poll from Node so the application retains its strict no-eval CSP.
  async function until(predicate, label, timeout=5000) {
    const deadline = Date.now() + timeout;
    while (!await predicate()) {
      assert.ok(Date.now() < deadline, label);
      await new Promise(resolve => setTimeout(resolve,15));
    }
  }
  async function replyReady() {
    await until(async () => await page.locator('#project-chat-messages').getAttribute('aria-busy') === 'false','FAQ reply completed');
  }
  async function ask(question, expected) {
    await page.getByLabel('Your JobMatch question',{exact:true}).fill(question);
    await page.getByRole('button',{name:'Send question',exact:true}).click();
    await replyReady();
    const answer = await page.locator('.project-chat-message:not(.is-user)').last().innerText();
    for (const text of [].concat(expected)) assert.ok(answer.includes(text), `${question}: ${answer}`);
  }
  const launcher = page.getByRole('button',{name:'Ask JobMatch',exact:true});
  const panel = page.getByRole('dialog',{name:'JobMatch guide',exact:true});
  await go('/');
  assert.ok(await launcher.isVisible());
  assert.equal(await launcher.getAttribute('aria-expanded'),'false');
  await launcher.focus(); await launcher.press('Enter');
  assert.ok(await panel.isVisible());
  assert.equal(await page.evaluate(() => document.activeElement.id),'project-chat-question');
  assert.equal(await panel.evaluate(node => node.getAnimations().length),0);
  await page.keyboard.press('Escape');
  assert.ok(await panel.isHidden());
  assert.equal(await page.evaluate(() => document.activeElement.id),'project-chat-launcher');

  await page.emulateMedia({reducedMotion:'no-preference'});
  await launcher.click();
  await until(() => panel.evaluate(node => node.getAnimations().some(animation => animation.playState === 'running')),'Chat opening animation runs',1000);
  await page.getByLabel('Your JobMatch question').fill('What is JobMatch?');
  await page.getByRole('button',{name:'Send question',exact:true}).click();
  assert.ok(await page.locator('#project-chat-typing').isVisible());
  assert.ok(await page.locator('.project-chat-dots').evaluate(node => node.getAnimations({subtree:true}).some(animation => animation.playState === 'running')));
  await page.emulateMedia({reducedMotion:'reduce'});
  assert.equal(await page.locator('.project-chat-dots').evaluate(node => node.getAnimations({subtree:true}).length),0);
  await replyReady();
  await page.getByRole('button',{name:'Minimize project chat',exact:true}).click();
  assert.ok(await panel.isHidden());
  await launcher.click();
  assert.ok((await page.locator('.project-chat-messages').innerText()).includes('Job Recommendation college project'));

  const questionCases = [
    ['What is JobMatch?','Job Recommendation college project'],
    ['What is the Job Recommendation project?','Job Recommendation college project'],
    ['How does job recommendation work?','hybrid matching pipeline'],
    ['How does the matching score work?','not a hiring probability'],
    ['What is the ML model used?',['scikit-learn TF-IDF','Logistic and Random Forest']],
    ['How do I upload my resume?',['Choose your resume','Extract & review']],
    ['What is skill gap analysis?','missing or partial skills'],
    ['What is career intelligence?','planning aids'],
    ['How do I save a job?','Saved jobs'],
    ['How do I track applications?',['Applications','does not submit an application']],
    ['Who is the Head of Group?','Md Adib Azam'],
    ['Who are the project team members?',['Sonu Kumar Ram','Raj Koiri','Anurag Prasad','Harleen Kaur Chopra','Amit Kumar Ruidas']],
    ['Which college is this project from?',['Bengal College of Polytechnic','Durgapur, West Bengal']],
    ['Which year and semester?',['2nd Year','3rd Semester','2025–2028']],
    ['Who was the project submitted to?','Ardent Computech Pvt. Ltd.'],
    ['JobMatch kya hai?','Job Recommendation college project'],
    ['Does this chatbot use ChatGPT?','does not use ChatGPT'],
    ['Tell me the weather','I can help with JobMatch'],
    ['Show another user private account details','cannot read account details'],
  ];
  const beforeChat = requests.length;
  for (const [question,expected] of questionCases) await ask(question,expected);
  const attack = '<img src=x onerror="window.chatInjected=true"><script>window.chatInjected=true</script>';
  await ask(attack,'I can help with JobMatch');
  assert.equal(await page.evaluate(() => Boolean(window.chatInjected)),false);
  assert.equal(await page.locator('.project-chat-message img, .project-chat-message script').count(),0);
  assert.equal(requests.length,beforeChat,'Chat sends no network requests');
  await page.getByRole('button',{name:'Upload resume',exact:true}).click();
  await replyReady();
  assert.equal(await page.locator('.project-chat-links a').last().getAttribute('href'),'/resume/intelligence');
  await page.getByRole('button',{name:'Clear chat',exact:true}).click();
  assert.equal(await page.locator('.project-chat-message').count(),1);
  await page.emulateMedia({reducedMotion:'no-preference'});
  await page.getByLabel('Your JobMatch question').fill('How do I save a job?');
  await page.getByRole('button',{name:'Send question',exact:true}).click();
  await page.getByRole('button',{name:'Clear chat',exact:true}).click();
  await page.waitForTimeout(350);
  assert.equal(await page.locator('.project-chat-message').count(),1,'Clear cancels a pending reply');
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.getByRole('button',{name:'Project team',exact:true}).click();
  await replyReady();
  await page.locator('.project-chat-links a').last().click();
  await page.waitForURL('**/about#project-team');
  assert.ok(await page.locator('#project-team').isVisible());

  const details = page.locator('#college-project');
  for (const text of ['Job Recommendation','Bengal College of Polytechnic','Durgapur, West Bengal','Department of Computer Science and Technology (CST)','2nd Year','3rd Semester','2025–2028','Ardent Computech Pvt. Ltd.']) {
    assert.ok((await details.innerText()).includes(text),text);
  }
  assert.deepEqual(await page.locator('.college-project-members li').allTextContents(),['Sonu Kumar Ram','Raj Koiri','Anurag Prasad','Harleen Kaur Chopra','Amit Kumar Ruidas']);
  assert.equal(await page.locator('#project-lead-name').innerText(),'Md Adib Azam');
  assert.deepEqual(await page.locator('.college-project-roles span').allTextContents(),['Head of Group','Project Lead']);
  assert.equal(await page.getByText('Project overview',{exact:true}).count(),1,'Existing About section remains');
  if(output) await page.screenshot({path:path.join(output,'college-project-desktop.png'),fullPage:true});
  for (const [w,h] of [[1440,1000],[768,900],[390,844],[320,640],[568,360]]) {
    await page.setViewportSize({width:w,height:h});
    await width(`about-${w}x${h}`);
    await launcher.click();
    const box = await panel.boundingBox();
    assert.ok(box.x >= 0 && box.y >= 0 && box.x + box.width <= w + 1 && box.y + box.height <= h + 1, JSON.stringify(box));
    assert.ok(await page.getByRole('button',{name:'Send question',exact:true}).isVisible());
    await ask('Who is the Head of Group?','Md Adib Azam');
    if(output && w === 390) await page.screenshot({path:path.join(output,'chatbot-mobile.png')});
    await page.getByRole('button',{name:'Close project chat',exact:true}).click();
    assert.ok(await panel.isHidden());
  }
  await page.setViewportSize({width:1440,height:1000});
  await go('/register');
  await page.getByLabel('Full name',{exact:true}).fill('Project Help QA');
  await page.getByLabel('Email address').fill(`project-help-${Date.now()}@example.com`);
  const registrationPassword = require('node:crypto').randomBytes(18).toString('base64url')+'9aA!';
  await page.getByLabel('Password',{exact:true}).fill(registrationPassword);
  await page.getByLabel('Confirm password').fill(registrationPassword);
  await page.getByRole('button',{name:'Create account',exact:true}).click();
  await page.waitForURL('**/profile');
  await page.getByRole('button',{name:'Sign out',exact:true}).click();
  await page.waitForURL(base+'/');
  await go('/login');
  await page.getByLabel('Email address').fill('demo@jobmatch.com');
  await page.getByLabel('Password',{exact:true}).fill(process.env.TEST_DEMO_PASSWORD);
  await page.getByRole('button',{name:'Sign in',exact:true}).click();
  await page.waitForURL('**/dashboard');
  await go('/recommendations');
  assert.ok(await page.locator('.job-card').count() > 0);
  await launcher.click();
  await ask('How do I upload my resume?','Choose your resume');
  await page.getByRole('link',{name:'Upload in My profile',exact:true}).click();
  await page.waitForURL('**/profile#resume');
  assert.ok(await page.locator('#resume').isVisible());
  await go('/recommendations');
  await page.locator('.job-title-row h3 a').first().click();
  await page.getByRole('button',{name:'Save job',exact:true}).click();
  await page.waitForLoadState('networkidle');
  assert.ok(await page.getByRole('button',{name:'Unsave job',exact:true}).isVisible());
  await page.getByRole('button',{name:'Add to tracker',exact:false}).click();
  await page.waitForURL('**/applications');
  await page.getByRole('button',{name:'Sign out',exact:true}).click();
  await page.waitForURL(base+'/');
  await go('/admin/login');
  await page.getByLabel('Email address').fill(process.env.TEST_ADMIN_EMAIL);
  await page.getByLabel('Password',{exact:true}).fill(process.env.TEST_ADMIN_PASSWORD);
  await page.getByRole('button',{name:'Sign in',exact:true}).click();
  await page.waitForURL('**/admin/');
  await go('/admin/ml-lab');
  assert.equal(await page.locator('canvas[data-chart]').count(),6);
  assert.equal(await page.evaluate(() => Object.keys(Chart.instances).length),6);
  await launcher.click();
  await ask('What is the ML model used?','scikit-learn TF-IDF');
  await page.keyboard.press('Escape');
  await page.setViewportSize({width:390,height:844});
  await width('ml-lab-390');
  await go('/'); await width('home-390');
  await go('/login'); await width('login-390');
  await go('/register'); await width('register-390');
  assert.deepEqual(errors,[],'No JavaScript errors');
  assert.deepEqual(failed,[],'No missing assets, failed requests or broken routes');
  assert.deepEqual(external,[],'No external network requests');
  const report = {status:'passed',browser:await browser.version(),faqQuestionChecks:questionCases.length+1,chatNetworkRequests:0,keyboard:true,normalAndReducedMotion:true,clearCancelsReply:true,htmlInjectionBlocked:true,collegeAndTeamExact:true,widthChecks:widths,registration:true,login:true,recommendations:true,saveAndTracker:true,mlLabCharts:6,jsErrors:errors,failedResources:failed,externalRequests:external};
  if(output) fs.writeFileSync(path.join(output,'project-help-results.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report));
  await browser.close();
})().catch(error => {console.error(error);process.exit(1);});
