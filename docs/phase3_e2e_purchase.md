# Phase 3 - E2E Purchase Flow

This document explains the current project files and the reason for the
structure used in the E2E automation.

## Root files

- `.gitignore`: keeps local/generated files out of git, including `venv/`,
  pytest cache, Python bytecode, reports, screenshots, logs, and packaged zip
  files. The repository should contain source code and configuration, not
  runtime artifacts.
- `README.md`: gives the quick setup commands and the Phase 1 smoke-test
  checkpoint. It is intentionally short because the final Spanish execution
  guide is planned for Phase 5.
- `requirements.txt`: pins the tool categories needed by the challenge:
  Selenium for browser automation, pytest for execution, pytest-html for later
  reports, and requests for the future API phase.
- `pytest.ini`: registers the `e2e` and `api` markers, enables strict marker
  validation, sets the project root on `pythonpath`, and tells pytest where test
  packages live. This prevents import errors when tests import project modules.
- `conftest.py`: centralizes pytest fixtures and hooks. The `driver` fixture
  creates and closes Chrome for each E2E test, while the failure hook saves a
  screenshot under `reports/screenshots/` when a test with `driver` fails.

## E2E support files

- `e2e_tests/config.py`: stores SauceDemo URL, credentials, and default wait
  timeout in one place. Tests and Page Objects import these values instead of
  duplicating literals.
- `e2e_tests/__init__.py`: marks `e2e_tests` as a Python package so imports are
  consistent.
- `e2e_tests/pages/__init__.py`: exports the Page Object classes from a single
  import point. Tests can use `from e2e_tests.pages import LoginPage` instead
  of importing every concrete file path.
- `e2e_tests/pages/base_page.py`: contains shared Selenium behavior: explicit
  waits, finding elements, clicking, typing, text reads, URL waits, and a safe
  XPath string helper. Keeping this shared logic in one base class avoids
  repeating wait/click/type code across every page.
- `e2e_tests/pages/login_page.py`: models the login screen. It knows the login
  locators and user actions, but it does not contain test assertions.
- `e2e_tests/pages/inventory_page.py`: models the product listing screen. It
  exposes product names, sorting, add/remove product actions, cart badge count,
  and cart navigation.
- `e2e_tests/pages/cart_page.py`: models the cart screen. It exposes cart item
  names, remove product, continue shopping, and checkout actions.
- `e2e_tests/pages/checkout_page.py`: models the checkout information,
  overview, and complete screens. SauceDemo splits checkout across multiple
  URLs, but they are one business flow, so one `CheckoutPage` keeps those
  related actions together.

## Test files

- `e2e_tests/test_smoke.py`: validates the foundation only. It opens SauceDemo
  and confirms the login button is visible, proving Selenium and Chrome are
  working.
- `e2e_tests/test_purchase.py`: validates the complete user purchase journey:
  login, add product to cart, checkout, fill buyer information, finish, and
  assert the final `THANK YOU FOR YOUR ORDER!` message.

## API placeholders

- `api_tests/__init__.py`: marks the future API test folder as a package.
- `api_tests/config.py`: stores the PetStore API base URL and timeout for Phase
  4, keeping API configuration separate from E2E browser configuration.

## Why Page Object Model

The test file should describe the business scenario, not Selenium mechanics.
Selectors and browser operations live inside Page Objects, so when SauceDemo
changes an element ID or layout detail, only the relevant page class should need
to change. This keeps tests shorter, easier to read, and easier to maintain.

## Reliability choices

All waits are explicit through `WebDriverWait` instead of implicit waits. This
makes timing problems easier to diagnose and avoids hidden wait behavior.

`BasePage.type_text()` first uses normal Selenium typing. In this local Chrome
session the SauceDemo postal-code field sometimes dropped keystrokes, so the
method verifies the input value and uses a JavaScript input-event fallback only
when normal typing fails. The fallback also notifies React's value tracker so
the app state matches the visible field value.

Checkout footer buttons use `js_click()` because SauceDemo keeps them in a
fixed footer area that can be flaky with coordinate-based Selenium clicks in
some browser/window combinations. Other page clicks still use normal Selenium
clicks.

## Manual QA findings and persistent issues

These are the most relevant issues noticed while manually exercising and
debugging the Phase 3 flow. They are useful to keep in mind when reviewing a
failed run, because not every failure means the business flow is broken.

- Chrome may show a password/data-breach warning for the public SauceDemo
  password `secret_sauce`. This is not a SauceDemo checkout defect; it happens
  because the exercise uses a well-known shared demo password. In manual runs it
  can distract from the login step or cover part of the browser UI. The
  automated test still uses the official challenge credentials from
  `e2e_tests/config.py`.
- The checkout postal-code field was the most persistent automation issue.
  During local runs, Selenium sometimes focused the field but dropped part or
  all of the typed value. The visible symptom was that checkout stayed on
  `Checkout: Your Information` instead of advancing to overview.
- A plain JavaScript value assignment was not enough for checkout fields because
  SauceDemo is a React app. The value could appear on screen, but React state
  did not always update, so clicking `Continue` behaved as if the postal code
  was still empty. The fix dispatches input/change events and updates React's
  value tracker only after normal Selenium typing fails.
- The `Continue` and `Finish` buttons live near a fixed footer area. In some
  browser/window positions, coordinate-based Selenium clicks did not trigger the
  button even when it was visible. The checkout Page Object uses `js_click()`
  for those footer actions, while the rest of the app still uses normal
  Selenium clicks.
- Failure screenshots were essential for separating real flow failures from
  automation mechanics. For example, screenshots showed whether the test was
  still on the information form, had reached checkout overview, or was blocked
  near the footer controls.
- Window size and headless mode can change how SauceDemo lays out the checkout
  footer. The project uses a fixed `1280x800` browser size and supports
  `HEADLESS=true` so local and CI runs behave as consistently as possible.
- The final assertion intentionally checks only the completion message:
  `THANK YOU FOR YOUR ORDER!`. Earlier steps are still necessary to reach that
  state, but the test stays focused on the business outcome instead of adding
  many intermediate assertions that could make the flow brittle.

## Phase 3 checkpoint

Run:

```bash
source venv/bin/activate
pytest e2e_tests/test_purchase.py
```

Expected result:

```text
1 passed
```
