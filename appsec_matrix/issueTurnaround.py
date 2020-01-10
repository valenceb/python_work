from jiraOps import JiraOperator, JiraIssue
import pyecharts.options as opts
import csv
from pyecharts.charts import Line, Scatter
from pyecharts.globals import ThemeType


def areaChart(prodLine, issueList) -> Line:
    x = []
    y1_TurnaroundTime = []
    y2_IdleTime = []
    y3_ClosedTime = []
    for issue in issueList:
        # 坐标刻度竖排
        # keyStr = ""
        # for char in str(issue.key):
        #     keyStr += (char + '\n')
        # x.append(keyStr)
        x.append(issue.key)
        y1_TurnaroundTime.append(issue.turnaroundTime)
        y2_IdleTime.append(issue.idleTime)
        y3_ClosedTime.append(issue.closeTime)
    c = (
        # Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        Line()
            .add_xaxis(x)
            .add_yaxis(
            "In Progress", y1_TurnaroundTime, areastyle_opts=opts.AreaStyleOpts(opacity=0.5)
        )
            .add_yaxis(
            "Idle Time", y2_IdleTime, areastyle_opts=opts.AreaStyleOpts(opacity=0.4)
        )
            .set_global_opts(title_opts=opts.TitleOpts(title=prodLine + " Security Turnaround (days)",
                                                       subtitle="Including issues' idle time and overall turnaround time."),
                             legend_opts=opts.LegendOpts(pos_left="60%", pos_top="6%"))
    )
    scatter = (
        Scatter()
            .add_xaxis(x)
            .add_yaxis("Closed", y3_ClosedTime, markpoint_opts=opts.MarkPointOpts(symbol='diamond'))
    )
    c.overlap(scatter)
#     c.render("output/" + prodLine + "_area_chart.html")

#     with open('output/' + prodLine + '_turnaround.csv', 'w', newline='')as f:
#         csvfile = csv.writer(f)
#         data = [
#             x,
#             y2_IdleTime,
#             y1_TurnaroundTime,
#             y3_ClosedTime
#         ]
#         csvfile.writerows(data)
#         f.close()

    return c


def prodLineAreaChart(prodLine, jql):
    jiraOperator = JiraOperator()
    jiList = jiraOperator.jqlSearch(jql)
    jiraOperator.idleTimeBatch(jiList)
    jiraOperator.turnaroundTimeBatch(jiList)
    return areaChart(prodLine, jiList)


if __name__ == '__main__':

    jql = "issue in linkedIssues('ASEC-201') AND Project = 'Back Office CORE team' AND 'Target Release Date' <= endOfMonth('-1M') and 'Target Release Date' >= endofMonth('-5M') ORDER BY Severity, 'CVSS Score', Created DESC"
    prodLineAreaChart("BackOffice", jql)

    jql = "issue in linkedIssues('ASEC-201') AND Project = 'Carrier Integration' AND 'Target Release Date' <= endOfMonth('-1M') and 'Target Release Date' >= endofMonth('-5M') ORDER BY Severity, 'CVSS Score', Created DESC"
    prodLineAreaChart("Carrier Integration", jql)

    jql = "issue in linkedIssues('ASEC-201') AND Project = 'Yoda - IFP Front Office' AND 'Target Release Date' <= endOfMonth('-1M') and 'Target Release Date' >= endofMonth('-5M') ORDER BY Severity, 'CVSS Score', Created DESC"
    prodLineAreaChart("IFP", jql)

    jql = "issue in linkedIssues('ASEC-201') AND Project = 'Medicare Scrum Project' AND 'Target Release Date' <= endOfMonth('-1M') and 'Target Release Date' >= endofMonth('-5M') ORDER BY Severity, 'CVSS Score', Created DESC"
    prodLineAreaChart("Medicare", jql)

    jql = "issue in linkedIssues('ASEC-201') AND Project in ('Platform Service', 'Product Center', 'Financial Systems and Informational Systems') AND 'Target Release Date' <= endOfMonth('-1M') and 'Target Release Date' >= endofMonth('-5M') ORDER BY Severity, 'CVSS Score', Created DESC"
    prodLineAreaChart("Platform", jql)

    jql = "issue in linkedIssues('ASEC-201') AND Project = 'VADR - SMB Front Office' AND 'Target Release Date' <= endOfMonth('-1M') and 'Target Release Date' >= endofMonth('-5M') ORDER BY Severity, 'CVSS Score', Created DESC"
    prodLineAreaChart("SMB", jql)