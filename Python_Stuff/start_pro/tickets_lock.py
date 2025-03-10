from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import logging
import datetime
import signal
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ticket_booking.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
URL = "https://store.piletilevi.ee/public/et/event/461869/purchase/sector/9013"
SEAT_XPATHS = {
    "17": "//*[@id='place_1192928']",
    "18": "//*[@id='place_1192929']"
}
GECKODRIVER_PATH = "/usr/local/bin/geckodriver"
BOOKING_INTERVAL = 16 * 60  # 16 minutes in seconds (15 min booking + 1 min buffer)
REFRESH_INTERVAL = 30  # Check every 30 seconds

# Global flag for graceful shutdown
running = True


def signal_handler(sig, frame):
    """Handle Ctrl+C to stop the script gracefully"""
    global running
    logger.info("Stopping the auto-booking process...")
    running = False


# Register signal handler
signal.signal(signal.SIGINT, signal_handler)


def setup_driver():
    """Set up and return a headless Firefox driver"""
    options = Options()
    options.add_argument("-headless")  # Run in headless mode
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.window.width", 1920)
    options.set_preference("browser.window.height", 1080)

    service = Service(executable_path=GECKODRIVER_PATH)
    driver = webdriver.Firefox(service=service, options=options)
    return driver


def attempt_booking():
    """Try to book tickets and return success status"""
    driver = None
    try:
        driver = setup_driver()

        # Load the page
        driver.get(URL)
        logger.info(f"Page opened at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(10)

        # Page loaded, continue with booking

        # Check if seats are available
        seats_available = True
        for seat_num, xpath in SEAT_XPATHS.items():
            try:
                seat_element = driver.find_element(By.XPATH, xpath)

                # Check if the seat is available (not already booked)
                seat_classes = seat_element.get_attribute("class") or ""
                if "sold" in seat_classes or "reserved" in seat_classes or "unavailable" in seat_classes:
                    logger.info(f"Seat {seat_num} is not available")
                    seats_available = False
                else:
                    logger.info(f"Seat {seat_num} appears to be available")
            except Exception as e:
                logger.error(f"Error checking seat {seat_num}: {str(e)}")
                seats_available = False

        if not seats_available:
            logger.info("Not all seats are available, waiting for next check...")
            return False

        # Attempt to book each seat
        for seat_num, xpath in SEAT_XPATHS.items():
            try:
                logger.info(f"Attempting to book seat {seat_num}")

                # Find the seat element
                seat_element = driver.find_element(By.XPATH, xpath)

                # Try to find clickable circle within the seat group
                try:
                    circle = seat_element.find_element(By.TAG_NAME, "circle")
                    clickable_element = circle
                except:
                    clickable_element = seat_element

                # Scroll to element
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", clickable_element)
                time.sleep(1)

                # Method 1: MouseEvent via JavaScript (most reliable for SVG)
                js_script = """
                var element = arguments[0];
                var evt = new MouseEvent('click', {
                    bubbles: true,
                    cancelable: true,
                    view: window
                });
                element.dispatchEvent(evt);
                """
                driver.execute_script(js_script, clickable_element)
                time.sleep(1)

                # Method 2: mousedown/mouseup events
                mousedown_script = """
                var element = arguments[0];
                var evt = new MouseEvent('mousedown', {
                    bubbles: true,
                    cancelable: true,
                    view: window
                });
                element.dispatchEvent(evt);
                """
                driver.execute_script(mousedown_script, clickable_element)
                time.sleep(0.5)

                mouseup_script = """
                var element = arguments[0];
                var evt = new MouseEvent('mouseup', {
                    bubbles: true,
                    cancelable: true,
                    view: window
                });
                element.dispatchEvent(evt);
                """
                driver.execute_script(mouseup_script, clickable_element)
                time.sleep(1)

            except Exception as e:
                logger.error(f"Error booking seat {seat_num}: {str(e)}")

        # Seats selected, continue with cart

        # Find and click cart button
        cart_button_found = False
        cart_buttons = []

        try:
            # Try multiple selectors for cart button
            selectors = [
                "//button[contains(text(), 'Lisa kõik korvi')]",
                "//button[contains(text(), 'Lisa korvi')]",
                "//button[contains(text(), 'Add to cart')]",
                "//button[contains(@class, 'cart')]",
                "//button[contains(@class, 'primary')]"
            ]

            for selector in selectors:
                cart_buttons = driver.find_elements(By.XPATH, selector)
                if cart_buttons:
                    break

            if not cart_buttons:
                all_buttons = driver.find_elements(By.TAG_NAME, "button")
                if all_buttons:
                    cart_buttons = [all_buttons[-1]]  # Use the last button as fallback

            if cart_buttons:
                cart_button = cart_buttons[0]
                cart_button_found = True

        except Exception as e:
            logger.error(f"Error finding cart button: {str(e)}")

        if cart_button_found:
            try:
                # Scroll to cart button
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cart_button)
                time.sleep(1)

                logger.info(f"Found cart button with text: {cart_button.text}")

                # Click the cart button
                try:
                    cart_button.click()
                except:
                    driver.execute_script("arguments[0].click();", cart_button)

                logger.info("Clicked cart button")

                # Wait for confirmation
                time.sleep(3)

                # Cart button clicked, check result

                # Check for successful booking (adjust based on site behavior)
                current_url = driver.current_url.lower()
                if "basket" in current_url or "cart" in current_url or "korv" in current_url:
                    logger.info("SUCCESS: Tickets have been added to cart!")
                    return True
                else:
                    logger.info("Tickets may not have been added to cart successfully")
                    return False

            except Exception as e:
                logger.error(f"Error clicking cart button: {str(e)}")
                return False
        else:
            logger.error("No cart button found")
            return False

    except Exception as e:
        logger.error(f"Booking attempt failed: {str(e)}")
        return False

    finally:
        if driver:
            driver.quit()
            logger.info("Browser closed")


