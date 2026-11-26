#!/usr/bin/env node
'use strict';
// Opt-in rendered contracts for the catalog's design examples. No server/install.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

function contrast(first, second) {
  const luminance = (rgb) => rgb.slice(0, 3).map((channel) => {
    const value = channel / 255;
    return value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
  }).reduce((sum, value, index) => sum + value * [0.2126, 0.7152, 0.0722][index], 0);
  const values = [luminance(first), luminance(second)].sort((a, b) => a - b);
  return (values[1] + 0.05) / (values[0] + 0.05);
}

// Runs inside the page. Audit actual computed colors and rendered geometry, not
// token names. Unknown paint (images/alpha/opacity) fails rather than being skipped.
function installAudit() {
  const requireCheck = (condition, message) => { if (!condition) throw new Error(message); };
  const describe = (element) => `${element.tagName.toLowerCase()}${element.id ? `#${element.id}` : ''} ${element.textContent.trim().slice(0, 65)}`;
  const rgba = (value) => {
    const match = value.match(/^rgba?\(([^)]+)\)$/);
    requireCheck(match, `Unsupported computed color: ${value}`);
    const channels = match[1].split(/[,\s/]+/).map(Number);
    if (channels.length === 3) channels.push(1);
    requireCheck(channels.length === 4 && channels.every(Number.isFinite), `Invalid color: ${value}`);
    return channels;
  };
  const visible = (element) => {
    const css = getComputedStyle(element);
    return css.visibility === 'visible' && element.getClientRects().length > 0;
  };
  const surface = (element) => {
    for (let current = element; current; current = current.parentElement) {
      const css = getComputedStyle(current);
      requireCheck(css.backgroundImage === 'none', `Unaudited background image: ${describe(current)}`);
      const color = rgba(css.backgroundColor);
      requireCheck(color[3] === 0 || color[3] === 1, `Translucent surface: ${describe(current)}`);
      if (color[3] === 1) return color;
    }
    throw new Error('No opaque surface behind content');
  };
  const opaque = (element) => {
    for (let current = element; current; current = current.parentElement) {
      requireCheck(Number(getComputedStyle(current).opacity) === 1, `Faded content: ${describe(current)}`);
    }
  };
  const ratio = (ink, background, minimum, label) => {
    requireCheck(ink[3] === 1, `Translucent ink: ${label}`);
    const value = window.designContrast(ink, background);
    requireCheck(value >= minimum, `${label}: contrast ${value} < ${minimum}`);
    return value; // Never round before comparing.
  };
  const tabbables = () => Array.from(document.querySelectorAll(
    'a[href], button, input, select, textarea, summary, [tabindex], [contenteditable="true"]',
  )).filter((element) => element.tabIndex >= 0 && !element.matches(':disabled') && visible(element));

  window.designAudit = {
    tabCount: () => tabbables().length,
    activeIndex: () => tabbables().indexOf(document.activeElement),
    layout: () => {
      requireCheck(document.documentElement.scrollWidth <= innerWidth,
        `Page scrolls horizontally: ${document.documentElement.scrollWidth} > ${innerWidth}`);
      requireCheck(document.body.scrollWidth <= innerWidth, 'Body scrolls horizontally');
    },
    colors: () => {
      let texts = 0;
      let indicators = 0;
      let minimumText = Infinity;
      let minimumIndicator = Infinity;
      const text = (element, color) => {
        opaque(element);
        minimumText = Math.min(minimumText, ratio(rgba(color), surface(element), 4.5, `Text ${describe(element)}`));
        texts += 1;
      };
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      for (let node = walker.nextNode(); node; node = walker.nextNode()) {
        const element = node.parentElement;
        if (!node.textContent.trim() || element.closest('script, style, template') || !visible(element)) continue;
        const range = document.createRange();
        range.selectNodeContents(node);
        if (Array.from(range.getClientRects()).some((rect) => rect.width && rect.height)) text(element, getComputedStyle(element).color);
      }
      for (const element of document.querySelectorAll('input, textarea, select')) {
        if (!visible(element)) continue;
        if (element.value) text(element, getComputedStyle(element).color);
        if (!element.value && element.getAttribute('placeholder')) {
          const placeholder = getComputedStyle(element, '::placeholder');
          requireCheck(Number(placeholder.opacity) === 1, 'Faded placeholder');
          text(element, placeholder.color);
        }
      }
      // Essential control edges; faint card/table separators are decorative.
      for (const element of document.querySelectorAll('button, input, select, textarea, .action-link, .notice')) {
        if (!visible(element)) continue;
        opaque(element);
        const css = getComputedStyle(element);
        for (const side of ['Top', 'Right', 'Bottom', 'Left']) {
          requireCheck(parseFloat(css[`border${side}Width`]) > 0 && !['none', 'hidden'].includes(css[`border${side}Style`]), `Missing control edge: ${describe(element)}`);
          const ink = rgba(css[`border${side}Color`]);
          // Solid primary actions use the fill/edge against the outside surface;
          // outlined fields and neutral sort buttons also contrast with their fill.
          minimumIndicator = Math.min(minimumIndicator,
            ratio(ink, surface(element.parentElement), 3, `Outer edge ${describe(element)}`));
          if (element.matches('input, select, textarea, .sort-button, :disabled, [aria-disabled="true"], .notice')) {
            minimumIndicator = Math.min(minimumIndicator, ratio(ink, surface(element), 3, `Inner edge ${describe(element)}`));
          }
          indicators += 1;
        }
      }
      for (const icon of document.querySelectorAll('.icon')) {
        if (!visible(icon)) continue;
        minimumIndicator = Math.min(minimumIndicator, ratio(rgba(getComputedStyle(icon).stroke), surface(icon), 3, 'Navigation icon'));
        indicators += 1;
      }
      requireCheck(texts > 0, 'No rendered text was audited');
      return { texts, indicators, minimumText, minimumIndicator };
    },
    focus: (forcedColors) => {
      const element = document.activeElement;
      requireCheck(tabbables().includes(element), 'Tab did not reach an expected element');
      requireCheck(element.matches(':focus-visible'), `No keyboard focus-visible: ${describe(element)}`);
      const css = getComputedStyle(element);
      const width = parseFloat(css.outlineWidth);
      const offset = parseFloat(css.outlineOffset);
      const root = getComputedStyle(document.documentElement);
      requireCheck(width >= parseFloat(root.getPropertyValue('--focus-width')) && css.outlineStyle !== 'none', `Missing focus outline: ${describe(element)}`);
      requireCheck(offset >= parseFloat(root.getPropertyValue('--focus-offset')), `Focus offset lost: ${describe(element)}`);
      opaque(element);
      // In forced colors the system palette owns contrast (Chromium's emulated
      // Highlight is translucent); check that the ring uses Highlight instead.
      if (!forcedColors) ratio(rgba(css.outlineColor), surface(element.parentElement), 3, `Focus ${describe(element)}`);
      if (forcedColors) {
        const probe = document.createElement('span');
        probe.style.color = 'Highlight';
        document.body.append(probe);
        const highlight = getComputedStyle(probe).color;
        probe.remove();
        requireCheck(css.outlineColor === highlight, `Focus lost system Highlight: ${describe(element)}`);
        requireCheck(css.forcedColorAdjust !== 'none', 'Forced colors disabled');
      }
      // Check every inline fragment and every clipping ancestor, including the
      // viewport. Table focus must fit inside the local scrollport's padding.
      const extent = width + offset;
      for (const rect of element.getClientRects()) {
        const ring = { left: rect.left - extent, top: rect.top - extent, right: rect.right + extent, bottom: rect.bottom + extent };
        requireCheck(ring.left >= 0 && ring.right <= innerWidth && ring.top >= 0 && ring.bottom <= innerHeight,
          `Focus clipped by viewport: ${describe(element)}`);
        for (let parent = element.parentElement; parent; parent = parent.parentElement) {
          const parentCSS = getComputedStyle(parent);
          const box = parent.getBoundingClientRect();
          if (/(auto|scroll|hidden|clip)/.test(parentCSS.overflowX)) {
            requireCheck(ring.left >= box.left + parent.clientLeft && ring.right <= box.left + parent.clientLeft + parent.clientWidth,
              `Focus clipped horizontally by ${describe(parent)}`);
          }
          if (/(auto|scroll|hidden|clip)/.test(parentCSS.overflowY)) {
            requireCheck(ring.top >= box.top + parent.clientTop && ring.bottom <= box.top + parent.clientTop + parent.clientHeight,
              `Focus clipped vertically by ${describe(parent)}`);
          }
        }
      }
      return describe(element);
    },
    motion: () => {
      requireCheck(matchMedia('(prefers-reduced-motion: reduce)').matches, 'Reduced motion not emulated');
      for (const element of document.querySelectorAll('*')) {
        for (const pseudo of [null, '::before', '::after']) {
          const css = getComputedStyle(element, pseudo);
          for (const property of ['transitionDuration', 'transitionDelay', 'animationDuration', 'animationDelay']) {
            requireCheck(css[property].split(',').every((value) => parseFloat(value) === 0), `Motion remains: ${describe(element)} ${property}`);
          }
          requireCheck(css.scrollBehavior !== 'smooth', `Smooth scrolling remains: ${describe(element)}`);
        }
      }
      requireCheck(document.getAnimations().length === 0, 'Animation still running');
    },
  };
}

