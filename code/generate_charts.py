#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成三大指数对比图表：
1. 年度收益率对比折线图
2. 指数价格（市值）对比折线图
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # Mac系统中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

print("="*80)
print("开始生成三大指数对比图表")
print("="*80)

# ==================== 图表1: 年度收益率对比 ====================
print("\n生成图表1: 年度收益率对比折线图...")

# 读取对比表
comparison_df = pd.read_csv('/Users/miaoji.norman/Desktop/投资/三大指数年化收益率对比表.csv')

# 筛选年度收益数据
annual_data = comparison_df[comparison_df['类别'] == '年度收益'].copy()

# 移除2015年（数据不全）
annual_data = annual_data[annual_data['期间'] != 2015]

# 处理缺失值（'-' 替换为 NaN）
for col in ['S&P 500 TR (%)', 'Nasdaq 100 TR (%)', '沪深300 TR (%)']:
    annual_data[col] = pd.to_numeric(annual_data[col], errors='coerce')

# 创建图表1
fig1, ax1 = plt.subplots(figsize=(14, 8))

years = annual_data['期间'].values

# 绘制三条折线
ax1.plot(years, annual_data['S&P 500 TR (%)'], marker='o', linewidth=2.5, 
         label='S&P 500 TR', color='#1f77b4', markersize=8)
ax1.plot(years, annual_data['Nasdaq 100 TR (%)'], marker='s', linewidth=2.5, 
         label='Nasdaq 100 TR', color='#ff7f0e', markersize=8)
ax1.plot(years, annual_data['沪深300 TR (%)'], marker='^', linewidth=2.5, 
         label='沪深300 TR', color='#2ca02c', markersize=8)

# 添加零线
ax1.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)

# 设置标题和标签
ax1.set_title('三大指数年度收益率对比 (2016-2025)', fontsize=18, fontweight='bold', pad=20)
ax1.set_xlabel('年份', fontsize=14, fontweight='bold')
ax1.set_ylabel('年化收益率 (%)', fontsize=14, fontweight='bold')

# 设置网格
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_axisbelow(True)

# 设置图例
ax1.legend(loc='upper left', fontsize=12, framealpha=0.9, shadow=True)

# 设置x轴刻度
ax1.set_xticks(years)
ax1.set_xticklabels(years, rotation=45)

# 调整布局
plt.tight_layout()

# 保存图表1
chart1_file = '/Users/miaoji.norman/Desktop/投资/年度收益率对比图.png'
plt.savefig(chart1_file, dpi=300, bbox_inches='tight')
print(f"✓ 图表1已保存: {chart1_file}")

plt.close()


# ==================== 图表2: 指数价格对比 ====================
print("\n生成图表2: 指数价格（市值）对比折线图...")

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
print(f"沪深300数据已重采样为月度数据，共 {len(csi300_monthly)} 个数据点")

# 用月度数据替换原数据
csi300_df = csi300_monthly

# 标准化：以第一个数据点为基准（设为100）
sp500_base = sp500_df['Price'].iloc[0]
nasdaq_base = nasdaq_df['Price'].iloc[0]
csi300_base = csi300_df['收盘Close'].iloc[0]

sp500_df['Normalized'] = (sp500_df['Price'] / sp500_base) * 100
nasdaq_df['Normalized'] = (nasdaq_df['Price'] / nasdaq_base) * 100
csi300_df['Normalized'] = (csi300_df['收盘Close'] / csi300_base) * 100

# 创建图表2 - 原始价格（三个子图）
fig2, (ax2_1, ax2_2, ax2_3) = plt.subplots(3, 1, figsize=(14, 18))

# 子图1: 标准化指数（基准=100）
ax2_1.plot(sp500_df['Date'], sp500_df['Normalized'], linewidth=2, 
          label='S&P 500 TR', color='#1f77b4', alpha=0.9)
ax2_1.plot(nasdaq_df['Date'], nasdaq_df['Normalized'], linewidth=2, 
          label='Nasdaq 100 TR', color='#ff7f0e', alpha=0.9)
ax2_1.plot(csi300_df['日期Date'], csi300_df['Normalized'], linewidth=2, 
          label='沪深300 TR', color='#2ca02c', alpha=0.9)

ax2_1.set_title('三大指数标准化走势对比 (基准=100)', fontsize=18, fontweight='bold', pad=20)
ax2_1.set_xlabel('日期', fontsize=14, fontweight='bold')
ax2_1.set_ylabel('标准化指数 (起始点=100)', fontsize=14, fontweight='bold')
ax2_1.grid(True, alpha=0.3, linestyle='--')
ax2_1.legend(loc='upper left', fontsize=12, framealpha=0.9, shadow=True)
ax2_1.set_axisbelow(True)

