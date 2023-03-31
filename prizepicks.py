from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time


def main():
    chrome_options = Options()
    chrome_options.add_argument("--enable-extensions")

    driver = webdriver.Chrome(
        ChromeDriverManager().install(), chrome_options=chrome_options)

    ############## PRIZEPICKS ################################################
    #
    url = "https://app.prizepicks.com/"

    driver.get(url)

    # this is to get rid of the pop-up box that shows after you Selenium opens the prizepicks page
    driver.find_element(By.CLASS_NAME, "close").click()

    # Selecting NBA
    driver.find_element(By.XPATH,
                        "//div[@class='name'][normalize-space()= 'NBA']").click()

    time.sleep(3)

    all_stats = driver.find_elements(By.CLASS_NAME, 'stat ')

    scoring_options = []

    for st in all_stats:
        scoring_options.append(st.text)

    for j, i in enumerate(scoring_options):
        current_stat = str(i)
        print("Stat name:" + i)

        # Clicking the next stat tab
        if j == 0:
            pass
        else:
            driver.find_element(By.XPATH,
                                "//div[@class='stat '][normalize-space()='"+str(i)+"']").click()

        # gathering projections
        projections = WebDriverWait(driver, 40).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".projection")))

        # creating a list of the players names and scores to be collected
        nbaPlayers = []

        for projection in projections:

            names = projection.find_element(
                By.XPATH, './/div[@class="name"]').text
            points = projection.find_element(By.XPATH,
                                             './/div[@class="presale-score"]').get_attribute('innerHTML')

            players = {
                'Name': names,
                'Stat': current_stat,
                'Line': points,
            }

            nbaPlayers.append(players)

        # Put the list in a dataframe
        if j == 0:
            df = pd.DataFrame(nbaPlayers)
        else:
            df2 = pd.DataFrame(nbaPlayers)
            df = pd.concat([df, df2], axis=0)
        time.sleep(3)

    print(df)

    timestr = time.strftime("%Y%m%d")

    df.to_csv(r'./PrizePicks/Datasets/' + timestr + '_pp.csv', index=False)

    return df


main()
