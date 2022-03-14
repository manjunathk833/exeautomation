import time
import sys
import os
from selenium import webdriver
from tkinter import *
import testrail, os
import creds
from selenium.webdriver.common.by import By

main_window = Tk()

def on_click():
    # print(testurl.get())
    main_window.quit()

#Labels
l = Label(main_window, text="Enter the url you want to test")
l.pack()

#Text Input
testurl = Entry(main_window, width=50, borderwidth=5 )
testurl.pack()

#Button
buttonclick = Button(main_window, height=1, width=10, text="Submit", command=lambda: on_click())
buttonclick.pack()

main_window.mainloop()

turl = testurl.get()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

driver = webdriver.Chrome(resource_path('./driver/chromedriver.exe'))

try:
    driver.get(turl)
    time.sleep(4.0)
    # print(driver.title)
    # driver.find_element(By.LINK_TEXT, 'Form Authentication' )
finally:
    driver.quit()

result1 = False
result2 = False

"""
TestRail integration
"""

def get_testrail_client():
    "Get the TestRail account credentials from the testrail.env file"
    testrail_file = os.path.join(os.path.dirname(__file__), 'creds.py')
    # Get the TestRail Url
    #testrail_url = Conf_Reader.get_value(testrail_file, 'TESTRAIL_URL')
    testrail_url = creds.TESTRAIL_URL
    client = testrail.APIClient(testrail_url)
    # Get and set the TestRail User and Password
    #client.user = Conf_Reader.get_value(testrail_file, 'TESTRAIL_USER')
    client.user = creds.TESTRAIL_USER
    #client.password = Conf_Reader.get_value(testrail_file, 'TESTRAIL_PASSWORD')
    client.password = creds.TESTRAIL_PASSWORD

    return client


def update_testrail(case_id, run_id, result_flag, msg=""):
    "Update TestRail for a given run_id and case_id"
    update_flag = False
    # Get the TestRail client account details
    client = get_testrail_client()

    # Update the result in TestRail using send_post function.
    # Parameters for add_result_for_case is the combination of runid and case id.
    # status_id is 1 for Passed, 2 For Blocked, 4 for Retest and 5 for Failed
    status_id = 1 if result_flag is True else 5
    print('add_result_for_case/%s/%s' % (run_id, case_id))
    if run_id is not None:
        try:
            result = client.send_post(
                'add_result_for_case/%s/%s' % (run_id, case_id),
                {'status_id': status_id, 'comment': msg})
        except Exception as e:
            print('Exception in update_testrail() updating TestRail.')
            print('PYTHON SAYS: ')
            print(e)
        else:
            print('Updated test result for case: %s in test run: %s with msg:%s' % (case_id, run_id, msg))

    return update_flag

'''
def get_project_id(project_name):
    client = get_testrail_client()
    project_id = None
    projects = client.send_get('get_projects')
    for project in projects:
        if project['name'] == project_name:
            project_id = project['id']
            # project_found_flag=True
            break
    print(project_id)
    return project_id

def get_run_id(test_run_name, project_name):
    "Get the run ID using test name and project name"
    run_id = None
    client = get_testrail_client()
    project_id = get_project_id(project_name)
    try:
        test_runs = client.send_get('get_runs/%s' % (project_id))
    except Exception as e:
        print('Exception in update_testrail() updating TestRail.')
        print('PYTHON SAYS: ')
        print(e)
        return None
    else:
        for test_run in test_runs:
            if test_run['name'] == test_run_name:
                run_id = test_run['id']
                break
        return run_id

'''


#Update TestRail
case1_id = 2
case2_id = 1
test_run_id = 3
if result1 or result2 is True:
    msg = "updating for true"
else:
    msg = "updating for false"
update_testrail(case1_id, test_run_id, result1, msg=msg)
update_testrail(case2_id, test_run_id, result2, msg=msg)