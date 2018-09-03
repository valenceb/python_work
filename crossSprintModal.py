#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = "valenceb"
import urllib.request
import re
import datetime


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
    def __init__(self, wiki, sprintList, exlRow, ws):
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
        self.renderProject(ws, sprintList)

    def renderProject(self, ws, sprintList):
        cell = 'A' + str(self.exlRow)
        ws[cell] = self.title
        ws[cell].style = 'projHeader'
        for sprint in sprintList:
            cell = sprint.exlCol + str(self.exlRow)
            ws[cell].style = 'backlog'
        for backlog in self.backlogs:
            cell = backlog.exlCol + str(backlog.exlRow)
            backlogDate = (backlog.date.strftime('%m/%d') + " ") \
                if backlog.date else "TBD "
            preValue = ws[cell].value if ws[cell].value else ""
            incValue = preValue + ("√ " if backlog.checked else "◆ ") + \
                       backlogDate + backlog.description
            ws[cell] = incValue
            if not backlog.checked:
                ws[cell].style = 'blackFont'



class Sprint:
    def __init__(self, sprintName, exlCol, ws):
        reg = r'Sprint (\d+)\((\d+/\d+)-(\d+/\d+)\)'
        searchObj = re.search(reg, sprintName, re.M | re.I)
        startDate = searchObj.group(2)
        endDate = searchObj.group(3)
        self.sprintName = sprintName
        self.sprintNum = searchObj.group(1)
        self.startDate = string2Date(startDate)
        self.endDate = string2Date(endDate)
        self.exlCol = chr(65 + exlCol)
        now = datetime.datetime.now()
        nowDate = datetime.datetime.strptime(now.strftime('%Y/%m/%d'), '%Y/%m/%d')
        if self.startDate <= nowDate and self.endDate >= nowDate:
            self.isCurSprint = True
        else:
            self.isCurSprint = False
        self.renderSprint(ws)

    def renderSprint(self, ws):
        ws.column_dimensions[self.exlCol].width = 35 if self.isCurSprint else 30
        cell = self.exlCol + '1'
        ws[cell] = self.sprintName
        ws[cell].style = 'header'


class Backlog:
    def __init__(self, sprintList, actionItem, projExlRow):
        reg = '<li (?:class=\"(.*?)\" )?data-inline-task-id=\"\d+\">(.*?)(?:<time datetime=\"(.*?)\" class=\".*?\">.*?</time>.*?)?</li>'
        searchObj = re.search(reg, actionItem)
        self.checked = True if searchObj.group(1) == 'checked' else False
        self.description = trimHtml(searchObj.group(2)) + "\n"
        self.description = self.description.replace("\\xc2\\xa0"," ")
        self.description = self.description.replace("\\xe2\\x80\\x93", "-")
        tempDate = searchObj.group(3)
        self.date = (None if not tempDate
                     else datetime.datetime.strptime(tempDate, '%Y-%m-%d'))
        self.exlRow = projExlRow
        self.exlCol = self.inSprint(sprintList)

    def inSprint(self, sprintList):
        column = 'A'
        if not self.date:
            for sprint in sprintList:
                if sprint.isCurSprint:
                    column = chr(ord(sprint.exlCol) + 1)
                    # 没有设置Timeline的Item默认放到下个Sprint
                    break
        else:
            for sprint in sprintList:
                if sprint.startDate <= self.date and sprint.endDate >= self.date:
                    column = sprint.exlCol
                    break
        return column
