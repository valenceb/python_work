#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "valenceb"

# from openpyxl import Workbook
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
        print(e)
        return False


def trimHtml(html):
    dr = re.compile(r'<[^>]+>', re.S)
    return dr.sub('', html)


def getBacklogs(html, sprintList, exlRow):
    reg = r'(<li (?:class=\"\w*\" )?data-inline-task-id=\"\d+\">.*?</li>)'
    actionItems = re.findall(reg, html)
    backlogs = []
    for ai in actionItems:
        backlogs.append(Backlog(sprintList, ai, exlRow))
    return backlogs


class Project:
    def __init__(self, wiki, sprintList, exlRow):
        html = getHtml(wiki)
        reg = r'<h1 id=\"title-text\" class=\".*?\">.*?<a href=\".*?\">(.*?)</a>.*?</h1>'
        searchObj = re.search(reg, html, re.M | re.I)
        if not searchObj:
            self.title = None
        else:
            self.title = searchObj.group(1)
        self.wiki = wiki
        self.exlRow = exlRow
        self.backlogs = getBacklogs(html, sprintList, exlRow)


class Sprint:
    def __init__(self, sprintName, exlCol):
        reg = r'Sprint (\d+)\((\d+/\d+)-(\d+/\d+)\)'
        searchObj = re.search(reg, sprintName, re.M | re.I)
        startDate = searchObj.group(2)
        endDate = searchObj.group(3)
        self.sprintNum = searchObj.group(1)
        self.startDate = string2Date(startDate)
        self.endDate = string2Date(endDate)
        self.exlCol = chr(65 + exlCol)
        now = datetime.datetime.now()
        if self.startDate < now and self.endDate > now:
            self.isCurSprint = True
        else:
            self.isCurSprint = False


class Backlog:
    def __init__(self, sprintList, actionItem, projExlRow):
        reg = '<li (?:class=\"(.*?)\" )?data-inline-task-id=\"\d+\">(.*?)(?:<time datetime=\"(.*?)\" class=\"date-past\">.*?</time>.*?)?</li>'
        searchObj = re.search(reg, actionItem)
        self.checked = True if searchObj.group(1) == 'checked' else False
        self.description = trimHtml(searchObj.group(2))
        tempDate = searchObj.group(3)
        self.date = None if not tempDate else datetime.datetime.strptime(tempDate, '%Y-%m-%d')
        self.exlRow = projExlRow
        self.exlCol = self.inSprint(sprintList)

    def inSprint(self, sprintList):
        column = 0
        if not self.date:
            for sprint in sprintList:
                if sprint.isCurSprint:
                    column = chr(ord(sprint.exlCol) + 1)  # 没有设置Timeline的Item默认放到下个Sprint
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

    with open('conf/sprint.csv') as f:
        csvLines = csv.reader(f)
        i = 1
        for csvL in csvLines:
            sprintList.append(Sprint(''.join(csvL), i))
            i += 1

    with open('conf/project.csv') as f:
        csvLines = csv.reader(f)
        i = 1
        for csvL in csvLines:
            proj = Project(''.join(csvL), sprintList, i)
            if not proj.title:
                print('No such project.')
            else:
                projectList.append(proj)
            i += 1
    print(projectList)
    print(sprintList)
    print('\nProcess Done.')
