import os
import json
import time
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
import urllib3
from openai import OpenAI

# 禁用SSL警告（仅用于测试环境）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class InvestmentAdvisor:
    def __init__(self):
        # 使用OpenAI SDK调用DeepSeek API
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com/v1"
        )
        self.model = "deepseek-reasoner"
        self.root_path = None
        self.history_dir = None
        self.money_dir = None
        self.session_id = None
        self.system_type = None
        self.financial_data = {}
        self.previous_portfolios = []  # 存储历史投资组合
        self.config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".finance_config.json")

    def check_api_key(self):
        """检查API密钥"""
        if not self.api_key:
            raise ValueError("❌ 错误: 未设置 DEEPSEEK_API_KEY 环境变量")
        if not self.api_key.startswith("sk-"):
            print("⚠️  API密钥格式可能不正确")
        else:
            print("✅ API密钥格式正确")

    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.root_path = config.get('root_path')
                    if self.root_path and os.path.exists(self.root_path):
                        print(f"✅ 从缓存加载根目录: {self.root_path}")
                        return True
                    else:
                        print("⚠️  缓存中的根目录不存在，将重新输入")
            except Exception as e:
                print(f"⚠️  读取配置文件失败: {str(e)}")
        return False

    def save_config(self):
        """保存配置到文件"""
        if self.root_path:
            config = {
                'root_path': self.root_path,
                'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            try:
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                print(f"✅ 配置已保存到: {self.config_file}")
                return True
            except Exception as e:
                print(f"⚠️  保存配置文件失败: {str(e)}")
        return False

    def initialize_system(self):
        """初始化系统"""
        print("正在启动投资顾问系统...")
        self.check_api_key()
        
        # 尝试从缓存加载配置
        if self.load_config():
            print(f"✅ 使用缓存的根目录: {self.root_path}")
        else:
            print("=== 投资顾问系统初始化 ===")
            # 获取根目录路径
            self.root_path = input("请输入根目录路径: ").strip()
            if not os.path.exists(self.root_path):
                print(f"📁 创建目录: {self.root_path}")
                os.makedirs(self.root_path)
            
            # 保存配置
            if not self.save_config():
                print("⚠️  警告: 无法保存配置，下次运行需要重新输入根目录")
        
        # 选择系统类型
        print("\n请选择您的电脑系统:")
        print("1. Windows")
        print("2. Mac")
        print("3. Linux")
        
        system_choice = input("请输入选择 (1/2/3): ").strip()
        system_map = {"1": "Windows", "2": "Mac", "3": "Linux"}
        self.system_type = system_map.get(system_choice, "Windows")
        
        # 创建目录结构
        self.history_dir = os.path.join(self.root_path, "history")
        self.money_dir = os.path.join(self.root_path, "money")
        
        for directory in [self.history_dir, self.money_dir]:
            if not os.path.exists(directory):
                print(f"📁 创建目录: {directory}")
                os.makedirs(directory)
        
        # 生成会话ID
        session_folders = [f for f in os.listdir(self.history_dir) if os.path.isdir(os.path.join(self.history_dir, f))]
        self.session_id = len(session_folders) + 1
        
        # 加载历史投资组合
        self.load_previous_portfolios()
        
        print(f"\n系统初始化完成！")
        print(f"系统类型: {self.system_type}")
        print(f"会话序号: {self.session_id}")
        print(f"历史记录将保存在: {self.history_dir}")
        print(f"财务数据将保存在: {self.money_dir}")
        print(f"发现历史投资组合数量: {len(self.previous_portfolios)}")

    def load_previous_portfolios(self):
        """加载历史投资组合"""
        money_file = os.path.join(self.money_dir, "financial_data.json")
        
        if os.path.exists(money_file):
            try:
                with open(money_file, 'r', encoding='utf-8') as f:
                    all_data = json.load(f)
                    self.previous_portfolios = all_data
                    print(f"📊 已加载 {len(all_data)} 个历史投资组合")
            except Exception as e:
                print(f"⚠️  读取历史数据时出错: {str(e)}")
                self.previous_portfolios = []
        else:
            print("📊 无历史投资记录，这是第一次运行")
            self.previous_portfolios = []

    def collect_financial_info(self):
        """收集财务信息"""
        print("\n" + "="*50)
        print("开始第 {} 次月度投资会话".format(self.session_id))
        print("="*50 + "\n")
        
        print("=== 投资信息收集 ===")
        
        # 收入信息
        while True:
            try:
                monthly_income = float(input("本月总收入 (人民币): "))
                if monthly_income <= 0:
                    print("❌ 收入必须为正数，请重新输入")
                    continue
                break
            except ValueError:
                print("❌ 请输入有效的数字")
        
        # 支出信息
        while True:
            try:
                living_expenses = float(input("本月生活费支出: "))
                if living_expenses <= 0:
                    print("❌ 支出必须为正数，请重新输入")
                    continue
                if living_expenses >= monthly_income:
                    print("❌ 支出不能大于或等于收入，请重新输入")
                    continue
                break
            except ValueError:
                print("❌ 请输入有效的数字")
        
        # 计算可用资金
        available_for_investment = monthly_income - living_expenses
        
        print(f"\n💰 财务概览:")
        print(f"  • 本月总收入: {monthly_income:,.0f}元")
        print(f"  • 本月支出: {living_expenses:,.0f}元")
        print(f"  • 可用于投资: {available_for_investment:,.0f}元")
        print(f"  • 当前现金储备: {available_for_investment:,.0f}元")
        
        # 市场状况
        print("\n请选择本月市场状况:")
        market_options = {
            "1": "市场平稳",
            "2": "市场上涨", 
            "3": "市场下跌",
            "4": "波动剧烈",
            "5": "熊市",
            "6": "牛市"
        }
        
        for key, value in market_options.items():
            print(f"{key}. {value}")
        
        market_choice = input("请输入选择 (1-6): ").strip()
        market_condition = market_options.get(market_choice, "市场平稳")
        
        # 投资心态
        print("\n请选择当前投资心态:")
        mood_options = {
            "1": "平静",
            "2": "焦虑",
            "3": "兴奋", 
            "4": "困惑",
            "5": "谨慎",
            "6": "乐观"
        }
        
        for key, value in mood_options.items():
            print(f"{key}. {value}")
        
        mood_choice = input("请输入选择 (1-6): ").strip()
        investment_mood = mood_options.get(mood_choice, "平静")
        
        # 特殊说明
        special_notes = input("\n特殊说明 (如大额支出、收入变化等，直接回车跳过): ").strip()
        
        # 存储财务数据
        self.financial_data = {
            "session_id": self.session_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "monthly_income": monthly_income,
            "living_expenses": living_expenses,
            "available_for_investment": available_for_investment,
            "market_condition": market_condition,
            "investment_mood": investment_mood,
            "special_notes": special_notes,
            "cash_reserve": available_for_investment
        }
        
        return self.financial_data

    def test_api_connection(self):
        """测试API连接"""
        print("🔍 测试API连接...")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": "Hello"},
                ],
                stream=False
            )
            
            print(f"✅ API连接测试成功")
            print(f"模型: {response.model}")
            return True
            
        except Exception as e:
            print(f"❌ API连接测试失败: {str(e)}")
            return False

    def call_deepseek_api(self, user_message, max_retries=3):
        """使用OpenAI SDK调用DeepSeek API"""
        
        for attempt in range(max_retries):
            try:
                print(f"🔄 正在发送请求到DeepSeek API... (尝试 {attempt + 1}/{max_retries})")
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "你是一个专业的投资顾问，专门为加拿大护照持有者在中国境内提供投资建议。"},
                        {"role": "user", "content": user_message},
                    ],
                    stream=False,
                    temperature=0.7
                )
                
                print(f"✅ API响应解析成功")
                print(f"模型: {response.model}")
                
                message_content = response.choices[0].message.content
                if message_content and len(message_content.strip()) > 0:
                    print("✅ AI投资建议生成成功！")
                    return message_content
                else:
                    print("❌ API返回空内容")
                    raise ValueError("API返回了空内容")
                    
            except Exception as e:
                print(f"❌ API调用失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 5
                    print(f"⏳ 等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise ConnectionError(f"❌ 所有重试均失败: {str(e)}")
        
        raise ConnectionError("❌ API调用失败，请检查网络连接和API密钥")

    def get_fallback_recommendation(self, financial_data):
        """当API不可用时提供备用投资建议"""
        print("⚠️  API不可用，使用备用投资建议系统")
        
        monthly_income = financial_data['monthly_income']
        living_expenses = financial_data['living_expenses']
        available_for_investment = financial_data['available_for_investment']
        market_condition = financial_data['market_condition']
        investment_mood = financial_data['investment_mood']
        
        # 根据市场状况和心态调整配置
        if market_condition in ["市场平稳", "牛市"] and investment_mood in ["平静", "乐观"]:
            # 积极配置
            equity_percent = 50
            fixed_income_percent = 30
            crypto_percent = 20
        elif market_condition in ["市场下跌", "熊市"] or investment_mood in ["焦虑", "谨慎"]:
            # 保守配置
            equity_percent = 30
            fixed_income_percent = 40
            crypto_percent = 30
        else:
            # 平衡配置
            equity_percent = 40
            fixed_income_percent = 35
            crypto_percent = 25
        
        equity_amount = available_for_investment * equity_percent / 100
        fixed_income_amount = available_for_investment * fixed_income_percent / 100
        crypto_amount = available_for_investment * crypto_percent / 100
        
        advice = f"""
# 投资顾问报告 - 备用建议

## 基于您的个人情况分析
考虑到您是加拿大护照持有者，目前在中国境内，结合您的八字信息（2002年11月26日出生），建议采用以下配置：

### 1. 具体的资产配置建议

#### 权益类资产（{equity_percent}%，{equity_amount:,.0f}元/月）
- **建议**: 投资于中证500指数基金 (代码: 510500)
- **理由**: 中证500代表中国中型公司，增长潜力较好。从八字角度看，五行属木，适合投资成长型资产。
- **平台**: Interactive Brokers - https://www.interactivebrokers.com/
- **投资金额**: {equity_amount:,.0f}元

#### 固定收益类资产（{fixed_income_percent}%，{fixed_income_amount:,.0f}元/月）
- **建议**: 投资于中国政府债券ETF (代码: 019547)
- **理由**: 提供稳定收益，风险较低。五行属金，有助于平衡投资组合。
- **平台**: 富途牛牛 - https://www.futunn.com/
- **投资金额**: {fixed_income_amount:,.0f}元

#### 加密货币资产（{crypto_percent}%，{crypto_amount:,.0f}元/月）
- **建议**: 比特币（使用现有冷钱包存储）
- **理由**: 高流动性，全球通用资产。五行属水，有利于资金流动和财富增长。
- **平台**: 比特币冷钱包
- **交易平台**: Binance - https://www.binance.com/
- **投资金额**: {crypto_amount:,.0f}元

### 2. 风险分析
- **汇率风险**: 作为加拿大护照持有者，需关注人民币兑加元汇率波动
- **地缘政治风险**: 中加关系可能影响投资环境
- **市场风险**: 股市波动可能影响权益类资产价值
- **加密货币风险**: 比特币价格波动较大，需注意风险管理

### 3. 操作建议
1. 在Interactive Brokers开设国际账户
2. 通过银行跨境汇款进行资金转移
3. 在富途牛牛开设国内投资账户
4. 在Binance购买比特币后转入冷钱包
5. 设置每月定投计划

### 4. 基于客户背景的特殊建议
- **税务规划**: 作为加拿大税务居民，需申报全球收入，包括加密货币收益
- **外汇管理**: 合理利用个人年度5万美元外汇额度
- **合规性**: 确保所有投资行为符合中国和加拿大法规
- **八字分析**: 2002年出生属马，五行需要平衡，建议多关注木属性（成长型）和金属性（稳定型）资产

---
*生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
*使用模型: 备用建议系统*
*注意: 由于API连接问题，使用了备用建议系统*
"""
        
        return advice

    def show_progress_bar(self, description, duration=3):
        """显示进度条"""
        for i in tqdm(range(100), desc=description, ncols=100):
            time.sleep(duration / 100)

    def get_current_news_context(self):
        """获取当前新闻和全球大事的上下文"""
        print("📰 正在分析当前新闻和全球大事...")
        
        # 这里可以使用新闻API，但为了简化，我们使用AI来生成当前新闻分析
        current_date = datetime.now().strftime("%Y年%m月%d日")
        
        news_context = f"""
基于当前日期{current_date}的全球经济和市场环境分析：

重要新闻和全球大事考虑因素：
1. 全球经济状况：通胀、利率政策、经济增长预期
2. 地缘政治事件：国际关系、贸易政策、地区冲突
3. 科技发展：人工智能、区块链、新能源等领域的进展
4. 货币政策：主要央行（美联储、欧洲央行、中国人民银行）的政策动向
5. 市场情绪：投资者信心、市场波动性、风险偏好
6. 行业趋势：科技、医疗、能源、消费等主要行业的发展
7. 加密货币监管：全球各国对加密货币的政策变化
8. 中国与加拿大关系：可能影响跨境投资的双边关系

当前需要特别关注的因素：
- 全球通胀水平和央行的应对措施
- 中美关系和其对全球市场的影响
- 加密货币市场的监管发展
- 科技行业的创新和投资机会
- 地缘政治风险对投资组合的影响

这些因素将影响资产配置决策，特别是风险资产的配置比例。
"""
        
        return news_context

    def get_investment_recommendation(self, financial_data):
        """获取投资建议 - 让AI自行决定具体投资选项"""
        print("\n=== 历史投资表现追踪 ===")
        
        # 构建历史投资组合信息
        history_context = ""
        if self.previous_portfolios:
            history_context = "## 历史投资组合记录:\n"
            for i, portfolio_data in enumerate(self.previous_portfolios[-3:]):  # 只显示最近3次
                history_context += f"\n### 第{portfolio_data['session_id']}次投资 (时间: {portfolio_data['timestamp']})\n"
                
                if 'investment_portfolio' in portfolio_data:
                    portfolio = portfolio_data['investment_portfolio']
                    if isinstance(portfolio, list):
                        for item in portfolio:
                            history_context += f"- {item}\n"
                    else:
                        history_context += f"- {portfolio}\n"
                
                history_context += f"- 投资金额: {portfolio_data['available_for_investment']:,.0f}元\n"
                history_context += f"- 市场状况: {portfolio_data['market_condition']}\n"
        
        # 获取新闻和全球大事分析
        news_context = self.get_current_news_context()
        
        # 构建AI提示 - 让AI自行决定具体投资选项
        prompt = f"""
作为专业的投资顾问，请基于以下财务信息、客户背景以及当前全球新闻和大事提供详细的投资建议：

客户背景:
- 加拿大护照持有者，目前在中国境内
- 男性2002年11月26日凌晨3点半加拿大安大略省多伦多出生，八字信息需要考虑五行平衡和流年运势
- 需要兼顾国际投资和国内合规性
- 拥有比特币冷钱包，可以存储加密货币
- 这是第{self.session_id}次投资咨询

客户财务概况:
- 月收入: {financial_data['monthly_income']:,.0f} 元
- 生活支出: {financial_data['living_expenses']:,.0f} 元
- 可用于投资金额: {financial_data['available_for_investment']:,.0f} 元
- 市场状况: {financial_data['market_condition']}
- 投资心态: {financial_data['investment_mood']}
{f"- 特殊说明: {financial_data['special_notes']}" if financial_data['special_notes'] else ""}

{history_context if history_context else "无历史投资记录"}

{news_context}

重要要求：
1. 请结合当前全球新闻和大事分析投资环境
2. 考虑地缘政治、经济政策、市场情绪等宏观因素
3. 根据当前市场环境调整资产配置比例
4. 请自行决定每个投资类别的具体投资产品（股票、债券、加密货币等）
5. 每个类别只推荐一个具体的投资产品
6. 必须包含加密货币类别，并推荐比特币（使用现有冷钱包存储）
7. 为比特币推荐一个交易平台（用于购买比特币），然后转移到冷钱包
8. 平台推荐要保持一致性，不要频繁更换平台
9. 考虑加拿大身份和在中国境内的实际情况
10. 结合八字五行分析提供个性化建议
11. 为每个投资产品提供具体的投资平台和链接
12. 请提供具体的投资金额分配
13. 如果这是第一次投资，建议从比特币冷钱包开始加密货币投资
14. 如果有历史投资记录，请保持平台一致性，不要推荐新的平台
15. 特别说明当前全球事件如何影响投资决策

请按照以下结构提供建议：

### 1. 当前市场环境分析
（基于新闻和全球大事的分析）

### 2. 具体的资产配置建议

#### 权益类资产（具体比例%）
- **建议**: 明确推荐一个具体的指数基金或股票（自行决定）
- **理由**: 结合市场状况、客户背景、八字分析和当前新闻事件说明
- **平台**: 具体的投资平台名称和链接（保持平台一致性）
- **投资金额**: 具体金额（元）

#### 固定收益类资产（具体比例%）
- **建议**: 明确推荐一个具体的债券基金（自行决定）
- **理由**: 结合市场状况、客户背景、八字分析和当前新闻事件说明
- **平台**: 具体的投资平台名称和链接（保持平台一致性）
- **投资金额**: 具体金额（元）

#### 加密货币资产（具体比例%）
- **建议**: 比特币（使用现有冷钱包存储）
- **理由**: 结合市场状况、客户背景、八字分析和当前新闻事件说明
- **平台**: 比特币冷钱包
- **交易平台**: 具体的比特币交易平台名称和链接（用于购买比特币）
- **投资金额**: 具体金额（元）

### 3. 风险分析
（详细的风险分析，包括市场风险、汇率风险、地缘政治风险等，特别考虑当前新闻事件）

### 4. 操作建议
（具体的操作步骤，包括开户、转账、投资等）

### 5. 基于客户背景和当前环境的特殊建议
（考虑加拿大身份、在中国境内、八字、当前全球大事等因素的特殊建议）

请用中文回复，确保建议专业、实用且具体。每个类别只推荐一个产品，平台要保持一致性。
请务必提供完整的投资建议，不要因为长度限制而省略内容。
特别强调当前新闻和全球大事对投资决策的影响。
"""
        
        # 调用AI获取建议
        try:
            print("🔄 正在生成AI投资建议...")
            advice = self.call_deepseek_api(prompt)
            
            # 检查建议是否为空
            if not advice or len(advice.strip()) < 50:
                print("❌ AI建议内容过短，使用备用建议")
                return self.get_fallback_recommendation(financial_data)
                
            return advice
        except Exception as e:
            print(f"❌ AI建议获取失败: {str(e)}")
            print("🔄 切换到备用建议系统...")
            return self.get_fallback_recommendation(financial_data)

    def parse_investment_details(self, advice):
        """从AI建议中解析投资详情"""
        investment_details = {
            "equity": {"name": "", "platform": "", "amount": ""},
            "fixed_income": {"name": "", "platform": "", "amount": ""},
            "crypto": {"name": "", "platform": "", "trading_platform": "", "amount": ""}
        }
        
        try:
            lines = advice.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                
                # 检测章节
                if "#### 权益类资产" in line:
                    current_section = "equity"
                elif "#### 固定收益类资产" in line:
                    current_section = "fixed_income"
                elif "#### 加密货币资产" in line:
                    current_section = "crypto"
                
                # 解析具体信息
                if current_section:
                    if "**建议**:" in line:
                        investment_details[current_section]["name"] = line.split(":**")[-1].strip()
                    elif "**平台**:" in line:
                        investment_details[current_section]["platform"] = line.split(":**")[-1].strip()
                    elif "**交易平台**:" in line:
                        investment_details[current_section]["trading_platform"] = line.split(":**")[-1].strip()
                    elif "**投资金额**:" in line:
                        investment_details[current_section]["amount"] = line.split(":**")[-1].strip()
                        
        except Exception as e:
            print(f"⚠️  解析投资详情时出错: {str(e)}")
        
        return investment_details

    def update_investment_portfolio(self, advice):
        """更新投资组合 - 从AI建议中提取投资组合信息"""
        print("🔄 正在解析AI建议并更新投资组合...")
        
        # 从AI建议中提取投资组合信息
        portfolio = []
        
        # 简单的关键词提取逻辑
        investment_keywords = [
            "中证500", "510500", "沪深300", "创业板", "科创板", 
            "VT", "ASHR", "QQQ", "VOO", "ARKK", "SPY",
            "BND", "TLT", "AGG", "IEF", "债券", "国债",
            "比特币", "以太坊", "加密货币", "数字货币",
            "余额宝", "货币基金", "现金"
        ]
        
        for keyword in investment_keywords:
            if keyword.lower() in advice.lower():
                portfolio.append(keyword)
                if len(portfolio) >= 3:  # 最多3个投资产品
                    break
        
        # 确保包含比特币
        if "比特币" not in portfolio:
            portfolio.append("比特币")
        
        # 如果没有找到匹配的，使用默认组合
        if len(portfolio) < 2:
            portfolio = ["中证500指数基金", "中国政府债券ETF", "比特币"]
        
        print(f"✅ 已更新投资组合: {portfolio}")
        return portfolio

    def save_session_data(self, financial_data, advice, portfolio):
        """保存会话数据"""
        # 创建会话目录
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = os.path.join(
            self.history_dir, 
            f"{self.session_id:03d}_{timestamp}"
        )
        os.makedirs(session_dir, exist_ok=True)
        
        # 解析投资详情
        investment_details = self.parse_investment_details(advice)
        
        # 保存财务数据
        money_file = os.path.join(self.money_dir, "financial_data.json")
        all_data = []
        
        if os.path.exists(money_file):
            try:
                with open(money_file, 'r', encoding='utf-8') as f:
                    all_data = json.load(f)
            except:
                all_data = []
        
        # 添加投资组合到财务数据
        financial_data["investment_portfolio"] = portfolio
        financial_data["advice"] = advice  # 保存完整的建议
        financial_data["investment_details"] = investment_details  # 保存结构化的投资详情
        
        all_data.append(financial_data)
        
        with open(money_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 财务数据已保存: {money_file}")
        
        # 保存详细报告
        report_file = os.path.join(
            session_dir, 
            f"session_{self.session_id:03d}_{timestamp}.md"
        )
        
        report_content = f"""# 投资顾问报告 - 会话 {self.session_id}

## 基本信息
- **报告时间**: {financial_data['timestamp']}
- **市场状况**: {financial_data['market_condition']}
- **投资心态**: {financial_data['investment_mood']}
- **客户背景**: 加拿大护照持有者，在中国境内
- **投资次数**: 第{self.session_id}次月度投资

## 财务概况
- **月收入**: {financial_data['monthly_income']:,.0f} 元
- **生活支出**: {financial_data['living_expenses']:,.0f} 元  
- **可用于投资**: {financial_data['available_for_investment']:,.0f} 元
- **现金储备**: {financial_data['cash_reserve']:,.0f} 元

## 投资组合
{chr(10).join(['- ' + item for item in portfolio])}

## 投资详情
### 权益类资产
- **产品**: {investment_details['equity']['name']}
- **平台**: {investment_details['equity']['platform']}
- **金额**: {investment_details['equity']['amount']}

### 固定收益类资产
- **产品**: {investment_details['fixed_income']['name']}
- **平台**: {investment_details['fixed_income']['platform']}
- **金额**: {investment_details['fixed_income']['amount']}

### 加密货币资产
- **产品**: {investment_details['crypto']['name']}
- **存储平台**: {investment_details['crypto']['platform']}
- **交易平台**: {investment_details['crypto']['trading_platform']}
- **金额**: {investment_details['crypto']['amount']}

## AI投资建议

{advice}

---
*生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
*使用模型: {self.model}*
*个性化建议: 考虑加拿大身份、中国境内居住、八字五行平衡、当前全球新闻和大事*
*历史记录: 包含{len(self.previous_portfolios)}个历史投资组合*
"""
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✅ 投资报告已保存: {report_file}")
        return report_file

    def display_recommendation_summary(self, advice, portfolio, report_file):
        """显示建议摘要"""
        print("\n" + "="*60)
        print("📋 本月投资建议摘要")
        print("="*60)
        print(advice)
        print("="*60)
        print(f"💡 提示: 完整报告已保存至 {report_file}")
        print("💡 您可以使用 get_report.py 查看可视化分析")
        print("💡 您可以使用 pay.py 启动投资平台进行投资")

    def run(self):
        """运行主程序"""
        try:
            self.initialize_system()
            financial_data = self.collect_financial_info()
            
            # 测试API连接
            if not self.test_api_connection():
                print("⚠️  API连接测试失败，使用备用建议系统")
                advice = self.get_fallback_recommendation(financial_data)
            else:
                # 尝试获取AI建议，如果失败则使用备用方案
                try:
                    print("🔄 尝试获取AI投资建议...")
                    advice = self.get_investment_recommendation(financial_data)
                    print("✅ AI建议获取成功")
                except Exception as e:
                    print(f"⚠️  AI建议获取失败: {str(e)}")
                    print("🔄 切换到备用建议系统...")
                    advice = self.get_fallback_recommendation(financial_data)
            
            portfolio = self.update_investment_portfolio(advice)
            report_file = self.save_session_data(financial_data, advice, portfolio)
            self.display_recommendation_summary(advice, portfolio, report_file)
            
        except Exception as e:
            print(f"\n❌ 系统运行失败: {str(e)}")
            print("💡 建议检查:")
            print("  1. 网络连接是否正常")
            print("  2. API密钥是否正确设置")
            print("  3. 防火墙或代理设置")
            return False
        
        return True

def main():
    """主函数"""
    advisor = InvestmentAdvisor()
    success = advisor.run()
    
    if success:
        print("\n🎉 投资顾问系统运行完成！")
        print("💡 下一步操作:")
        print("  1. 使用 get_report.py 查看详细分析")
        print("  2. 使用 pay.py 启动投资平台进行投资")
        print("  3. 下个月再次运行此程序以获取新的投资建议")
    else:
        print("\n💔 投资顾问系统运行失败，请检查上述错误信息")

if __name__ == "__main__":
    main()
