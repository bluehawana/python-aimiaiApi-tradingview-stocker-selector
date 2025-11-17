"""
为金叉股票CSV添加中文名称
"""
import pandas as pd

# 24只金叉股票的中文名称映射
STOCK_NAMES = {
    '002074': '国轩高科',
    '002129': '中环股份',
    '002371': '北方华创',
    '002459': '晶澳科技',
    '002460': '赣锋锂业',
    '002466': '天齐锂业',
    '002812': '恩捷股份',
    '300014': '亿纬锂能',
    '300274': '阳光电源',
    '300308': '中际旭创',
    '300316': '晶盛机电',
    '300450': '先导智能',
    '300502': '新易盛',
    '300750': '宁德时代',
    '300763': '锦浪科技',
    '601012': '隆基绿能',
    '601865': '唯捷创芯',
    '603986': '兆易创新',
    '688005': '容百科技',
    '688008': '澜起科技',
    '688256': '寒武纪',
    '688390': '固德威',
    '688599': '天合光能',
    '688981': '中芯国际'
}


def add_chinese_names(input_file, output_file):
    """添加中文名称到CSV"""
    # 读取CSV，确保symbol列为字符串
    df = pd.read_csv(input_file, dtype={'symbol': str})

    # 确保symbol列是6位数字格式
    df['symbol'] = df['symbol'].str.zfill(6)

    # 添加中文名称列
    df.insert(1, 'name', df['symbol'].map(STOCK_NAMES))

    # 保存
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"✅ 已添加中文名称")
    print(f"📁 输入: {input_file}")
    print(f"📁 输出: {output_file}")
    print(f"\n前5行预览:")
    print(df[['symbol', 'name', 'date', 'close', 'status']].head())


if __name__ == '__main__':
    input_file = 'results/golden_cross_20251117_200957.csv'
    output_file = 'results/golden_cross_with_names.csv'
    add_chinese_names(input_file, output_file)
