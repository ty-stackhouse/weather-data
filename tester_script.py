# tester_script.py
# Playwright test harness for end-to-end testing
# Integrates with Aider's --test-cmd for automated test-fix loops
# Detects console errors and verifies page content

import sys
from playwright.sync_api import sync_playwright
import server_manager

# Flags to track test outcome
console_errors = []
page_crashed = False


def on_console(msg):
    """Handle console messages from the browser."""
    if msg.type == 'error':
        console_errors.append(str(msg))


def on_page_error(exception):
    """Handle uncaught exceptions in the page."""
    global page_crashed
    page_crashed = True
    console_errors.append(f"Page error: {exception}")


def run_test():
    """Run the end-to-end test sequence."""
    # Start the server
    try:
        server_manager.start_server()
    except Exception as e:
        print(f"Failed to start server: {e}")
        sys.exit(1)
    
    try:
        # Launch browser
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Set up event listeners
            page.on('console', on_console)
            page.on('pageerror', on_page_error)
            
            # Navigate to the page
            page.goto('http://localhost:5000')
            
            # Wait for the expected content to appear
            try:
                page.wait_for_selector('h1', timeout=1000)
            except Exception:
                print("Test failed: Expected text not found")
                sys.exit(1)
            
            # Close browser
            browser.close()
    
    except Exception as e:
        print(f"Test failed with exception: {e}")
        sys.exit(1)
    
    finally:
        # Always stop the server
        server_manager.stop_server()
    
    # Check for any errors captured
    if console_errors or page_crashed:
        print("Test failed due to browser errors:")
        for err in console_errors:
            print(f"- {err}")
        sys.exit(1)
    
    # All checks passed
    print("Test passed: No errors detected")
    sys.exit(0)

if __name__ == "__main__":
    run_test()
