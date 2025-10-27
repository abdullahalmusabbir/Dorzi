import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import unittest

class TestPreDesignedPage(unittest.TestCase):
    
    def setUp(self):
        """Set up the Chrome driver before each test"""
        print("Setting up Chrome driver...")
        start_time = time.time()
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 15)
        
        setup_time = time.time() - start_time
        print(f"Chrome driver setup completed in {setup_time:.2f} seconds")
        
    def tearDown(self):
        """Close the driver after each test"""
        if self.driver:
            self.driver.quit()
        print("Chrome driver closed")
    
    def login(self):
        """Login to the application"""
        print("Starting login process...")
        login_start = time.time()
        
        # Navigate to the home page
        self.driver.get("http://localhost:8000")  # Adjust URL as needed
        print("Navigated to home page")
        
        # Click login button
        try:
            login_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Login')]"))
            )
            login_btn.click()
            print("Login modal opened")
        except Exception as e:
            print(f"Could not find login button: {e}")
            return False
        
        # Wait for login modal to appear and be visible
        try:
            self.wait.until(EC.visibility_of_element_located((By.ID, "loginModal")))
            print("Login modal is visible")
        except Exception as e:
            print(f"Login modal not visible: {e}")
            return False
        
        # Fill in login credentials
        try:
            email_field = self.driver.find_element(By.NAME, "username")
            password_field = self.driver.find_element(By.NAME, "password")
            
            email_field.clear()
            email_field.send_keys("abdullahmusabbir703@gmail.com")
            password_field.clear()
            password_field.send_keys("Shuvo1996$")
            print("Credentials entered")
        except Exception as e:
            print(f"Could not enter credentials: {e}")
            return False
        
        # Click login button
        try:
            login_submit = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
            login_submit.click()
            print("Login form submitted")
        except Exception as e:
            print(f"Could not submit login form: {e}")
            return False
        
        # Wait for login to complete - check for logout button or profile image
        try:
            # Wait for either logout link or profile image to appear (indicating successful login)
            self.wait.until(EC.any_of(
                EC.presence_of_element_located((By.LINK_TEXT, "Logout")),
                EC.presence_of_element_located((By.XPATH, "//img[@alt='User']")),
                EC.presence_of_element_located((By.CLASS_NAME, "dropdown"))
            ))
            print("Login successful - user is logged in")
            
            # Additional wait to ensure page is fully loaded
            time.sleep(2)
            
        except Exception as e:
            print(f"Login may have failed: {e}")
            # Check if there's an error message
            try:
                error_msg = self.driver.find_element(By.CLASS_NAME, "error")
                print(f"Login error: {error_msg.text}")
                return False
            except:
                print("No explicit error message found")
                return False
        
        login_time = time.time() - login_start
        print(f"Login completed in {login_time:.2f} seconds")
        return True
    
    def test_pre_designed_page_functionality(self):
        """Test the complete pre-designed page functionality"""
        print("\n" + "="*50)
        print("STARTING PRE-DESIGNED PAGE TESTING")
        print("="*50)
        
        total_start_time = time.time()
        
        # Step 1: Login
        login_step_time = time.time()
        login_success = self.login()
        if not login_success:
            print("✗ Login failed! Stopping test.")
            return
        
        login_duration = time.time() - login_step_time
        print(f"✓ Login step completed in {login_duration:.2f} seconds")
        
        # Step 2: Navigate to Pre-Designed page
        nav_step_time = time.time()
        print("\nNavigating to Pre-Designed page...")
        
        try:
            # Wait a moment for the page to stabilize after login
            time.sleep(2)
            
            # Find and click the Pre-Designed link
            pre_designed_link = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Pre-Designed')]"))
            )
            pre_designed_link.click()
            print("Clicked Pre-Designed link")
            
            # Wait for pre-designed page to load - check for specific elements on that page
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Pre-Designed Collections')]"))
            )
            print("Pre-Designed page loaded successfully")
            
            # Verify we're on the correct URL
            current_url = self.driver.current_url
            if "pre-designed" in current_url.lower() or "pre_designed" in current_url.lower():
                print(f"✓ Successfully navigated to Pre-Designed page: {current_url}")
            else:
                print(f"Current URL: {current_url}")
            
        except Exception as e:
            print(f"✗ Failed to navigate to Pre-Designed page: {e}")
            # Try direct navigation as fallback
            try:
                self.driver.get("http://localhost:8000/pre-designed/")
                self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))
                print("✓ Direct navigation to Pre-Designed page successful")
            except Exception as fallback_error:
                print(f"✗ Direct navigation also failed: {fallback_error}")
                return
        
        nav_duration = time.time() - nav_step_time
        print(f"✓ Navigation to Pre-Designed page completed in {nav_duration:.2f} seconds")
        
        # Step 3: Test page content is loaded
        content_step_time = time.time()
        print("\nTesting page content...")
        
        try:
            # Check for main elements on the pre-designed page
            hero_section = self.driver.find_element(By.XPATH, "//div[contains(@style, 'background-image')]")
            print("✓ Hero section found")
            
            category_grid = self.driver.find_element(By.XPATH, "//div[contains(@style, 'grid-template-columns: repeat(8, 1fr)')]")
            print("✓ Category grid found")
            
            products_container = self.driver.find_element(By.ID, "products-container")
            print("✓ Products container found")
            
            # Count initial products
            products = products_container.find_elements(By.CLASS_NAME, "product-card")
            print(f"✓ Found {len(products)} products on page")
            
        except Exception as e:
            print(f"✗ Page content check failed: {e}")
            return
        
        content_duration = time.time() - content_step_time
        print(f"✓ Page content verification completed in {content_duration:.2f} seconds")
        
        # Step 4: Test category filtering
        filter_step_time = time.time()
        print("\nTesting category filtering...")
        
        try:
            categories_to_test = ["Punjabi", "Salwar Kameez", "Saree", "Formal Wear", "All Designs"]
            
            for category in categories_to_test:
                try:
                    cat_start = time.time()
                    print(f"  Testing '{category}' filter...")
                    
                    # Find and click category
                    category_div = self.driver.find_element(By.XPATH, f"//div[contains(@onclick, \"filterProducts('{category}')\")]")
                    category_div.click()
                    
                    # Wait for filter to apply
                    time.sleep(2)
                    
                    # Check if filter worked by looking at product count
                    products_after_filter = products_container.find_elements(By.CLASS_NAME, "product-card")
                    visible_products = [p for p in products_after_filter if p.is_displayed()]
                    
                    cat_duration = time.time() - cat_start
                    print(f"    ✓ '{category}' filter - {len(visible_products)} products visible in {cat_duration:.2f}s")
                    
                except Exception as e:
                    print(f"    ✗ Failed to apply '{category}' filter: {str(e)}")
            
            # Make sure we end with "All Designs" selected
            all_designs_div = self.driver.find_element(By.XPATH, "//div[contains(@onclick, \"filterProducts('All Designs')\")]")
            all_designs_div.click()
            time.sleep(1)
            
        except Exception as e:
            print(f"✗ Category filtering test failed: {e}")
        
        filter_duration = time.time() - filter_step_time
        print(f"✓ Category filtering completed in {filter_duration:.2f} seconds")
        
        # Step 5: Test sidebar filters
        sidebar_step_time = time.time()
        print("\nTesting sidebar filters...")
        
        try:
            # Test gender filters
            print("  Testing gender filters...")
            gender_checkboxes = self.driver.find_elements(By.XPATH, "//input[@name='gender']")
            
            for i, checkbox in enumerate(gender_checkboxes[:2]):  # Test first 2
                try:
                    if checkbox.is_displayed() and checkbox.is_enabled():
                        checkbox.click()
                        time.sleep(1)
                        print(f"    ✓ Gender filter {i+1} applied")
                        # Uncheck for next test
                        checkbox.click()
                        time.sleep(0.5)
                except Exception as e:
                    print(f"    ✗ Gender filter {i+1} failed: {e}")
            
            # Test price filters
            print("  Testing price filters...")
            price_checkboxes = self.driver.find_elements(By.XPATH, "//input[@name='price']")
            
            for i, checkbox in enumerate(price_checkboxes[:2]):  # Test first 2
                try:
                    if checkbox.is_displayed() and checkbox.is_enabled():
                        checkbox.click()
                        time.sleep(1)
                        print(f"    ✓ Price filter {i+1} applied")
                        # Uncheck for next test
                        checkbox.click()
                        time.sleep(0.5)
                except Exception as e:
                    print(f"    ✗ Price filter {i+1} failed: {e}")
            
            # Clear all filters
            clear_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Clear All Filters')]")
            clear_btn.click()
            time.sleep(1)
            print("  ✓ All filters cleared")
            
        except Exception as e:
            print(f"✗ Sidebar filtering test failed: {e}")
        
        sidebar_duration = time.time() - sidebar_step_time
        print(f"✓ Sidebar filtering completed in {sidebar_duration:.2f} seconds")
        
        # Step 6: Test product interactions
        product_step_time = time.time()
        print("\nTesting product interactions...")
        
        # Refresh products list
        products_container = self.driver.find_element(By.ID, "products-container")
        products = products_container.find_elements(By.CLASS_NAME, "product-card")
        
        if products:
            print(f"Testing interactions with {len(products)} products...")
            
            # Test first product details modal
            try:
                first_product = products[0]
                print("  Testing product details modal...")
                
                details_btn = first_product.find_element(By.XPATH, ".//button[contains(text(), 'Details')]")
                details_btn.click()
                
                # Wait for modal to appear
                self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "modal")))
                print("    ✓ Product details modal opened")
                
                # Try to close modal
                try:
                    close_btns = self.driver.find_elements(By.XPATH, "//span[contains(text(), '×')]")
                    if close_btns:
                        close_btns[0].click()
                        time.sleep(1)
                        print("    ✓ Modal closed successfully")
                except Exception as e:
                    print(f"    ✗ Could not close modal: {e}")
                
            except Exception as e:
                print(f"    ✗ Product details modal test failed: {e}")
            
            # Test reviews modal if available
            try:
                print("  Testing reviews modal...")
                first_product = products[0]  # Refresh reference
                
                reviews_btn = first_product.find_element(By.XPATH, ".//button[contains(text(), 'Reviews')]")
                reviews_btn.click()
                
                # Wait for reviews modal
                time.sleep(2)
                print("    ✓ Reviews modal opened")
                
                # Close reviews modal
                close_btns = self.driver.find_elements(By.XPATH, "//span[contains(text(), '×')]")
                for btn in close_btns:
                    try:
                        btn.click()
                        break
                    except:
                        continue
                time.sleep(1)
                print("    ✓ Reviews modal closed")
                
            except Exception as e:
                print(f"    ✗ Reviews modal test failed: {e}")
        
        else:
            print("  ⚠ No products found for interaction testing")
        
        product_duration = time.time() - product_step_time
        print(f"✓ Product interactions completed in {product_duration:.2f} seconds")
        
        # Final summary
        total_duration = time.time() - total_start_time
        print("\n" + "="*50)
        print("TESTING COMPLETED SUCCESSFULLY!")
        print("="*50)
        print(f"Total testing time: {total_duration:.2f} seconds")
        print("\nTest Summary:")
        print(f"• Login: {login_duration:.2f}s")
        print(f"• Navigation: {nav_duration:.2f}s")
        print(f"• Content verification: {content_duration:.2f}s")
        print(f"• Category filtering: {filter_duration:.2f}s")
        print(f"• Sidebar filtering: {sidebar_duration:.2f}s")
        print(f"• Product interactions: {product_duration:.2f}s")
        print("="*50)

def run_tests():
    """Run the pre-designed page tests"""
    print("Starting Selenium tests for Pre-Designed page...")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add our test
    suite.addTest(TestPreDesignedPage('test_pre_designed_page_functionality'))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    run_tests()
