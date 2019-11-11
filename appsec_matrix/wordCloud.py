from jiraOps import JiraOperator, JiraIssue
import pyecharts.options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType


def wordCloud(issueList) -> WordCloud:
    words = []
    words_raw = []
    for jiraIssue in issueList:
        words_raw.extend(jiraIssue.summary.split(" "))
    words_clean = list(set(words_raw))
    for word in words_clean:
        words.append((word, words_raw.count(word)))
    c = (
        WordCloud()
            .add("", words, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
            .set_global_opts(title_opts=opts.TitleOpts(title="Security Issue Wordcloud"))
    )
    c.render("output/wordCloud.html")
    return c


if __name__ == '__main__':
    jiraOperator = JiraOperator()
    jql = "issue in linkedIssues('ASEC-201') AND 'Target Release Date' <= endOfMonth('-1M') and 'Target Release Date' >= endofMonth('-5M') ORDER BY Severity, 'CVSS Score', Created DESC"
    ji = jiraOperator.jqlSearch(jql)
    jiraOperator.summaryBatch(ji)
    wordCloud(ji)
