# from jira import JIRA
import json
import datetime
import requests
from requests.auth import HTTPBasicAuth


class JiraIssue:
    def __init__(self, key="", turnaroundTime=0, idleTime=0):
        self.key = key
        self.turnaroundTime = turnaroundTime
        self.idleTime = idleTime
        self.closeTime = ""
        self.summary = ""


class JiraOperator:
    def __init__(self):
        filename = 'conf/jira.json'
        with open(filename) as f_obj:
            acct = json.load(f_obj)
        self.jiraUrl = acct[0]
        self.jiraUser = acct[1]
        self.jiraPwd = acct[2]
        self.issueCreated = ""
        self.issueStarted = ""
        self.issueDone = ""
        f_obj.close()

    def turnaroundTime(self, jiraIssue):
        self.issueCreated = ""  # reset the values
        self.issueDone = ""  # reset the values
        headers = {
            "X-Atlassian-Token": "no-check",
            'content-type': "application/json"
        }
        requests.packages.urllib3.disable_warnings()
        url = self.jiraUrl + "/rest/api/2/issue/{}?expand=changelog".format(jiraIssue.key)
        response = requests.get(url, headers=headers, verify=False,
                                auth=HTTPBasicAuth(self.jiraUser, self.jiraPwd))
        issueClosed = False
        if response.status_code == 200:
            self.issueCreated = response.json()["fields"]["created"]
            print(jiraIssue.key + " was created at " + self.issueCreated)
            histories = response.json()["changelog"]["histories"]
            for history in histories:
                if "8.0 Current Release" == history["items"][-1]["toString"]:
                    self.issueDone = history["created"]
                    issueClosed = True
                    print(jiraIssue.key + " was released at " + history["created"])
                    break
                if "Closed" == history["items"][-1]["toString"]:
                    self.issueDone = history["created"]
                    issueClosed = True
                    print(jiraIssue.key + " was closed at " + history["created"])
                    break
            self.issueDone = str(datetime.datetime.now()) if self.issueDone == "" else self.issueDone
            if self.issueCreated != "":
                d1 = datetime.datetime.strptime(self.issueCreated[:10], '%Y-%m-%d')
                d2 = datetime.datetime.strptime(self.issueDone[:10], '%Y-%m-%d')
                delta = d2 - d1
                print("Turnaround time for " + str(delta.days) + " days.")
                jiraIssue.turnaroundTime = delta.days
        jiraIssue.closeTime = jiraIssue.turnaroundTime if issueClosed else jiraIssue.closeTime

    def turnaroundTimeBatch(self, issueList):
        for jiraIssue in issueList:
            self.turnaroundTime(jiraIssue)

    def idleTime(self, jiraIssue):
        self.issueCreated = ""  # reset the values
        self.issueStarted = ""  # reset the values
        headers = {
            "X-Atlassian-Token": "no-check",
            'content-type': "application/json"
        }
        requests.packages.urllib3.disable_warnings()
        url = self.jiraUrl + "/rest/api/2/issue/{}?expand=changelog".format(jiraIssue.key)
        response = requests.get(url, headers=headers, verify=False,
                                auth=HTTPBasicAuth(self.jiraUser, self.jiraPwd))
        if response.status_code == 200:
            self.issueCreated = response.json()["fields"]["created"]
            print(jiraIssue.key + " was created at " + self.issueCreated)
            histories = response.json()["changelog"]["histories"]
            for history in histories:
                if ("2.0 In Progress" == history["items"][-1]["toString"]):
                    self.issueStarted = history["created"]
                    print(jiraIssue.key + " was in progress at " + history["created"])
                    break
                if "Closed" == history["items"][-1]["toString"]:
                    self.issueStarted = history["created"]
                    print(jiraIssue.key + " was closed at " + history["created"])
                    break
            self.issueStarted = str(datetime.datetime.now()) if self.issueStarted == "" else self.issueStarted
            if self.issueCreated != "" and self.issueStarted != "":
                d1 = datetime.datetime.strptime(self.issueCreated[:10], '%Y-%m-%d')
                d2 = datetime.datetime.strptime(self.issueStarted[:10], '%Y-%m-%d')
                delta = d2 - d1
                print("Idle for " + str(delta.days) + " days.")
                return delta.days
        return 0

    def idleTimeBatch(self, issueList):
        for jiraIssue in issueList:
            jiraIssue.idleTime = self.idleTime(jiraIssue)

    def summary(self, jiraIssue):
        headers = {
            "X-Atlassian-Token": "no-check",
            'content-type': "application/json"
        }
        requests.packages.urllib3.disable_warnings()
        url = self.jiraUrl + "/rest/api/2/issue/{}".format(jiraIssue.key)
        response = requests.get(url, headers=headers, verify=False,
                                auth=HTTPBasicAuth(self.jiraUser, self.jiraPwd))
        if response.status_code == 200:
            return response.json()["fields"]["summary"]
        else:
            return ""

    def summaryBatch(self, issueList):
        for jiraIssue in issueList:
            jiraIssue.summary = self.summary(jiraIssue)

    def jqlSearch(self, jqlString):
        headers = {
            "X-Atlassian-Token": "no-check",
            'content-type': "application/json"
        }
        payload = {
            "jql": jqlString,
            "startAt": 0,
            "maxResults": 50,
            "fields": [
                "key",
                "summary",
                "status"
            ]
        }
        data = json.dumps(payload)
        requests.packages.urllib3.disable_warnings()
        url = self.jiraUrl + "/rest/api/2/search"
        response = requests.post(url, data=data, headers=headers, verify=False,
                                 auth=HTTPBasicAuth(self.jiraUser, self.jiraPwd))
        issues = response.json()["issues"]
        jiraIssues = []
        for issue in issues:
            ji = JiraIssue(issue["key"])
            jiraIssues.append(ji)
            # print (ji.key + str(ji.turnaroundTime))
        return jiraIssues


if __name__ == '__main__':
    jiraOperator = JiraOperator()
    # jiraOperator.turnaroundTime("YODA-10555")
    ji = jiraOperator.jqlSearch("project=YODA")
