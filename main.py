import logging
import os
import json
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twocaptcha import TwoCaptcha, ValidationException, NetworkException, ApiException, TimeoutException
import time
import concurrent.futures


# Configure logging
log_file = 'script.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
    ]
)

logger = logging.getLogger(__name__)

class TkinterLogHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        log_entry = self.format(record)
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, log_entry + '\n')
        self.text_widget.config(state=tk.DISABLED)
        self.text_widget.yview(tk.END)

class CaptchaSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Scrapper")
        self.root.geometry("500x500")

        self.file_path = ""
        self.urls = []
        self.current_url_index = 0
        self.is_cancelled = False
        
        self.api_key = self.load_api_key()
        
        # Initialize the 2Captcha solver with the API key
        self.solver = TwoCaptcha(self.api_key)

        self.setup_gui()

    def load_api_key(self):
        config_path = 'config.json'
        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                config = json.load(file)
                return config.get('api_key')
        
        # If config.json doesn't exist or doesn't contain an API key, prompt the user
        api_key = simpledialog.askstring("API Key Required", "Please enter your 2Captcha API key:")
        if api_key:
            with open(config_path, 'w') as file:
                json.dump({'api_key': api_key}, file)
            return api_key
        else:
            messagebox.showerror("Error", "API key is required to proceed.")
            self.root.quit()

    def setup_gui(self):
        # File selection row
        file_select_frame = tk.Frame(self.root)
        file_select_frame.pack(pady=10, fill=tk.X)

        self.file_label = tk.Label(file_select_frame, text="No File Selected")
        self.file_label.pack(side=tk.LEFT, padx=(10, 5), expand=True)

        self.file_button = tk.Button(file_select_frame, text="Select File", command=self.select_file)
        self.file_button.pack(side=tk.RIGHT, padx=(5, 10))

        self.submit_button = tk.Button(file_select_frame, text="Start Scraping", command=self.submit)
        self.submit_button.pack(side=tk.RIGHT)

        # Progress and controls row
        progress_frame = tk.Frame(self.root)
        progress_frame.pack(pady=10, fill=tk.X)

        self.progress_label = tk.Label(progress_frame, text="Progress: 0/0")
        self.progress_label.pack(side=tk.LEFT, padx=(10, 5), pady=10)

        self.cancel_button = tk.Button(progress_frame, text="Cancel", command=self.cancel, state=tk.DISABLED)
        self.cancel_button.pack(side=tk.RIGHT, padx=(5, 10), pady=10)

        self.progress_bar = ttk.Progressbar(progress_frame, orient='horizontal', length=300, mode='determinate')
        self.progress_bar.pack(side=tk.LEFT, expand=True, padx=(0, 5), pady=10)
        
        # Configuration frame
        config_frame = tk.Frame(self.root)
        config_frame.pack(pady=10, fill=tk.X)
        
        # thread count spinbox
        self.thread_count_label = tk.Label(config_frame, text="Thread count:")
        self.thread_count_label.pack(side=tk.LEFT, padx=(10, 0), pady=10)
        
        self.thread_count_var = tk.IntVar(value=5)
        self.thread_count_spinbox = tk.Spinbox(config_frame, from_=1, to=10, textvariable=self.thread_count_var)
        self.thread_count_spinbox.pack(side=tk.LEFT, padx=(0, 10), pady=10)
        
        # Headless label and checkbox
        self.headless_label = tk.Label(config_frame, text="Show browser automation")
        self.headless_label.pack(side=tk.RIGHT, padx=(0, 10), pady=10)
        
        self.headless_var = tk.BooleanVar()
        self.headless_checkbox = tk.Checkbutton(config_frame, variable=self.headless_var)
        self.headless_checkbox.pack(side=tk.RIGHT, padx=(10, 0), pady=10)
        
        # Tool credits frame
        credits_frame = tk.Frame(self.root)
        credits_frame.pack(pady=10, fill=tk.X)

        # Credits label
        github_label = tk.Label(credits_frame, text="For any information/issues, visit:")
        github_label.pack(side=tk.LEFT, padx=(10, 0), pady=10)

        # GitHub link
        github_link = tk.Label(credits_frame, text="credits @tensor35", fg="blue", cursor="hand2")
        github_link.pack(side=tk.LEFT, padx=(0, 10), pady=10)
        github_link.bind("<Button-1>", lambda e: self.open_github())
        
        # Log frame
        log_frame = tk.Frame(self.root)
        log_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Add a Text widget with horizontal and vertical Scrollbars for logging
        self.log_text = tk.Text(log_frame, wrap=tk.NONE, state=tk.DISABLED)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        log_scrollbar_y = tk.Scrollbar(log_frame, command=self.log_text.yview)
        log_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        log_scrollbar_x = tk.Scrollbar(log_frame, command=self.log_text.xview, orient=tk.HORIZONTAL)
        log_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.log_text.config(yscrollcommand=log_scrollbar_y.set, xscrollcommand=log_scrollbar_x.set)

        # Add a custom log handler to update the log_text widget
        log_handler = TkinterLogHandler(self.log_text)
        log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(log_handler)

    def open_github(self):
        import webbrowser
        webbrowser.open("https://github.com/your-repo-url")

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.file_path:
            self.file_label.config(text=f"Selected File: {os.path.basename(self.file_path)}")

            with open(self.file_path, 'r') as file:
                self.urls = file.readlines()
                self.urls = [url.strip() for url in self.urls if url.strip()]

            self.progress_label.config(text=f"Progress: 0/{len(self.urls)}")
            self.progress_bar.config(maximum=len(self.urls))

    def submit(self):
        if self.urls:
            self.submit_button.config(state=tk.DISABLED)
            self.cancel_button.config(state=tk.NORMAL)
            self.start_scraping()
        else:
            messagebox.showerror("Error", "Please select a file with URLs.")

    def cancel(self):
        self.is_cancelled = True
        self.cancel_button.config(state=tk.DISABLED)
        self.cancel_button.config(text="Cancelling...")
        logger.info("Cancelled scraping.")
        
    def batch_urls(self, urls, batch_size=5):
        for i in range(0, len(urls), batch_size):
            yield urls[i:i + batch_size]

    def start_scraping(self):
        self.is_cancelled = False
        self.current_url_index = 0
        self.progress_bar.config(value=0)
        threading.Thread(target=self.scrape_urls).start()

    def scrape_urls(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.thread_count_var.get()) as executor:
            futures = {executor.submit(self.scrape_url, url): url for url in self.urls}

            for future in concurrent.futures.as_completed(futures):
                if self.is_cancelled:
                    break

                url = futures[future]
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"Error scraping URL {url}: {e}")

                self.current_url_index += 1
                self.progress_label.config(text=f"Progress: {self.current_url_index}/{len(self.urls)}")
                self.progress_bar.config(value=self.current_url_index)

        if not self.is_cancelled:
            messagebox.showinfo("Info", "Scraping completed.")
        else:
            messagebox.showinfo("Info", "Scraping cancelled.")
        self.submit_button.config(state=tk.NORMAL)
        self.cancel_button.config(text="Cancel")
        
        
    def solve_captcha(self, base64_image):
        try:
            result = self.solver.normal(base64_image)
            return result['code']
        except ValidationException as e:
            logger.error(f"Validation error solving captcha: {e}")
        except NetworkException as e:
            logger.error(f"Network error solving captcha: {e}")
        except ApiException as e:
            logger.error(f"API error solving captcha: {e}")
        except TimeoutException as e:
            logger.error(f"Timeout error solving captcha: {e}")
        except Exception as e:
            logger.error(f"Unexpected error solving captcha: {e}")
        return None

    def scrape_url(self, base_url):
        # Set up Chrome options for downloading
        chrome_options = webdriver.ChromeOptions()
        download_dir = os.path.abspath("downloads")
        os.makedirs(download_dir, exist_ok=True)
        initial_pdf_count = len([name for name in os.listdir(download_dir) if name.endswith('.pdf')])

        # Experimental options to set the download directory and disable the prompt
        prefs = {
            'download.default_directory': download_dir,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': False,
            'plugins.always_open_pdf_externally': True
        }
        chrome_options.add_experimental_option('prefs', prefs)
        if not self.headless_var.get():
            chrome_options.add_argument("--headless=new")

        # Initialize the Chrome driver
        try:
            driver = webdriver.Chrome(options=chrome_options)
            logger.info("Initialized Chrome driver successfully.")
        except Exception as e:
            logger.error(f"Error initializing Chrome driver: {e}")
            return

        try:
            # Navigating to URL
            driver.get(base_url)
            logger.info(f"Navigated to URL: {base_url}")
        except Exception as e:
            logger.error(f"Error navigating to URL: {e}")
            driver.quit()
            return

        try:
            # Wait for the page to load and locate the PDF object
            pdf_object = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "objtcontentpdf")))
            logger.info("Located PDF object.")
        except Exception as e:
            logger.error(f"Error locating PDF object: {e}")
            driver.quit()
            return

        try:
            # Bypassing shadow-root and opening captcha embedder in new tab
            direct_url = pdf_object.get_attribute("data")
            driver.execute_script("window.open();")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(direct_url)
            logger.info("Opened direct URL in a new tab.")
        except Exception as e:
            logger.error(f"Error navigating to direct URL: {e}")
            driver.quit()
            return

        try:
            # Locate the captcha image by its src attribute
            captcha_image = driver.find_element(By.XPATH, "//img[contains(@src, 'stickyImg')]")
            captcha_image_url = captcha_image.get_attribute("src")
            driver.execute_script(f"window.open('{captcha_image_url}', '_blank');")
            driver.switch_to.window(driver.window_handles[2])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
            logger.info("Located captcha image.")
        except Exception as e:
            logger.error(f"Error locating captcha image: {e}")
            driver.quit()
            return

        try:
            # Get the base64 encoded image directly from the page
            captcha_image_base64 = driver.execute_script(
                """
                var canvas = document.createElement('canvas');
                var img = document.querySelector('img');
                canvas.width = img.width;
                canvas.height = img.height;
                canvas.getContext('2d').drawImage(img, 0, 0);
                return canvas.toDataURL('image/png').substring(22);
                """
            )
            logger.info("Extracted base64 image from captcha.")
        except Exception as e:
            logger.error(f"Error extracting base64 image: {e}")
            driver.quit()
            return

        # Solve the captcha
        captcha_solution = self.solve_captcha(captcha_image_base64)
        if not captcha_solution:
            logger.error("Failed to solve captcha.")
            driver.quit()
            return

        logger.info(f"Captcha solution: {captcha_solution}")

        try:
            # Close the new tab and switch back to the base captcha tab
            driver.close()
            driver.switch_to.window(driver.window_handles[1])
            logger.info("Closed captcha image tab and switched back.")
        except Exception as e:
            logger.error(f"Error switching tabs: {e}")
            driver.quit()
            return

        try:
            # Enter the captcha solution into the input field
            captcha_input = driver.find_element(By.ID, 'captcha')
            captcha_input.send_keys(captcha_solution)
            # Click the submit button
            submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
            submit_button.click()
            logger.info("Submitted captcha solution.")
        except Exception as e:
            logger.error(f"Error submitting captcha solution: {e}")
            driver.quit()
            return

        try:
            # Wait for the PDF to download
            logger.info("Waiting for PDF to download.")
            seconds_passed = 0
            while len([name for name in os.listdir(download_dir) if name.endswith('.pdf')]) == initial_pdf_count:
                if seconds_passed > 30:
                    logger.error("Waited too long for PDF to download.")
                    messagebox.showerror("Error", "PDF download took too long. Aborting!")
                    break
                time.sleep(1)
                seconds_passed += 1
        except Exception as e:
            logger.error(f"Error during wait: {e}")

        logger.info(f"PDF should be downloaded to {download_dir}")
        
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = CaptchaSolverApp(root)
    root.mainloop()
