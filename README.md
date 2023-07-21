# pixiv-top-tags
A Python script that counts the top tags in all illustrations of a Pixiv user. Uses the [`pixivpy3`](https://github.com/upbit/pixivpy) library to interact with the Pixiv API.

## Installation
### Prerequisites
You will need Python 3.7+ installed on your system. You can download it [here](https://www.python.org/downloads/) if you are on Windows, or by using a package manager in your Linux distribution.

You also need to install Chromium (or Google Chrome) and ChromeDriver. You can download Chromium [here](https://www.chromium.org/getting-involved/download-chromium) and ChromeDriver [here](https://chromedriver.chromium.org/downloads). Make sure to download the version of ChromeDriver that matches your Chromium version.

### Steps
1. Clone the repository, either by using `git clone` or by downloading the ZIP file.
2. Install the required dependencies by running `pip install -r requirements.txt` in the repository directory.
3. Run `python3 authenticate.py` to get the access & refresh token.
    - The script will open a Chrome browser window, allowing you to log in to your Pixiv account. Once logged in, the script will   automatically retrieve the required tokens and save them in the credentials.json file for future use.

## Usage
To count the top tags in all illustrations of a Pixiv user, the command is:
```bash
python3 count.py <user_id>
```

where:
- `<user_id>` is the ID of the Pixiv user whose illustrations you want to count the tags of.

The script will create a `count.json` file, which contains all tags counted in the illustrations, sorted descendingly.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Feel free to contribute to the project and improve its functionality. If you encounter any issues or have suggestions for enhancements, please submit them!