async function tabThrough(page, forcedColors) {
  const count = await page.evaluate(() => window.designAudit.tabCount());
  assert.ok(count > 0, 'No tab stops');
  for (let index = 0; index < count; index += 1) {
    await page.keyboard.press('Tab');
    assert.equal(await page.evaluate(() => window.designAudit.activeIndex()), index, `Unexpected Tab order at ${index}`);
    await page.evaluate((forced) => window.designAudit.focus(forced), forcedColors);
    if (!forcedColors) await page.evaluate(() => window.designAudit.colors());
    await page.evaluate(() => window.designAudit.layout());
  }
  // Exercise reverse keyboard traversal too; no programmatic focus calls.
  for (let index = count - 2; index >= 0; index -= 1) {
    await page.keyboard.press('Shift+Tab');
    assert.equal(await page.evaluate(() => window.designAudit.activeIndex()), index);
    await page.evaluate((forced) => window.designAudit.focus(forced), forcedColors);
  }
  return count;
}

async function tabTo(page, selector) {
  const count = await page.evaluate(() => window.designAudit.tabCount());
  for (let step = 0; step < count + 2; step += 1) {
    if (await page.locator(selector).evaluate((element) => element === document.activeElement)) return;
    await page.keyboard.press('Tab');
  }
  throw new Error(`Cannot reach ${selector} using Tab`);
}

