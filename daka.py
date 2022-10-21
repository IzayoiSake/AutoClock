from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from DingRobot import dingpush
import argparse
import datetime
import time
import os

class AutoDaka:
    def __init__(self, args):
        self.url = args.url
        self.username = args.username  
        self.password = args.password
        self.latitude = args.latitude
        self.longitude = args.longitude
        self.DD_BOT_TOKEN = args.DD_BOT_TOKEN
        self.DD_BOT_SECRET = args.DD_BOT_SECRET

    def init_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-infobars") # 禁用浏览器正在受到自动化软件的控制的提示

        if args.headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('window-size=1920x1080')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--hide-scrollbars')
        if args.proxy:
            chrome_options.add_argument(f'--proxy-server={args.proxy-server}')  

        driver = webdriver.Chrome(options=chrome_options)
        try:
            driver.get(self.url)
        except WebDriverException:
            print("page down")
        driver.maximize_window()

        return driver

    def login(self, driver):
        print("\n[Time] %s" %
              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print("🚌 打卡任务启动")

        username_input = driver.find_element(by=By.ID, value="username")
        password_input = driver.find_element(by=By.ID, value="password")
        login_button = driver.find_element(by=By.ID, value="dl")

        print("登录到浙大统一身份认证平台...")

        try:
            username_input.send_keys(self.username)
            password_input.send_keys(self.password)
            print("已登录到浙大统一身份认证平台")
            login_button.click()
            time.sleep(1)
        except Exception as err:
            print(str(err))
            raise Exception
    
    def click_by_xpath(self, driver, form, xpath, submit=False):
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        except Exception as err:
            print(f'write {form} Information wrong...')
        else:
            if submit:
                print('submit success...')
            else:
                print(f'write {form} Information success...')
        time.sleep(1)

    def daka(self, driver):
        print("打卡任务启动...")
        print("正在获得虚拟地理位置信息...")

        # 获取虚拟地理位置信息
        driver.execute_cdp_cmd(
            "Browser.grantPermissions",  # 授权地理位置信息
            {
                "origin": self.url,
                "permissions": ["geolocation"]
            },
        )

        driver.execute_cdp_cmd(
            "Emulation.setGeolocationOverride",  # 虚拟位置信息
            {
                "latitude": self.latitude,
                "longitude": self.longitude,
                "accuracy": args.accuracy
            },
        )

        time.sleep(2)  # 等待位置信息
        # 需要提交的表单
        forms = {'inSchool': '/html/body/div[1]/div[1]/div/section/div[4]/ul/li[4]/div/div/div[1]/span[1]', # on campus 
                 'roomMate': '/html/body/div[1]/div[1]/div/section/div[4]/ul/li[7]/div/div/div[2]/span[1]',  # people living with you
                 'inPractice': '/html/body/div[1]/div[1]/div/section/div[4]/ul/li[8]/div/div/div[3]/span[1]', # internship 
                 'location': '/html/body/div[1]/div[1]/div/section/div[4]/ul/li[11]/div/input', # location
                 'commit': '/html/body/div[1]/div[1]/div/section/div[4]/ul/li[28]/div/div/div/span[1]', # commit 
                 }

<<<<<<< HEAD
        for form in forms:
            self.click_by_xpath(driver, form, forms[form])

        print("表单信息填写成功，正在提交表单...")
        time.sleep(1)

        # 提交表单
        submit_xpath = '/html/body/div[1]/div[1]/div/section/div[5]/div/a'
        self.click_by_xpath(driver, 'submit', submit_xpath, submit=True)
=======
        print("在校信息填写中...")
        # 是否在校
        try:
            inSchool = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/section/div[4]/ul/li[4]/div/div/div[1]/span[1]")))
            inSchool.click()
        except Exception as error:
            print('write inSchool Information wrong...\n', error)
        time.sleep(1)

        # 是否在实习
        print("实习信息填写中...")
        try:
            inPractice =  WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/section/div[4]/ul/li[7]/div/div/div[3]/span[1]")))
            inPractice.click()
            print("实习信息已提交")
        except Exception as error:
            print('write inPractice Information wrong...\n', error)
        
        #print("基本信息填写中...")
        print("在校信息填写中...")
        # 是否在校
        try:
            inSchool=driver.find_element(by=By.NAME,value="sfzx")
            inSchoolOption=inSchool.find_element(by=By.TAG_NAME, value="div").find_elements(by=By.TAG_NAME, value="div")
            inSchoolYes=WebDriverWait(driver, 10).until(EC.element_to_be_clickable(inSchoolOption[0]))
            inSchoolYes.click()
            Campus=driver.find_element(by=By.NAME,value="campus")
            CampusOption=Campus.find_element(by=By.TAG_NAME, value="div").find_elements(by=By.TAG_NAME, value="div")
            CampusYuquan=WebDriverWait(driver, 10).until(EC.element_to_be_clickable(CampusOption[1]))
            CampusYuquan.click()
            
        except Exception as error:
            print("在校信息填写异常\n", error)
        time.sleep(1)

        # 是否在实习
        print("实习信息填写中...")
        try:
            internship=driver.find_element(by=By.NAME,value="internship")
            internshipOption=internship.find_element(by=By.TAG_NAME, value="div").find_elements(by=By.TAG_NAME, value="div")
            internshipNo=WebDriverWait(driver, 10).until(EC.element_to_be_clickable(internshipOption[2]))
            internshipNo.click()
            print("实习信息已提交")
        except Exception as error:
            print("实习信息填写异常\n", error)
        time.sleep(1)

        # 位置填写
        print("位置信息填写中...")

        try:  # 提交位置信息
            area_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[1]/div[1]/div/section/div[4]/ul/li[10]/div/input"))
            )
            area_element.click()
            print("地理位置信息已提交")
        except Exception as error:
            print("地理位置信息填写异常\n", error)

        time.sleep(3)

        #健康码信息
        print("健康码信息填写中...")

        try:  # 提交健康码信息
            HealthCode=driver.find_element(by=By.NAME,value="sqhzjkkys")
            HealthCodeOption=HealthCode.find_element(by=By.TAG_NAME, value="div").find_elements(by=By.TAG_NAME, value="div")
            GreenCode=WebDriverWait(driver, 10).until(EC.element_to_be_clickable(HealthCodeOption[0]))
            GreenCode.click()
            print("健康码信息填写已提交")
        except Exception as error:
            print("健康码信息填写异常\n", error)



        #同住人员信息
        print("同住人员信息填写中...")

        try:  # 提交同住人员信息
            RoomMate=driver.find_element(by=By.NAME,value="sfymqjczrj")
            RoomMateOption=RoomMate.find_element(by=By.TAG_NAME, value="div").find_elements(by=By.TAG_NAME, value="div")
            # 在RoomMateOption中寻找元素<span>否 No</span>
            RoomMateNo=WebDriverWait(driver, 10).until(EC.element_to_be_clickable(RoomMateOption[1]))
            RoomMateNo.click()
            print("同住人员信息填写已提交")
        except Exception as error:
            print("同住人员信息填写异常\n", error)

        time.sleep(3)
        
        # 本人承诺
        try:
            Commit=driver.find_element(by=By.NAME,value="sfqrxxss")
            CommitYes=Commit.find_element(by=By.TAG_NAME, value="div").find_element(by=By.TAG_NAME, value="div")
            CommitYes.click()
        except Exception as error:
            print("承诺失败\n", error)

        time.sleep(1)
        
        # 提交信息
        driver.find_element(by=By.XPATH, 
                            value="/html/body/div[1]/div[1]/div/section/div[5]/div/a").click()

