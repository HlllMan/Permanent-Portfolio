#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
计算标普500、纳斯达克100和沪深300指数的年化收益率
包括：每年年化收益率、10年/5年/3年几何平均年化收益率
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


def calculate_annual_returns(df, price_col, date_col, index_name):
    """
    通用的收益率计算函数
    
    参数:
        df: DataFrame，包含历史数据
        price_col: 价格列名
        date_col: 日期列名
        index_name: 指数名称
    
    返回:
        combined_df: 包含年度收益率和多年期几何平均收益率的DataFrame
    """
    # 确保价格列是浮点数
    if df[price_col].dtype == 'object':
        df[price_col] = df[price_col].astype(str).str.replace(',', '').astype(float)
    
    # 删除缺失值
    df = df.dropna(subset=[date_col, price_col])
    
    # 按日期排序（从旧到新）
    df = df.sort_values(date_col).reset_index(drop=True)
    
    # 提取年份和月份
    df['Year'] = df[date_col].dt.year
    df['Month'] = df[date_col].dt.month
    
    print(f"\n{'='*80}")
    print(f"{index_name} 数据范围")
    print(f"{'='*80}")
    print(f"最早日期: {df[date_col].min()}")
    print(f"最晚日期: {df[date_col].max()}")
    print(f"总共数据点: {len(df)}")
    
    # 计算每年的年化收益率
    yearly_data = []
    years = sorted(df['Year'].unique())
    
    for year in years:
        year_df = df[df['Year'] == year]
        if len(year_df) > 0:
            start_price = year_df.iloc[0][price_col]
            end_price = year_df.iloc[-1][price_col]
            annual_return = ((end_price / start_price) - 1) * 100
            
            yearly_data.append({
                '期间类型': '年度收益',
                '期间': year,
                '起始价格': round(start_price, 2),
                '结束价格': round(end_price, 2),
                '年化收益率(%)': round(annual_return, 2)
            })
    
    # 计算几何平均年化收益率
    def geometric_mean_return(start_price, end_price, years):
        """计算几何平均年化收益率"""
        return ((end_price / start_price) ** (1 / years) - 1) * 100
    
    latest_date = df[date_col].max()
    latest_price = df[df[date_col] == latest_date][price_col].values[0]
    
    multi_period_data = []
    
    # 10年收益率
    start_year = years[0]
    date_10y = pd.Timestamp(f'{start_year}-01-01')
    df_10y = df[df[date_col] >= date_10y]
    if len(df_10y) > 0:
        price_10y = df_10y[price_col].values[0]
        years_10 = (latest_date - df_10y[date_col].values[0]) / pd.Timedelta(days=365.25)
        return_10y = geometric_mean_return(price_10y, latest_price, years_10)
        
        multi_period_data.append({
            '期间类型': '多年期几何平均',
            '期间': f'10年 ({start_year}-{latest_date.year})',
            '起始价格': round(price_10y, 2),
            '结束价格': round(latest_price, 2),
            '年化收益率(%)': round(return_10y, 2)
        })
    
    # 5年收益率
    date_5y_target = latest_date - pd.DateOffset(years=5)
    df_5y = df[df[date_col] >= date_5y_target]
    if len(df_5y) > 0:
        price_5y = df_5y[price_col].values[0]
        date_5y_actual = df_5y[date_col].values[0]
        years_5 = (latest_date - date_5y_actual) / pd.Timedelta(days=365.25)
        return_5y = geometric_mean_return(price_5y, latest_price, years_5)
        
        multi_period_data.append({
            '期间类型': '多年期几何平均',
            '期间': f'5年 ({pd.Timestamp(date_5y_actual).year}-{latest_date.year})',
            '起始价格': round(price_5y, 2),
            '结束价格': round(latest_price, 2),
            '年化收益率(%)': round(return_5y, 2)
        })
    
    # 3年收益率
    date_3y_target = latest_date - pd.DateOffset(years=3)
    df_3y = df[df[date_col] >= date_3y_target]
    if len(df_3y) > 0:
        price_3y = df_3y[price_col].values[0]
        date_3y_actual = df_3y[date_col].values[0]
        years_3 = (latest_date - date_3y_actual) / pd.Timedelta(days=365.25)
        return_3y = geometric_mean_return(price_3y, latest_price, years_3)
        
        multi_period_data.append({
            '期间类型': '多年期几何平均',
            '期间': f'3年 ({pd.Timestamp(date_3y_actual).year}-{latest_date.year})',
            '起始价格': round(price_3y, 2),
            '结束价格': round(latest_price, 2),
            '年化收益率(%)': round(return_3y, 2)
        })
    
    # 合并数据
    combined_df = pd.concat([pd.DataFrame(yearly_data), pd.DataFrame(multi_period_data)], ignore_index=True)
    
    return combined_df


