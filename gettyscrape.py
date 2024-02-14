from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from bs4 importBS4 as BS4
import os
import tkinter as tk
from tkinter import filedialog
import time

def videoscrape():    
    try:
        chromeOptions = webdriver.ChromeOptions()
        prefs = {"download.default_directory": scrape_directory}
        chromeOptions.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=chromeOptions)
        driver.maximize_window()
        container_window_handle = None
        while not container_window_handle:
            container_window_handle = driver.current_window_handle
        for i in range(1, searchPage + 1):
            url = "https://www.gettyimages.com/videos/" + searchTerm + "?page=" + str(i)
            driver.get(url)
            print("Page " + str(i))
            for j in range(0, 100):
                while True:
                    container = driver.find_elements_by_xpath("//article[@gi-asset='" + str(j) + "']")
                    if len(container) != 0:
                        break
                    if len(driver.find_elements_by_xpath("//article[@gi-asset='" + str(j + 1) + "']")) == 0 and i == searchPage:
                        driver.close()
                        return
                    time.sleep(10)
                    driver.get(url)
                    print(str(j))
                section = container[0].find_element_by_xpath(".//section[@class='image-section']")
                link = section.find_element_by_xpath(".//a[@class='search-result-asset-link']")
                video_url = link.get_attribute("href")
                driver.get(video_url)
                
                while True:
                    wait = WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.XPATH, "//video[@autoplay='true']")))
                    data = driver.execute_script("return document.documentElement.outerHTML")
                    scraper =BS4(data, "lxml")
                    video_container = scraper.find_all("video", {"autoplay": "true"})
                    if len(video_container) != 0:
                        break
                    time.sleep(10)
                    driver.get(video_url)
                video_src = video_container[0].get("src")
                name = video_src.rsplit("/", 1)[-1]
                
                try:
                    driver.get(video_src + "?p=1")
                    print("Scraped " + name)
                except Exception as e:
                    print(e)
                driver.get(url)
    except Exception as e:
        print(e)

print("GettyScrape v1.1")

scrape_directory = ""

while True:
    while True:
        print("Please select a directory to save your scraped files.")
        scrape_directory = filedialog.askdirectory()
        if scrape_directory == "":
            print("You must select a directory to save your scraped files.")
            continue
        break
    searchCount = int(input("Number of search terms: "))
    if searchCount < 1:
        print("You must have at least one search term.")
        continue
    searchTerm = input("Enter search term(s) separated by space: ")
    searchPage = int(input("Number of pages to scrape: "))
    if searchPage < 1:
        print("You must scrape at least one page.")
        continue

    videoscrape()

    print("Scraping complete.")
    restartScrape = input("Keep scraping? ('y' for yes or 'n' for no) ")
    if restartScrape.lower() == "n":
        print("Scraping ended.")
        break