# 格式化x轴日期
ax2_1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax2_1.xaxis.set_major_locator(mdates.YearLocator())
plt.setp(ax2_1.xaxis.get_majorticklabels(), rotation=45)

# 子图2: 原始价格（统一Y轴）
ax2_2.plot(sp500_df['Date'], sp500_df['Price'], linewidth=2, 
          label='S&P 500 TR', color='#1f77b4', alpha=0.9)
ax2_2.plot(nasdaq_df['Date'], nasdaq_df['Price'], linewidth=2, 
          label='Nasdaq 100 TR', color='#ff7f0e', alpha=0.9)
ax2_2.plot(csi300_df['日期Date'], csi300_df['收盘Close'], linewidth=2, 
          label='沪深300 TR', color='#2ca02c', alpha=0.9)

ax2_2.set_title('三大指数原始价格走势对比（统一比例尺）', fontsize=18, fontweight='bold', pad=20)
ax2_2.set_xlabel('日期', fontsize=14, fontweight='bold')
ax2_2.set_ylabel('指数价格', fontsize=14, fontweight='bold')

# 设置Y轴从0开始
ax2_2.set_ylim(bottom=0)

ax2_2.grid(True, alpha=0.3, linestyle='--')
ax2_2.set_axisbelow(True)

ax2_2.legend(loc='upper left', fontsize=12, framealpha=0.9, shadow=True)

# 格式化x轴日期
ax2_2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax2_2.xaxis.set_major_locator(mdates.YearLocator())
plt.setp(ax2_2.xaxis.get_majorticklabels(), rotation=45)

# 子图3: 原始价格（各自独立的比例尺 - 三个Y轴）
ax2_3_nasdaq = ax2_3.twinx()
ax2_3_csi = ax2_3.twinx()

# 调整第三个y轴位置
ax2_3_csi.spines['right'].set_position(('outward', 60))

# 绘制三条线
line1 = ax2_3.plot(sp500_df['Date'], sp500_df['Price'], linewidth=2, 
                   label='S&P 500 TR', color='#1f77b4', alpha=0.9)
line2 = ax2_3_nasdaq.plot(nasdaq_df['Date'], nasdaq_df['Price'], linewidth=2, 
                          label='Nasdaq 100 TR', color='#ff7f0e', alpha=0.9)
line3 = ax2_3_csi.plot(csi300_df['日期Date'], csi300_df['收盘Close'], linewidth=2, 
                       label='沪深300 TR', color='#2ca02c', alpha=0.9)

ax2_3.set_title('三大指数原始价格走势对比（各自独立比例尺）', fontsize=18, fontweight='bold', pad=20)
ax2_3.set_xlabel('日期', fontsize=14, fontweight='bold')
ax2_3.set_ylabel('S&P 500 TR 价格', fontsize=12, fontweight='bold', color='#1f77b4')
ax2_3_nasdaq.set_ylabel('Nasdaq 100 TR 价格', fontsize=12, fontweight='bold', color='#ff7f0e')
ax2_3_csi.set_ylabel('沪深300 TR 价格', fontsize=12, fontweight='bold', color='#2ca02c')

# 设置y轴颜色
ax2_3.tick_params(axis='y', labelcolor='#1f77b4')
ax2_3_nasdaq.tick_params(axis='y', labelcolor='#ff7f0e')
ax2_3_csi.tick_params(axis='y', labelcolor='#2ca02c')

# 设置Y轴从0开始
ax2_3.set_ylim(bottom=0)
ax2_3_nasdaq.set_ylim(bottom=0)
ax2_3_csi.set_ylim(bottom=0)

ax2_3.grid(True, alpha=0.3, linestyle='--')
ax2_3.set_axisbelow(True)

# 合并图例
lines = line1 + line2 + line3
labels = [l.get_label() for l in lines]
ax2_3.legend(lines, labels, loc='upper left', fontsize=12, framealpha=0.9, shadow=True)

# 格式化x轴日期
ax2_3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax2_3.xaxis.set_major_locator(mdates.YearLocator())
plt.setp(ax2_3.xaxis.get_majorticklabels(), rotation=45)

# 调整布局
plt.tight_layout()

# 保存图表2
chart2_file = '/Users/miaoji.norman/Desktop/投资/指数价格对比图.png'
plt.savefig(chart2_file, dpi=300, bbox_inches='tight')
print(f"✓ 图表2已保存: {chart2_file}")

plt.close()

print("\n" + "="*80)
print("图表生成完成！")
print("="*80)
print(f"已生成:")
print(f"  1. {chart1_file}")
print(f"  2. {chart2_file}")
print("="*80)

