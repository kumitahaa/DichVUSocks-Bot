# --------------------------------- Import -------------------------------------
import time, pandas as pd, traceback
from datetime import datetime
from selenium import webdriver as uc
# import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import credits

# --------------------------------- Initializing Variables -------------------------------------
driver = ""
line_break = "="*30

EMAIL = credits.EMAIL
PASSWORD = credits.PASSWORD
COLUMNS = ["","","name", "remark", "platform", "username", "cookie", "proxytype", "proxy", "proxyurl", "proxyid", "ip", "countrycode", "ua"]
df = pd.DataFrame(columns=COLUMNS)

ips_list = []
required_ips = 10




# --------------------------------- Add Captcha Solver -------------------------------------
def init():
    global driver
    print(line_break.center(60))
    print("Start of INIT Fucntion...".center(60))
    options = Options()

    options.add_argument("--log-level=3")
    options.add_argument("--disable-logging")
    
    options.add_extension('cap_sol.crx')
    driver = uc.Chrome(options=options)
    driver.maximize_window()
    
    print("Captcha Solver Added")
    time.sleep(2)
    try:
        print("Clicking Extension button")
        driver.find_elements(By.CLASS_NAME, "el-switch__core")[0].click()
        print("Clicked...")
    except:
        print("Can't click extension...")

    try:
        driver.get("chrome-extension://hlifkpholllijblknnmbfagnkjneagid/popup/popup.html#/")
        print("Opened extension page...")
    except:
        print("Can't open extension page...")

    print("End of INIT Fucntion...".center(60))
    print(line_break.center(60))

# --------------------------------- Open Login Page -------------------------------------
def open_login_page():
    print(line_break.center(60))
    print("Start of OPEN_PAGE Fucntion...".center(60))

    url = f"https://dichvusocks.net/login"
    driver.get(url)
    print("WebPage Opened...")

    print("End of OPEN_PAGE Fucntion...".center(60))
    print(line_break.center(60))

# --------------------------------- Check Captcha on Login Page -------------------------------------
def is_captcha_solved():
    print(line_break.center(60))
    print("Start of CAPTCHA_SOLVE_CHECK Function".center(60))

    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID,"l_email")))
    except:
        print("Can't Find Email Address, meaning we are not on Login Page Yet...")
        is_captcha_solved()
        return 0

    try:
        print("waiting 10 seconds")
        time.sleep(10)
        print("Trying to switch to the iFrame...")
        iframe = driver.find_elements(By.TAG_NAME, 'iframe')[1]
        print("got iframe")
        print(iframe.get_attribute("outerHTML"))
        driver.switch_to.frame(iframe)
        print("switched to iframe")
    except:
        print(f"Can't switch to iFrame. Error.")

    try:
        print("Looking for Captcha Checkbox")
        captcha_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "recaptcha-accessible-status")))
        # captcha_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[3]/div[1]/div/div/span")))
        print("Captcha Checkbox...")
        try:
            captcha_solution = captcha_element.get_attribute('aria-checked')
            print(f"Captcha Solution: {captcha_solution}")

            if "fa" in captcha_solution:
                captcha_solution = False
            else:
                captcha_solution = True

            if not captcha_solution:
                print("Captcha has not been solved Yet. Sleeping for 10 secconds")
                time.sleep(10)
                is_captcha_solved()
                return 0
            elif captcha_solution:
                print("Captcha has been solved")
                print("End of CAPTCHA_SOLVE_CHECK Function")
                print(line_break.center(60))
                return True
        except:
            print("Can't Get Aria-Attribute of Captcha CheckBox...")
    except:
        print("Can't Find the CheckBox for Captcha...")
        print("            =================================================================            ")
        print("<<========= Select Me to Pause the bot to complete Captcha if still remaining =========>>")
        print("            =================================================================            ")
        time.sleep(15)
        driver.switch_to.default_content()

    try:
        driver.switch_to.default_content()
    except:
        print("Erorr switching back... Error")

    print("End of CAPTCHA_SOLVE_CHECK Function".center(60))
    print(line_break.center(60))