async function checkTable(page, width) {
  await tabTo(page, '.table-scroll');
  if (width === 320) {
    assert.ok(await page.locator('.table-scroll').evaluate((element) => element.scrollWidth > element.clientWidth));
    await page.locator('.table-scroll').evaluate((element) => { element.scrollLeft = 0; });
    const before = await page.locator('.table-scroll').evaluate((element) => element.scrollLeft);
    await page.keyboard.press('ArrowRight');
    await page.waitForFunction((previous) => document.querySelector('.table-scroll').scrollLeft > previous, before);
    // Keyboard scrolling animates and Home does not reset it horizontally: let the
    // scroll settle before Tab moves focus, then start the sorting checks at 0.
    await page.locator('.table-scroll').evaluate((element) => new Promise((resolve) => {
      let last = -1;
      const settle = () => {
        if (element.scrollLeft === last) { resolve(); return; }
        last = element.scrollLeft;
        setTimeout(settle, 150);
      };
      settle();
    }));
    await page.locator('.table-scroll').evaluate((element) => { element.scrollLeft = 0; });
  }
  for (const [column, key, values, direction] of [
    ['2', 'Enter', [3, 8, 12], 'ascending'],
    ['2', 'Space', [12, 8, 3], 'descending'],
    ['0', 'Enter', ['Content review', 'Release notes', 'Setup guide'], 'ascending'],
  ]) {
    const selector = `[data-column="${column}"]`;
    await tabTo(page, selector);
    await page.keyboard.press(key);
    assert.deepEqual(await page.locator(`tbody tr > :nth-child(${Number(column) + 1})`).allTextContents(), values.map(String));
    assert.equal(await page.locator('[aria-sort]').count(), 1);
    assert.equal(await page.locator(selector).evaluate((element) => element.parentElement.getAttribute('aria-sort')), direction);
    assert.ok(await page.locator(selector).evaluate((element) => element === document.activeElement), 'Sorting moved focus');
    assert.match(await page.locator('#sort-status').textContent(), new RegExp(`3 projects, sorted by .+, ${direction}\\.`));
    await page.evaluate(() => window.designAudit.focus(false));
    await page.evaluate(() => window.designAudit.colors());
  }
}

