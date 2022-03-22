# libraries
import os, time
from numpy import greater

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


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

        # change the filters.
        lower_limit_value = 1.04
        greater_limit_value = 1.25

        lower_limit_xpath = '//*[@id="root"]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div/ul/li[1]/span/span[4]/span[4]/span[2]'
        greater_limit_xpath = '//*[@id="root"]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div/ul/li[2]/span/span[4]/span[4]/span[2]'
        
        lower_limit = driver.find_element_by_xpath(lower_limit_xpath)
        lower_limit.click()
        lower_limit_btn = driver.find_element_by_xpath(lower_limit_xpath + '/span/span/input');
        lower_limit_btn.click()
        lower_limit_btn.send_keys(Keys.CONTROL, 'a')
        lower_limit_btn.send_keys(Keys.BACKSPACE)
        lower_limit_btn.send_keys(lower_limit_value)

        greater_limit = driver.find_element_by_xpath(greater_limit_xpath)
        greater_limit.click()
        greater_limit_btn = driver.find_element_by_xpath(greater_limit_xpath + '/span/span/input');
        greater_limit_btn.click()
        greater_limit_btn.send_keys(Keys.CONTROL, 'a')
        greater_limit_btn.send_keys(Keys.BACKSPACE)
        greater_limit_btn.send_keys(greater_limit_value)

        # run scan
        run_btn = driver.find_element_by_xpath('//*[@id="root"]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/button[1]')
        run_btn.click()
        time.sleep(4)

        # download the csv.
        download_btn = driver.find_element_by_xpath('//*[@id="backtest-container"]/div[2]/a')
        download_btn.click()
        
        # close the driver.
        time.sleep(2)
        driver.close()
        return True
    except Exception as e:
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
