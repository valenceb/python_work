from jiraOps import JiraOperator, JiraIssue
import pyecharts.options as opts
import csv
from pyecharts.charts import Line
from pyecharts.globals import ThemeType


def areaChart(prodLine, issueList) -> Line:
    x = []
    y1_TurnaroundTime = []
    y2_IdleTime = []
    for issue in issueList:
        # 坐标刻度竖排
        # keyStr = ""
        # for char in str(issue.key):
        #     keyStr += (char + '\n')
        # x.append(keyStr)
        x.append(issue.key)
        y1_TurnaroundTime.append(issue.turnaroundTime)
        y2_IdleTime.append(issue.idleTime)
    c = (
        # Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        Line()
            .add_xaxis(x)
            .add_yaxis(
            "Turnaround Time", y1_TurnaroundTime, areastyle_opts=opts.AreaStyleOpts(opacity=0.5)
        )
            .add_yaxis(
            "Idle Time", y2_IdleTime, areastyle_opts=opts.AreaStyleOpts(opacity=0.5)
        )
            .set_global_opts(title_opts=opts.TitleOpts(title=prodLine + " Security Turnaround (days)",
                                                       subtitle="Including issues' idle time and overall turnaround time."),
                             legend_opts=opts.LegendOpts(pos_left="60%", pos_top="8%"))
    )
    c.render("output/" + prodLine + "_area_chart.html")

    with open('output/' + prodLine + '_turnaround.csv', 'w', newline='')as f:
        csvfile = csv.writer(f)
        data = [
            x,
            y2_IdleTime,
            y1_TurnaroundTime
        ]
        csvfile.writerows(data)
        f.close()

    return c


def prodLineAreaChart(prodLine, jql):
    jiraOperator = JiraOperator()
    jiList = jiraOperator.jqlSearch(jql)
    jiraOperator.idleTimeBatch(jiList)
    jiraOperator.turnaroundTimeBatch(jiList)
    areaChart(prodLine, jiList)


if __name__ == '__main__':
    jql = "issue in linkedIssues('ASEC-201') AND Project = 'Medicare Scrum Project' AND 'Target Release Date' <= endOfMonth('-1M') and 'Target Release Date' >= endofMonth('-5M') ORDER BY Severity, 'CVSS Score', Created DESC"
    prodLineAreaChart("Medicare", jql)
