# tester_script.py
# Playwright test harness for end-to-end testing
# Integrates with Aider's --test-cmd for automated test-fix loops
# Detects console errors and verifies page content

import sys
import datetime
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
            
            # Test 1: Verify main heading exists
            try:
                heading = page.wait_for_selector('h1.main-heading', timeout=1000)
                if not heading or "Overland Park Precipitation" not in heading.inner_text():
                    print("Test failed: Main heading not found or incorrect")
                    sys.exit(1)
            except Exception:
                print("Test failed: Main heading not found")
                sys.exit(1)
            
            # Test 2: Verify data source text
            try:
                data_source = page.wait_for_selector('p.data-source', timeout=1000)
                if not data_source or "NOAA ACIS" not in data_source.inner_text():
                    print("Test failed: Data source text not found or incorrect")
                    sys.exit(1)
            except Exception:
                print("Test failed: Data source text not found")
                sys.exit(1)
            
            # Test 3: Verify today's precipitation section exists
            try:
                today_section = page.wait_for_selector('section[aria-labelledby="today-precip-heading"]', timeout=1000)
                if not today_section:
                    print("Test failed: Today's precipitation section not found")
                    sys.exit(1)
            except Exception:
                print("Test failed: Today's precipitation section not found")
                sys.exit(1)
            
            # Test 4: Verify historical data table exists
            try:
                table = page.wait_for_selector('#precip-table', timeout=1000)
                if not table:
                    print("Test failed: Precipitation table not found")
                    sys.exit(1)
            except Exception:
                print("Test failed: Precipitation table not found")
                sys.exit(1)

            # Test 5: Verify table is sorted by date descending by default
            try:
                date_cells = page.locator('#precip-table tbody tr td:first-child').all()
                dates = [datetime.datetime.strptime(cell.inner_text(), '%Y-%m-%d') for cell in date_cells]
                if dates != sorted(dates, reverse=True):
                    print("Test failed: Table not sorted by date descending by default")
                    sys.exit(1)
            except Exception as e:
                print(f"Test failed: Could not verify date sorting - {e}")
                sys.exit(1)
            
            # Test 6: Verify chart container exists
            try:
                chart = page.wait_for_selector('#chart', timeout=1000)
                if not chart:
                    print("Test failed: Chart container not found")
                    sys.exit(1)
            except Exception:
                print("Test failed: Chart container not found")
                sys.exit(1)
            
            # Test 7: Verify last updated text exists
            try:
                last_updated = page.wait_for_selector('.last-updated', timeout=1000)
                if not last_updated:
                    print("Test failed: Last updated text not found")
                    sys.exit(1)
            except Exception:
                print("Test failed: Last updated text not found")
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
    print("Test passed: All key elements present and no errors detected")
    sys.exit(0)

if __name__ == "__main__":
    run_test()
