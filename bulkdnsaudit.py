from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests  
import pandas as pd

#AUDIT DNS CLUSTER 1 per 1
#file source audit all whm server

user = "isikan usermu"
passwd = "isikan passwordmu"
lokasi = "scripts7/clusterstatus"

print("\n==============================")
print("=  BULK DNS CLUSTER AUDITOR  =")
print("==============kuliOnline0011==")
    
def nggoleki():    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    chrome_driver = '/chromedriver_win32'
    driver = webdriver.Chrome(chrome_driver, options=options)
    driver.get(url6)
    time.sleep(1)

    ngetik = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[3]/div/div/div[2]/div[2]/form/div[2]/input')
    ngetik.send_keys(user)

    ngetik = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[3]/div/div/div[2]/div[2]/form/div[4]/input')    
    ngetik.send_keys(passwd)

    ngetik = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[3]/div/div/div[2]/div[2]/form/div[5]/div/button')
    ngetik.click()
    time.sleep(1)

    ngetik = driver.current_url
    time.sleep(1)
    gm = ngetik.count("/")
    
    if gm <= 4:
        parseurl = urlparse(ngetik)
        urlterfilter = parseurl.scheme + "://" + parseurl.netloc + parseurl.path
    else:
        akhir_gm = ngetik.rindex("/")
        urlterfilter = ngetik[:akhir_gm - 8]
    urlbaru = urlterfilter + lokasi
    time.sleep(1)
    driver.get(urlbaru)

    halaman = driver.page_source
    soup = BeautifulSoup(halaman, "html.parser")
    td_elem = soup.find_all("td", class_="serverstatus")

    hiterror = 0

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    for td in td_elem:
        elemen = td.find("img")
        if elemen["title"] != "Server Active":
            hiterror += 1

    if hiterror == 0:
        print(f"\n{subdomain}")
        print("NORMAL\n")
    else:
        print(f"\n{hiterror} ERROR\n")

a = 0
data = pd.read_csv('Audit_dnscluster.csv')
diulang = data.shape[0]
for i in range(diulang):
    print("Bulk Audit DNS Cluster ke ",i+1)
    alamat = data.iloc[i]['target']
    if pd.notnull(alamat):
        url_list = alamat.split(',')
        for url in url_list:
            url = url.strip()
            url2 = "http://" + url + ":2087/"
            url3 = "https://" + url + ":2087/"
            url4 = "http://" + url + "/whm"
            url5 = "https://" + url + "/whm"
            subdomain = url.split('.')[0].upper()
            
            try:
                sc = requests.get(url2)
                if sc.status_code == 200 :
                    url6 = url2
                    nggoleki()
                else:
                    cek2 = url3
                    sc = requests.get(cek2)
                    if sc.status_code == 200 :
                        url6 = url3
                        nggoleki()
                    else:
                        cek3 = url4
                        sc = requests.get(cek3)
                        if sc.status_code == 200 :
                            url6 = url4
                            nggoleki()
                        else:
                            cek4 = url5
                            sc = requests.get(cek4)
                            if sc.status_code == 200 :
                                url6 = url5
                                nggoleki()
            except requests.exceptions.ConnectionError:
                print(f"\n{subdomain}")
                print("SERVER NONAKTIF\n")
    continue
