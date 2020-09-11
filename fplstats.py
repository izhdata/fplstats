from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import csv
import time

# Open up Firefox and go to stats page
driver = webdriver.Firefox()
driver.implicitly_wait(3)
driver.get("https://fantasy.premierleague.com/statistics")

# Create header row for our CSV
header_row = ["Name", "Position", "Club", "Price",
              "Season", "Points", "Minutes played",
              "Goals scored", "Assists", "Clean sheets",
              "Goals conceded", "Own goals", "Penalties saved",
              "Penalties missed", "Yellow cards", "Red cards",
              "Saves", "Bonus", "Bonus Points System", "Influence",
              "Creativity", "Threat", "ICT Index",
              "Price at start of season", "Price at end of season"]
with open('fplstats.csv', 'a', newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header_row)

#Grab final page number (Page 1 of 18)
page_num_text = driver.find_element_by_xpath("/html/body/main/div/div[2]/div/div/div[3]/div")
final_page_num = page_num_text.text.split()[-1]

# Do this for all pages    
for x in range(int(final_page_num)):
    
    #page_num_text = driver.find_element_by_xpath("/html/body/main/div/div[2]/div/div/div/div")
    
    print("Processing page: ", page_num_text.text)

    players_table = driver.find_element_by_xpath("/html/body/main/div/div[2]/div/div/table/tbody")
    players = players_table.find_elements_by_css_selector('tr')
    num_players = len(players)
    #Do this for each player on page
    for i in range(num_players):
        xpath_str = "/html/body/main/div/div[2]/div/div/table/tbody/tr[" + str(i+1) + "]/td[1]/button"
        driver.find_element_by_xpath(xpath_str).click() # Click info button for current player
        # Some player info pages contain div sections for injuries and suspensions, this if/else bit handles the extra div tags
        extra_divs=driver.find_elements_by_xpath("/html/body/div/div/dialog/div/div[2]/div[2]/div/div/div[1]/h2")
        if not extra_divs:
            player_name = driver.find_element_by_xpath("/html/body/div/div/dialog/div/div[2]/div[1]/div/div/div[1]/h2")
            player_position = driver.find_element_by_xpath("/html/body/div/div/dialog/div/div[2]/div[1]/div/div/div[1]/span")
            player_club = driver.find_element_by_xpath("/html/body/div/div/dialog/div/div[2]/div[1]/div/div/div[1]/div")
            player_price = driver.find_element_by_xpath("/html/body/div/div/dialog/div/div[2]/div[1]/ul[1]/li[4]/div")
            try:
                player_stats = driver.find_element_by_xpath("/html/body/div/div/dialog/div/div[2]/div[2]/div/div/div[3]/div/table/tbody")
            except NoSuchElementException:
                player_stats = []
        else:
            player_name = driver.find_element_by_xpath("/html/body/div/div/dialog/div/div[2]/div[2]/div/div/div[1]/h2")
            player_position = driver.find_element_by_xpath("/html/body/div/div/dialog/div/div[2]/div[2]/div/div/div[1]/span")
            player_club = driver.find_element_by_xpath("/html/body/div/div/dialog/div/div[2]/div[2]/div/div/div[1]/div")
            player_price = driver.find_element_by_xpath("/html/body/div/div/dialog/div/div[2]/div[2]/ul[1]/li[4]/div")
            try:
                player_stats = driver.find_element_by_xpath("/html/body/div/div/dialog/div/div[2]/div[3]/div/div/div[3]/div/table/tbody")
            except NoSuchElementException:
                player_stats = []
        player = [player_name.text, player_position.text, player_club.text, player_price.text]
        #print(player)
        with open('fplstats.csv', 'a', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            # Include previous season stats if available, otherwise just output player details
            if not player_stats:
                writer.writerow(player)
            else:
                if len(player_stats.text) > 0:  
                    for row in player_stats.find_elements_by_css_selector('tr'):
                        player_data = [d.text for d in row.find_elements_by_css_selector('td')]
                        player_output = player + player_data
                        writer.writerow(player_output)
                else:
                    writer.writerow(player)
                
        driver.find_element_by_xpath("/html/body/div/div/dialog/div/div[1]/div/button").click() # Close the info page

    driver.find_element_by_xpath("/html/body/main/div/div[2]/div/div/div/button[3]").click() # Click next page button
    time.sleep(5) # Wait for page to load 

# All done, close the browser
driver.close()