# --------------------------------- Login Function -------------------------------------
def login():
    print(line_break.center(60))
    print("Start of LOGIN function".center(60))
    try:
        email_field = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID,"l_email")))
        password_field = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "l_password")))
        # login_btn = driver.find_element(By.ID,"auth_button_continue")
        try:
            email_field.clear()
            password_field.clear()

            email_field.send_keys(EMAIL)
            password_field.send_keys(PASSWORD)

            password_field.send_keys(Keys.ENTER)
            # login_btn.click()
            
        except:
            print("Error while sending keys to Email and Password`")
    except:
        print("Can't find Email/Password Fields...")
    
    if is_logged_in:
        pass
    else:
        print("IS_LOGGED_IN is False... Trying again")
        login()

    print("End of LOGIN function".center(60))
    print(line_break.center(60))

# --------------------------------- Logged In Checker -------------------------------------
def is_logged_in():
    print(line_break.center(60))
    print("Start of IS_LOGGED_IN function.".center(60))
    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID,"l_email")))
        print("Email Found in LoginChecker Function...")
        
        print(line_break.center(60))
        print("End of IS_LOGGED_IN function.")
        return False
    except:
        print("Email not Found in LoginChecker Function")
        
        print(line_break.center(60))
        print("End of IS_LOGGED_IN function.".center(60))
        return True

# --------------------------------- Open IP Page -------------------------------------
def open_sock_list():
    url = "https://dichvusocks.net/sockslist"
    driver.get(url)
    print(line_break.center(60))
    print("Opened Socks List Page".center(60))
    print(line_break.center(60))

# --------------------------------- Starts from Here -------------------------------------
def start():
    print(line_break.center(60))
    print("Start of START Fucntion...".center(60))
    
    is_ip_page()
    remove_blacklisted()

    try:
        all_pages_list = WebDriverWait(driver, 7).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "uk-first-column")))
        total_pages = all_pages_list[3].text.split(" ")[-1]
        print(f"total_pages == {total_pages}")
        try:
            total_pages = int(total_pages)
        except:
            print("Total Pages can't be changed to INT")
    except:
        print("Can't find total pages...")
    
    for i in range(total_pages):
        if len(ips_list) > required_ips:
            print(f"""{line_break}
                  Got 10 IPs in total, quitting now...
                  {line_break}""")
            break

        total_rows()
        # all_pages_list[3].text.split(" ")[-1]
        next_page()
    
    print("End of START Fucntion...".center(60))
    print(line_break.center(60))

# --------------------------------- Check Page of IPs presence -------------------------------------
def is_ip_page():
    print(line_break.center(60))
    print("Start of IS_IP_PAGE function".center(60))
    try:
        WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.ID, "totalView")))
        print("This is IP Page...")
    except:
        print("IP Page not found...")

    print("End of IS_IP_PAGE function".center(60))
    print(line_break.center(60))

# --------------------------------- Remove Blacklisted Results -------------------------------------
def remove_unwanted_results():
    print(line_break.center(60))
    print("Start Remove Blacklisted Results...".center(60))
    try:
        time.sleep(4)
        print("Trying to remove")
        driver.execute_script("""

var rows = document.querySelectorAll("tr[id^='socks_']");

rows.forEach(function(row) {                  
    var cells = row.getElementsByTagName("td");
    if (cells.length > 1) {
        var secondLastCell = cells[cells.length - 3];
        if (secondLastCell.textContent.trim() === "Yes") {
            row.remove();
                                                            }
                            }
                            }
            );


rows.forEach(function(row) {
      var cells = row.getElementsByTagName("td");
      if (cells.length > 1) {
          var secondCell = cells[1];
          if (secondCell.textContent.trim() != "United States") {
              row.remove();
                                                               }
                            }
                            }
                ); 

rows.forEach(function(row) {
      var cells = row.getElementsByTagName("td");
      if (cells.length > 1) {
          var lastCell = cells[cells.length - 1];
          if (lastCell.textContent.trim() != "Residential") {
              row.remove();
                                                              }
                            }
                            }
                );
                                          """)
    except:
        print(f"Error while removing blacklisted: Error")
    
    time.sleep(2)
    print("End of Blacklisted Results Removing".center(60))
    print(line_break.center(60))

