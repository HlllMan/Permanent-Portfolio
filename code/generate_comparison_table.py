#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成三大指数横向对比表
左边是年份/期间，右边三列分别是三个指数的年化收益率
"""

import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# 读取三个汇总表
sp500_df = pd.read_csv('/Users/miaoji.norman/Desktop/投资/SP500_年化收益率汇总表.csv')
nasdaq_df = pd.read_csv('/Users/miaoji.norman/Desktop/投资/Nasdaq100_年化收益率汇总表.csv')
csi300_df = pd.read_csv('/Users/miaoji.norman/Desktop/投资/沪深300_年化收益率汇总表.csv')

print("="*80)
print("开始生成三大指数横向对比表")
print("="*80)

# 分离年度收益和多年期几何平均
sp500_annual = sp500_df[sp500_df['期间类型'] == '年度收益'].copy()
sp500_multi = sp500_df[sp500_df['期间类型'] == '多年期几何平均'].copy()

nasdaq_annual = nasdaq_df[nasdaq_df['期间类型'] == '年度收益'].copy()
nasdaq_multi = nasdaq_df[nasdaq_df['期间类型'] == '多年期几何平均'].copy()

csi300_annual = csi300_df[csi300_df['期间类型'] == '年度收益'].copy()
csi300_multi = csi300_df[csi300_df['期间类型'] == '多年期几何平均'].copy()

# ==================== 构建年度收益对比表 ====================
# 统一转换期间列为整数类型
sp500_annual['期间'] = sp500_annual['期间'].astype(int)
nasdaq_annual['期间'] = nasdaq_annual['期间'].astype(int)
csi300_annual['期间'] = csi300_annual['期间'].astype(int)

# 获取所有年份的并集
all_years = set()
all_years.update(sp500_annual['期间'].tolist())
all_years.update(nasdaq_annual['期间'].tolist())
all_years.update(csi300_annual['期间'].tolist())
all_years = sorted(all_years)

# 创建年度对比数据
annual_comparison = []
for year in all_years:
    row = {'年份': year}
    
    # S&P 500
    sp_row = sp500_annual[sp500_annual['期间'] == year]
    if len(sp_row) > 0:
        row['S&P 500 TR (%)'] = sp_row['年化收益率(%)'].values[0]
    else:
        row['S&P 500 TR (%)'] = '-'
    
    # Nasdaq 100
    nq_row = nasdaq_annual[nasdaq_annual['期间'] == year]
    if len(nq_row) > 0:
        row['Nasdaq 100 TR (%)'] = nq_row['年化收益率(%)'].values[0]
    else:
        row['Nasdaq 100 TR (%)'] = '-'
    
    # 沪深300
    csi_row = csi300_annual[csi300_annual['期间'] == year]
    if len(csi_row) > 0:
        row['沪深300 TR (%)'] = csi_row['年化收益率(%)'].values[0]
    else:
        row['沪深300 TR (%)'] = '-'
    
    annual_comparison.append(row)

annual_comparison_df = pd.DataFrame(annual_comparison)

# ==================== 构建多年期对比表 ====================
# 提取多年期数据
multi_periods = ['10年', '5年', '3年']
multi_comparison = []

for period in multi_periods:
    row = {'期间': f'{period}几何平均'}
    
    # S&P 500
    sp_row = sp500_multi[sp500_multi['期间'].str.contains(period, na=False)]
    row['S&P 500 TR (%)'] = sp_row['年化收益率(%)'].values[0] if len(sp_row) > 0 else '-'
    
    # Nasdaq 100
    nq_row = nasdaq_multi[nasdaq_multi['期间'].str.contains(period, na=False)]
    row['Nasdaq 100 TR (%)'] = nq_row['年化收益率(%)'].values[0] if len(nq_row) > 0 else '-'
    
    # 沪深300
    csi_row = csi300_multi[csi300_multi['期间'].str.contains(period, na=False)]
    row['沪深300 TR (%)'] = csi_row['年化收益率(%)'].values[0] if len(csi_row) > 0 else '-'
    
    multi_comparison.append(row)

multi_comparison_df = pd.DataFrame(multi_comparison)

# ==================== 合并两个表 ====================
# 年度表添加类型列
annual_comparison_df.insert(0, '类别', '年度收益')
annual_comparison_df.rename(columns={'年份': '期间'}, inplace=True)

# 多年期表添加类型列
multi_comparison_df.insert(0, '类别', '多年期几何平均')

# 合并
final_df = pd.concat([annual_comparison_df, multi_comparison_df], ignore_index=True)

# ==================== 显示和保存 ====================
print("\n" + "="*80)
print("三大指数年化收益率横向对比表")
print("="*80)
print(final_df.to_string(index=False))

# 保存为CSV
output_file = '/Users/miaoji.norman/Desktop/投资/三大指数年化收益率对比表.csv'
final_df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\n✓ 对比表已保存至: {output_file}")
print(f"✓ 共 {len(final_df)} 行数据")
print("="*80)

