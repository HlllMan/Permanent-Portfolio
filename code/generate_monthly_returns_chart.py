#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成三大指数月度收益率对比图
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

print("="*80)
print("开始生成三大指数月度收益率对比图")
print("="*80)

# 读取原始数据
sp500_df = pd.read_csv('/Users/miaoji.norman/Desktop/投资/S&P 500 TR Historical Data-2.csv')
nasdaq_df = pd.read_csv('/Users/miaoji.norman/Desktop/投资/Nasdaq 100 TR Historical Data.csv')
csi300_df = pd.read_csv('/Users/miaoji.norman/Desktop/投资/沪深300TR historical data.csv')

# 处理日期和价格
sp500_df['Date'] = pd.to_datetime(sp500_df['Date'], format='%m/%d/%Y')
sp500_df['Price'] = sp500_df['Price'].astype(str).str.replace(',', '').astype(float)

nasdaq_df['Date'] = pd.to_datetime(nasdaq_df['Date'], format='%m/%d/%Y')
nasdaq_df['Price'] = nasdaq_df['Price'].astype(str).str.replace(',', '').astype(float)

csi300_df['日期Date'] = pd.to_datetime(csi300_df['日期Date'], format='%Y%m%d')
csi300_df['收盘Close'] = pd.to_numeric(csi300_df['收盘Close'], errors='coerce')

# 排序
sp500_df = sp500_df.sort_values('Date')
nasdaq_df = nasdaq_df.sort_values('Date')
csi300_df = csi300_df.sort_values('日期Date')

# 将沪深300转换为月度数据（取每月最后一个交易日）
csi300_df['YearMonth'] = csi300_df['日期Date'].dt.to_period('M')
csi300_monthly = csi300_df.groupby('YearMonth').last().reset_index()
csi300_monthly['日期Date'] = csi300_monthly['日期Date']

print(f"\nS&P 500数据点: {len(sp500_df)}")
print(f"Nasdaq 100数据点: {len(nasdaq_df)}")
print(f"沪深300月度数据点: {len(csi300_monthly)}")

# 计算月度收益率
# S&P 500
sp500_df['Monthly_Return'] = sp500_df['Price'].pct_change() * 100
sp500_df['YearMonth'] = sp500_df['Date'].dt.to_period('M')

# Nasdaq 100
nasdaq_df['Monthly_Return'] = nasdaq_df['Price'].pct_change() * 100
nasdaq_df['YearMonth'] = nasdaq_df['Date'].dt.to_period('M')

# 沪深300
csi300_monthly['Monthly_Return'] = csi300_monthly['收盘Close'].pct_change() * 100
csi300_monthly['YearMonth'] = csi300_monthly['日期Date'].dt.to_period('M')

# 移除第一行（没有前一个月数据）
sp500_df = sp500_df[sp500_df['Monthly_Return'].notna()]
nasdaq_df = nasdaq_df[nasdaq_df['Monthly_Return'].notna()]
csi300_monthly = csi300_monthly[csi300_monthly['Monthly_Return'].notna()]

print(f"\n计算月度收益率后:")
print(f"S&P 500: {len(sp500_df)} 个月")
print(f"Nasdaq 100: {len(nasdaq_df)} 个月")
print(f"沪深300: {len(csi300_monthly)} 个月")

# 创建图表
fig, ax = plt.subplots(figsize=(16, 9))

# 绘制折线图
ax.plot(sp500_df['Date'], sp500_df['Monthly_Return'], linewidth=1.5, 
        label='S&P 500 TR', color='#1f77b4', alpha=0.8)
ax.plot(nasdaq_df['Date'], nasdaq_df['Monthly_Return'], linewidth=1.5, 
        label='Nasdaq 100 TR', color='#ff7f0e', alpha=0.8)
ax.plot(csi300_monthly['日期Date'], csi300_monthly['Monthly_Return'], linewidth=1.5, 
        label='沪深300 TR', color='#2ca02c', alpha=0.8)

# 添加零线
ax.axhline(y=0, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)

# 设置标题和标签
ax.set_title('三大指数月度收益率对比 (2016-2025)', fontsize=20, fontweight='bold', pad=20)
ax.set_xlabel('日期', fontsize=14, fontweight='bold')
ax.set_ylabel('月度收益率 (%)', fontsize=14, fontweight='bold')

# 设置网格
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

# 设置图例
ax.legend(loc='upper left', fontsize=13, framealpha=0.9, shadow=True)

# 格式化x轴日期
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.xaxis.set_major_locator(mdates.YearLocator())
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

# 调整y轴范围，让图表更清晰
ax.set_ylim([-30, 50])

# 调整布局
plt.tight_layout()

# 保存图表
output_file = '/Users/miaoji.norman/Desktop/投资/月度收益率对比图.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\n✓ 月度收益率对比图已保存: {output_file}")

plt.close()

# 统计信息
print("\n" + "="*80)
print("月度收益率统计")
print("="*80)

stats_data = []
for name, df, col in [
    ('S&P 500 TR', sp500_df, 'Monthly_Return'),
    ('Nasdaq 100 TR', nasdaq_df, 'Monthly_Return'),
    ('沪深300 TR', csi300_monthly, 'Monthly_Return')
]:
    stats_data.append({
        '指数': name,
        '平均月度收益(%)': round(df[col].mean(), 2),
        '月度收益中位数(%)': round(df[col].median(), 2),
        '月度收益标准差(%)': round(df[col].std(), 2),
        '最大单月涨幅(%)': round(df[col].max(), 2),
        '最大单月跌幅(%)': round(df[col].min(), 2)
    })

stats_df = pd.DataFrame(stats_data)
print(stats_df.to_string(index=False))

# 保存统计数据
stats_output = '/Users/miaoji.norman/Desktop/投资/月度收益率统计.csv'
stats_df.to_csv(stats_output, index=False, encoding='utf-8-sig')
print(f"\n✓ 统计数据已保存: {stats_output}")

print("\n" + "="*80)
print("完成！")
print("="*80)

