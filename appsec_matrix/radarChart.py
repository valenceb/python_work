from pyecharts import options as opts
from pyecharts.charts import Radar

v1 = [[4300, 10000, 28000, 35000, 50000, 19000]]
v2 = [[5000, 14000, 28000, 31000, 42000, 21000]]


def radar_base(prodline, v1) -> Radar:
    c = (
        Radar()
            .add_schema(
            schema=[
                opts.RadarIndicatorItem(name="Momentum", max_=100),
                opts.RadarIndicatorItem(name="Efficiency", max_=100),
                opts.RadarIndicatorItem(name="Checkmarx Robusty", max_=100),
                opts.RadarIndicatorItem(name="WhiteSource Robusty", max_=100),
                opts.RadarIndicatorItem(name="Qualys Robusty", max_=100),
            ]
        )
            # .add("BackOffice", v1)
            .add(prodline, v1, linestyle_opts=opts.LineStyleOpts(opacity=1, width=5, color='rgb(255, 0, 0)'))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="Radar Matrix"))
    )
    c.render("output/"+prodline+"_radarChart.html")
    return c


if __name__ == '__main__':
    backOffice_v1 = [[39,55,16,60,62]]
    ci_v1 = [[31,48,20,50,98]]
    ifp_v1 = [[48,65,16,56,100]]
    medicare_v1 = [[82,76,2,56,87]]
    platform_v1 = [[86,74,5,50,93]]
    smb_v1 = [[81,73,53,97,100]]
    radar_base("BackOffice",backOffice_v1)
    radar_base("CarrierIntegration", ci_v1)
    radar_base("IFP", ifp_v1)
    radar_base("Medicare", medicare_v1)
    radar_base("Platform", platform_v1)
    radar_base("SMB", smb_v1)
