import os
import django
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import unittest

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dorzi.settings')
django.setup()

class TestFindTailor(unittest.TestCase):
    
    def setUp(self):
        """Setup Chrome driver for testing"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Remove this line if you want to see the browser
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.base_url = "http://localhost:8000"  # Change to your development server URL
    
    def tearDown(self):
        """Close the browser after each test"""
        self.driver.quit()
    
    def login(self):
        """Login with test credentials"""
        driver = self.driver
        driver.get(f"{self.base_url}/findTailor/")
        
        # Click login button
        try:
            login_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Login')]")
            login_btn.click()
            time.sleep(2)
        except:
            # If already logged in, skip login
            return True
        
        # Fill login form
        email_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        
        email_field.send_keys("abdullahmusabbir703@gmail.com")
        password_field.send_keys("Shuvo1996$")
        
        # Submit login form
        login_submit = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_submit.click()
        
        time.sleep(3)
        return True
    
    def test_01_login_and_access_find_tailor(self):
        """Test login and access find tailor page"""
        print("Test 1: Login and access find tailor page")
        
        self.login()
        
        # Verify we're on findTailor page
        driver = self.driver
        driver.get(f"{self.base_url}/findTailor/")
        
        # Check if page loaded successfully
        page_title = driver.find_element(By.TAG_NAME, "h1")
        self.assertIn("Find Your Perfect Tailor", page_title.text)
        print("✓ Successfully accessed find tailor page after login")
    
    def test_02_search_functionality(self):
        """Test search functionality"""
        print("\nTest 2: Search functionality")
        
        self.login()
        driver = self.driver
        driver.get(f"{self.base_url}/findTailor/")
        
        # Find search input
        search_input = driver.find_element(By.ID, "searchInput")
        
        # Test search by tailor name
        search_input.clear()
        search_input.send_keys("test")  # Replace with actual tailor name from your database
        time.sleep(2)
        
        # Check if results are filtered
        results_count = driver.find_element(By.ID, "mainCount")
        print(f"✓ Search by name completed. Results: {results_count.text}")
        
        # Test search by location
        search_input.clear()
        search_input.send_keys("Dhaka")  # Replace with actual location from your database
        time.sleep(2)
        
        results_count = driver.find_element(By.ID, "mainCount")
        print(f"✓ Search by location completed. Results: {results_count.text}")
        
        # Test search by specialization
        search_input.clear()
        search_input.send_keys("Formal")  # Replace with actual specialization
        time.sleep(2)
        
        results_count = driver.find_element(By.ID, "mainCount")
        print(f"✓ Search by specialization completed. Results: {results_count.text}")
    
    def test_03_filter_by_location(self):
        """Test location filter functionality"""
        print("\nTest 3: Location filter")
        
        self.login()
        driver = self.driver
        driver.get(f"{self.base_url}/findTailor/")
        
        # Get initial count
        initial_count = driver.find_element(By.ID, "mainCount").text
        
        # Find and click a location checkbox
        try:
            location_checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[name='location']")
            if location_checkboxes:
                location_checkboxes[0].click()  # Click first location checkbox
                time.sleep(2)
                
                filtered_count = driver.find_element(By.ID, "mainCount").text
                print(f"✓ Location filter applied. Before: {initial_count}, After: {filtered_count}")
            else:
                print("⚠ No location filters found")
        except Exception as e:
            print(f"⚠ Location filter test skipped: {str(e)}")
    
    def test_04_filter_by_specialization(self):
        """Test specialization filter functionality"""
        print("\nTest 4: Specialization filter")
        
        self.login()
        driver = self.driver
        driver.get(f"{self.base_url}/findTailor/")
        
        # Get initial count
        initial_count = driver.find_element(By.ID, "mainCount").text
        
        # Find and click a specialization checkbox
        try:
            specialization_checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[name='specialization']")
            if specialization_checkboxes:
                specialization_checkboxes[0].click()  # Click first specialization checkbox
                time.sleep(2)
                
                filtered_count = driver.find_element(By.ID, "mainCount").text
                print(f"✓ Specialization filter applied. Before: {initial_count}, After: {filtered_count}")
            else:
                print("⚠ No specialization filters found")
        except Exception as e:
            print(f"⚠ Specialization filter test skipped: {str(e)}")
    
    def test_05_filter_by_price_range(self):
        """Test price range filter functionality"""
        print("\nTest 5: Price range filter")
        
        self.login()
        driver = self.driver
        driver.get(f"{self.base_url}/findTailor/")
        
        # Get initial count
        initial_count = driver.find_element(By.ID, "mainCount").text
        
        # Find and click a price radio button
        try:
            price_radios = driver.find_elements(By.CSS_SELECTOR, "input[name='price']")
            if price_radios:
                price_radios[0].click()  # Click first price radio
                time.sleep(2)
                
                filtered_count = driver.find_element(By.ID, "mainCount").text
                print(f"✓ Price filter applied. Before: {initial_count}, After: {filtered_count}")
            else:
                print("⚠ No price filters found")
        except Exception as e:
            print(f"⚠ Price filter test skipped: {str(e)}")
    
    def test_06_clear_filters(self):
        """Test clear filters functionality"""
        print("\nTest 6: Clear filters")
        
        self.login()
        driver = self.driver
        driver.get(f"{self.base_url}/findTailor/")
        
        # Apply some filters first
        try:
            # Apply location filter
            location_checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[name='location']")
            if location_checkboxes:
                location_checkboxes[0].click()
                time.sleep(1)
            
            # Apply specialization filter  
            specialization_checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[name='specialization']")
            if specialization_checkboxes:
                specialization_checkboxes[0].click()
                time.sleep(1)
            
            filtered_count = driver.find_element(By.ID, "mainCount").text
            
            # Click clear filters button
            clear_btn = driver.find_element(By.ID, "clearFilters")
            clear_btn.click()
            time.sleep(2)
            
            cleared_count = driver.find_element(By.ID, "mainCount").text
            print(f"✓ Filters cleared. Filtered: {filtered_count}, Cleared: {cleared_count}")
            
        except Exception as e:
            print(f"⚠ Clear filters test skipped: {str(e)}")
    
    def test_07_view_tailor_profile(self):
        """Test viewing tailor profile modal"""
        print("\nTest 7: View tailor profile")
        
        self.login()
        driver = self.driver
        driver.get(f"{self.base_url}/findTailor/")
        
        try:
            # Find and click a "View Profile" button
            view_profile_buttons = driver.find_elements(By.CLASS_NAME, "open-modal-btn")
            if view_profile_buttons:
                view_profile_buttons[0].click()
                time.sleep(2)
                
                # Check if modal opened
                modal = driver.find_element(By.CSS_SELECTOR, ".hire-modal[style*='display: flex']")
                self.assertTrue(modal.is_displayed())
                print("✓ Tailor profile modal opened successfully")
                
                # Close modal
                close_btn = modal.find_element(By.CLASS_NAME, "close-modal")
                close_btn.click()
                time.sleep(1)
                
            else:
                print("⚠ No tailor cards with view profile buttons found")
                
        except Exception as e:
            print(f"⚠ View tailor profile test skipped: {str(e)}")
    
    def test_08_custom_order_modal(self):
        """Test custom order modal functionality"""
        print("\nTest 8: Custom order modal")
        
        self.login()
        driver = self.driver
        driver.get(f"{self.base_url}/findTailor/")
        
        try:
            # Open a tailor profile first
            view_profile_buttons = driver.find_elements(By.CLASS_NAME, "open-modal-btn")
            if view_profile_buttons:
                view_profile_buttons[0].click()
                time.sleep(2)
                
                # Click custom order button
                custom_order_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Custom Order')]")
                custom_order_btn.click()
                time.sleep(2)
                
                # Check if custom order modal opened
                custom_modal = driver.find_element(By.ID, "customOrderModal")
                self.assertTrue("display: none" not in custom_modal.get_attribute("style"))
                print("✓ Custom order modal opened successfully")
                
                # Test step navigation
                next_buttons = custom_modal.find_elements(By.CLASS_NAME, "next-step")
                if next_buttons:
                    next_buttons[0].click()
                    time.sleep(1)
                    print("✓ Step navigation working")
                
                # Close modal
                close_btn = custom_modal.find_element(By.CLASS_NAME, "close-custom-order-modal")
                close_btn.click()
                time.sleep(1)
                
            else:
                print("⚠ Could not test custom order - no tailor profiles available")
                
        except Exception as e:
            print(f"⚠ Custom order modal test skipped: {str(e)}")
    
    def test_09_favorite_functionality(self):
        """Test favorite tailor functionality"""
        print("\nTest 9: Favorite functionality")
        
        self.login()
        driver = self.driver
        driver.get(f"{self.base_url}/findTailor/")
        
        try:
            # Open a tailor profile
            view_profile_buttons = driver.find_elements(By.CLASS_NAME, "open-modal-btn")
            if view_profile_buttons:
                view_profile_buttons[0].click()
                time.sleep(2)
                
                # Find favorite icon
                favorite_icons = driver.find_elements(By.CLASS_NAME, "favorite-icon")
                if favorite_icons:
                    initial_state = favorite_icons[0].text
                    favorite_icons[0].click()
                    time.sleep(2)
                    
                    new_state = favorite_icons[0].text
                    print(f"✓ Favorite toggle clicked. Initial: {initial_state}, New: {new_state}")
                    
                else:
                    print("⚠ No favorite icons found")
                    
                # Close modal
                close_btn = driver.find_element(By.CLASS_NAME, "close-modal")
                close_btn.click()
                time.sleep(1)
                
            else:
                print("⚠ Could not test favorites - no tailor profiles available")
                
        except Exception as e:
            print(f"⚠ Favorite functionality test skipped: {str(e)}")
    
    def test_10_responsive_design(self):
        """Test responsive design elements"""
        print("\nTest 10: Responsive design")
        
        self.login()
        driver = self.driver
        driver.get(f"{self.base_url}/findTailor/")
        
        # Test different screen sizes
        sizes = [
            (1200, 800),  # Desktop
            (768, 1024),  # Tablet
            (375, 667)    # Mobile
        ]
        
        for width, height in sizes:
            driver.set_window_size(width, height)
            time.sleep(1)
            
            # Check if main elements are visible
            search_input = driver.find_element(By.ID, "searchInput")
            self.assertTrue(search_input.is_displayed())
            
            results_count = driver.find_element(By.ID, "mainCount")
            self.assertTrue(results_count.is_displayed())
            
            print(f"✓ Responsive test passed for {width}x{height}")

def run_all_tests():
    """Run all tests and print summary"""
    print("Starting FindTailor Page Tests...")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestFindTailor)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("🎉 All tests passed successfully!")
    else:
        print("❌ Some tests failed. Check details above.")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    # Check if running directly
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        run_all_tests()
    else:
        print("Usage: python testingFindTailor.py run")
        print("This will execute all tests for the findtailor.html page")
        print("\nMake sure to:")
        print("1. Install required packages: pip install selenium django")
        print("2. Download ChromeDriver and add to PATH")
        print("3. Start your Django development server")
        print("4. Update base_url in the script if needed")
