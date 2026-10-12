import time
from dataclasses import asdict
from selenium.webdriver.common.by import By
from src.driver_manager import DriverManager
from src.data_models import Product
from src.utils import safe_click

class ScraperAgent:
    def __init__(self, config: dict, browser: str = "chrome", headless: bool = True):
        self.config = config
        self.driver_manager = DriverManager(browser_type=browser, headless=headless)
        self.driver = self.driver_manager.get_driver()

    def run(self) -> list:
        results = []
        try:
            self.driver.get(self.config["start_url"])
            current_page = 1

            while current_page <= self.config["max_pages"]:
                print(f"Scraping page {current_page}...")
                time.sleep(self.config["delay_between_pages"])

                items = self.driver.find_elements(By.CSS_SELECTOR, self.config["item_container_selector"])
                for item in items:
                    product_data = self._parse_item(item)
                    results.append(asdict(product_data))

                # Handle Pagination
                pagination_selector = self.config.get("pagination_selector")
                if pagination_selector and current_page < self.config["max_pages"]:
                    next_buttons = self.driver.find_elements(By.CSS_SELECTOR, pagination_selector)
                    if next_buttons:
                        safe_click(self.driver, next_buttons[0])
                        current_page += 1
                    else:
                        print("No next page button found. Stopping.")
                        break
                else:
                    break

        finally:
            self.driver_manager.close_driver()

        return results

    def _parse_item(self, item) -> Product:
        selectors = self.config["item_data_selectors"]
        
        def get_text(selector):
            if not selector: return None
            try:
                return item.find_element(By.CSS_SELECTOR, selector).text.strip()
            except:
                return None

        def get_attr(selector, attr):
            if not selector: return None
            try:
                return item.find_element(By.CSS_SELECTOR, selector).get_attribute(attr)
            except:
                return None

        return Product(
            name=get_text(selectors.get("name")),
            price=get_text(selectors.get("price")),
            description=get_text(selectors.get("description")),
            url=get_attr(selectors.get("url"), "href"),
            image_url=get_attr(selectors.get("image_url"), "src")
        )
