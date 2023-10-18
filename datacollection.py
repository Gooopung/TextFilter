from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import time

driver = webdriver.Chrome("")
print('loading...')

driver.get("https://login.sina.com.cn/signup/signin.php")
wait = WebDriverWait(driver,5)
time.sleep(60)


search = driver.find_element_by_css_selector('#search_input')
search.send_keys() #添加内容！！！！
confirm_btn = driver.find_element_by_css_selector('#search_submit')
confirm_btn.click()

driver.switch_to.window(driver.window_handles[1])


comment = []
username = []

nodes = driver.find_elements_by_css_selector('div.card > div.card-feed > div.content')

for i in range(0,len(nodes),1):
    flag = False
    try:
        nodes[i].find_element_by_css_selector("p>a[action-type='fl_unfold']").is_displayed()
        flag = True
    except:
        flag = False

    if (flag and nodes[i].find_element_by_css_selector("p>a[action-type='fl_unfold']").text.startswith('展开c')):
        nodes[i].find_element_by_css_selector("p>a[action-type='fl_unfold']").click()
        comment.append(nodes[i].find_element_by_css_selector('p[node-type="feed_list_content_full"]').text)
    else:
        comment.append(nodes[i].find_element_by_css_selector('p[node-type="feed_list_content"]').text)
    username.append(nodes[i].find_element_by_css_selector("div.info>div:nth-child(2)>a").text)

for page in range(49):
    print(page)
    nextpage_button = driver.find_element_by_link_text('下一页')
    driver.execute_script("arguments[0].click();", nextpage_button)
    wait = WebDriverWait(driver,5)
    nodes1 = driver.find_elements_by_css_selector('div.card > div.card-feed > div.content')
    for i in range(0,len(nodes1),1):
        flag = False
        try:
            nodes1[i].find_element_by_css_selector("p>a[action-type='fl_unfold']").is_displayed()
            flag = True
        except:
            flag = False
        if (flag and nodes1[i].find_element_by_css_selector("p>a[action-type='fl_unfold']").text.startswith('展开c')):
            nodes1[i].find_element_by_css_selector("p>a[action-type='fl_unfold']").click()
            comment.append(nodes1[i].find_element_by_css_selector('p[node-type="feed_list_content_full"]').text)
        else:
            comment.append(nodes1[i].find_element_by_css_selector('p[node-type="feed_list_content"]').text)
        username.append(nodes1[i].find_element_by_css_selector("div.info>div:nth-child(2)>a").text)

data = pd.DataFrame({'username' : username,'comment' : comment})
data.to_excel('dataset.xlsx')
# data.to_csv('dataset.csv')