def auto_book_tickets():
    """Continuously attempt to book tickets until successful or stopped"""
    global running

    successful_bookings = 0
    attempts = 0

    logger.info("Starting continuous headless auto-booking process")
    logger.info("Press Ctrl+C to stop the process")
    print(f"Auto-booking started at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("The process is now running in the background.")
    print("Check ticket_booking.log for progress updates.")
    print("Press Ctrl+C to stop the process.")

    while running:
        attempts += 1

        logger.info(f"Booking attempt #{attempts} starting...")

        if attempt_booking():
            successful_bookings += 1
            logger.info(f"Booking successful! (Total successful: {successful_bookings})")
            print(
                f"Booking successful at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}! (Total: {successful_bookings})")

            # Wait for booking to expire before trying again
            wait_time = BOOKING_INTERVAL
            logger.info(f"Waiting {wait_time // 60} minutes for booking to expire...")

            # Wait in smaller increments to allow for clean interruption
            for _ in range(wait_time // 10):
                if not running:
                    break
                time.sleep(10)

        else:
            logger.info(f"Booking attempt #{attempts} failed")

            # Wait before next attempt
            logger.info(f"Waiting {REFRESH_INTERVAL} seconds before next attempt...")
            time.sleep(REFRESH_INTERVAL)

    logger.info(f"Auto-booking stopped. Made {attempts} attempts with {successful_bookings} successful bookings.")
    print(f"Auto-booking stopped. Made {attempts} attempts with {successful_bookings} successful bookings.")


if __name__ == "__main__":
    try:
        auto_book_tickets()
    except KeyboardInterrupt:
        logger.info("Process stopped by user")
        print("Process stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"Unexpected error: {str(e)}")
    finally:
        logger.info("Auto-booking script terminated")
        print("Auto-booking script terminated")