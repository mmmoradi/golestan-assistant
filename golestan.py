from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
from time import sleep

# TODO get config as class parameter 
import config


class Golestan:
    def __init__(self):
        # self.config = config # TODO
        self.driver = webdriver.Chrome()
        self.turn = 2 # number for FaciX

    def __del__(self):
        self.driver.quit()


    def login(self):
        self.driver.get(config.login_url)

        sleep(5)

        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME,"iframe")))
        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'Master')))
        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'Form_Body')))

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "F80351")))

        username = self.driver.find_element(By.ID, "F80351")
        username.send_keys(config.username)

        password = self.driver.find_element(By.ID, "F80401")
        password.send_keys(config.password)

        captcha = self.driver.find_element(By.ID, "F51701")
        captcha.send_keys(input('Enter captcha: '))

        captcha.send_keys(Keys.ENTER)

        self.driver.switch_to.default_content()

    
    def report(self, code):
        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "Faci2")))
        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"Master")))
        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "Form_Body")))

        self.driver.find_element(By.ID, "F20851").send_keys(str(code))

        self.driver.find_element(By.ID, "OK").click()


        self.driver.switch_to.default_content()


    def get_lessons(self, code):
        WebDriverWait(self.driver, 50).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "Faci3")))
        WebDriverWait(self.driver, 50).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"Master")))
        WebDriverWait(self.driver, 50).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "Form_Body")))

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "GF078012_0")))


        self.driver.find_element(By.ID, "GF078012_0").send_keys(code, Keys.ENTER)

        self.driver.switch_to.default_content()


    def pars_lessons(self):
        df_list = []
        flag = True

        while flag:

            self.driver.switch_to.frame(self.driver.find_element(By.NAME, "Faci3"))
            self.driver.switch_to.frame(self.driver.find_element(By.NAME,"Master"))
            self.driver.switch_to.frame(self.driver.find_element(By.NAME,"Header"))
            self.driver.switch_to.frame(self.driver.find_element(By.ID, "Form_Body"))

            table = self.driver.find_element(By.ID, "Table3")

            html = table.get_attribute('outerHTML')

            self.driver.switch_to.default_content()

            df_list.append(pd.read_html(html)[0])

            flag = self.next_page()

        return pd.concat(df_list)
    
    def next_page(self):
        self.driver.switch_to.frame(self.driver.find_element(By.NAME, "Faci3"))
        self.driver.switch_to.frame(self.driver.find_element(By.NAME,"Commander"))

        next_button = self.driver.find_element(By.ID, "MoveLeft")
        page_number = self.driver.find_element(By.ID, "TextPage")

        before = page_number.get_attribute('value')
        next_button.click()
        after = page_number.get_attribute('value')

        self.driver.switch_to.default_content()

        if before == after:
            return False
        else:
            return  True



    def refresh(self):
        self.driver.switch_to.frame(self.driver.find_element(By.NAME, "Faci3"))
        self.driver.switch_to.frame(self.driver.find_element(By.NAME,"Commander"))

        ref_button = self.driver.find_element(By.ID, "IM_Refresh")

        ref_button.click()

        self.driver.switch_to.default_content()


    def filter_page(self):
        self.driver.switch_to.frame(self.driver.find_element(By.NAME, "Faci3"))
        self.driver.switch_to.frame(self.driver.find_element(By.NAME,"Commander"))

        ref_button = self.driver.find_element(By.ID, "IM91_gofilter")

        ref_button.click()

        self.driver.switch_to.default_content()


        self.driver.switch_to.frame(self.driver.find_element(By.NAME, "Faci3"))
        self.driver.switch_to.frame(self.driver.find_element(By.NAME,"Master"))
        self.driver.switch_to.frame(self.driver.find_element(By.NAME, "Form_Body"))

        self.driver.find_element(By.ID, "GF078012_0").clear()
        self.driver.find_element(By.ID, "GF078516_0").clear()
        self.driver.find_element(By.ID, "GF079020_0").clear()
        self.driver.find_element(By.ID, "GF079524_0").clear()

        self.driver.switch_to.default_content()


    def scores(self):
        self.turn = self.turn + 1

        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "Faci2")))
        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"Master")))
        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"Form_Body")))

        self.driver.execute_script('menuauth("0"+";"+"12310"+";");')

        self.driver.switch_to.default_content()

        sleep(5)

        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "Faci"+str(self.turn) )))
        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"Master")))
        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"Form_Body")))

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "T01")))

        self.driver.execute_script('TrmDetail("4022","80");')

        self.driver.switch_to.default_content()

        sleep(5)

        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "Faci3")))
        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"Master")))
        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"Form_Body")))
        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"FrameNewForm"))) #POINT using id instead of name

        table = self.driver.find_element(By.ID, "T02")

        html = table.get_attribute('outerHTML')

        pdtable = pd.read_html(html)[0]

        self.driver.switch_to.default_content()

        self.driver.find_elements(By.XPATH, '//*[@title="close"]')[1].click()

        return pdtable




if __name__ == '__main__':

    g = Golestan()
    g.login()
    g.report(102)
    g.get_lessons("2301")
    input()
    # pddf = g.pars_lessons()
    # print(pddf)
