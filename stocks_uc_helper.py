# libraries
import os, time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# function to download the required csv file.
def download_csv(file_loc):
    # initialize web driver.
    options = webdriver.ChromeOptions();

    try:
        # set download folder.
        download_folder = file_loc.split('\\')[0]
        options = Options()
        options.add_experimental_option("prefs", {
            "download.default_directory": os.getcwd() + '\\' + download_folder,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "profile.default_content_setting_values.automatic_downloads": True
        })

        # load the driver and browse to the website.
        url = 'https://chartink.com/screener/upper-circuit'
        driver = webdriver.Chrome(executable_path = './driver/chromedriver', chrome_options = options);
        driver.get(url);

        # download the csv.
        download_btn = driver.find_element_by_xpath('//*[@id="backtest-container"]/div[2]/a')
        download_btn.click()
        
        # close the driver.
        time.sleep(2)
        driver.close()
        return True
    except:
        return False
    return False


# rename the downloaded file.
def rename_csv(file_loc):
    try:
        # prepare the variables.
        resource_dir = file_loc.split('\\')[0] + '\\'
        final_filename = file_loc.split('\\')[1]

        # get list of files under resource directory.
        files = os.listdir(resource_dir)
        for file in files:
            if file.startswith('Backtest'):
                # rename the downloaded file.
                os.remove(resource_dir + final_filename)
                os.rename(resource_dir + file, resource_dir + final_filename)
                break;

        return True
    except Exception as e:
        return False
    return False
