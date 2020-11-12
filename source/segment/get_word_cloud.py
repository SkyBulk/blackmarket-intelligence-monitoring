# coding=utf-8
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType

# 数据
words = [
    ('数据', 518030), ('飞机', 322917), ('代发', 297703), ('一手', 287843), ('联系', 266548), ('测试', 245080), ('劫持', 209523),
    ('合作', 208343), ('QQ', 201881), ('广告', 169091), ('长期', 158902), ('免费', 157373), ('棋牌', 154080), ('精准', 153463),
    ('通道', 148850), ('TG', 147242), ('微信', 144305), ('稳定', 139457), ('机房', 134278), ('欢迎', 125962), ('专业', 125023),
    ('卡发', 123602), ('国内', 121731), ('运营商', 116028), ('小时', 111486), ('https', 110846), ('me', 110667), ('发送', 108432),
    ('团队', 104830)
]

# 渲染图
def wordcloud_base() -> WordCloud:
    c = (
        WordCloud()
        .add("", words, word_size_range=[20, 100], shape='diamond')  # SymbolType.ROUND_RECT
        .set_global_opts(title_opts=opts.TitleOpts(title='Telegram黑灰产群组通讯信息 · 词云图'))
    )
    return c

# 生成图
wordcloud_base().render('词云图.html')