# ==================== 处理 S&P 500 ====================
print("\n" + "="*80)
print("开始处理 S&P 500 总回报指数")
print("="*80)

sp500_df = pd.read_csv('/Users/miaoji.norman/Desktop/投资/S&P 500 TR Historical Data-2.csv')
sp500_df['Date'] = pd.to_datetime(sp500_df['Date'], format='%m/%d/%Y')

sp500_result = calculate_annual_returns(sp500_df, 'Price', 'Date', 'S&P 500 TR')

print("\n" + "="*80)
print("S&P 500 总回报指数 - 年化收益率分析汇总表")
print("="*80)
print(sp500_result.to_string(index=False))

sp500_output = '/Users/miaoji.norman/Desktop/投资/SP500_年化收益率汇总表.csv'
sp500_result.to_csv(sp500_output, index=False, encoding='utf-8-sig')
print(f"\n✓ S&P 500汇总表已保存至: {sp500_output}")


# ==================== 处理 Nasdaq 100 ====================
print("\n\n" + "="*80)
print("开始处理 Nasdaq 100 总回报指数")
print("="*80)

nasdaq_df = pd.read_csv('/Users/miaoji.norman/Desktop/投资/Nasdaq 100 TR Historical Data.csv')
nasdaq_df['Date'] = pd.to_datetime(nasdaq_df['Date'], format='%m/%d/%Y')

nasdaq_result = calculate_annual_returns(nasdaq_df, 'Price', 'Date', 'Nasdaq 100 TR')

print("\n" + "="*80)
print("Nasdaq 100 总回报指数 - 年化收益率分析汇总表")
print("="*80)
print(nasdaq_result.to_string(index=False))

nasdaq_output = '/Users/miaoji.norman/Desktop/投资/Nasdaq100_年化收益率汇总表.csv'
nasdaq_result.to_csv(nasdaq_output, index=False, encoding='utf-8-sig')
print(f"\n✓ Nasdaq 100汇总表已保存至: {nasdaq_output}")


# ==================== 处理 沪深300 ====================
print("\n\n" + "="*80)
print("开始处理 沪深300全收益指数")
print("="*80)

csi300_df = pd.read_csv('/Users/miaoji.norman/Desktop/投资/沪深300TR historical data.csv')
csi300_df['日期Date'] = pd.to_datetime(csi300_df['日期Date'], format='%Y%m%d')
csi300_df['收盘Close'] = pd.to_numeric(csi300_df['收盘Close'], errors='coerce')

csi300_result = calculate_annual_returns(csi300_df, '收盘Close', '日期Date', '沪深300 TR')

print("\n" + "="*80)
print("沪深300全收益指数 - 年化收益率分析汇总表")
print("="*80)
print(csi300_result.to_string(index=False))

csi300_output = '/Users/miaoji.norman/Desktop/投资/沪深300_年化收益率汇总表.csv'
csi300_result.to_csv(csi300_output, index=False, encoding='utf-8-sig')
print(f"\n✓ 沪深300汇总表已保存至: {csi300_output}")


# ==================== 汇总对比 ====================
print("\n\n" + "="*80)
print("三大指数10年/5年/3年几何平均年化收益率对比")
print("="*80)

comparison_data = []

# 提取多年期数据
for result, name in [(sp500_result, 'S&P 500 TR'), 
                      (nasdaq_result, 'Nasdaq 100 TR'), 
                      (csi300_result, '沪深300 TR')]:
    multi_year = result[result['期间类型'] == '多年期几何平均']
    
    returns = {}
    for _, row in multi_year.iterrows():
        if '10年' in str(row['期间']):
            returns['10年'] = row['年化收益率(%)']
        elif '5年' in str(row['期间']):
            returns['5年'] = row['年化收益率(%)']
        elif '3年' in str(row['期间']):
            returns['3年'] = row['年化收益率(%)']
    
    comparison_data.append({
        '指数': name,
        '10年年化(%)': returns.get('10年', 'N/A'),
        '5年年化(%)': returns.get('5年', 'N/A'),
        '3年年化(%)': returns.get('3年', 'N/A')
    })

comparison_df = pd.DataFrame(comparison_data)
print(comparison_df.to_string(index=False))

comparison_output = '/Users/miaoji.norman/Desktop/投资/三大指数对比.csv'
comparison_df.to_csv(comparison_output, index=False, encoding='utf-8-sig')
print(f"\n✓ 对比表已保存至: {comparison_output}")

print("\n" + "="*80)
print("所有处理完成！")
print("="*80)

