from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.service import Service

s = Service("C:\Program Files (x86)\chromedriver.exe")

#PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(service=s)

driver.get("https://www.resultatsendirect.org/home")

temp_url_list = []

def get_sec(time_str):
    """Get seconds from time."""
    m, s, ms = time_str.split(':')
    if m == '' or s == '' or ms == '':
        m = 99
        s = 99
        ms = 999
    return float(m) * 60 + float(s) + float(ms) * 0.001

def get_1500_urls(): # returns list of 1500 times to remove duplicates between this list and 500 list
    elems = driver.find_elements(By.PARTIAL_LINK_TEXT, '1500')
    for element in elems:
        temp_url_list.append(element.get_attribute("href"))
    return temp_url_list

def get_distance_urls(distance): # returns urls of all the distances specified by the user as a list
    url_list = []
    cp_button = driver.find_element(By.CLASS_NAME, 'btn.btn-outline-secondary')
    cp_button.click()

    # national_events_button = driver.find_element(By.ID, 'details-panel10')
    national_events_button = driver.find_element(By.XPATH, "//summary[text()='Événements Nationaux']")
    elite_circuit_button = driver.find_element(By.XPATH, "//summary[text()='Circuit Élite']")
    collegial_circuit_button = driver.find_element(By.XPATH, "//summary[text()='Circuit Collégial']")

    level_of_comp = input("Enter 'a, b, c' for the level of competition you would like the results for "
                          "\na) National \nb) Elite \nc) Collegial \n> ")

    if level_of_comp == 'a':
        national_events_button.click()
        comp = input("Enter 'a, b, c' for the competition you would like the results for \na) Canadian Champs \nb) "
                 "Canadian Juniors \nc) Invitational \n> ")

        if comp == 'a':
            can_champs_button = driver.find_element(By.LINK_TEXT, 'Championnats Canadiens, 14 au 16 octobre 2022, Québec')
            can_champs_button.click()
        elif comp == 'b':
            can_juniors_button = driver.find_element(By.LINK_TEXT, 'Championnats Canadiens Juniors, 25 au 27 novembre 2022, Sherbrooke')
            can_juniors_button.click()
        elif comp == 'c':
            invitational_button = driver.find_element(By.LINK_TEXT, 'Invitation Canadienne, 9 au 11 décembre 2022, Montréal')
            invitational_button.click()
        else:
            input("Enter a valid national event please.")
            output_final_ranking(get_distance_urls(distance), distance)

    elif level_of_comp == 'b':
        elite_circuit_button.click()
        comp = input("Enter 'a' for the competition you would like the results for \na) Elite 1 \n> ")
        if comp == 'a':
            elite1_button = driver.find_element(By.LINK_TEXT, 'Élite #1, 1-2 octobre 2022, Sherbrooke')
            elite1_button.click()
        else:
            input("Enter a valid elite event please.")
            output_final_ranking(get_distance_urls(distance), distance)

    elif level_of_comp == 'c':
        collegial_circuit_button.click()
        comp = input("Enter 'a, b' for the competition you would like the results for \na) Collegiale 1 \nb) Collegiale 2 \n> ")
        if comp == 'a':
            collegiale1_button = driver.find_element(By.LINK_TEXT, 'Collégiale #1, 23 octobre 2022, Sherbrooke')
            collegiale1_button.click()
        elif comp == 'b':
            collegiale2_button = driver.find_element(By.LINK_TEXT, 'Collégiale #2, 19 novembre 2022, Québec')
            collegiale2_button.click()
        else:
            input("Enter a valid elite event please.")
            output_final_ranking(get_distance_urls(distance), distance)
    else:
        input("Enter a valid level of competition please.")
        output_final_ranking(get_distance_urls(distance), distance)

    elems = driver.find_elements(By.PARTIAL_LINK_TEXT, distance)
    for element in elems:
        url_list.append(element.get_attribute("href"))
    #time.sleep(1)
    if distance == '500':
        url_list_1500 = get_1500_urls()
        url_list = set(url_list) - set(url_list_1500)

    temp_list = []
    for url in url_list:
        if '00m' not in url:
            temp_list.append(url)
    return temp_list


def compare_times(dict1, dict2):
    if not bool(dict1): # checks if dict1 is empty
        return dict2
    if not bool(dict2): # checks if dict2 is empty
        return dict1

    if len(dict2) > len(dict1):
        for skater in dict1: # u take keys from shorter list since the keys from longer list will have the fastest time
            if skater not in dict2:
                dict2.update({skater: dict1[skater]})
            if dict2[skater] > dict1[skater]:
                dict2[skater] = dict1[skater]
        return dict2
    else: # if dict2 length is less than or equal to dict1 length
        for skater in dict2:
            if skater not in dict1:
                dict1.update({skater: dict2[skater]})
            if dict1[skater] > dict2[skater]:
                dict1[skater] = dict2[skater]
        return dict1


def rank(url, dictionary):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    heat = soup.find_all('div', attrs={'style': 'background-color:white; width:97%; border:none'}) #gets all of the heats on a page
    for racer in heat:
        racer_results = racer.findAll('span', attrs={'style': 'width: 35%'})  #this is an array of the racers names in a heat
        racer_times = racer.findAll('span', attrs={'style': 'width: 15%; '}) #array of racers' times
        for i in range(len(racer_results)):
            blank = ''
            if racer_times[i].text == blank:
                dictionary.update({''.join([i for i in racer_results[i].text if not i.isdigit()]).lstrip(): 999999})
            else:
                dictionary.update({''.join([i for i in racer_results[i].text if not i.isdigit()]).lstrip(): get_sec(racer_times[i].text.replace(',', ':'))})
            #print(f'{racer_results[i].text.replace(racer_results[i].text[0:4], blank, 1)}, time: {racer_times[i].text}')
    return dictionary


def output_final_ranking(listof_urls, race_distance):
    if race_distance == '500':
        best_times = {}
        for url in listof_urls:
            temp = {}
            best_times = compare_times(best_times, rank(url, temp))
        #print(best_times)
        return best_times

    elif race_distance == '1500':
        best_times = {}
        for url in listof_urls:
            temp = {}
            best_times = compare_times(best_times, rank(url, temp))
        #print(best_times)
        return best_times

    elif race_distance == '1000':
        best_times = {}
        for url in listof_urls:
            temp = {}
            best_times = compare_times(best_times, rank(url, temp))
        #print(best_times)
        return best_times

    else:
        print("enter a valid distance")
        return output_final_ranking(get_distance_urls(race_distance), race_distance)


if __name__ == '__main__':
    race_distance = input("Enter the distance you would like to rank: ")
    final_results = output_final_ranking(get_distance_urls(race_distance), race_distance)

    df = pd.DataFrame(data=final_results, index=[0])
    df = (df.T)
    print(df)
    file_name = input("The results are about to be saved in a file, please name the file: ")
    df.to_excel(f'{file_name}.xlsx')