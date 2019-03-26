# -*- coding:utf-8 -*-

import os
import json
import sys
import createJson

execCommand = "curl --basic --user %s"
path = "existTestCycle.json"
folderDirectory = "./jira_new"

# get all test cases in specific test cycle and generate one case list
def readJsonFile(path, testCycle):
    command = "curl --basic --user luckylyw19930104:031118luckylyw -X GET http://localhost:8080/rest/atm/latest/testrun/" + testCycle
    os.system(command + " > " + path)
    with open(path, "r") as j:
        data = json.load(j)
    #print(data['items'])
    testCaseKeyList = []
    # get all test case key from get
    for i in range(0, len(data['items']), 1):
        testCaseKeyList.append(data['items'][i]['testCaseKey'])
    if len(testCaseKeyList):
        return testCaseKeyList
    else:
        testCaseKeyList = ["no file in this list"]
        return testCaseKeyList

# update the status and fields in existing test case
def updateTestCase(testCaseKeyList, List, testCycle):
    # get each test case key in specific test cycle now
    #print(testCaseKeyList)
    #print List
    middleList = []
    for testCase in testCaseKeyList:
            # get dictory from dictory list and find one match test case key from cycle
            for list in List:
                if list['testCaseKey'] == testCase:
                    middleList.append(testCase)
                    httpMethod = "-X PUT"
                    execUpdate(testCase, list, httpMethod, testCycle)
    #print middleList
    diffList = sortlist(middleList, List)
    if diffList == None:
       print("Can not find new test case to update")
    else:
        for l in diffList:
            for list in List:
                if list['testCaseKey'] == l:
                    httpMethod = "-X POST"
                    execUpdate(testCase, list, httpMethod, testCycle)

# exec update command to update test case in specific cycle
def execUpdate(testCase, list, httpMethod, testCycle):
    os.system("pwd")
    command = "curl --basic --user luckylyw19930104:031118luckylyw -H Content-Type:application/json --data @jira/updateCycle.json "
    updateJson = {}
    #print list
    updateJson.update(status=list['status'])
    updateJson.update(comment=list['comment'])
    updateBody = json.dumps(updateJson)
    #print(list['testCaseKey'])
    #print(updateBody)
    with open("jira/updateCycle.json", "w") as f:
        f.write(updateBody)
    print(command + " " + httpMethod + " " + "http://localhost:8080/rest/atm/latest/testrun/" + testCycle + "/testcase/" + list['testCaseKey'] + "/testresult")

# get test case not in cycle now, and post it to cycle
def sortlist(middleList, List):
    l = []
    result = []
    for list in List:
        l.append(list['testCaseKey'])
        #print(l)
    #print(l)
    if l == middleList:
        return None
    else:
        for x in l:
            if x not in middleList:
                result.append(x)
        #print result
        return result






List = createJson.createOneJson(folderDirectory)
#testCycle = sys.argv[1]
print(List)
testCaseKeyList = readJsonFile(path, testCycle="DEM-C20")
updateTestCase(testCaseKeyList, List, testCycle="DEM-C20")


#sortlist(middleList, List)
