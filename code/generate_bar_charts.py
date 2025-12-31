#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成三大指数各自的柱状图
每个指数一张独立的柱状图，从0开始，独立比例尺
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
print("开始生成三大指数各自的柱状图")
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

# 将沪深300转换为月度数据
csi300_df['YearMonth'] = csi300_df['日期Date'].dt.to_period('M')
csi300_monthly = csi300_df.groupby('YearMonth').last().reset_index()
csi300_monthly['日期Date'] = csi300_monthly['日期Date']

print(f"数据点: S&P 500={len(sp500_df)}, Nasdaq 100={len(nasdaq_df)}, 沪深300={len(csi300_monthly)}")

# ==================== 创建一个包含3个子图的图表 ====================
print("\n生成三合一柱状图...")
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(16, 20))

# ==================== 子图1: S&P 500 ====================

ax1.bar(sp500_df['Date'], sp500_df['Price'], width=20, 
        color='#1f77b4', alpha=0.8, edgecolor='#0d5a8f', linewidth=0.5)

ax1.set_title('S&P 500 总回报指数价格走势（月度）', fontsize=20, fontweight='bold', pad=20)
ax1.set_xlabel('日期', fontsize=14, fontweight='bold')
ax1.set_ylabel('指数价格', fontsize=14, fontweight='bold')
ax1.set_ylim(bottom=0)

# 添加网格
ax1.grid(True, alpha=0.3, linestyle='--', axis='y')
ax1.set_axisbelow(True)

# 格式化x轴
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax1.xaxis.set_major_locator(mdates.YearLocator())
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)

# 添加数值标注（每年1月）
for idx, row in sp500_df.iterrows():
    if row['Date'].month == 1:
        ax1.text(row['Date'], row['Price'], f"{int(row['Price']):,}", 
                ha='center', va='bottom', fontsize=8, rotation=0)

# ==================== 子图2: Nasdaq 100 ====================

ax2.bar(nasdaq_df['Date'], nasdaq_df['Price'], width=20, 
        color='#ff7f0e', alpha=0.8, edgecolor='#d66002', linewidth=0.5)

ax2.set_title('Nasdaq 100 总回报指数价格走势（月度）', fontsize=20, fontweight='bold', pad=20)
ax2.set_xlabel('日期', fontsize=14, fontweight='bold')
ax2.set_ylabel('指数价格', fontsize=14, fontweight='bold')
ax2.set_ylim(bottom=0)

# 添加网格
ax2.grid(True, alpha=0.3, linestyle='--', axis='y')
ax2.set_axisbelow(True)

# 格式化x轴
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax2.xaxis.set_major_locator(mdates.YearLocator())
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)

# 添加数值标注（每年1月）
for idx, row in nasdaq_df.iterrows():
    if row['Date'].month == 1:
        ax2.text(row['Date'], row['Price'], f"{int(row['Price']):,}", 
                ha='center', va='bottom', fontsize=8, rotation=0)

# ==================== 子图3: 沪深300 ====================

ax3.bar(csi300_monthly['日期Date'], csi300_monthly['收盘Close'], width=20, 
        color='#2ca02c', alpha=0.8, edgecolor='#1a7a1a', linewidth=0.5)

ax3.set_title('沪深300全收益指数价格走势（月度）', fontsize=20, fontweight='bold', pad=20)
ax3.set_xlabel('日期', fontsize=14, fontweight='bold')
ax3.set_ylabel('指数价格', fontsize=14, fontweight='bold')
ax3.set_ylim(bottom=0)

# 添加网格
ax3.grid(True, alpha=0.3, linestyle='--', axis='y')
ax3.set_axisbelow(True)

# 格式化x轴
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax3.xaxis.set_major_locator(mdates.YearLocator())
plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)

# 添加数值标注（每年1月）
for idx, row in csi300_monthly.iterrows():
    if row['日期Date'].month == 1:
        ax3.text(row['日期Date'], row['收盘Close'], f"{int(row['收盘Close']):,}", 
                ha='center', va='bottom', fontsize=8, rotation=0)

# ==================== 保存图表 ====================
plt.tight_layout()
output = '/Users/miaoji.norman/Desktop/投资/三大指数价格柱状图对比.png'
plt.savefig(output, dpi=300, bbox_inches='tight')
print(f"\n✓ 已保存: {output}")
plt.close()

print("\n" + "="*80)
print("三合一柱状图已生成！")
print("="*80)
print(f"  {output}")
print("="*80)

