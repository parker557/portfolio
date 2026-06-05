import os
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import textwrap
import re
from datetime import datetime
from tabulate import tabulate
import matplotlib
matplotlib.use('TkAgg')
import openai
from pathlib import Path
import time
from tqdm import tqdm

class ReportGenerator:
    def __init__(self):
        self.root_path = None
        self.money_dir = None
        self.history_dir = None
        self.temp_dir = None
        self.all_data = []
        self.current_session = None
        self.config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".finance_config.json")
        self.openai_client = None
        self.setup_openai()
        
    def setup_openai(self):
        """设置OpenAI客户端"""
        try:
            api_key = os.getenv("DEEPSEEK_API_KEY")
            if api_key:
                self.openai_client = openai.OpenAI(
                    api_key=api_key,
                    base_url="https://api.deepseek.com/v1"
                )
            # 不显示成功消息，隐藏AI使用
        except Exception:
            # 静默失败
            pass
    
    def show_progress(self, desc="处理中", duration=2):
        """显示进度条"""
        for _ in tqdm(range(100), desc=desc, ncols=80, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'):
            time.sleep(duration / 100)
    
    def print_header(self, title):
        """打印美观的标题"""
        print("\n" + "=" * 60)
        print(f"📊 {title}")
        print("=" * 60)
    
    def print_section(self, title):
        """打印章节标题"""
        print(f"\n📋 {title}")
        print("-" * 40)
    
    def print_success(self, message):
        """打印成功消息"""
        print(f"✅ {message}")
    
    def print_warning(self, message):
        """打印警告消息"""
        print(f"⚠️  {message}")
    
    def print_error(self, message):
        """打印错误消息"""
        print(f"❌ {message}")
    
    def print_info(self, message):
        """打印信息消息"""
        print(f"💡 {message}")
    
    def clean_text(self, text):
        """清理文本"""
        if not text:
            return ""
        cleaned = re.sub(r'\s+', ' ', str(text)).strip()
        cleaned = re.sub(r'[•·▪▫–—]', '', cleaned)
        return cleaned
    
    def parse_investment_details_smart(self, advice_text):
        """智能解析投资详情 - 隐藏AI使用"""
        # 显示进度条
        self.show_progress("正在解析投资详情", 2)
        
        # 首先尝试本地解析
        details = self.parse_investment_details_local(advice_text)
        
        # 如果本地解析结果不完整，使用AI辅助（不告诉用户）
        needs_ai_help = False
        for asset_type in ['equity', 'fixed_income', 'crypto']:
            asset = details.get(asset_type, {})
            if not asset.get('name') and not asset.get('platform'):
                needs_ai_help = True
                break
        
        if needs_ai_help and self.openai_client:
            try:
                ai_details = self.parse_investment_details_with_ai(advice_text)
                # 合并结果，优先使用AI结果
                for asset_type in ['equity', 'fixed_income', 'crypto']:
                    ai_asset = ai_details.get(asset_type, {})
                    local_asset = details.get(asset_type, {})
                    
                    # 如果AI提供了更好的结果，使用AI的结果
                    if ai_asset.get('name') and (not local_asset.get('name') or len(ai_asset['name']) > len(local_asset['name'])):
                        details[asset_type]['name'] = ai_asset['name']
                    
                    if ai_asset.get('platform') and (not local_asset.get('platform') or len(ai_asset['platform']) > len(local_asset['platform'])):
                        details[asset_type]['platform'] = ai_asset['platform']
                    
                    if ai_asset.get('amount') and (not local_asset.get('amount') or len(ai_asset['amount']) > len(local_asset['amount'])):
                        details[asset_type]['amount'] = ai_asset['amount']
                    
                    if asset_type == 'crypto' and ai_asset.get('trading_platform'):
                        details[asset_type]['trading_platform'] = ai_asset['trading_platform']
            except Exception:
                # 静默失败，继续使用本地结果
                pass
        
        return details
    
    def parse_investment_details_with_ai(self, advice_text):
        """使用AI辅助解析投资详情 - 内部使用"""
        if not self.openai_client:
            return {
                "equity": {"name": "", "platform": "", "amount": ""},
                "fixed_income": {"name": "", "platform": "", "amount": ""},
                "crypto": {"name": "", "platform": "", "trading_platform": "", "amount": ""}
            }
        
        try:
            prompt = f"""
请从以下投资建议中提取投资分配信息，包括权益类资产、固定收益类资产、加密货币资产的详细信息。
返回JSON格式，包含以下字段：
- equity: {{name, platform, amount}}
- fixed_income: {{name, platform, amount}}  
- crypto: {{name, platform, trading_platform, amount}}

投资建议：
{advice_text[:3000]}

请只返回JSON格式，不要其他内容。
"""
            
            response = self.openai_client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个专业的投资分析师，专门从投资建议中提取结构化信息。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            result = response.choices[0].message.content.strip()
            result = re.sub(r'```json\n?|\n?```', '', result)
            
            details = json.loads(result)
            return details
            
        except Exception:
            return {
                "equity": {"name": "", "platform": "", "amount": ""},
                "fixed_income": {"name": "", "platform": "", "amount": ""},
                "crypto": {"name": "", "platform": "", "trading_platform": "", "amount": ""}
            }
    
    def parse_investment_details_local(self, advice_text):
        """本地方法解析投资详情"""
        details = {
            "equity": {"name": "", "platform": "", "amount": ""},
            "fixed_income": {"name": "", "platform": "", "amount": ""},
            "crypto": {"name": "", "platform": "", "trading_platform": "", "amount": ""}
        }
        
        try:
            lines = advice_text.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if '权益类资产' in line or '权益类' in line:
                    current_section = 'equity'
                elif '固定收益类资产' in line or '固定收益类' in line or '固定收益' in line:
                    current_section = 'fixed_income'
                elif '加密货币资产' in line or '加密货币' in line:
                    current_section = 'crypto'
                
                if current_section:
                    if '建议:' in line or '建议：' in line or '- **建议**' in line:
                        if ':' in line:
                            parts = line.split(':', 1)
                            if len(parts) > 1:
                                details[current_section]['name'] = self.clean_text(parts[1])
                        elif '：' in line:
                            parts = line.split('：', 1)
                            if len(parts) > 1:
                                details[current_section]['name'] = self.clean_text(parts[1])
                        else:
                            match = re.search(r'建议\s*(.*?)(?=平台|金额|理由|$)', line)
                            if match:
                                details[current_section]['name'] = self.clean_text(match.group(1))
                    
                    elif '平台:' in line or '平台：' in line or '- **平台**' in line:
                        if ':' in line:
                            parts = line.split(':', 1)
                            if len(parts) > 1:
                                platform_text = self.clean_text(parts[1])
                                if current_section == 'crypto' and ('交易平台' in line or 'trading' in line.lower()):
                                    details[current_section]['trading_platform'] = platform_text
                                else:
                                    details[current_section]['platform'] = platform_text
                        elif '：' in line:
                            parts = line.split('：', 1)
                            if len(parts) > 1:
                                platform_text = self.clean_text(parts[1])
                                if current_section == 'crypto' and ('交易平台' in line or 'trading' in line.lower()):
                                    details[current_section]['trading_platform'] = platform_text
                                else:
                                    details[current_section]['platform'] = platform_text
                    
                    elif '投资金额:' in line or '投资金额：' in line or '- **投资金额**' in line:
                        if ':' in line:
                            parts = line.split(':', 1)
                            if len(parts) > 1:
                                details[current_section]['amount'] = self.extract_amount(parts[1])
                        elif '：' in line:
                            parts = line.split('：', 1)
                            if len(parts) > 1:
                                details[current_section]['amount'] = self.extract_amount(parts[1])
            
        except Exception:
            # 静默失败
            pass
        
        return details
    
    def extract_amount(self, text):
        """提取金额"""
        try:
            matches = re.findall(r'[\d,]+\.?\d*', text)
            if matches:
                return f"{float(matches[0].replace(',', '')):,.0f}元"
            return text
        except:
            return text
    
    def format_amount(self, amount):
        """格式化金额"""
        try:
            if isinstance(amount, (int, float)):
                return f"{amount:,.0f}元"
            elif isinstance(amount, str):
                if '元' in amount:
                    return amount
                numbers = re.findall(r'[\d,]+\.?\d*', amount)
                if numbers:
                    return f"{float(numbers[0].replace(',', '')):,.0f}元"
                else:
                    return amount
            else:
                return str(amount)
        except:
            return str(amount)
    
    def wrap_text(self, text, width=50):
        """文本换行"""
        if not text:
            return ""
        return '\n'.join(textwrap.wrap(str(text), width=width))
    
    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.root_path = config.get('root_path')
                    if self.root_path and os.path.exists(self.root_path):
                        return True
            except Exception:
                pass
        return False

    def save_config(self):
        """保存配置"""
        if self.root_path:
            config = {
                'root_path': self.root_path,
                'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            try:
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                return True
            except Exception:
                return False
        return False

    def initialize(self):
        """初始化系统"""
        self.print_header("投资报告系统")
        
        if self.load_config():
            self.print_success(f"已加载配置")
        else:
            self.root_path = input("📁 请输入根目录路径: ").strip()
            if not os.path.exists(self.root_path):
                self.print_error("目录不存在")
                return False
            
            self.save_config()
        
        self.money_dir = os.path.join(self.root_path, "money")
        self.history_dir = os.path.join(self.root_path, "history")
        self.temp_dir = os.path.join(self.root_path, "temp")
        
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        
        if not os.path.exists(self.money_dir):
            self.print_error("money目录不存在")
            return False
        
        if not self.load_all_data():
            return False
        
        return self.select_report_session()
    
    def load_all_data(self):
        """加载所有数据"""
        money_file = os.path.join(self.money_dir, "financial_data.json")
        
        if not os.path.exists(money_file):
            self.print_error("财务数据文件不存在")
            return False
        
        try:
            with open(money_file, 'r', encoding='utf-8') as f:
                self.all_data = json.load(f)
            
            self.print_success(f"已加载 {len(self.all_data)} 条投资记录")
            return True
            
        except Exception as e:
            self.print_error(f"读取数据失败: {str(e)}")
            return False
    
    def select_report_session(self):
        """选择报告会话"""
        if not self.all_data:
            self.print_error("没有可用的投资数据")
            return False
        
        self.all_data.sort(key=lambda x: x['session_id'])
        
        if len(self.all_data) == 1:
            self.current_session = self.all_data[0]
            self.print_success(f"已选择投资报告")
            return True
        
        self.print_section("选择投资报告")
        
        recent_sessions = self.all_data[-5:]
        recent_sessions.reverse()
        
        for i, session in enumerate(recent_sessions, 1):
            print(f"  {i}. 第{session['session_id']}次投资 - {session['timestamp']}")
        
        print(f"  {len(recent_sessions) + 1}. 选择其他报告")
        
        try:
            choice = input(f"\n🎯 请选择报告 (1-{len(recent_sessions) + 1}, 默认1): ").strip()
            
            if choice == "":
                choice = 1
            else:
                choice = int(choice)
            
            if 1 <= choice <= len(recent_sessions):
                self.current_session = recent_sessions[choice - 1]
            elif choice == len(recent_sessions) + 1:
                session_id = input("请输入会话ID: ").strip()
                if session_id.isdigit():
                    session_id = int(session_id)
                    for session in self.all_data:
                        if session['session_id'] == session_id:
                            self.current_session = session
                            break
                    if not self.current_session:
                        self.print_error(f"未找到会话ID为{session_id}的记录")
                        return False
                else:
                    self.print_error("无效的会话ID")
                    return False
            else:
                self.print_error("无效的选择")
                return False
            
            self.print_success(f"已选择投资报告")
            return True
            
        except Exception as e:
            self.print_error(f"选择报告时出错: {str(e)}")
            return False
    
    def generate_summary_report(self):
        """生成汇总报告"""
        if not self.all_data:
            self.print_error("没有可用的数据")
            return
        
        self.print_header("投资汇总分析报告")
        
        # 基本统计
        total_investments = len(self.all_data)
        total_invested = sum(item['available_for_investment'] for item in self.all_data)
        avg_investment = total_invested / total_investments if total_investments > 0 else 0
        
        key_metrics = [
            ["📈 总投资次数", f"{total_investments} 次"],
            ["💰 总投资金额", self.format_amount(total_invested)],
            ["📅 平均每月投资", self.format_amount(avg_investment)],
            ["🏦 数据覆盖期", f"{len(self.all_data)} 个月"]
        ]
        
        print(tabulate(key_metrics, tablefmt="grid", colalign=("left", "right")))
        
        # 市场状况统计
        self.print_section("市场状况分析")
        market_stats = {}
        for item in self.all_data:
            market = self.clean_text(item['market_condition'])
            market_stats[market] = market_stats.get(market, 0) + 1
        
        market_table = []
        for market, count in market_stats.items():
            percentage = (count / total_investments) * 100
            market_table.append([market, count, f"{percentage:.1f}%"])
        
        if market_table:
            print(tabulate(market_table, headers=["市场状况", "出现次数", "占比"], tablefmt="grid"))
        
        # 投资心态统计
        self.print_section("投资心态分析")
        mood_stats = {}
        for item in self.all_data:
            mood = self.clean_text(item['investment_mood'])
            mood_stats[mood] = mood_stats.get(mood, 0) + 1
        
        mood_table = []
        for mood, count in mood_stats.items():
            percentage = (count / total_investments) * 100
            mood_table.append([mood, count, f"{percentage:.1f}%"])
        
        if mood_table:
            print(tabulate(mood_table, headers=["投资心态", "出现次数", "占比"], tablefmt="grid"))
        
        # 显示当前选择的投资详情
        if self.current_session:
            self.print_section(f"当前选择投资详情 (第{self.current_session['session_id']}次)")
            
            if 'advice' in self.current_session:
                investment_details = self.parse_investment_details_smart(self.current_session['advice'])
                
                investment_table = []
                
                equity = investment_details.get("equity", {})
                if equity.get("name"):
                    investment_table.append([
                        "📈 权益类",
                        equity["name"],
                        self.format_amount(equity.get("amount", ""))
                    ])
                
                fixed_income = investment_details.get("fixed_income", {})
                if fixed_income.get("name"):
                    investment_table.append([
                        "💰 固定收益",
                        fixed_income["name"],
                        self.format_amount(fixed_income.get("amount", ""))
                    ])
                
                crypto = investment_details.get("crypto", {})
                if crypto.get("name"):
                    investment_table.append([
                        "🔗 加密货币",
                        crypto["name"],
                        self.format_amount(crypto.get("amount", ""))
                    ])
                
                if investment_table:
                    print(tabulate(investment_table, headers=["资产类型", "产品名称", "投资金额"], tablefmt="grid"))
                else:
                    self.print_warning("未能解析出投资详情")
    
    def plot_investment_trend(self):
        """绘制投资趋势图"""
        if len(self.all_data) < 2:
            self.print_error("数据不足，至少需要2次投资记录")
            return
        
        try:
            # 显示进度条
            self.show_progress("正在生成图表", 3)
            
            sessions = [item['session_id'] for item in self.all_data]
            investments = [item['available_for_investment'] for item in self.all_data]
            
            plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
            plt.rcParams['axes.unicode_minus'] = False
            
            plt.figure(figsize=(12, 8))
            
            # 投资金额趋势
            plt.subplot(2, 2, 1)
            plt.plot(sessions, investments, 'o-', linewidth=2, markersize=6, color='#2E86AB')
            plt.title('投资金额趋势')
            plt.xlabel('投资会话')
            plt.ylabel('投资金额 (元)')
            plt.grid(True, alpha=0.3)
            
            # 收入支出对比
            plt.subplot(2, 2, 2)
            incomes = [item['monthly_income'] for item in self.all_data]
            expenses = [item['living_expenses'] for item in self.all_data]
            
            bar_width = 0.35
            x = np.arange(len(sessions))
            
            plt.bar(x - bar_width/2, incomes, bar_width, label='月收入', color='#A8D5BA')
            plt.bar(x + bar_width/2, expenses, bar_width, label='月支出', color='#F9C784')
            
            plt.title('收入支出对比')
            plt.xlabel('投资会话')
            plt.ylabel('金额 (元)')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.xticks(x, sessions)
            
            # 市场状况分布
            plt.subplot(2, 2, 3)
            market_conditions = [self.clean_text(item['market_condition']) for item in self.all_data]
            market_counts = pd.Series(market_conditions).value_counts()
            
            plt.pie(market_counts.values, labels=market_counts.index, autopct='%1.1f%%', startangle=90)
            plt.title('市场状况分布')
            
            # 投资心态分布
            plt.subplot(2, 2, 4)
            investment_moods = [self.clean_text(item['investment_mood']) for item in self.all_data]
            mood_counts = pd.Series(investment_moods).value_counts()
            
            plt.pie(mood_counts.values, labels=mood_counts.index, autopct='%1.1f%%', startangle=90)
            plt.title('投资心态分布')
            
            plt.tight_layout()
            
            chart_file = os.path.join(self.temp_dir, "investment_analysis.png")
            plt.savefig(chart_file, dpi=300, bbox_inches='tight')
            
            self.print_success(f"图表已生成: {chart_file}")
            plt.show()
            
        except Exception as e:
            self.print_error(f"生成图表时出错: {str(e)}")
    
    def show_detailed_records(self):
        """显示详细记录"""
        if not self.all_data:
            self.print_error("没有可用的数据")
            return
        
        self.print_header("详细投资记录")
        
        for i, item in enumerate(self.all_data):
            print(f"\n🎯 第 {item['session_id']} 次投资")
            print("=" * 50)
            
            basic_info = [
                ["投资时间", item['timestamp']],
                ["月收入", self.format_amount(item['monthly_income'])],
                ["生活支出", self.format_amount(item['living_expenses'])],
                ["投资金额", self.format_amount(item['available_for_investment'])],
                ["市场状况", self.clean_text(item['market_condition'])],
                ["投资心态", self.clean_text(item['investment_mood'])]
            ]
            
            print(tabulate(basic_info, tablefmt="simple", colalign=("right", "left")))
            
            if 'advice' in item:
                investment_details = self.parse_investment_details_smart(item['advice'])
                
                investment_table = []
                
                equity = investment_details.get("equity", {})
                if equity.get("name"):
                    investment_table.append([
                        "权益类资产",
                        equity["name"],
                        equity.get("platform", ""),
                        self.format_amount(equity.get("amount", ""))
                    ])
                
                fixed_income = investment_details.get("fixed_income", {})
                if fixed_income.get("name"):
                    investment_table.append([
                        "固定收益资产",
                        fixed_income["name"],
                        fixed_income.get("platform", ""),
                        self.format_amount(fixed_income.get("amount", ""))
                    ])
                
                crypto = investment_details.get("crypto", {})
                if crypto.get("name"):
                    platform_info = crypto.get("platform", "")
                    if crypto.get("trading_platform"):
                        platform_info += f" ({crypto['trading_platform']})"
                    
                    investment_table.append([
                        "加密货币资产",
                        crypto["name"],
                        platform_info,
                        self.format_amount(crypto.get("amount", ""))
                    ])
                
                if investment_table:
                    print(tabulate(investment_table, headers=["资产类型", "产品名称", "平台", "金额"], tablefmt="grid"))
            
            if i < len(self.all_data) - 1:
                print("\n" + "-" * 50)
    
    def export_to_excel(self):
        """导出到Excel"""
        if not self.all_data:
            self.print_error("没有可用的数据")
            return
        
        try:
            # 显示进度条
            self.show_progress("正在导出数据", 2)
            
            data_for_export = []
            for item in self.all_data:
                row = {
                    '会话ID': item['session_id'],
                    '时间': item['timestamp'],
                    '月收入': item['monthly_income'],
                    '生活支出': item['living_expenses'],
                    '投资金额': item['available_for_investment'],
                    '市场状况': self.clean_text(item['market_condition']),
                    '投资心态': self.clean_text(item['investment_mood'])
                }
                
                if 'advice' in item:
                    investment_details = self.parse_investment_details_smart(item['advice'])
                    
                    equity = investment_details.get('equity', {})
                    row['权益类产品'] = equity.get('name', '')
                    row['权益类平台'] = equity.get('platform', '')
                    row['权益类金额'] = equity.get('amount', '')
                    
                    fixed_income = investment_details.get('fixed_income', {})
                    row['固定收益产品'] = fixed_income.get('name', '')
                    row['固定收益平台'] = fixed_income.get('platform', '')
                    row['固定收益金额'] = fixed_income.get('amount', '')
                    
                    crypto = investment_details.get('crypto', {})
                    row['加密货币产品'] = crypto.get('name', '')
                    row['加密货币平台'] = crypto.get('platform', '')
                    row['加密货币交易平台'] = crypto.get('trading_platform', '')
                    row['加密货币金额'] = crypto.get('amount', '')
                
                data_for_export.append(row)
            
            df = pd.DataFrame(data_for_export)
            excel_file = os.path.join(self.temp_dir, "investment_data.xlsx")
            df.to_excel(excel_file, index=False)
            
            self.print_success(f"数据已导出: {excel_file}")
            
            stats = [
                ["总记录数", f"{len(df)} 条"],
                ["时间范围", f"{df['时间'].min()} 至 {df['时间'].max()}"],
                ["总投资金额", self.format_amount(df['投资金额'].sum())]
            ]
            print(tabulate(stats, tablefmt="grid"))
            
        except Exception as e:
            self.print_error(f"导出数据时出错: {str(e)}")
    
    def show_platform_summary(self):
        """显示平台汇总"""
        if not self.all_data:
            self.print_error("没有可用的数据")
            return
        
        self.print_header("平台使用汇总")
        
        platforms_used = {}
        
        for item in self.all_data:
            if 'advice' in item:
                investment_details = self.parse_investment_details_smart(item['advice'])
                
                for asset_type in ['equity', 'fixed_income']:
                    platform = investment_details.get(asset_type, {}).get('platform')
                    if platform:
                        platforms_used[platform] = platforms_used.get(platform, 0) + 1
                
                crypto = investment_details.get('crypto', {})
                if crypto.get('trading_platform'):
                    platforms_used[crypto['trading_platform']] = platforms_used.get(crypto['trading_platform'], 0) + 1
                if crypto.get('platform'):
                    platforms_used[crypto['platform']] = platforms_used.get(crypto['platform'], 0) + 1
        
        if platforms_used:
            platform_table = []
            for platform, count in sorted(platforms_used.items(), key=lambda x: x[1], reverse=True):
                platform_table.append([platform, count, f"{(count/len(self.all_data))*100:.1f}%"])
            
            print(tabulate(platform_table, headers=["平台", "使用次数", "使用频率"], tablefmt="grid"))
        else:
            self.print_warning("暂无平台使用记录")
    
    def show_full_advice(self):
        """显示完整投资建议"""
        if not self.current_session or 'advice' not in self.current_session:
            self.print_error("没有可用的投资建议")
            return
        
        self.print_header("完整投资建议")
        print(self.current_session['advice'])
    
    def run(self):
        """运行报告系统"""
        if not self.initialize():
            return
        
        while True:
            self.print_header("投资报告系统")
            
            menu_options = [
                ["1", "📈 生成汇总报告", "查看投资概览"],
                ["2", "📊 显示投资趋势图", "可视化数据变化"],
                ["3", "📋 显示详细记录", "查看完整信息"],
                ["4", "📖 显示完整建议", "查看原始建议"],
                ["5", "🏦 显示平台汇总", "分析平台使用"],
                ["6", "💾 导出到Excel", "导出数据"],
                ["7", "🔄 切换报告", "选择其他报告"],
                ["8", "🚪 退出系统", "结束程序"]
            ]
            
            print(tabulate(menu_options, headers=["选项", "功能", "说明"], tablefmt="grid"))
            
            choice = input("\n🎯 请选择功能 (1-8): ").strip()
            
            if choice == "1":
                self.generate_summary_report()
            elif choice == "2":
                self.plot_investment_trend()
            elif choice == "3":
                self.show_detailed_records()
            elif choice == "4":
                self.show_full_advice()
            elif choice == "5":
                self.show_platform_summary()
            elif choice == "6":
                self.export_to_excel()
            elif choice == "7":
                if self.select_report_session():
                    self.print_success(f"已切换到投资报告")
                else:
                    self.print_error("切换报告失败")
            elif choice == "8":
                self.print_success("感谢使用投资报告系统！📈")
                break
            else:
                self.print_error("无效选择，请重新输入")
            
            if choice != "8":
                input("\n⏎ 按回车键继续...")

def main():
    """主函数"""
    try:
        generator = ReportGenerator()
        generator.run()
    except KeyboardInterrupt:
        print("\n\n👋 用户中断程序，再见！")
    except Exception as e:
        print(f"\n💥 程序运行出错: {str(e)}")

if __name__ == "__main__":
    main()