# --------------------------------- Remove Blacklisted Results -------------------------------------
def remove_blacklisted():
    print(line_break.center(60))
    print("Start Remove Blacklisted Results...".center(60))
    try:
        time.sleep(4)
        print("Trying to remove")
        driver.execute_script("""

document.getElementById("useType").value = "Residential";
document.getElementById("search_country").value = "United States";
document.getElementById("search_YN").value = "No";
document.getElementsByClassName("sockslist__card__btnP sockslist__card__btnP--c1 uk-button uk-button-default uk-button-small")[0].click();
                                          """)
    except:
        print(f"Error while removing blacklisted: Error")
    
    time.sleep(2)
    print("End of Blacklisted Results Removing".center(60))
    print(line_break.center(60))

# --------------------------------- Next Page of Results -------------------------------------
def next_page():
    print(line_break.center(60))
    print("Start of NEXT_PAGE function".center(60))

    time.sleep(2)
    try:
        print("Getting Next Page's Anchor tag")
        next_page_btn = driver.execute_script("""return document.getElementsByClassName("page_item")[11].getElementsByTagName("a")[0]""")
    except:
        print("Did not get next page...")
    try:
        next_page_btn.click()
    except:
        print("Can't Click Next Page button...")
    # except:
    #     print("Can't Find Next Page button...")

    time.sleep(5)
    print("End of NEXT_PAGE function".center(60))
    print(line_break.center(60))

# --------------------------------- Reveal IPs from the page -------------------------------------
def reveal_ips(rows):
    print(line_break.center(60))
    print("Start of REVEAL_IPs Function".center(60))

    i = 0
    for row in rows:
        if i+len(ips_list) > required_ips:
            print("Revealed enough IPs")
            break
        i+=1
        try:
            ip_field = row.find_elements(By.TAG_NAME, "td")[0].find_elements(By.TAG_NAME, "a")[0]
            try:
                ip_field.click()
                time.sleep(4)
                print(f"Clicked {i}th IP")
            except:
                print(f"Can't Click IP# {i}")
        except:
            print(f"Can't find IP field for row# {i}")
    
    print("End of REVEAL_IPs Function".center(60))
    print(line_break.center(60))

# --------------------------------- Scrape the IPs from the page -------------------------------------
def scrape_ips(rows):
    global ips_list
    global df
    print(line_break.center(60))
    print("Start of SCRAPE_IPs Function".center(60))

    i = 0
    for row in rows:
        if len(ips_list) > required_ips:
            print(f"""{line_break}
                  Got 10 IPs in total, quitting now...
                  {line_break}""")
            break

        i+=1
        try:
            ip_field = row.find_elements(By.TAG_NAME, "td")[0]
            try:
                ip = ip_field.text
                if ip:
                    if "sorry" not in ip:
                        if "offline" not in ip:
                            if "*" not in ip:
                                ips_list.append(ip)
                                print(f"{i}th IP is : {ip}")
            except:
                print(f"Can't find IP# {i}")
        except:
            print(f"Can't find IP field for row# {i}")
    
    print("End of SCRAPE_IPs Function".center(60))
    print(line_break.center(60))

# --------------------------------- Find total results on screen -------------------------------------
def total_rows():
    print(line_break.center(60))
    print("Start of TOTAL_ROWS Function".center(60))
    try:
        table = driver.execute_script("""return document.getElementsByClassName("sockslist__table uk-table uk-table-small uk-table-divider")[0];""")
        print("Got Table...")
        try:
            rows = table.find_elements(By.TAG_NAME, 'tr')
            rows.pop(0)
            print(f"Total Rows in this Results are: {len(rows)}")
            time.sleep(5)
            reveal_ips(rows)
            scrape_ips(rows)
        except:
            print("Can't Extract Rows from Table")
    except:
        print("Can't Find Table...")
    
    print("End of TOTAL_ROWS Function".center(60))
    print(line_break.center(60))



# ------------------------------------ Driver Function drives the flow ---------------------------------
def driver():
    init()
    open_login_page()
    is_captcha_solved()
    login()
    open_sock_list()
    start()
    

# ================================== Main function for TRY-FINALLY ==================================
def main():
    try:
        driver()
    except Exception as e:
        print('"Except Block" of driver()')
        print(e)
        traceback.print_exc()
    else:
        print('"Else Block" of driver()')
    finally:
        df["proxy"] = ips_list
        df["proxytype"] = "Socks5"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        df.to_excel(f"Kumi_T._{timestamp}.xlsx", index=False)

        print("Quitting browser...")
        driver.quit()


# ================================== Start Call ==================================
main()