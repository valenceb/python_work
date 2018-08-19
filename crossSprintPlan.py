#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "valenceb"

from openpyxl import Workbook
import datetime
import csv
import urllib.request
import re


def string2Date(dateStr):
    dateStr = str(datetime.datetime.now().year) + '/' + dateStr
    date = datetime.datetime.strptime(dateStr, '%Y/%m/%d')
    return date


def getHtml(url):
    try:
        page = urllib.request.urlopen(url)
        html = page.read()
        html = str(html)
        return html
    except Exception as e:
        print(e.reason)
        return False


class Project:
    def __init__(self, wiki):
        self.wiki = wiki
        html = getHtml(wiki)
        reg = 'Project Title Regular Formular'
        self.title = re.search(reg, html).group()
        self.exlRow = 0


class Sprint:
    def __init__(self, sprintName, exlCol):
        reg = r'Sprint (\d+)\((\d+/\d+)-(\d+/\d+)\)'
        searchObj = re.search(reg, sprintName, re.M | re.I)
        startDate = searchObj.group(2)
        endDate = searchObj.group(3)
        self.sprintNum = searchObj.group(1)
        self.startDate = string2Date(startDate)
        self.endDate = string2Date(endDate)
        self.exlCol = chr(65+exlCol)
        now = datetime.datetime.now()
        if self.startDate < now and self.endDate > now:
            self.isCurSprint = True
        else:
            self.isCurSprint = False


class Backlog:
    def __init__(self, sprintList, checkItem, projExlRow):
        reg = 'Identify date/description'
        self.date = ""
        self.description = ""
        self.checked = False
        self.exlRow = projExlRow
        self.exlCol = self.inSprint(sprintList)

    def inSprint(self, sprintList):
        column = 0
        if self.date == "":
            for sprint in sprintList:
                if sprint.isCurSprint:
                    column = sprint.exlCol + 1  # 没有设置Timeline的Item默认放到下个Sprint
                    break
        else:
            for sprint in sprintList:
                if sprint.startDate < self.date and sprint.endDate > self.date:
                    column = sprint.exlCol
                    break
        return column


if __name__ == '__main__':
    projectList = []
    sprintList = []
    with open('conf/project.csv') as f:
        csvLines = csv.reader(f)
        for csvL in csvLines:
            projectList.append(csvL)
    print(projectList)
    with open('conf/sprint.csv') as f:
        csvLines = csv.reader(f)
        i=1
        for csvL in csvLines:
            sprintList.append(Sprint(''.join(csvL),i))
            i+=1
    print(sprintList)
    print('\nProcess Done.')

