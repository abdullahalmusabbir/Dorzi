import os
import sys
import time
import unittest
import django
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dorzi.settings')
try:
    django.setup()
except Exception as e:
    print(f"⚠ Django setup warning: {e}")

class DorziCompleteTest(unittest.TestCase):
    """Complete test suite for Dorzi application"""
    
    @classmethod
    def setUpClass(cls):
        """Setup once before all tests"""
        print("🚀 Initializing Dorzi Complete Test Suite...")
        cls.base_url = "http://localhost:8000" 
        cls.setup_driver()
        cls.wait = WebDriverWait(cls.driver, 15)
        cls.total_start_time = time.time()  
    
    @classmethod
    def tearDownClass(cls):
        """Cleanup after all tests"""
        total_execution_time = time.time() - cls.total_start_time
        print(f"\n⏱️ Total Test Suite Execution Time: {total_execution_time:.2f} seconds")
        
        if hasattr(cls, 'driver') and cls.driver:
            cls.driver.quit()
        print("\n🎉 All tests completed!")
    
    @classmethod
    def setup_driver(cls):
        """Setup Chrome driver with options"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        try:
            print("📥 Setting up ChromeDriver...")
            service = Service(ChromeDriverManager().install())
            cls.driver = webdriver.Chrome(service=service, options=chrome_options)
            cls.driver.implicitly_wait(10)
            print("✓ Chrome driver initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize driver: {e}")
            print("Please make sure:")
            print("1. Google Chrome is installed")
            print("2. You have internet connection for ChromeDriver download")
            raise
    
    def login_user(self):
        """Login with provided credentials"""
        print("\n🔐 Logging in user...")
        
        try:
            self.driver.get(self.base_url)
            time.sleep(2)
            
            login_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Login')]"))
            )
            login_btn.click()
            modal = self.wait.until(EC.visibility_of_element_located((By.ID, "loginModal")))
            email_field = self.driver.find_element(By.NAME, "username")
            password_field = self.driver.find_element(By.NAME, "password")
            email_field.clear()
            email_field.send_keys("abdullahmusabbir703@gmail.com")
            
            password_field.clear()
            password_field.send_keys("Shuvo1996$")
            login_submit_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
            login_submit_btn.click()
            time.sleep(3)
            try:
                profile_icon = self.driver.find_element(By.XPATH, "//img[@alt='User']")
                print("✓ Login successful - User is logged in")
                return True
            except NoSuchElementException:
                try:
                    error_message = self.driver.find_element(By.XPATH, "//div[contains(@class, 'error')]")
                    print(f"❌ Login failed: {error_message.text}")
                    return False
                except NoSuchElementException:
                    if "customer" in self.driver.current_url or "tailor" in self.driver.current_url:
                        print("✓ Login successful - Redirected to dashboard")
                        return True
                    else:
                        print("❌ Login may have failed - Not redirected to expected page")
                        return False
                        
        except Exception as e:
            print(f"❌ Login process failed: {str(e)}")
            self.take_screenshot("login_error")
            return False
    
    def take_screenshot(self, name):
        """Take screenshot for debugging"""
        try:
            self.driver.save_screenshot(f"screenshot_{name}.png")
        except:
            pass
    
    def scroll_to_element(self, element):
        """Scroll to specific element"""
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        time.sleep(1)
    
    def scroll_to_bottom(self):
        """Scroll to bottom of page"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
    
    def scroll_to_top(self):
        """Scroll to top of page"""
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
    
    # ==================== TEST CASES ====================
    
    def test_00_user_login(self):
        """Test 0: User login before running other tests"""
        print("\n" + "="*60)
        print("TEST 0: User Login")
        print("="*60)
        
        start_time = time.time()
        
        try:
            login_success = self.login_user()
            self.assertTrue(login_success, "User login failed")
            
            execution_time = time.time() - start_time
            print(f"⏱️ TEST 0 Execution Time: {execution_time:.2f} seconds")
            print("✅ TEST 0 PASSED: User logged in successfully")
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"⏱️ TEST 0 Execution Time: {execution_time:.2f} seconds")
            self.take_screenshot("test_00_login_error")
            print(f"❌ TEST 0 FAILED: {str(e)}")
            raise
    
    def test_01_home_page_load(self):
        """Test 1: Home page loads correctly with all elements"""
        print("\n" + "="*60)
        print("TEST 1: Home Page Load")
        print("="*60)
        
        start_time = time.time()
        
        try:
            self.driver.get(self.base_url)
            time.sleep(2)
            
            self.assertIn("Dorzi", self.driver.title)
            print("✓ Page title is correct")
            
            nav_elements = {
                "Logo": "//a[contains(text(), 'DorZi')]",
                "About Link": "//a[contains(text(), 'About')]",
                "Find Tailor Link": "//a[contains(text(), 'Find Tailor')]",
                "Pre-Designed Link": "//a[contains(text(), 'Pre-Designed')]",
                "Profile Icon": "//img[@alt='User']"
            }
            
            for element_name, xpath in nav_elements.items():
                element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                self.assertTrue(element.is_displayed())
                print(f"✓ {element_name} is displayed")
            
            execution_time = time.time() - start_time
            print(f"⏱️ TEST 1 Execution Time: {execution_time:.2f} seconds")
            print("✅ TEST 1 PASSED: Home page loaded successfully with all navigation elements")
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"⏱️ TEST 1 Execution Time: {execution_time:.2f} seconds")
            self.take_screenshot("test_01_home_page_load_error")
            print(f"❌ TEST 1 FAILED: {str(e)}")
            raise
    
    def test_02_hero_section(self):
        """Test 2: Hero section with slideshow functionality"""
        print("\n" + "="*60)
        print("TEST 2: Hero Section")
        print("="*60)
        
        start_time = time.time()
        
        try:
            if "home" not in self.driver.current_url:
                self.driver.get(self.base_url)
            hero_elements = {
                "Main Heading": "//h1[contains(text(), 'Find the Perfect')]",
                "Sub Heading": "//span[contains(text(), 'Tailor Near You')]",
                "Description": "//p[contains(text(), 'Connect with expert tailors')]",
                "Find Tailors Button": "//a[contains(text(), 'Find Tailors')]",
                "Custom Order Button": "//a[contains(text(), 'Custom Order')]"
            }
            
            for element_name, xpath in hero_elements.items():
                element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                self.assertTrue(element.is_displayed())
                print(f"✓ {element_name} is displayed")
            
            slideshow_container = self.driver.find_element(By.ID, "slideshow-container")
            self.assertTrue(slideshow_container.is_displayed())
            
            slide_images = self.driver.find_elements(By.CLASS_NAME, "slide-image")
            self.assertGreater(len(slide_images), 0, "No slide images found")
            print(f"✓ Slideshow found with {len(slide_images)} images")
            
            find_tailors_btn = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Find Tailors')]")
            find_tailors_btn.click()
            self.wait.until(EC.url_contains("findTailor"))
            print("✓ Find Tailors button navigates correctly")
            
            self.driver.back()
            self.wait.until(EC.url_contains("home") or self.driver.current_url == self.base_url + "/")
            
            execution_time = time.time() - start_time
            print(f"⏱️ TEST 2 Execution Time: {execution_time:.2f} seconds")
            print("✅ TEST 2 PASSED: Hero section works correctly")
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"⏱️ TEST 2 Execution Time: {execution_time:.2f} seconds")
            self.take_screenshot("test_02_hero_section_error")
            print(f"❌ TEST 2 FAILED: {str(e)}")
            raise
    
    def test_03_services_section(self):
        """Test 3: Services section with cards"""
        print("\n" + "="*60)
        print("TEST 3: Services Section")
        print("="*60)
        
        start_time = time.time()
        
        try:
            self.driver.execute_script("window.scrollTo(0, 600);")
            time.sleep(2)
            
            services_heading = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Our Services')]"))
            )
            self.assertTrue(services_heading.is_displayed())
            print("✓ Services heading is displayed")
            
            service_cards = self.driver.find_elements(
                By.XPATH, "//section[contains(@style, 'background-color: #f9fafb')]//div[contains(@style, 'background: white')]"
            )
            self.assertGreaterEqual(len(service_cards), 4, "Expected at least 4 service cards")
            print(f"✓ Found {len(service_cards)} service cards")
            
            expected_services = ["Find Expert Tailors", "Custom Clothing", "Pre-Designed Collections", "Order Tracking"]
            
            for service_name in expected_services:
                service_element = self.driver.find_element(
                    By.XPATH, f"//h3[contains(text(), '{service_name}')]"
                )
                self.assertTrue(service_element.is_displayed())
                print(f"✓ Service '{service_name}' is displayed")
            

            learn_more_links = self.driver.find_elements(By.XPATH, "//a[contains(text(), 'Learn More →')]")
            self.assertGreaterEqual(len(learn_more_links), 2, "Expected Learn More links")
            
            execution_time = time.time() - start_time
            print(f"⏱️ TEST 3 Execution Time: {execution_time:.2f} seconds")
            print("✅ TEST 3 PASSED: Services section displayed correctly")
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"⏱️ TEST 3 Execution Time: {execution_time:.2f} seconds")
            self.take_screenshot("test_03_services_section_error")
            print(f"❌ TEST 3 FAILED: {str(e)}")
            raise
    
    def test_04_featured_tailors_section(self):
        """Test 4: Featured tailors section"""
        print("\n" + "="*60)
        print("TEST 4: Featured Tailors Section")
        print("="*60)
        
        start_time = time.time()
        
        try:
            self.driver.execute_script("window.scrollTo(0, 1200);")
            time.sleep(2)
            
            featured_heading = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Featured Tailors')]"))
            )
            self.assertTrue(featured_heading.is_displayed())
            print("✓ Featured Tailors heading is displayed")
            
            tailor_cards = self.driver.find_elements(By.CLASS_NAME, "tailor-card")
            
            if tailor_cards:
                print(f"✓ Found {len(tailor_cards)} tailor cards")
                
                first_card = tailor_cards[0]
                self.scroll_to_element(first_card)
                
                card_elements = [
                    (".//h3", "Tailor Name"),
                    (".//img", "Profile Image"),
                    (".//div[contains(@style, 'background: rgba(255,255,255,0.9)')]", "Rating Badge"),
                    (".//button[contains(text(), 'View Profile')]", "View Profile Button")
                ]
                
                for selector, element_name in card_elements:
                    try:
                        element = first_card.find_element(By.XPATH, selector)
                        self.assertTrue(element.is_displayed())
                        print(f"✓ {element_name} is displayed in tailor card")
                    except NoSuchElementException:
                        print(f"⚠ {element_name} not found in tailor card")
                
            else:
                print("ℹ No tailor cards found (this might be normal if no tailors in database)")
            
            execution_time = time.time() - start_time
            print(f"⏱️ TEST 4 Execution Time: {execution_time:.2f} seconds")
            print("✅ TEST 4 PASSED: Featured tailors section checked")
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"⏱️ TEST 4 Execution Time: {execution_time:.2f} seconds")
            self.take_screenshot("test_04_tailors_section_error")
            print(f"❌ TEST 4 FAILED: {str(e)}")
            raise
    
    def test_05_navigation_functionality(self):
        """Test 5: Navigation links work correctly"""
        print("\n" + "="*60)
        print("TEST 5: Navigation Functionality")
        print("="*60)
        
        start_time = time.time()
        
        try:
            # Ensure we're on home page
            self.driver.get(self.base_url)
            time.sleep(2)
            
            # Test navigation links
            nav_links = {
                "About": "about",
                "Find Tailor": "findTailor", 
                "Pre-Designed": "pre_designed"
            }
            
            for link_text, expected_url_part in nav_links.items():
                # Find and click navigation link
                nav_link = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{link_text}')]"))
                )
                nav_link.click()
                
                # Verify navigation
                self.wait.until(EC.url_contains(expected_url_part))
                print(f"✓ {link_text} navigation works")
                
                # Go back to home
                self.driver.back()
                self.wait.until(EC.url_contains("home") or self.driver.current_url == self.base_url + "/")
                time.sleep(1)
            
            execution_time = time.time() - start_time
            print(f"⏱️ TEST 5 Execution Time: {execution_time:.2f} seconds")
            print("✅ TEST 5 PASSED: All navigation links work correctly")
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"⏱️ TEST 5 Execution Time: {execution_time:.2f} seconds")
            self.take_screenshot("test_05_navigation_error")
            print(f"❌ TEST 5 FAILED: {str(e)}")
            raise
    
    def test_06_tailor_profile_modal(self):
        """Test 6: Tailor profile modal functionality"""
        print("\n" + "="*60)
        print("TEST 6: Tailor Profile Modal")
        print("="*60)
        
        start_time = time.time()
        
        try:
            # Ensure we're on home page and scroll to tailors
            self.driver.get(self.base_url)
            self.driver.execute_script("window.scrollTo(0, 1200);")
            time.sleep(2)
            
            # Find View Profile buttons
            view_profile_buttons = self.driver.find_elements(
                By.XPATH, "//button[contains(text(), 'View Profile')]"
            )
            
            if view_profile_buttons:
                # Click first available View Profile button
                first_button = view_profile_buttons[0]
                self.scroll_to_element(first_button)
                first_button.click()
                
                # Wait for modal to appear
                modal = self.wait.until(
                    EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'hire-modal')]"))
                )
                self.assertTrue(modal.is_displayed())
                print("✓ Tailor profile modal opened")
                
                # Test modal tabs
                tabs_to_test = ["About", "Portfolio", "Contact"]
                
                for tab_name in tabs_to_test:
                    try:
                        tab_btn = self.driver.find_element(
                            By.XPATH, f"//button[contains(text(), '{tab_name}')]"
                        )
                        tab_btn.click()
                        time.sleep(1)
                        print(f"✓ {tab_name} tab works")
                    except NoSuchElementException:
                        print(f"⚠ {tab_name} tab not found")
                
                # Test modal close
                close_btn = self.driver.find_element(By.XPATH, "//span[@id='closeModal']")
                close_btn.click()
                
                # Wait for modal to close
                self.wait.until(EC.invisibility_of_element(modal))
                print("✓ Tailor profile modal closes correctly")
                
            else:
                print("ℹ No View Profile buttons found (might be normal if not logged in or no tailors)")
            
            execution_time = time.time() - start_time
            print(f"⏱️ TEST 6 Execution Time: {execution_time:.2f} seconds")
            print("✅ TEST 6 PASSED: Tailor profile modal functionality works")
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"⏱️ TEST 6 Execution Time: {execution_time:.2f} seconds")
            self.take_screenshot("test_06_tailor_modal_error")
            print(f"❌ TEST 6 FAILED: {str(e)}")
            raise
    
    def test_07_footer_section(self):
        """Test 7: Footer section and links"""
        print("\n" + "="*60)
        print("TEST 7: Footer Section")
        print("="*60)
        
        start_time = time.time()
        
        try:
            # Scroll to footer
            self.scroll_to_bottom()
            time.sleep(2)
            
            # Test footer sections
            footer_sections = [
                "About Us",
                "Important Links", 
                "My Services",
                "Connect With Us"
            ]
            
            for section in footer_sections:
                try:
                    section_element = self.driver.find_element(
                        By.XPATH, f"//h3[contains(text(), '{section}')]"
                    )
                    self.assertTrue(section_element.is_displayed())
                    print(f"✓ Footer section '{section}' found")
                except NoSuchElementException:
                    print(f"⚠ Footer section '{section}' not found")
            
            # Test social media links
            social_platforms = ["facebook", "instagram", "twitter"]
            social_links_found = 0
            
            for platform in social_platforms:
                try:
                    social_link = self.driver.find_element(
                        By.XPATH, f"//footer//a[contains(@href, '{platform}')]"
                    )
                    self.assertTrue(social_link.is_displayed())
                    social_links_found += 1
                except NoSuchElementException:
                    print(f"⚠ {platform.capitalize()} link not found")
            
            print(f"✓ Found {social_links_found} social media links")
            
            # Test footer links
            footer_links = ["Home", "About", "Find Tailor", "Pre-Designed"]
            
            for link_text in footer_links:
                try:
                    footer_link = self.driver.find_element(
                        By.XPATH, f"//footer//a[contains(text(), '{link_text}')]"
                    )
                    self.assertTrue(footer_link.is_displayed())
                except NoSuchElementException:
                    print(f"⚠ Footer link '{link_text}' not found")
            
            # Test legal links
            legal_links = ["Privacy", "T & C"]
            for link_text in legal_links:
                try:
                    legal_link = self.driver.find_element(
                        By.XPATH, f"//a[contains(text(), '{link_text}')]"
                    )
                    self.assertTrue(legal_link.is_displayed())
                except NoSuchElementException:
                    print(f"⚠ Legal link '{link_text}' not found")
            
            execution_time = time.time() - start_time
            print(f"⏱️ TEST 7 Execution Time: {execution_time:.2f} seconds")
            print("✅ TEST 7 PASSED: Footer section checked")
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"⏱️ TEST 7 Execution Time: {execution_time:.2f} seconds")
            self.take_screenshot("test_07_footer_error")
            print(f"❌ TEST 7 FAILED: {str(e)}")
            raise
    
    def test_08_responsive_design(self):
        """Test 8: Basic responsive design check"""
        print("\n" + "="*60)
        print("TEST 8: Responsive Design")
        print("="*60)
        
        start_time = time.time()
        
        try:
            # Test different screen sizes
            screen_sizes = [
                (1920, 1080, "Desktop"),
                (1366, 768, "Laptop"), 
                (768, 1024, "Tablet"),
                (375, 667, "Mobile")
            ]
            
            for width, height, device_name in screen_sizes:
                self.driver.set_window_size(width, height)
                time.sleep(1)
                
                # Check if essential elements are still visible
                essential_elements = [
                    "//a[contains(text(), 'DorZi')]",  # Logo
                    "//a[contains(text(), 'Find Tailor')]",  # Navigation
                ]
                
                all_visible = True
                for xpath in essential_elements:
                    try:
                        element = self.driver.find_element(By.XPATH, xpath)
                        if not element.is_displayed():
                            all_visible = False
                            break
                    except NoSuchElementException:
                        all_visible = False
                        break
                
                if all_visible:
                    print(f"✓ {device_name} ({width}x{height}): Essential elements visible")
                else:
                    print(f"⚠ {device_name} ({width}x{height}): Some elements not visible")
            
            # Reset to default size
            self.driver.set_window_size(1920, 1080)
            
            execution_time = time.time() - start_time
            print(f"⏱️ TEST 8 Execution Time: {execution_time:.2f} seconds")
            print("✅ TEST 8 PASSED: Responsive design check completed")
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"⏱️ TEST 8 Execution Time: {execution_time:.2f} seconds")
            self.take_screenshot("test_08_responsive_error")
            print(f"❌ TEST 8 FAILED: {str(e)}")
            raise
    
    def test_09_performance_and_loading(self):
        """Test 9: Performance and loading checks"""
        print("\n" + "="*60)
        print("TEST 9: Performance Checks")
        print("="*60)
        
        start_time = time.time()
        
        try:
            # Test home page load time
            start_load_time = time.time()
            self.driver.get(self.base_url)
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Find the Perfect')]")))
            load_time = time.time() - start_load_time
            
            print(f"✓ Home page loaded in {load_time:.2f} seconds")
            
            # Check for broken images
            images = self.driver.find_elements(By.TAG_NAME, "img")
            broken_images = 0
            
            for image in images:
                natural_width = image.get_attribute("naturalWidth")
                if natural_width == "0" or not natural_width:
                    broken_images += 1
            
            if broken_images == 0:
                print(f"✓ All {len(images)} images loaded correctly")
            else:
                print(f"⚠ {broken_images} broken images found")
            
            # Performance thresholds
            if load_time < 5.0:
                print("✓ Page load time is acceptable (< 5 seconds)")
            else:
                print(f"⚠ Page load time is slow: {load_time:.2f} seconds")
            
            execution_time = time.time() - start_time
            print(f"⏱️ TEST 9 Execution Time: {execution_time:.2f} seconds")
            print("✅ TEST 9 PASSED: Performance checks completed")
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"⏱️ TEST 9 Execution Time: {execution_time:.2f} seconds")
            self.take_screenshot("test_09_performance_error")
            print(f"❌ TEST 9 FAILED: {str(e)}")
            raise

