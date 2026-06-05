import os
import json
import webbrowser
import re
import textwrap
from datetime import datetime
from tabulate import tabulate
import urllib.parse
from pathlib import Path
import time
from tqdm import tqdm
from openai import OpenAI

class InvestmentExecutor:
    def __init__(self):
        self.root_path = None
        self.money_dir = None
        self.history_dir = None
        self.temp_dir = None
        self.current_report_file = None
        self.report_content = None
        self.config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".finance_config.json")
        
        # 初始化DeepSeek API客户端
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.deepseek.com/v1"
            )
            self.model = "deepseek-reasoner"
        else:
            self.client = None
            self.model = None
        
    def show_progress(self, desc="处理中", duration=4):
        """显示进度条"""
        for _ in tqdm(range(100), desc=desc, ncols=80, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'):
            time.sleep(duration / 100)
    
    def print_header(self, title):
        """打印美观的标题"""
        print("\n" + "=" * 60)
        print(f"🏦 {title}")
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
        """清理文本，移除多余的空格和特殊符号"""
        if not text:
            return ""
        cleaned = re.sub(r'\s+', ' ', str(text)).strip()
        cleaned = re.sub(r'[•·▪▫–—]', '', cleaned)
        return cleaned
    
    def find_latest_report(self):
        """查找最新的投资报告文件"""
        if not os.path.exists(self.history_dir):
            self.print_error("history目录不存在")
            return None
        
        # 查找所有会话目录，按照finance_advice.py的格式
        session_dirs = []
        for item in os.listdir(self.history_dir):
            item_path = os.path.join(self.history_dir, item)
            if os.path.isdir(item_path):
                # 匹配类似 "001_20251014_163339" 的目录名
                if re.match(r'\d+_\d{8}_\d{6}', item):
                    session_dirs.append(item_path)
        
        if not session_dirs:
            self.print_error("未找到任何投资报告目录")
            return None
        
        # 按目录名中的数字排序，获取最新的目录
        session_dirs.sort(key=lambda x: int(re.search(r'^(\d+)_', os.path.basename(x)).group(1)), reverse=True)
        latest_dir = session_dirs[0]
        
        # 在该目录中查找Markdown报告文件
        for file in os.listdir(latest_dir):
            if file.endswith(".md") and file.startswith("session_"):
                report_file = os.path.join(latest_dir, file)
                self.print_success(f"找到最新报告: {os.path.basename(report_file)}")
                return report_file
        
        self.print_error("在最新会话目录中未找到Markdown报告文件")
        return None
    
    def read_report_content(self, report_file):
        """读取报告文件内容"""
        try:
            with open(report_file, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            self.print_error(f"读取报告文件失败: {str(e)}")
            return None
    
    def extract_platforms_via_api(self, report_content):
        """使用DeepSeek API提取平台和链接"""
        if not self.client:
            self.print_warning("DeepSeek API未配置，无法使用智能提取")
            return {}
        
        try:
            # 构建提示词
            prompt = f"""
请从以下投资报告中提取所有提到的投资平台及其官方网站链接。

投资报告内容：
{report_content[:8000]}  # 限制内容长度避免超过token限制

要求：
1. 提取报告中提到的所有投资平台、交易平台、存储平台等
2. 提取对应的官方网站链接
3. 返回格式为JSON，包含platforms数组，每个元素包含name和url字段
4. 平台名称要简洁明了，不要包含描述性文字

例如：
{{
  "platforms": [
    {{"name": "Interactive Brokers", "url": "https://www.interactivebrokers.com/"}},
    {{"name": "Coinbase", "url": "https://www.coinbase.com/"}},
    {{"name": "Ledger钱包", "url": "https://www.ledger.com/"}}
  ]
}}

请只返回JSON格式的结果，不要其他文字。
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的投资报告分析助手，擅长从投资报告中提取关键信息。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # 清理响应文本，提取JSON部分
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                result_data = json.loads(json_str)
                
                platforms = {}
                for platform in result_data.get("platforms", []):
                    name = platform.get("name", "").strip()
                    url = platform.get("url", "").strip()
                    if name and url:
                        # 清理URL
                        clean_url = self.clean_url(url)
                        if clean_url and self.is_valid_url(clean_url):
                            platforms[name] = clean_url
                
                return platforms
            else:
                self.print_warning("API响应格式不正确，无法解析平台信息")
                return {}
                
        except Exception as e:
            self.print_error(f"API提取平台信息失败: {str(e)}")
            return {}
    
    def clean_url(self, url):
        """清理URL"""
        if not url or not isinstance(url, str):
            return None
        
        url = url.strip()
        
        # 移除多余的协议前缀
        if url.startswith('https://https://'):
            url = url.replace('https://https://', 'https://')
        elif url.startswith('http://https://'):
            url = url.replace('http://https://', 'https://')
        
        # 确保以https://开头
        if not url.startswith(('https://', 'http://')):
            url = 'https://' + url
        
        # 移除URL后面的非URL字符
        url = re.sub(r'[\)）\.,;:!?<>].*$', '', url)
        
        # 确保URL以域名结束，移除路径中的问题字符
        url = re.sub(r'[^\w\-\/\.\:\#\?\=\&\%]+\/*$', '', url)
        
        return url
    
    def is_valid_url(self, url):
        """检查URL是否有效"""
        if not url or not isinstance(url, str):
            return False
        
        # 基本格式检查
        if not url.startswith(('https://', 'http://')):
            return False
        
        # 检查是否包含有效的域名
        domain_pattern = r'https?://([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        match = re.search(domain_pattern, url)
        if not match:
            return False
        
        domain = match.group(1)
        if not domain or len(domain) < 3:
            return False
        
        return True
    
    def parse_investment_details_via_api(self, report_content):
        """使用API解析投资详情"""
        if not self.client:
            self.print_warning("DeepSeek API未配置，无法使用智能解析")
            return {}
        
        try:
            prompt = f"""
请从以下投资报告中提取详细的投资配置信息。

投资报告内容：
{report_content[:8000]}

要求：
1. 提取权益类资产、固定收益类资产、加密货币资产的详细信息
2. 每类资产包含：产品名称、投资平台、投资金额
3. 对于加密货币资产，还要提取交易平台和存储平台
4. 返回格式为JSON

格式示例：
{{
  "equity": {{
    "name": "iShares Core S&P 500 ETF (IVV)",
    "platform": "Interactive Brokers",
    "amount": "2,560元"
  }},
  "fixed_income": {{
    "name": "Vanguard Total Bond Market ETF (BND)",
    "platform": "Interactive Brokers", 
    "amount": "2,560元"
  }},
  "crypto": {{
    "name": "比特币 (BTC)",
    "platform": "比特币冷钱包",
    "trading_platform": "Coinbase",
    "amount": "1,280元"
  }}
}}

请只返回JSON格式的结果，不要其他文字。
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的投资报告分析助手，擅长提取结构化投资信息。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1500
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # 清理响应文本，提取JSON部分
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                result_data = json.loads(json_str)
                return result_data
            else:
                self.print_warning("API响应格式不正确，无法解析投资详情")
                return {}
                
        except Exception as e:
            self.print_error(f"API解析投资详情失败: {str(e)}")
            return {}
    
    def extract_amount(self, text):
        """从文本中提取金额"""
        try:
            matches = re.findall(r'[\d,]+\.?\d*', text)
            if matches:
                amount = float(matches[0].replace(',', ''))
                return f"{amount:,.0f}元"
            return text
        except:
            return text
    
    def format_amount(self, amount):
        """格式化金额显示"""
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
        """保存配置到文件"""
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
        self.print_header("投资执行系统")
        
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
        
        if not os.path.exists(self.history_dir):
            self.print_error("history目录不存在")
            return False
        
        # 查找最新的报告文件
        self.current_report_file = self.find_latest_report()
        if not self.current_report_file:
            return False
        
        # 读取报告内容
        self.report_content = self.read_report_content(self.current_report_file)
        if not self.report_content:
            return False
        
        self.print_success(f"已加载最新投资报告")
        return True
    
    def display_portfolio(self):
        """显示投资组合概览"""
        if not self.report_content:
            self.print_error("没有可用的投资报告")
            return
        
        self.print_header("投资报告概览")
        
        # 提取报告基本信息
        report_info = []
        
        # 从文件名提取会话信息
        file_name = os.path.basename(self.current_report_file)
        session_match = re.search(r'session_(\d+)_(\d{8})_(\d{6})', file_name)
        if session_match:
            session_id = session_match.group(1)
            date_str = session_match.group(2)
            time_str = session_match.group(3)
            formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]} {time_str[:2]}:{time_str[2:4]}:{time_str[4:6]}"
            report_info.append(["会话ID", session_id])
            report_info.append(["报告时间", formatted_date])
        
        # 从内容中提取其他信息
        if "月收入" in self.report_content:
            income_match = re.search(r'月收入[：:]\s*([\d,]+\.?\d*)', self.report_content)
            if income_match:
                report_info.append(["月收入", f"{float(income_match.group(1).replace(',', '')):,.0f}元"])
        
        if "可用于投资" in self.report_content:
            investment_match = re.search(r'可用于投资[：:]\s*([\d,]+\.?\d*)', self.report_content)
            if investment_match:
                report_info.append(["可用投资", f"{float(investment_match.group(1).replace(',', '')):,.0f}元"])
        
        if "市场状况" in self.report_content:
            market_match = re.search(r'市场状况[：:]\s*([^\n]+)', self.report_content)
            if market_match:
                report_info.append(["市场状况", self.clean_text(market_match.group(1))])
        
        if report_info:
            print(tabulate(report_info, tablefmt="grid", colalign=("right", "left")))
        
        # 解析投资详情
        self.print_section("正在解析投资详情...")
        investment_details = self.parse_investment_details_via_api(self.report_content)
        
        self.print_section("投资分配详情")
        
        investment_table = []
        
        equity = investment_details.get("equity", {})
        if equity.get("name") or equity.get("platform") or equity.get("amount"):
            investment_table.append([
                "📈 权益类资产",
                equity.get("name", "待确定"),
                equity.get("platform", "待确定"),
                self.format_amount(equity.get("amount", "")) or "待分配"
            ])
        
        fixed_income = investment_details.get("fixed_income", {})
        if fixed_income.get("name") or fixed_income.get("platform") or fixed_income.get("amount"):
            investment_table.append([
                "💰 固定收益资产",
                fixed_income.get("name", "待确定"),
                fixed_income.get("platform", "待确定"),
                self.format_amount(fixed_income.get("amount", "")) or "待分配"
            ])
        
        crypto = investment_details.get("crypto", {})
        if crypto.get("name") or crypto.get("platform") or crypto.get("amount"):
            platform_info = crypto.get("platform", "")
            if crypto.get("trading_platform"):
                if platform_info:
                    platform_info += f" ({crypto['trading_platform']})"
                else:
                    platform_info = crypto['trading_platform']
            
            investment_table.append([
                "🔗 加密货币资产",
                crypto.get("name", "待确定"),
                platform_info or "待确定",
                self.format_amount(crypto.get("amount", "")) or "待分配"
            ])
        
        if investment_table:
            print(tabulate(
                investment_table, 
                headers=["资产类型", "产品名称", "投资平台", "投资金额"],
                tablefmt="grid"
            ))
        else:
            self.print_warning("未能解析出投资详情")
    
    def display_full_advice(self):
        """显示完整的投资建议"""
        if not self.report_content:
            self.print_error("没有可用的投资报告")
            return
        
        self.print_header("完整投资报告")
        print(self.report_content)
    
    def open_investment_platforms(self):
        """打开投资平台 - 使用API提取平台和链接"""
        if not self.report_content:
            self.print_error("没有可用的投资报告")
            return
        
        self.print_header("平台链接导航")
        
        # 使用API提取平台和链接
        self.show_progress("正在通过AI分析报告中的平台链接", 3)
        
        platforms = self.extract_platforms_via_api(self.report_content)
        
        # 显示找到的平台
        self.print_section("报告中提到的投资平台")
        
        if not platforms:
            self.print_warning("未找到任何投资平台链接")
            self.print_info("请查看完整投资报告获取平台信息")
            return
        
        # 创建平台列表显示
        platform_list = []
        for i, (name, url) in enumerate(platforms.items(), 1):
            platform_list.append([i, name, self.wrap_text(url, 40)])
        
        print(tabulate(platform_list, headers=["编号", "平台名称", "官方网站"], tablefmt="grid"))
        
        # 用户选择菜单
        print("\n" + "=" * 50)
        print("🎯 平台导航菜单")
        print("=" * 50)
        
        options = list(platforms.keys())
        for i, option in enumerate(options, 1):
            print(f"  {i}. 🌐 打开 {option}")
        print(f"  {len(options) + 1}. 🚀 一键打开所有报告中的平台")
        print(f"  {len(options) + 2}. 📖 查看完整投资报告")
        print(f"  {len(options) + 3}. ↩️ 返回主菜单")
        
        try:
            choice = input("\n🎯 请输入您的选择: ").strip()
            
            if not choice:
                self.print_error("请输入选择")
                return
            
            if choice.isdigit():
                choice_num = int(choice)
                
                # 单个平台打开
                if 1 <= choice_num <= len(options):
                    platform_name = options[choice_num - 1]
                    url = platforms[platform_name]
                    self.print_success(f"正在打开 {platform_name}...")
                    print(f"🔗 官方网站: {url}")
                    webbrowser.open(url)
                
                # 一键打开所有平台
                elif choice_num == len(options) + 1:
                    self.print_success("正在打开报告中提到的所有平台...")
                    success_count = 0
                    for name, url in platforms.items():
                        if self.is_valid_url(url):
                            self.print_info(f"打开 {name}")
                            webbrowser.open(url)
                            success_count += 1
                        else:
                            self.print_warning(f"跳过 {name}，链接无效: {url}")
                    self.print_success(f"成功打开 {success_count} 个平台")
                
                # 查看完整报告
                elif choice_num == len(options) + 2:
                    self.display_full_advice()
                
                # 返回主菜单
                elif choice_num == len(options) + 3:
                    return
                
                else:
                    self.print_error("无效的选择，请重新输入")
            else:
                self.print_error("请输入有效的数字")
                
        except Exception as e:
            self.print_error(f"操作过程中出错: {str(e)}")
    
    def create_investment_plan(self):
        """创建投资计划"""
        if not self.report_content:
            self.print_error("没有可用的投资报告")
            return
        
        self.print_header("创建投资执行计划")
        
        self.print_section("正在解析投资详情...")
        investment_details = self.parse_investment_details_via_api(self.report_content)
        
        plan_content = self.generate_investment_plan(investment_details)
        
        # 使用会话ID作为文件名
        file_name = os.path.basename(self.current_report_file).replace('.md', '_plan.md')
        plan_file = os.path.join(self.temp_dir, file_name)
        
        try:
            with open(plan_file, 'w', encoding='utf-8') as f:
                f.write(plan_content)
            
            self.print_success(f"投资计划已保存: {plan_file}")
            
            self.print_section("投资计划摘要")
            print(self.wrap_text(plan_content, width=70))
            
        except Exception as e:
            self.print_error(f"保存投资计划失败: {str(e)}")
    
    def generate_investment_plan(self, investment_details):
        """生成投资计划内容"""
        # 从文件名提取会话信息
        file_name = os.path.basename(self.current_report_file)
        session_match = re.search(r'session_(\d+)_(\d{8})_(\d{6})', file_name)
        
        if session_match:
            session_id = session_match.group(1)
            date_str = session_match.group(2)
            time_str = session_match.group(3)
            formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]} {time_str[:2]}:{time_str[2:4]}:{time_str[4:6]}"
        else:
            session_id = "未知"
            formatted_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 从报告内容中提取金额信息
        available_amount = "待确定"
        if "可用于投资" in self.report_content:
            investment_match = re.search(r'可用于投资[：:]\s*([\d,]+\.?\d*)', self.report_content)
            if investment_match:
                available_amount = f"{float(investment_match.group(1).replace(',', '')):,.0f}元"
        
        plan_content = f"""# 📋 投资执行计划

## 📊 基本信息
- **计划时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **投资会话**: 第{session_id}次
- **报告时间**: {formatted_date}
- **总投资金额**: {available_amount}
- **报告文件**: {os.path.basename(self.current_report_file)}

## 💰 投资分配
"""
        
        asset_types = [
            ("equity", "📈 权益类资产"),
            ("fixed_income", "💰 固定收益类资产"), 
            ("crypto", "🔗 加密货币资产")
        ]
        
        for asset_key, asset_name in asset_types:
            asset = investment_details.get(asset_key, {})
            if asset.get("name") or asset.get("platform"):
                plan_content += f"""
### {asset_name}
- **产品**: {asset.get('name', '待确定')}
- **平台**: {asset.get('platform', '待确定')}
- **金额**: {self.format_amount(asset.get('amount', '待分配'))}
- **操作步骤**:
  1. 登录投资平台
  2. 搜索目标产品
  3. 输入投资金额
  4. 确认交易信息
  5. 完成交易并保存凭证
"""
        
        plan_content += f"""
## ⚠️ 注意事项
- 基于投资报告生成，请仔细核对
- 确保网络连接安全
- 仔细核对交易信息
- 保存所有交易凭证

---
*生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
*基于AI解析报告中实际内容生成*
"""
        
        return plan_content
    
    def show_investment_instructions(self):
        """显示投资操作指南"""
        if not self.report_content:
            self.print_error("没有可用的投资报告")
            return
        
        self.print_header("投资操作指南")
        
        self.print_section("正在解析投资详情...")
        investment_details = self.parse_investment_details_via_api(self.report_content)
        
        asset_types = [
            ("equity", "📈 权益类资产"),
            ("fixed_income", "💰 固定收益资产"),
            ("crypto", "🔗 加密货币资产")
        ]
        
        for asset_key, asset_name in asset_types:
            asset = investment_details.get(asset_key, {})
            if asset.get("name") or asset.get("platform"):
                self.print_section(f"{asset_name} - {asset.get('name', '投资产品')}")
                
                instructions = [
                    ["1️⃣", "登录平台", asset.get("platform", "投资平台")],
                    ["2️⃣", "搜索产品", asset.get("name", "目标产品")],
                    ["3️⃣", "输入金额", self.format_amount(asset.get("amount", "指定金额"))],
                    ["4️⃣", "确认交易", "仔细核对信息"],
                    ["5️⃣", "完成投资", "保存交易凭证"]
                ]
                
                print(tabulate(instructions, tablefmt="simple", colalign=("center", "left", "left")))
        
        self.print_section("💡 温馨提示")
        tips = [
            "🔸 建议在安全的网络环境下操作",
            "🔸 仔细核对所有交易信息", 
            "🔸 保存交易记录和凭证",
            "🔸 如有疑问请查看完整投资报告"
        ]
        for tip in tips:
            print(f"  {tip}")
    
    def run(self):
        """运行投资执行系统"""
        if not self.initialize():
            return False
        
        while True:
            self.print_header("投资执行系统")
            
            menu_options = [
                ["1", "📊 查看投资组合", "显示投资配置详情"],
                ["2", "📖 查看完整报告", "显示原始投资报告"],
                ["3", "🌐 平台链接导航", "打开报告中提到的平台"],
                ["4", "📋 创建投资计划", "生成执行计划"],
                ["5", "📖 查看操作指南", "获取步骤指导"],
                ["6", "🔄 重新加载报告", "重新加载最新报告"],
                ["7", "🚪 退出系统", "结束程序运行"]
            ]
            
            print(tabulate(menu_options, headers=["选项", "功能", "说明"], tablefmt="grid"))
            
            choice = input("\n🎯 请选择功能 (1-7): ").strip()
            
            if choice == "1":
                self.display_portfolio()
            elif choice == "2":
                self.display_full_advice()
            elif choice == "3":
                self.open_investment_platforms()
            elif choice == "4":
                self.create_investment_plan()
            elif choice == "5":
                self.show_investment_instructions()
            elif choice == "6":
                # 重新加载最新报告
                self.current_report_file = self.find_latest_report()
                if self.current_report_file:
                    self.report_content = self.read_report_content(self.current_report_file)
                    if self.report_content:
                        self.print_success("已重新加载最新投资报告")
                    else:
                        self.print_error("重新加载报告失败")
                else:
                    self.print_error("未找到最新报告")
            elif choice == "7":
                self.print_success("感谢使用投资执行系统！祝您投资顺利！💰")
                break
            else:
                self.print_error("无效选择，请重新输入")
            
            if choice != "7":
                input("\n⏎ 按回车键继续...")

def main():
    """主函数"""
    try:
        executor = InvestmentExecutor()
        executor.run()
    except KeyboardInterrupt:
        print("\n\n👋 用户中断程序，再见！")
    except Exception as e:
        print(f"\n💥 程序运行出错: {str(e)}")

if __name__ == "__main__":
    main()
