#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
永久投资组合分析 - 配置驱动版
通过修改config文件即可分析不同的投资组合策略
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def load_config(config_path):
    """加载配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

def load_asset_data(asset, base_path):
    """根据配置加载资产数据"""
    if asset.get('type') == 'cash':
        # 现金资产，返回None，后续特殊处理
        return None
    
    # 常规资产数据
    file_path = os.path.join(base_path, asset['data_file'])
    df = pd.read_csv(file_path)
    
    # 转换日期
    df['Date'] = pd.to_datetime(df[asset['date_column']], 
                                 format=asset['date_format'])
    
    # 转换价格
    df['Price'] = df[asset['price_column']].astype(str).str.replace(',', '').astype(float)
    
    return df[['Date', 'Price']].sort_values('Date')

def generate_filename(config):
    """根据配置生成文件名"""
    parts = []
    
    for asset in config['assets']:
        name = asset['name']
        weight = int(asset['weight'] * 100)
        parts.append(f"{name}{weight}")
    
    filename = '_'.join(parts) + '.csv'
    return filename

def analyze_portfolio(config_path):
    """分析投资组合"""
    # 获取基础路径
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(config_path)))
    
    # 加载配置
    print("="*80)
    print("读取配置文件...")
    config = load_config(config_path)
    
    # 显示配置信息
    print(f"\n投资组合: {config['portfolio_name']}")
    print(f"再平衡频率: {config['rebalance_frequency']}")
    print("\n资产配置:")
    for asset in config['assets']:
        print(f"  {asset['name']}: {asset['weight']*100:.0f}%")
    
    print("\n" + "="*80)
    print("加载数据...")
    
    # 加载各资产数据
    assets_data = {}
    cash_assets = []
    
    for i, asset in enumerate(config['assets']):
        asset_id = f"asset_{i}"
        
        if asset.get('type') == 'cash':
            cash_assets.append((asset_id, asset))
            continue
        
        df = load_asset_data(asset, base_path)
        if df is not None:
            assets_data[asset_id] = {
                'data': df,
                'config': asset
            }
            print(f"{asset['name']}数据: {len(df)}行, {df['Date'].min()} 至 {df['Date'].max()}")
    
    # 转换为月度数据并合并
    print("\n数据预处理...")
    monthly_data = {}
    
    for asset_id, asset_info in assets_data.items():
        df = asset_info['data']
        monthly = df.set_index('Date').resample('ME').last().dropna()
        monthly.columns = [asset_id]
        monthly_data[asset_id] = monthly
    
    # 合并所有资产数据
    if len(monthly_data) > 0:
        portfolio_df = monthly_data[list(monthly_data.keys())[0]]
        for asset_id in list(monthly_data.keys())[1:]:
            portfolio_df = pd.merge(portfolio_df, monthly_data[asset_id], 
                                   left_index=True, right_index=True, how='inner')
    else:
        print("错误：没有可用的资产数据")
        return
    
    # 添加现金资产（固定收益率）
    for asset_id, asset in cash_assets:
        annual_return = asset['annual_return']
        portfolio_df[asset_id] = 100 * ((1 + annual_return) ** (1/12)) ** np.arange(len(portfolio_df))
    
    print(f"合并后数据: {len(portfolio_df)}行")
    print(f"数据范围: {portfolio_df.index.min()} 至 {portfolio_df.index.max()}")
    
    # 构建投资组合
    print("\n" + "="*80)
    print("构建投资组合（每年再平衡）...")
    
    initial_value = 10000
    portfolio_df['Year'] = portfolio_df.index.year
    portfolio_df['Portfolio_value'] = 0.0
    
    # 初始化每个资产的份额
    current_shares = {}
    for i in range(len(config['assets'])):
        current_shares[f"asset_{i}"] = 0
    
    years = sorted(portfolio_df['Year'].unique())
    rebalance_count = len(years) - 1
    print(f"再平衡次数: {rebalance_count}")
    
    for idx in portfolio_df.index:
        year = portfolio_df.loc[idx, 'Year']
        
        # 年初再平衡
        first_month = portfolio_df[portfolio_df['Year'] == year].index[0]
        if idx == first_month:
            if year == years[0]:
                current_total = initial_value
            else:
                prev_idx = portfolio_df[portfolio_df.index < idx].index[-1]
                current_total = portfolio_df.loc[prev_idx, 'Portfolio_value']
            
            # 再平衡：按权重分配
            for i, asset in enumerate(config['assets']):
                asset_id = f"asset_{i}"
                amount = current_total * asset['weight']
                current_shares[asset_id] = amount / portfolio_df.loc[idx, asset_id]
        
        # 计算当前总值
        total_value = 0
        for i in range(len(config['assets'])):
            asset_id = f"asset_{i}"
            total_value += current_shares[asset_id] * portfolio_df.loc[idx, asset_id]
        portfolio_df.loc[idx, 'Portfolio_value'] = total_value
    
    # 计算年度收益率
    print("\n计算年度收益率...")
    annual_returns = []
    for year in years:
        year_data = portfolio_df[portfolio_df['Year'] == year]
        if len(year_data) > 0:
            start_value = year_data['Portfolio_value'].iloc[0]
            end_value = year_data['Portfolio_value'].iloc[-1]
            annual_return = (end_value / start_value - 1) * 100
            
            annual_returns.append({
                '年份': year,
                '年初投资组合价值': round(start_value, 2),
                '年末投资组合价值': round(end_value, 2),
                '年化收益率(%)': round(annual_return, 2)
            })
    
    annual_returns_df = pd.DataFrame(annual_returns)
    print("\n年度收益率:")
    print(annual_returns_df.to_string(index=False))
    
    # 计算最大回撤
    print("\n\n计算最大回撤...")
    portfolio_df['Peak'] = portfolio_df['Portfolio_value'].cummax()
    portfolio_df['Drawdown'] = (portfolio_df['Portfolio_value'] / portfolio_df['Peak'] - 1) * 100
    
    max_drawdown = portfolio_df['Drawdown'].min()
    max_drawdown_date = portfolio_df['Drawdown'].idxmin()
    peak_date = portfolio_df[portfolio_df.index <= max_drawdown_date]['Peak'].idxmax()
    
    # 找到回撤修复日期
    recovery_data = portfolio_df[portfolio_df.index > max_drawdown_date]
    recovery_data = recovery_data[recovery_data['Portfolio_value'] >= portfolio_df.loc[peak_date, 'Peak']]
    
    if len(recovery_data) > 0:
        recovery_date = recovery_data.index[0]
        recovery_months = (recovery_date.year - max_drawdown_date.year) * 12 + (recovery_date.month - max_drawdown_date.month)
    else:
        recovery_date = None
        recovery_months = None
    
    print(f"最大回撤: {max_drawdown:.2f}%")
    print(f"最大回撤日期: {max_drawdown_date.strftime('%Y-%m')}")
    print(f"峰值日期: {peak_date.strftime('%Y-%m')}")
    if recovery_date:
        print(f"修复日期: {recovery_date.strftime('%Y-%m')}")
        print(f"修复时间: {recovery_months} 个月")
    else:
        print(f"修复日期: 尚未修复")
    
    # 计算多年期收益率
    print("\n\n计算多年期几何平均收益率...")
    
    def calc_geometric_return(start_value, end_value, years):
        return ((end_value / start_value) ** (1 / years) - 1) * 100
    
    latest_date = portfolio_df.index[-1]
    latest_value = portfolio_df['Portfolio_value'].iloc[-1]
    available_years = (latest_date.year - portfolio_df.index[0].year) + (latest_date.month - portfolio_df.index[0].month) / 12
    
    multi_period_returns = []
    for period_years in [20, 15, 10, 5, 3]:
        if available_years >= period_years:
            start_date_target = latest_date - pd.DateOffset(years=period_years)
            start_data = portfolio_df[portfolio_df.index >= start_date_target]
            
            if len(start_data) > 0:
                start_date_actual = start_data.index[0]
                start_value = start_data['Portfolio_value'].iloc[0]
                actual_years = (latest_date.year - start_date_actual.year) + (latest_date.month - start_date_actual.month) / 12
                
                geometric_return = calc_geometric_return(start_value, latest_value, actual_years)
                
                multi_period_returns.append({
                    '期间': f'{period_years}年',
                    '起始日期': start_date_actual.strftime('%Y-%m'),
                    '结束日期': latest_date.strftime('%Y-%m'),
                    '起始价值': round(start_value, 2),
                    '结束价值': round(latest_value, 2),
                    '几何平均年化收益率(%)': round(geometric_return, 2)
                })
        else:
            multi_period_returns.append({
                '期间': f'{period_years}年',
                '起始日期': '数据不足',
                '结束日期': '-',
                '起始价值': '-',
                '结束价值': '-',
                '几何平均年化收益率(%)': '-'
            })
    
    multi_period_df = pd.DataFrame(multi_period_returns)
    print("\n多年期几何平均年化收益率:")
    print(multi_period_df.to_string(index=False))
    
    # 整理综合表
    print("\n\n整理综合分析表...")
    
    # 策略配置信息
    strategy_info = []
    for i, asset in enumerate(config['assets']):
        strategy_info.append({
            '类别': '策略配置',
            '期间': f'资产{i+1}',
            '起始价值': asset['full_name'],
            '结束价值': f"{int(asset['weight']*100)}%",
            '年化收益率(%)': ''
        })
    
    strategy_info.append({
        '类别': '策略说明',
        '期间': '再平衡频率',
        '起始价值': config['rebalance_frequency'] + '1次',
        '结束价值': '',
        '年化收益率(%)': ''
    })
    
    strategy_df = pd.DataFrame(strategy_info)
    
    # 年度收益
    annual_summary = annual_returns_df.copy()
    annual_summary.insert(0, '类别', '年度收益')
    annual_summary.rename(columns={
        '年份': '期间',
        '年初投资组合价值': '起始价值',
        '年末投资组合价值': '结束价值',
        '年化收益率(%)': '年化收益率(%)'
    }, inplace=True)
    annual_summary = annual_summary[['类别', '期间', '起始价值', '结束价值', '年化收益率(%)']]
    
    # 多年期收益
    multi_period_summary = multi_period_df[multi_period_df['起始日期'] != '数据不足'].copy()
    multi_period_summary.insert(0, '类别', '多年期几何平均')
    multi_period_summary['期间'] = (multi_period_summary['期间'] + ' (' + 
                                  multi_period_summary['起始日期'] + '至' + 
                                  multi_period_summary['结束日期'] + ')')
    multi_period_summary.rename(columns={
        '几何平均年化收益率(%)': '年化收益率(%)'
    }, inplace=True)
    multi_period_summary = multi_period_summary[['类别', '期间', '起始价值', '结束价值', '年化收益率(%)']]
    
    # 风险指标
    risk_summary = pd.DataFrame([{
        '类别': '风险指标',
        '期间': '最大回撤',
        '起始价值': f"{peak_date.strftime('%Y-%m')} (峰值)",
        '结束价值': f"{max_drawdown_date.strftime('%Y-%m')} (谷底)",
        '年化收益率(%)': round(max_drawdown, 2)
    }, {
        '类别': '风险指标',
        '期间': '修复时间',
        '起始价值': max_drawdown_date.strftime('%Y-%m'),
        '结束价值': recovery_date.strftime('%Y-%m') if recovery_date else '尚未修复',
        '年化收益率(%)': f"{recovery_months}个月" if recovery_months else '-'
    }])
    
    # 合并所有部分
    combined_df = pd.concat([strategy_df, annual_summary, multi_period_summary, risk_summary], 
                            ignore_index=True)
    
    # 保存结果
    output_dir = os.path.join(base_path, '永久投资组合')
    os.makedirs(output_dir, exist_ok=True)
    
    filename = generate_filename(config)
    output_file = os.path.join(output_dir, filename)
    combined_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print("\n" + "="*80)
    print("永久投资组合综合分析表")
    print("="*80)
    print(combined_df.to_string(index=False))
    print("\n" + "="*80)
    print(f"✓ 综合分析表已保存: {output_file}")
    print(f"✓ 共 {len(combined_df)} 行数据")
    print("="*80)
    print("\n分析完成！")
    print("="*80)

if __name__ == "__main__":
    import sys
    
    # 可以通过命令行参数指定配置文件
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        print("请指定配置文件路径")
        print("用法: python3 永久投资组合分析_配置版.py config/配置文件.json")
        sys.exit(1)
    
    analyze_portfolio(config_path)

