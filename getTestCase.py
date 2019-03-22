# -*- coding:utf-8 -*-

import os
import json
import sys
import createJson

path = "existTestCycle.json"
folderDirectory = "./"

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
    command = "curl --basic --user luckylyw19930104:031118luckylyw -H Content-Type:application/json --data @updateCycle.json "
    updateJson = {}
    updateJson.update(status=list['status'])
    updateJson.update(comment=list['comment'])
    updateBody = json.dumps(updateJson)
    #print(list['testCaseKey'])
    #print(updateBody)
    with open("updateCycle.json", "w") as f:
        f.write(updateBody)
    print(command + " " + httpMethod + " " + "http://localhost:8080/rest/atm/latest/testrun/" + testCycle + "/testcase/" + list['testCaseKey'] + "/testresult")

# get test case not in cycle now, and post it to cycle
def sortlist(middleList, List):
    l = []
    print middleList
    for list in List:
        l.append(list['testCaseKey'])
        print(l)
    if l == middleList:
        return None
    else:
        list(set(l).difference(set(middleList)))
        return l







List = createJson.createOneJson(folderDirectory)
#testCycle = sys.argv[1]
testCaseKeyList = readJsonFile(path, testCycle="DEM-C16")
updateTestCase(testCaseKeyList, List, testCycle="DEM-C16")