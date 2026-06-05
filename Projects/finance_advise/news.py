import os
import json
import re
import glob
from datetime import datetime
from openai import OpenAI
import sys

class FinanceAnalyzer:
    def __init__(self):
        # 使用OpenAI SDK调用DeepSeek API
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com/v1"
        )
        self.model = "deepseek-reasoner"
        self.root_path = None
        self.config_file = ".finance_config.json"
        self.history_dir = "history"
        self.temp_dir = "temp"
        
    def setup_api(self):
        """验证API设置"""
        if not self.api_key:
            print("❌ 未找到DEEPSEEK_API_KEY环境变量")
            print("请设置环境变量: export DEEPSEEK_API_KEY=your_api_key_here")
            sys.exit(1)
        
        try:
            # 测试API连接
            test_response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "测试连接"}],
                max_tokens=10
            )
            print("✅ API连接测试成功")
        except Exception as e:
            print(f"❌ API连接失败: {e}")
            print("请检查: 1) API密钥是否正确 2) 网络连接 3) API服务状态")
            sys.exit(1)
    
    def load_config(self):
        """加载或创建配置文件"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.root_path = config.get("root_path")
                print(f"✅ 加载配置文件: {self.root_path}")
        else:
            self.root_path = input("请输入根目录路径: ").strip()
            config = {
                "root_path": self.root_path,
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            print("✅ 配置文件创建成功")
        
        # 创建必要的目录
        os.makedirs(os.path.join(self.root_path, self.temp_dir), exist_ok=True)
        os.makedirs(os.path.join(self.root_path, self.history_dir), exist_ok=True)
    
    def get_latest_report(self):
        """获取最新的投资报告"""
        history_path = os.path.join(self.root_path, self.history_dir)
        
        # 查找所有符合命名模式的目录
        report_dirs = []
        for item in os.listdir(history_path):
            item_path = os.path.join(history_path, item)
            if os.path.isdir(item_path) and re.match(r'\d+_\d{8}_\d+', item):
                report_dirs.append(item_path)
        
        if not report_dirs:
            print("❌ 未找到历史报告目录")
            return None
        
        # 按序号排序，获取最新的报告目录
        def get_sequence(dir_path):
            match = re.search(r'(\d+)_', os.path.basename(dir_path))
            return int(match.group(1)) if match else 0
        
        latest_dir = max(report_dirs, key=get_sequence)
        print(f"✅ 找到最新报告目录: {os.path.basename(latest_dir)}")
        
        # 在目录中查找任何.md文件
        md_files = glob.glob(os.path.join(latest_dir, "*.md"))
        if not md_files:
            print(f"❌ 在目录 {os.path.basename(latest_dir)} 中未找到.md文件")
            return None
        
        # 如果有多个.md文件，选择第一个（或按需要选择其他策略）
        report_file = md_files[0]
        if len(md_files) > 1:
            print(f"⚠️ 目录中有多个.md文件，选择: {os.path.basename(report_file)}")
        
        try:
            with open(report_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"✅ 加载报告文件: {os.path.basename(report_file)}")
            return content, os.path.basename(latest_dir)
        except Exception as e:
            print(f"❌ 读取报告文件失败: {e}")
            return None
    
    def extract_stock_info(self, report_content):
        """从报告中提取股票信息"""
        stocks = []
        
        # 提取权益类资产
        equity_match = re.search(r'权益类资产.*?\*\*建议\*\*:\s*(.*?)\s*-', report_content, re.DOTALL)
        if equity_match:
            stock_info = equity_match.group(1).strip()
            stocks.append(stock_info)
        
        # 提取固定收益类资产
        fixed_income_match = re.search(r'固定收益类资产.*?\*\*建议\*\*:\s*(.*?)\s*-', report_content, re.DOTALL)
        if fixed_income_match:
            stock_info = fixed_income_match.group(1).strip()
            stocks.append(stock_info)
        
        # 提取加密货币
        crypto_match = re.search(r'加密货币资产.*?\*\*建议\*\*:\s*(.*?)\s*-', report_content, re.DOTALL)
        if crypto_match:
            crypto_info = crypto_match.group(1).strip()
            stocks.append(crypto_info)
        
        return stocks
    
    def generate_analysis_prompt(self, report_content, stocks):
        """生成分析提示词"""
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        prompt = f"""基于以下投资报告和当前日期 {current_date}，请提供专业的投资分析：

投资报告摘要：
{report_content[:2000]}...

持有的资产：
{chr(10).join(f"- {stock}" for stock in stocks)}

请分析以下内容：

1. 📈 **今日走势分析**
   - 上述资产的预期今日走势
   - 主要影响因素（宏观经济、行业新闻等）

2. ⚠️ **注意事项**
   - 需要特别关注的风险点
   - 技术面或基本面的关键信号

3. 💡 **投资建议**
   - 持有、增持、减持或卖出的建议
   - 仓位调整建议

4. 🔔 **重大事件提醒**
   - 近期可能影响持股的重要事件
   - 财报日期、分红除权等关键时间点
   - 行业政策变化或公司重大公告

5. 📊 **新闻摘要**
   - 与持股相关的重要新闻
   - 市场情绪和资金流向分析

请用中文回复，内容要专业、实用，避免过于技术化的术语，适合普通投资者理解。
"""
        return prompt
    
    def get_ai_analysis(self, prompt):
        """调用DeepSeek API获取分析"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的投资顾问，擅长分析股票市场、提供投资建议和风险评估。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ API调用失败: {e}")
            return None
    
    def save_analysis(self, analysis_content, base_filename):
        """保存分析结果"""
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        sequence = base_filename.split('_')[0]  # 提取序号
        
        filename = f"{sequence}_{current_time}.md"
        filepath = os.path.join(self.root_path, self.temp_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(analysis_content)
        
        print(f"✅ 分析结果已保存: {filepath}")
        return filepath
    
    def print_user_friendly(self, content):
        """以用户友好的格式打印内容"""
        print("\n" + "="*80)
        print("📊 投资分析报告")
        print("="*80)
        print(content)
        print("="*80)
    
    def update_config_timestamp(self):
        """更新配置文件的最后更新时间"""
        config = {
            "root_path": self.root_path,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def run(self):
        """主运行函数"""
        print("🚀 启动投资分析程序...")
        
        # 设置和验证API
        self.setup_api()
        
        # 加载配置
        self.load_config()
        
        # 获取最新报告
        report_data = self.get_latest_report()
        if not report_data:
            return
        
        report_content, base_filename = report_data
        
        # 提取股票信息
        stocks = self.extract_stock_info(report_content)
        print(f"✅ 提取的资产信息: {stocks}")
        
        # 生成提示词
        prompt = self.generate_analysis_prompt(report_content, stocks)
        
        # 获取AI分析
        print("🤖 正在获取AI分析...")
        analysis_content = self.get_ai_analysis(prompt)
        
        if analysis_content:
            # 打印结果
            self.print_user_friendly(analysis_content)
            
            # 保存结果
            saved_file = self.save_analysis(analysis_content, base_filename)
            
            # 更新配置时间戳
            self.update_config_timestamp()
            
            print(f"\n✅ 分析完成！文件已保存至: {saved_file}")
        else:
            print("❌ 分析失败，请检查API设置")

def main():
    analyzer = FinanceAnalyzer()
    analyzer.run()

if __name__ == "__main__":
    main()
