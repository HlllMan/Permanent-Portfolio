# Permanent Portfolio Analysis | 永久投资组合分析

A flexible, configuration-driven tool for analyzing permanent portfolio strategies with different asset allocations.

一个灵活的、配置驱动的永久投资组合分析工具，可以分析不同资产配置策略的表现。

## ✨ Features | 特性

- 🎯 **Configuration-Driven** | **配置驱动**: Easily test different portfolio strategies by modifying JSON config files
- 📊 **Multiple Metrics** | **多维度指标**: Annual returns, geometric average returns, max drawdown, recovery time
- 🔄 **Annual Rebalancing** | **年度再平衡**: Simulates portfolio rebalancing at customizable intervals
- 📈 **Multiple Assets Support** | **多资产支持**: Stocks (S&P 500, Nasdaq 100, CSI 300), Bonds, Gold, Cash
- 📁 **Automatic Naming** | **自动命名**: Output files are automatically named based on asset allocation
- 🌐 **Multi-Market** | **多市场**: Support for US and Chinese markets

## 🚀 Quick Start | 快速开始

```bash
# Clone the repository | 克隆仓库
git clone https://github.com/Hlllman/Permanent-Portfolio.git
cd Permanent-Portfolio

# Run with default configuration | 使用默认配置运行
python3 code/永久投资组合分析_配置版.py

# Run with specific configuration | 使用指定配置运行
python3 code/永久投资组合分析_配置版.py config/永久投资组合_美债版_config.json
```

## 📂 Project Structure | 项目结构

```
Permanent-Portfolio/
├── config/              # Configuration files | 配置文件
│   ├── 永久投资组合_config.json
│   ├── 永久投资组合_美债版_config.json
│   ├── Nas_易方达债_config.json
│   └── 沪深_易方达债_config.json
├── code/               # Python scripts | Python脚本
│   └── 永久投资组合分析_配置版.py
├── data/               # Market data (CSV files) | 市场数据
├── 永久投资组合/        # Analysis results | 分析结果
└── README.md
```

## 📊 Example Results | 示例结果

Current configurations generate comprehensive analysis including:
- Annual returns for each year
- Geometric average returns (3, 5, 10, 15, 20 years)
- Maximum drawdown and recovery time
- Strategy configuration details

当前配置生成的完整分析包括：
- 每年的年度收益率
- 几何平均年化收益率（3、5、10、15、20年）
- 最大回撤和修复时间
- 策略配置详情

---

## 📖 Detailed Documentation | 详细文档

## 使用方法

### 1. 基本使用

```bash
# 使用默认配置（永久投资组合_config.json）
python3 code/永久投资组合分析_配置版.py

# 使用指定配置文件
python3 code/永久投资组合分析_配置版.py config/永久投资组合_美债版_config.json
```

### 2. 配置文件格式

配置文件使用JSON格式，包含以下字段：

```json
{
  "portfolio_name": "投资组合名称",
  "rebalance_frequency": "再平衡频率（年度/季度/月度）",
  "assets": {
    "stock": { ... },   // 股票象限
    "bond": { ... },    // 债券象限
    "gold": { ... },    // 黄金象限
    "cash": { ... }     // 现金象限
  }
}
```

### 3. 资产配置字段

#### 常规资产（股票/债券/黄金）

```json
{
  "name": "简称",              // 用于文件名，如：S&P、Nas、沪深、黄金、美债、易方达债
  "full_name": "完整名称",     // 显示在表格中
  "data_file": "数据文件路径",  // 相对于投资文件夹的路径
  "date_format": "日期格式",    // 如：%m/%d/%Y、%Y-%m-%d、%b %y
  "date_column": "日期列名",    // CSV文件中的日期列名
  "price_column": "价格列名",   // CSV文件中的价格列名
  "weight": 0.25               // 配置比例（0-1之间）
}
```

#### 现金资产

```json
{
  "name": "现金",
  "full_name": "现金 (1%年化)",
  "annual_return": 0.01,       // 年化收益率
  "weight": 0.25
}
```

### 4. 可用的简称

- **股票**: S&P、Nas、沪深
- **债券**: 美债、易方达债、中债
- **黄金**: 黄金
- **现金**: 现金

### 5. 输出文件

生成的CSV文件会保存到 `永久投资组合/` 文件夹，文件名格式：

```
{股票}_{债券}_{黄金}_{现金}.csv
```

例如：
- `S&P25_易方达债25_黄金25_现金25.csv`
- `S&P25_美债25_黄金25_现金25.csv`

### 6. 示例配置

#### 示例1：易方达债券版本
使用配置文件：`永久投资组合_config.json`
- 股票：S&P 500 TR (25%)
- 债券：易方达增强回报债券 (25%)
- 黄金：黄金 (25%)
- 现金：1%年化 (25%)

#### 示例2：美债版本
使用配置文件：`永久投资组合_美债版_config.json`
- 股票：S&P 500 TR (25%)
- 债券：美国长债 TLT (25%)
- 黄金：黄金 (25%)
- 现金：1%年化 (25%)

### 7. 自定义配置

要创建新的投资组合配置：

1. 复制现有配置文件
2. 修改资产配置和比例
3. 运行程序时指定新配置文件

例如，创建50%股票、50%债券的配置：

```json
{
  "portfolio_name": "股债50-50",
  "rebalance_frequency": "年度",
  "assets": {
    "stock": {
      "name": "S&P",
      "full_name": "S&P 500 TR",
      "data_file": "data/S&P 500 TR Historical Data.csv",
      "date_format": "%m/%d/%Y",
      "date_column": "Date",
      "price_column": "Price",
      "weight": 0.50
    },
    "bond": {
      "name": "易方达债",
      "full_name": "易方达增强回报债券",
      "data_file": "data/易方达增强回报债券110017 Historical Data.csv",
      "date_format": "%b %y",
      "date_column": "Date",
      "price_column": "Price",
      "weight": 0.50
    }
  }
}
```

注意：
- 所有资产的weight总和应该等于1.0
- 至少需要配置一个资产
- 可以只使用部分象限（如只有股票和债券）

