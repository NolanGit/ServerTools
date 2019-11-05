class CommonActions(object):
    def __init__(self, driver):
        self.driver = driver

    def click(self, id_or_xpath_or_css):
        if id_or_xpath_or_css.find('/') == -1 and id_or_xpath_or_css.find(
                '[') == -1:
            try:
                target_element = self.driver.find_element_by_id(
                    id_or_xpath_or_css)
                self.driver.execute_script("arguments[0].scrollIntoView();",
                                           target_element)
                target_element.click()
            except Exception as e:
                print(e)
        elif id_or_xpath_or_css.find('/') == 0:
            try:
                target_element = self.driver.find_element_by_xpath(
                    id_or_xpath_or_css)
                self.driver.execute_script("arguments[0].scrollIntoView();",
                                           target_element)
                target_element.click()
            except Exception as e:
                print(e)
        else:
            try:
                target_element = self.driver.find_element_by_css_selector(
                    id_or_xpath_or_css)
                self.driver.execute_script("arguments[0].scrollIntoView();",
                                           target_element)
                target_element.click()
            except Exception as e:
                print(e)

    def send(self, id_or_xpath, text):
        # 使用方法为【CommonActions.sendkeys('id/xpath','xxx')】
        if id_or_xpath.find('/') == -1:
            # 因为xpath必然有右斜杠，如果没有的话则find方法返回的是-1，因此为id
            try:
                target_element = self.driver.find_element_by_id(id_or_xpath)
                self.driver.execute_script("arguments[0].scrollIntoView();",
                                           target_element)
                target_element.send_keys(text)

            except Exception as e:
                print(e)
        else:
            # 如不为-1，则证明有右斜杠，则为xpath
            try:
                target_element = self.driver.find_element_by_xpath(id_or_xpath)
                self.driver.execute_script("arguments[0].scrollIntoView();",
                                           target_element)
                target_element.send_keys(text)
            except Exception as e:
                print(e)