def run_complete_test_suite():
    """Run the complete test suite with summary"""
    print("🚀 DORZI COMPLETE SELENIUM TEST SUITE")
    print("=" * 70)
    print("This will test ALL functionality of your Dorzi application")
    print("Login Credentials: abdullahmusabbir703@gmail.com / Shuvo1996$")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests in order - Login first, then other tests
    test_methods = [
        'test_00_user_login',  # Login first
        'test_01_home_page_load',
        'test_02_hero_section', 
        'test_03_services_section',
        'test_04_featured_tailors_section',
        'test_05_navigation_functionality',
        'test_06_tailor_profile_modal',
        'test_07_footer_section',
        'test_08_responsive_design',
        'test_09_performance_and_loading'
    ]
    
    for method in test_methods:
        suite.addTest(DorziCompleteTest(method))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print final summary
    print("\n" + "=" * 70)
    print("📊 FINAL TEST SUMMARY")
    print("=" * 70)
    print(f"Total Tests Run: {result.testsRun}")
    print(f"Tests Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Tests Failed: {len(result.failures)}")
    print(f"Tests Errored: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("🎉 SUCCESS: All tests passed! Your Dorzi application is working correctly.")
    else:
        print("❌ SOME TESTS FAILED: Check the details above and fix the issues.")
        
        # Print failure details
        if result.failures:
            print("\nFailed Tests:")
            for test, traceback in result.failures:
                print(f"  - {test}: {traceback.splitlines()[-1]}")
        
        if result.errors:
            print("\nErrored Tests:")
            for test, traceback in result.errors:
                print(f"  - {test}: {traceback.splitlines()[-1]}")
    
    print("=" * 70)
    return result.wasSuccessful()

if __name__ == "__main__":
    try:
        success = run_complete_test_suite()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        print("Make sure:")
        print("1. Your Django development server is running on localhost:8000")
        print("2. You have internet connection for ChromeDriver download")
        print("3. Google Chrome is installed")
        print("4. The login credentials are correct: abdullahmusabbir703@gmail.com / Shuvo1996$")
        sys.exit(1)
