from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

import time

# Ensure Chrome driver in Python folder

driver = webdriver.Chrome()

def login(userId, password):
	driver.get("https://www.medi-cal.ca.gov/Eligibility/Login.asp")
	user = driver.find_element_by_id("UserID")
	user.send_keys(userId)
	pwd = driver.find_element_by_id("UserPW")
	pwd.send_keys(password)
	submit = driver.find_element_by_id("cmdSubmit")
	submit.click()
	#wait for page load
	loggedIn = False	
	try:
		element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "tabpanel_1")))
		loggedIn = True
	except:
		pass	
	return loggedIn
	
def gotoClaimsPage():
	driver.get("https://www.medi-cal.ca.gov/Eligibility/ClaimStatus.asp")
	#wait for page load
	loaded = False	
	try:
		element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "RecipDOS")))
		loaded = True
	except:
		pass	
	return loaded
	
def fillAndSubmit(subscriberID, dosFrom, dosTo):
	recipID = driver.find_element_by_id("RecipID")
	recipID.send_keys(subscriberID)
	dosF = driver.find_element_by_id("RecipDOS")
	dosF.send_keys(dosFrom)
	#dosT = driver.find_element_by_id("RecipDOSTo")
	#dosT.send_keys(dosTo)
	submit = driver.find_element_by_name("Submit")
	submit.click()
	#wait for page load
	loaded = False	
	try:
		element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "ClaimStatusResp")))
		loaded = True
	except:
		pass	
	return loaded
	
def downloadPage(path):
	content = driver.page_source
	with open(path, 'w') as f:
		f.write(content)
	return f.closed

if login(12345,12345):
	if gotoClaimsPage():
		if fillAndSubmit('20170500079901','11/23/2017',''):
			if downloadPage('test123.html'):
				print('done')
				driver.close()
			else:
				print('Download error')
		else:
			print('Fill and submit error')
	else:
		print('Claims page error')
else:
	print('Login error')
	
