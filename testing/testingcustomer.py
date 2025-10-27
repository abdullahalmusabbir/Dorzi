import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class CustomerProfileTest:
    def __init__(self):
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        self.total_time = 0
        self.test_results = {}

    def start_timer(self):
        self.start_time = time.time()

    def stop_timer(self, test_name):
        end_time = time.time()
        duration = end_time - self.start_time
        self.total_time += duration
        self.test_results[test_name] = round(duration, 2)
        print(f"⏱️  {test_name}: {duration:.2f} seconds")

    def login(self):
        """Test login functionality"""
        self.start_timer()
        
        try:
            # Navigate to home page
            self.driver.get("http://localhost:8000")  # Adjust URL as needed
            
            # Click login button
            login_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Login')]"))
            )
            login_btn.click()
            
            # Wait for modal to appear and fill credentials
            email_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_field = self.driver.find_element(By.NAME, "password")
            
            email_field.send_keys("emu@gmail.com")
            password_field.send_keys("emu")
            
            # Submit login form
            submit_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_btn.click()
            
            # Wait for redirect to customer profile
            self.wait.until(
                EC.url_contains("customer") or EC.presence_of_element_located((By.TAG_NAME, "main"))
            )
            
            print("✅ Login successful")
            self.stop_timer("Login Test")
            return True
            
        except Exception as e:
            print(f"❌ Login failed: {str(e)}")
            self.stop_timer("Login Test")
            return False

    def test_profile_stats_display(self):
        """Test if profile statistics are displayed correctly"""
        self.start_timer()
        
        try:
            # Check if stats cards are present
            stats_cards = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[style*='background: #f8f9fa']"))
            )
            
            expected_stats = ["Total order", "Completed", "Pending", "Favourite Tailors"]
            found_stats = []
            
            for card in stats_cards[:4]:  # First 4 cards
                text = card.text
                for stat in expected_stats:
                    if stat in text:
                        found_stats.append(stat)
            
            if len(found_stats) == len(expected_stats):
                print("✅ All profile statistics displayed correctly")
                self.stop_timer("Profile Stats Test")
                return True
            else:
                print(f"❌ Missing stats. Found: {found_stats}")
                self.stop_timer("Profile Stats Test")
                return False
                
        except Exception as e:
            print(f"❌ Profile stats test failed: {str(e)}")
            self.stop_timer("Profile Stats Test")
            return False

    def test_personal_info_section(self):
        """Test personal information section"""
        self.start_timer()
        
        try:
            # Check personal info section
            personal_info = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h4[contains(text(), 'Personal Information')]"))
            )
            
            # Verify personal info fields
            info_section = personal_info.find_element(By.XPATH, "./following-sibling::div")
            info_text = info_section.text
            
            required_fields = ["Name", "Email", "Phone", "Address"]
            missing_fields = []
            
            for field in required_fields:
                if field not in info_text:
                    missing_fields.append(field)
            
            if not missing_fields:
                print("✅ Personal information section complete")
                self.stop_timer("Personal Info Test")
                return True
            else:
                print(f"❌ Missing personal info fields: {missing_fields}")
                self.stop_timer("Personal Info Test")
                return False
                
        except Exception as e:
            print(f"❌ Personal info test failed: {str(e)}")
            self.stop_timer("Personal Info Test")
            return False

    def test_measurements_section(self):
        """Test saved measurements section"""
        self.start_timer()
        
        try:
            # Check measurements section
            measurements_header = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h4[contains(text(), 'Saved Measurements')]"))
            )
            
            # Check edit link
            edit_link = measurements_header.find_element(By.XPATH, "./following-sibling::a")
            if "Edit" in edit_link.text:
                print("✅ Measurements section with edit link found")
                
                # Test edit functionality
                edit_link.click()
                
                # Wait for modal to appear
                modal = self.wait.until(
                    EC.presence_of_element_located((By.ID, "editMeasurementsModal"))
                )
                
                # Check if modal has form
                form = modal.find_element(By.ID, "measurementsForm")
                if form:
                    print("✅ Measurements edit modal opened successfully")
                    
                    # Close modal
                    close_btn = modal.find_element(By.ID, "closeEditModal")
                    close_btn.click()
                    
                    # Wait for modal to close
                    self.wait.until(
                        EC.invisibility_of_element_located((By.ID, "editMeasurementsModal"))
                    )
                    
                    self.stop_timer("Measurements Test")
                    return True
                    
            self.stop_timer("Measurements Test")
            return False
            
        except Exception as e:
            print(f"❌ Measurements test failed: {str(e)}")
            self.stop_timer("Measurements Test")
            return False

    def test_orders_tab(self):
        """Test orders tab functionality"""
        self.start_timer()
        
        try:
            # Find and click orders tab
            orders_tab = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'My Orders')]"))
            )
            orders_tab.click()
            
            # Wait for orders content to load
            orders_content = self.wait.until(
                EC.presence_of_element_located((By.ID, "orders"))
            )
            
            # Check if orders are displayed
            order_items = orders_content.find_elements(By.CSS_SELECTOR, "div[style*='border: 1px solid #eee']")
            
            if order_items:
                print(f"✅ Orders tab loaded with {len(order_items)} orders")
                
                # Test view details functionality for first order
                if order_items:
                    view_details_link = order_items[0].find_element(By.XPATH, ".//a[contains(text(), 'View Details')]")
                    view_details_link.click()
                    
                    # Wait for order modal
                    order_modal = self.wait.until(
                        EC.presence_of_element_located((By.ID, "orderModal"))
                    )
                    
                    if order_modal.is_displayed():
                        print("✅ Order details modal opened successfully")
                        
                        # Close modal
                        close_btn = order_modal.find_element(By.ID, "closeModal")
                        close_btn.click()
                        
                        # Wait for modal to close
                        self.wait.until(
                            EC.invisibility_of_element_located((By.ID, "orderModal"))
                        )
            
            self.stop_timer("Orders Tab Test")
            return True
            
        except Exception as e:
            print(f"❌ Orders tab test failed: {str(e)}")
            self.stop_timer("Orders Tab Test")
            return False

    def test_favorite_tailors_tab(self):
        """Test favorite tailors tab functionality"""
        self.start_timer()
        
        try:
            # Find and click favorite tailors tab
            tailors_tab = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Favorite Tailor')]"))
            )
            tailors_tab.click()
            
            # Wait for tailors content to load
            tailors_content = self.wait.until(
                EC.presence_of_element_located((By.ID, "tailors"))
            )
            
            # Check if favorite tailors are displayed
            tailor_cards = tailors_content.find_elements(By.CSS_SELECTOR, "div[style*='flex: 0 0 500px']")
            
            if tailor_cards:
                print(f"✅ Favorite tailors tab loaded with {len(tailor_cards)} tailors")
                
                # Test view profile functionality for first tailor
                if tailor_cards:
                    view_profile_btn = tailor_cards[0].find_element(By.XPATH, ".//button[contains(text(), 'View Profile')]")
                    view_profile_btn.click()
                    
                    # Wait for tailor profile modal
                    tailor_modal = self.wait.until(
                        EC.presence_of_element_located((By.ID, "viewTailorProfileModal"))
                    )
                    
                    if tailor_modal.is_displayed():
                        print("✅ Tailor profile modal opened successfully")
                        
                        # Test tab switching in modal
                        about_tab = tailor_modal.find_element(By.XPATH, ".//button[contains(text(), 'About')]")
                        contact_tab = tailor_modal.find_element(By.XPATH, ".//button[contains(text(), 'Contact')]")
                        
                        contact_tab.click()
                        print("✅ Contact tab switched successfully")
                        
                        about_tab.click()
                        print("✅ About tab switched successfully")
                        
                        # Close modal
                        close_btn = tailor_modal.find_element(By.ID, "closeTailorModal")
                        close_btn.click()
                        
                        # Wait for modal to close
                        self.wait.until(
                            EC.invisibility_of_element_located((By.ID, "viewTailorProfileModal"))
                        )
            
            self.stop_timer("Favorite Tailors Test")
            return True
            
        except Exception as e:
            print(f"❌ Favorite tailors test failed: {str(e)}")
            self.stop_timer("Favorite Tailors Test")
            return False

    def test_navigation(self):
        """Test navigation back to home"""
        self.start_timer()
        
        try:
            # Click on logo to navigate home
            logo = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'DorZi')]"))
            )
            logo.click()
            
            # Wait for home page to load
            self.wait.until(
                EC.url_contains("home") or EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            print("✅ Navigation to home successful")
            self.stop_timer("Navigation Test")
            return True
            
        except Exception as e:
            print(f"❌ Navigation test failed: {str(e)}")
            self.stop_timer("Navigation Test")
            return False

    def test_logout(self):
        """Test logout functionality"""
        self.start_timer()
        
        try:
            # Hover over profile dropdown
            profile_dropdown = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "dropdown"))
            )
            
            # Use JavaScript to trigger hover
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('mouseover'))", profile_dropdown)
            
            # Wait for dropdown menu to appear
            logout_link = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Logout')]"))
            )
            logout_link.click()
            
            # Wait for logout to complete and redirect to home
            self.wait.until(
                EC.url_contains("home")
            )
            
            # Verify logout by checking login button is present
            login_btn = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Login')]"))
            )
            
            print("✅ Logout successful")
            self.stop_timer("Logout Test")
            return True
            
        except Exception as e:
            print(f"❌ Logout test failed: {str(e)}")
            self.stop_timer("Logout Test")
            return False

    def run_all_tests(self):
        """Run all customer profile tests"""
        print("🚀 Starting Customer Profile Tests...")
        print("=" * 50)
        
        all_tests = [
            ("Login", self.login),
            ("Profile Stats", self.test_profile_stats_display),
            ("Personal Info", self.test_personal_info_section),
            ("Measurements", self.test_measurements_section),
            ("Orders Tab", self.test_orders_tab),
            ("Favorite Tailors", self.test_favorite_tailors_tab),
            ("Navigation", self.test_navigation),
            ("Logout", self.test_logout)
        ]
        
        successful_tests = 0
        total_tests = len(all_tests)
        
        for test_name, test_method in all_tests:
            try:
                if test_method():
                    successful_tests += 1
                time.sleep(1)  # Brief pause between tests
            except Exception as e:
                print(f"❌ {test_name} crashed: {str(e)}")
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        
        for test_name, duration in self.test_results.items():
            print(f"📍 {test_name}: {duration} seconds")
        
        print(f"\n✅ Successful: {successful_tests}/{total_tests}")
        print(f"⏱️  Total time: {self.total_time:.2f} seconds")
        print(f"📈 Success rate: {(successful_tests/total_tests)*100:.1f}%")
        
        # Close browser
        self.driver.quit()
        
        return successful_tests == total_tests

if __name__ == "__main__":
    # Run the tests
    tester = CustomerProfileTest()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 ALL CUSTOMER PROFILE TESTS PASSED!")
    else:
        print("\n💥 SOME TESTS FAILED!")
    
    exit(0 if success else 1)