async function checkPointerStates(page) {
  // Read hover/pressed paint without activating links or submitting anything.
  const count = await page.evaluate(() => window.designAudit.tabCount());
  for (let index = 0; index < count; index += 1) {
    const target = await page.evaluateHandle((wanted) => Array.from(document.querySelectorAll(
      'a[href], button, input, select, textarea, summary, [tabindex], [contenteditable="true"]',
    )).filter((element) => element.tabIndex >= 0 && !element.matches(':disabled') &&
      getComputedStyle(element).visibility === 'visible' && element.getClientRects().length > 0)[wanted], index);
    try {
      await target.asElement().hover();
      // Let the tokenized transition finish; the final paint is the state pair.
      await page.waitForFunction(() => document.getAnimations().every((animation) => animation.playState === 'finished'));
      await page.evaluate(() => window.designAudit.colors());
      await page.mouse.down();
      await page.waitForFunction(() => document.getAnimations().every((animation) => animation.playState === 'finished'));
      await page.evaluate(() => window.designAudit.colors());
    } finally {
      await page.mouse.move(0, 0);
      await page.mouse.up();
      await target.dispose();
    }
  }
}

async function main() {
  if (process.argv.includes('--self-test')) {
    assert.equal(contrast([0, 0, 0], [255, 255, 255]), 21);
    const text = contrast([119, 119, 119], [255, 255, 255]);
    const indicator = contrast([149, 149, 149], [255, 255, 255]);
    assert.ok(text < 4.5 && text.toFixed(1) === '4.5');
    assert.ok(indicator < 3 && indicator.toFixed(1) === '3.0');
    assert.equal(contrast([255, 255, 255], [0, 0, 0]), 21);
    console.log('PASS browser contrast math (unrounded text and indicator thresholds)');
    return;
  }
  const modulePath = process.env.PLAYWRIGHT_MODULE;
  const executablePath = process.env.CHROMIUM_PATH;
  if (!modulePath || !executablePath) {
    console.log('skipped: Playwright not available');
    return;
  }
  let chromium;
  try {
    ({ chromium } = require(path.resolve(modulePath)));
  } catch (error) {
    if (error.code !== 'MODULE_NOT_FOUND') throw error;
    console.log('skipped: Playwright not available');
    return;
  }
  const root = path.resolve(__dirname, '..');
  const catalog = JSON.parse(fs.readFileSync(path.join(root, 'tools/catalog.json'), 'utf8'));
  const skill = catalog.skills.find((entry) => entry.name === 'design-style');
  const examples = skill.examples.filter((entry) => entry.path.endsWith('.html'));
  assert.ok(examples.length >= 4, 'Expected all design examples');
  const tokens = JSON.parse(fs.readFileSync(path.join(root, 'skills/design-style/references/tokens.json'), 'utf8'));
  const browser = await chromium.launch({ executablePath, headless: true }); // One launch; never retry or download.
  let cases = 0;
  let tabStops = 0;
  try {
    for (const colorScheme of ['light', 'dark']) {
      for (const viewport of [{ width: 320, height: 900 }, { width: 1440, height: 900 }, { width: 1100, height: 640 }]) {
        for (const mode of ['normal', 'forced-colors', 'reduced-motion']) {
          const context = await browser.newContext({ viewport, colorScheme,
            forcedColors: mode === 'forced-colors' ? 'active' : 'none',
            reducedMotion: mode === 'reduced-motion' ? 'reduce' : 'no-preference', offline: true });
          await context.route('**/*', (route) => route.request().url().startsWith('file:') ? route.continue() : route.abort());
          await context.addInitScript(`window.designContrast = ${contrast.toString()}; (${installAudit.toString()})();`);
          try {
            for (const example of examples) {
              const label = `${path.basename(example.path)} ${colorScheme} ${viewport.width}x${viewport.height} ${mode}`;
              const page = await context.newPage();
              page.setDefaultTimeout(5000);
              const errors = [];
              page.on('pageerror', (error) => errors.push(error.message));
              page.on('requestfailed', (request) => errors.push(`Resource failed: ${request.url()}`));
              try {
                await page.goto(pathToFileURL(path.join(root, 'skills/design-style', example.path)).href);
                assert.equal(await page.locator('html').getAttribute('data-theme'), null, 'System theme must remain selected');
                await page.evaluate(() => window.designAudit.layout());
                if (mode !== 'forced-colors') {
                  assert.equal(await page.evaluate(() => getComputedStyle(document.documentElement).getPropertyValue('--color-sheet').trim()), tokens.themes[colorScheme]['color-sheet']);
                  await page.evaluate(() => window.designAudit.colors());
                }
                if (mode === 'reduced-motion') {
                  await page.evaluate(() => window.designAudit.motion());
                } else {
                  tabStops += await tabThrough(page, mode === 'forced-colors');
                  if (mode === 'normal') {
                    if (example.path.endsWith('navigation-table.html')) {
                      await checkTable(page, viewport.width);
                      const tracks = await page.locator('.table-workspace').evaluate((element) => getComputedStyle(element).gridTemplateColumns.split(' '));
                      assert.equal(tracks.length, viewport.width === 320 ? 1 : 2);
                      if (viewport.width === 1100) {
                        const railWidth = await page.evaluate(() => {
                          const css = getComputedStyle(document.documentElement);
                          return parseFloat(css.getPropertyValue('--size-rail')) * parseFloat(css.fontSize);
                        });
                        assert.equal(parseFloat(tracks[0]), railWidth, 'Compact rail not rendered');
                      }
                    }
                    await checkPointerStates(page);
                  }
                }
                assert.deepEqual(errors, [], 'Page or resource errors');
                cases += 1;
                console.log(`PASS ${label}`);
              } catch (error) {
                throw new Error(`${label}: ${error.message}`, { cause: error });
              } finally {
                await page.close();
              }
            }
          } finally {
            await context.close();
          }
        }
      }
    }
    console.log(`PASS ${cases} rendered cases; ${tabStops} forward Tab stops plus reverse traversal; text >= 4.5 and indicators >= 3 (unrounded)`);
  } finally {
    await browser.close();
  }
}

if (require.main === module) main().catch((error) => { console.error(`FAIL design browser: ${error.stack}`); process.exitCode = 1; });
