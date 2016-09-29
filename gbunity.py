'''
Daniel Marcos -- 2016
UniT2 Combines scrapes TSquare to generate a combined gradebook of
all your current classes 

'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Replace with your own
USERNAME = ""
PASSWORD = ""
CHROME_PATH = "/home/danielms/Development/UniT2/chromedriver"
browser = webdriver.Chrome(executable_path = CHROME_PATH)

def loginToT2(username, password):
	# Navigate to the main page and click on login button
	url = "https://t-square.gatech.edu/portal"
	browser.get(url)
	browser.find_element_by_id('loginLink1').click()

	# Wait for page to load
	try:
		element = WebDriverWait(browser, 5).until(
			EC.presence_of_element_located((By.NAME, "username"))
		)
	except TimeoutException:
		print "Loading took too long fam"

	# Make sure username and password are empty
	browser.find_element_by_name("username").clear()
	browser.find_element_by_name("password").clear()
	# Enter my username and password, log in 
	browser.find_element_by_name("username").send_keys(username)
	browser.find_element_by_name("password").send_keys(password)
	browser.find_element_by_name('submit').click()


'''
You must be logged into T2 to get current classes
Returns a list of links to each class site for the current term.
'''
def getCurrentClasses():
	# Find list of active sites
	try:
		element = WebDriverWait(browser, 5).until(
			EC.presence_of_element_located((By.ID, "siteLinkList"))
			)
	except TimeoutException:
		print "Loading too hella long fam"

	# Clicks on "Active Sites"
	browser.execute_script("return dhtml_more_tabs();")
	# Selects the current term
	terms = []
	terms = browser.find_elements_by_class_name('termContainer')
	currentTerm = terms[0]
	# Finds all the lnks under the current term
	classes = currentTerm.find_elements_by_tag_name('a')
	classLinks = []
	for c in classes:
		classLinks.append(c.get_attribute("href"))

	return classLinks


def processGradebooks(classLinks):
	for link in classLinks:
		browser.get(link)
		toolMenu = browser.find_element_by_id("toolMenu")
		for elem in toolMenu.find_elements_by_tag_name("a"):
			if elem.get_attribute("class") == "icon-sakai-gradebook-tool ":
				browser.get(elem.get_attribute("href"))
				# Here we are looking at one Gradebook
				processTable()
				break

def processTable():
	# First we have to find the table. It has a class="listHier wideTable lines"
	iframe = browser.find_elements_by_tag_name('iframe')[0]
	browser.switch_to_frame(iframe)
	gbTable = None
	for t in browser.find_elements_by_tag_name("table"):
		if t.get_attribute("class") == "listHier wideTable lines":
			gbTable = t
	if gbTable:
		rows = browser.find_elements_by_tag_name("tr")
		# TODO(danielms215): Go through each row, get title and grad

	#TODO(danielms215): Switch to default content

def createCombinedGradebook():
	loginToT2(USERNAME, PASSWORD)
	processGradebooks(getCurrentClasses())

if __name__ == '__main__':
	if (USERNAME == "" and PASSWORD == ""):
		USERNAME = raw_input("Enter your GT Username: ") 
		PASSWORD = raw_input("Enter your password: ")
	
	createCombinedGradebook()
