
# PDF Scrapper with Captcha Solver

  

This project is a Tkinter-based desktop application that automates the process of downloading PDFs from multiple URLs, bypassing CAPTCHA challenges using the 2Captcha service.

  

## Features

  

-  **GUI Interface**: A user-friendly interface to manage URLs and monitor progress.

-  **2Captcha Integration**: Automatically solves CAPTCHAs encountered during the download process.

-  **Logging**: Detailed logging of the process for easy troubleshooting.

-  **Headless Browser Option**: Ability to run the browser in headless mode for a seamless experience.

-  **Customizable**: Easily add new functionalities or modify existing ones.

  

## Requirements
> ### No further requirements if you have an .exe file.


- Python 3.x

- Required Python packages: `selenium`, `twocaptcha`, `tkinter`, `pyinstaller`

- Simple Chrome Installation ***`Compulsory`***

`

  

## Installation

> ### Windows Executable (.exe):
> https://github.com/tensor35/pdf_scrapper_fiverr/releases/tag/Windows


1.  **Clone the repository**:

```sh

git clone https://github.com/your-repo-url/pdf-scrapper.git

cd pdf-scrapper

```

  

2.  **Install the required packages**:

```sh

pip install selenium twocaptcha

```

  

3.  **Download the ChromeDriver**:

- Download the ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads) and ensure it's in your PATH.

  

## Configuration

  

The application requires a 2Captcha API key to function. This can be configured in two ways:

  

1.  **Via the GUI**: The application will prompt you to enter the API key the first time it runs.

2.  **Manually**: Create a `config.json` file in the root directory with the following content:

```json

{

"api_key": "YOUR_2CAPTCHA_API_KEY"

}

```

  

> ***This step can be skipped. Script will ask for api key on initial
> execution***

  

## Usage

  

1.  **Run the application**:
> ***If you downloaded .exe executable  just run it on windows***
```sh

python main.py

```

  

2.  **Select the file with URLs**:

- Click the "Select File" button to choose a `.txt` file containing the list of URLs (one per line).

  

3.  **Start scraping**:

- Click the "Start Scraping" button to begin the process.

- The application will open each URL, solve any CAPTCHAs encountered, and download the PDF.

  

4.  **Monitor progress**:

- The progress bar and log window will update with the current status of the scraping process.

  

5.  **Cancel operation**:

- Click the "Cancel" button to stop the scraping process at any time.

  

## GUI Components

  

-  **File Selection**: Choose a `.txt` file containing the list of URLs.

-  **Progress Bar**: Visual representation of the scraping progress.

-  **Log Window**: Displays real-time logs of the scraping process.

-  **Headless Mode Checkbox**: Option to run the browser in headless (Hidden) mode.

-  **Credits Section**: Link to the GitHub repository for issues and further information.

  

## Logging

  

- All actions are logged to a file named `script.log` in the root directory.

- Logs are also displayed in the log window within the GUI.

  

## Error Handling

  

- The application handles various exceptions such as validation errors, network errors, and API errors from the 2Captcha service.

- Errors are logged and displayed in the log window.

  

## Contributing

  

1.  **Fork the repository**.

2.  **Create a new branch**:

```sh

git checkout -b feature-name

```

3.  **Commit your changes**:

```sh

git commit -m 'Add some feature'

```

4.  **Push to the branch**:

```sh

git push origin feature-name

```

5.  **Create a Pull Request**.

  

## License

  

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

  

## Acknowledgments

  

- [2Captcha](https://2captcha.com/) for their CAPTCHA solving service.

- [Selenium](https://www.selenium.dev/) for browser automation.

- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI framework.

  

---

  

Feel free to modify and extend this application as needed for your specific use case. Happy scraping!# PDF Scrapper with Captcha Solver

  

This project is a Tkinter-based desktop application that automates the process of downloading PDFs from multiple URLs, bypassing CAPTCHA challenges using the 2Captcha service.

  

## Features

  

-  **GUI Interface**: A user-friendly interface to manage URLs and monitor progress.

-  **2Captcha Integration**: Automatically solves CAPTCHAs encountered during the download process.

-  **Logging**: Detailed logging of the process for easy troubleshooting.

-  **Headless Browser Option**: Ability to run the browser in headless mode for a seamless experience.

-  **Customizable**: Easily add new functionalities or modify existing ones.

  

## Requirements

  

- Python 3.x

- Required Python packages: `selenium`, `twocaptcha`, `tkinter`

- Simple Chrome Installation ***`Compulsory`***

`

  

## Installation

  

1.  **Clone the repository**:

```sh

git https://github.com/tensor35/pdf_scrapper_fiverr.git

cd pdf_scrapper_fiverr

```

  

2.  **Install the required packages**:

```sh

pip install selenium twocaptcha

```

  

3.  **Download the ChromeDriver**:

- Download the ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads) and ensure it's in your PATH.

  

## Configuration

  

The application requires a 2Captcha API key to function. This can be configured in two ways:

  

1.  **Via the GUI**: The application will prompt you to enter the API key the first time it runs.

> `Below step can be skipped. Script will ask for api key on initial execution`

2.  **Manually**: Create a `config.json` file in the root directory with the following content:

```json

{

"api_key": "YOUR_2CAPTCHA_API_KEY"

}

```

  

## Usage

  

1.  **Run the application**:

```sh

python main.py

```

  

2.  **Select the file with URLs**:

- Click the "Select File" button to choose a `.txt` file containing the list of URLs (one per line).

  

3.  **Start scraping**:

- Click the "Start Scraping" button to begin the process.

- The application will open each URL, solve any CAPTCHAs encountered, and download the PDF.

  

4.  **Monitor progress**:

- The progress bar and log window will update with the current status of the scraping process.

  

5.  **Cancel operation**:

- Click the "Cancel" button to stop the scraping process at any time.

  

## GUI Components

  

-  **File Selection**: Choose a `.txt` file containing the list of URLs.

-  **Progress Bar**: Visual representation of the scraping progress.

-  **Log Window**: Displays real-time logs of the scraping process.

-  **Headless Mode Checkbox**: Option to run the browser in headless mode.

-  **Credits Section**: Link to the GitHub repository for issues and further information.

  

## Logging

  

- All actions are logged to a file named `script.log` in the root directory.

- Logs are also displayed in the log window within the GUI.

  

## Error Handling

  

- The application handles various exceptions such as validation errors, network errors, and API errors from the 2Captcha service.

- Errors are logged and displayed in the log window.

  

## Contributing

  

1.  **Fork the repository**.

2.  **Create a new branch**:

```sh

git checkout -b feature-name

```

3.  **Commit your changes**:

```sh

git commit -m 'Add some feature'

```

4.  **Push to the branch**:

```sh

git push origin feature-name

```

5.  **Create a Pull Request**.

  

## License

  

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

  

## Acknowledgments

  

- [2Captcha](https://2captcha.com/) for their CAPTCHA solving service.

- [Selenium](https://www.selenium.dev/) for browser automation.

- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI framework.

  

---

  

Feel free to modify and extend this application as needed for your specific use case. Happy scraping!