>>>>>>> parent of 1fba632 ('填写地理位置'等项的路径依赖修改为类名称依赖)
        time.sleep(2)

        # 弹出的确认提交窗口，点击确定
        try:
            # 寻找<div class="wapcf-btn wapcf-btn-ok">确认提交</div>的按钮
            submit=driver.find_element(by=By.ID, value="wapcf")
            submit=submit.find_element(by=By.CLASS_NAME, value="wapcf-inner")
            submitTitle=submit.find_element(by=By.CLASS_NAME, value="wapcf-title")
            if submitTitle.text=="每天只能填报一次，请确认信息是否全部正确？":
                submit=submit.find_element(by=By.CLASS_NAME, value="wapcf-btn-box")
                submit=submit.find_element(by=By.CLASS_NAME, value="wapcf-btn-ok")
                submit = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable(submit))
            submit.click()
            print("确认提交...")
            self.Reminder("今天的打卡完成了🚌，耶！")
        except:
            try:
                # 寻找<div class="wapat-title">每天只能填报一次，你已提交过</div>的按钮
                HaveSubmitted=driver.find_element(by=By.CLASS_NAME, value="wapat-title")
                print('您今天已提交过了...')
                self.Reminder("您今天已提交过")
            except Exception as error:
                print('提交失败...')
                # self.Reminder("提交失败,请手动填写或检查代码仓库更新情况")

        time.sleep(1)
    
    def Reminder(self, content):
        if self.DD_BOT_TOKEN:
            ding= dingpush('浙江大学每日健康打卡小助手', content, self.DD_BOT_TOKEN,self.DD_BOT_SECRET)
            ding.SelectAndPush()
        else:
            print("钉钉推送未配置，请自行查看签到结果")
        print("推送完成！")

    def run(self):
        driver = self.init_driver()
        self.login(driver)
        self.daka(driver)
        driver.close()
        print("打卡完成")

def get_parser():
    user_name = os.getenv("account")
    password = os.getenv("password")
    token = os.getenv("DD_BOT_TOKEN")
    secret = os.getenv("DD_BOT_SECRET")
    url = 'https://healthreport.zju.edu.cn/ncov/wap/default/index'
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', default=user_name, help='浙江大学统一身份认证平台用户名')
    parser.add_argument('--password', default=password, help='浙江大学统一身份认证平台密码')
    parser.add_argument('--latitude', type=float ,default=30.27, help='虚拟地理位置纬度, 默认为杭州市西湖区浙江大学')
    parser.add_argument('--longitude', type=float, default=120.13, help='虚拟地理位置经度')
    parser.add_argument('--accuracy', default=50, help='虚拟地理位置精度')
    parser.add_argument('--url', type=str, default=url, help='浙江大学统一身份认证平台地址')
    parser.add_argument('--headless', type=bool, default=True, help='是否开启无头模式')
    parser.add_argument('--proxy', type=bool, default=False, help='是否使用代理')
    parser.add_argument('--proxy-server', type=str, help='代理服务器地址 (e.g. http://')
    parser.add_argument('--DD_BOT_TOKEN', type=str, default=token, help='钉钉机器人token')
    parser.add_argument('--DD_BOT_SECRET', type=str, default=secret, help='钉钉机器人secret')
    return parser

def print_arguments(args):
    print("---------------------  Configuration Arguments ---------------------")
    for arg, value in sorted(vars(args).items()):
        print("%s: %s" % (arg, value))
    print("--------------------------------------------------------------------")

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    print_arguments(args)
    daka = AutoDaka(args)
    daka.run()
