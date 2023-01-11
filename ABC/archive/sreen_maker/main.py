from PIL import Image
from selenium import webdriver
from time import sleep


class ScreenMaker:
    # DESKTOP = (1080,1980) # height, width
    DESKTOP = (900, 1440)
    # PHONE = (1088 + 170, 544 + 40) # old
    PHONE = (1088 + 70, 544 + 40)

    SCROLL_PX_W = 15

    def __init__(self):
        self.browser = self._init_browser()

    def _init_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument(f"--window-size={500},{250}")  # width, height
        browser = webdriver.Chrome('./chromedriver', options=options)
        return browser

    def make_screenshot(self, screen_size, path_to_save, del_scroll=True):
        height, width = screen_size
        if del_scroll:
            width += self.SCROLL_PX_W
        self.browser.set_window_size(width, height)
        self.browser.get_screenshot_as_file(path_to_save)
        if del_scroll:
            self.delete_scroll_from_image(path_to_save)
        return path_to_save

    def get(self, url):
        self.browser.get(url)

    def quit(self):
        self.browser.quit()

    @staticmethod
    def delete_scroll_from_image(image_path):
        img = Image.open(image_path)
        w, h = img.size
        img = img.crop((0, 0, w - ScreenMaker.SCROLL_PX_W, h))
        img.save(image_path)

