# -*- coding:utf-8 -*-

import json
import os
import re
import sys
import argparse

path = "./" # specific folder
testPath = "/Users/luckylyw19930104/Documents/output_results/result2.json"
resultPath = "./httpBody.json"

# read Json file from specific folder
def readOneJson(path):
    with open(path, "r") as j:
        data = json.load(j)
        return data[0]

# read custom fields that we need from json file
def readFieldsFromJson(path):
    Json = readOneJson(path) # TODO:
    fieldList = []
    testCaseKey = Json['elements'][0]['tags'][0]['name']
    middleValue = testCaseKey.split("=")
    testCaseKey = middleValue[1]
    #print(testCaseKey)
    fieldList.append(testCaseKey)
    status = Json['elements'][0]['steps'][0]['result']['status']
    fieldList.append(status)
    if status == "failed":
        errorMsg = Json['elements'][0]['steps'][0]['result']['error_message']
        fieldList.append(errorMsg)
    else:
        fieldList.append("passed")
    return fieldList

# get one list about files under specific folder
def getAllFiles(path):
    for files in os.walk(path):
        return files[2]

# get all json files in specific folder
def findAllJson(path):
    files = getAllFiles(path) # TODO:
    jsonList = []
    for file in files:
        if file.endswith(".json") and file.startswith("result"):
            jsonList.append(file)
    return jsonList

# create json list for test cases in cycle
def createOneJson(path):
    jsonList = findAllJson(path) # TODO:
    List = []
    for json in jsonList:
        jsonPath = path + "/" + json
        fieldList = readFieldsFromJson(jsonPath)
        testCaseKey = fieldList[0]
       # print(testCaseKey)
        status = fieldList[1]
        errorMsg = fieldList[2]
        fieldDict = {}
        fieldDict.update(testCaseKey=testCaseKey)
        fieldDict.update(status=status)
        fieldDict.update(comment=errorMsg)
        List.append(fieldDict)
    return List

# create one http body json according to TM4J API
def createBodyJson(path, projectKey, name, folder, resultPath):
    List = createOneJson(path) # TODO:
    JsonDict = {}
    JsonDict.update(projectKey=projectKey) # input from cli
    JsonDict.update(name=name)
    #JsonDict.update(status=status)
    JsonDict.update(folder=folder)
    JsonDict.update(items=List)
    #print(JsonDict)
    jsonFile = json.dumps(JsonDict)
    with open(resultPath, "w") as f:
        f.write(jsonFile)

# main method for createJson

projectKey = sys.argv[1]
name = sys.argv[2]
status = sys.argv[3]
folder = sys.argv[3]
createBodyJson(path, projectKey, name, folder, resultPath)

