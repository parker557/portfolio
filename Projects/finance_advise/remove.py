import os
import shutil
from pathlib import Path
import sys
import glob

class ProjectCleaner:
    def __init__(self):
        self.root_path = None
        self.protected_files = [
            'finance_advice.py',
            'get_report.py', 
            'pay.py',
            'remove.py',
            'news.py',
            'requirements.txt',
            'README.md',
            '.git',
            '.gitignore'
        ]
        self.protected_extensions = ['.py', '.txt', '.md']
        
        # 定义需要清理的缓存文件模式
        self.cache_patterns = [
            '__pycache__',
            '*.pyc',
            '*.pyo',
            '*.pyd',
            '.Python',
            'pip-log.txt',
            'pip-delete-this-directory.txt',
            'htmlcov',
            '.tox',
            '.coverage',
            '.cache',
            'nosetests.xml',
            'coverage.xml',
            '*.cover',
            '*.log',
            '.pytest_cache',
            '.mypy_cache',
            '.vscode',
            '.idea',
            '*.egg-info',
            '.eggs',
            'dist',
            'build'
        ]
        
    def initialize(self):
        """初始化系统"""
        print("⚠️ " * 20)
        print("🚨 项目清理工具 - 危险操作!")
        print("⚠️ " * 20)
        
        self.root_path = input("请输入要清理的根目录路径: ").strip()
        
        if not os.path.exists(self.root_path):
            print("❌ 路径不存在!")
            return False
            
        # 转换为绝对路径
        self.root_path = os.path.abspath(self.root_path)
        
        print(f"\n目标目录: {self.root_path}")
        return True
    
    def scan_directory(self):
        """扫描目录内容"""
        print(f"\n📁 扫描目录内容...")
        
        all_items = []
        protected_items = []
        to_delete_items = []
        
        # 扫描根目录下的所有文件和文件夹
        for item in Path(self.root_path).iterdir():
            item_info = {
                'name': item.name,
                'path': item,
                'is_file': item.is_file(),
                'is_dir': item.is_dir(),
                'size': item.stat().st_size if item.is_file() else 0,
                'type': 'regular'
            }
            
            # 检查是否受保护
            if self.is_protected(item):
                protected_items.append(item_info)
            else:
                to_delete_items.append(item_info)
            
            all_items.append(item_info)
        
        # 扫描缓存文件和目录
        cache_items = self.scan_cache_files()
        
        return {
            'all': all_items,
            'protected': protected_items,
            'to_delete': to_delete_items,
            'cache': cache_items
        }
    
    def scan_cache_files(self):
        """扫描缓存文件和目录"""
        cache_items = []
        
        print("🔍 扫描缓存文件...")
        
        for pattern in self.cache_patterns:
            try:
                # 使用glob模式匹配
                matches = []
                if pattern.startswith('*'):
                    # 文件模式
                    matches = list(Path(self.root_path).rglob(pattern))
                else:
                    # 目录模式
                    dir_path = Path(self.root_path) / pattern
                    if dir_path.exists():
                        matches = [dir_path]
                    else:
                        # 也尝试递归查找
                        matches = list(Path(self.root_path).rglob(pattern))
                
                for match in matches:
                    # 跳过受保护的文件
                    if self.is_protected(match):
                        continue
                        
                    # 检查是否在根目录下（避免删除系统文件）
                    try:
                        match_relative = match.relative_to(self.root_path)
                    except ValueError:
                        continue  # 不在目标目录内
                    
                    item_info = {
                        'name': str(match_relative),
                        'path': match,
                        'is_file': match.is_file(),
                        'is_dir': match.is_dir(),
                        'size': match.stat().st_size if match.is_file() else 0,
                        'type': 'cache'
                    }
                    
                    # 避免重复
                    if not any(cache_item['path'] == match for cache_item in cache_items):
                        cache_items.append(item_info)
                        
            except Exception as e:
                print(f"⚠️  扫描缓存模式 '{pattern}' 时出错: {e}")
                continue
        
        return cache_items
    
    def is_protected(self, item_path):
        """检查项目是否受保护"""
        item_name = item_path.name
        
        # 检查保护文件列表
        if item_name in self.protected_files:
            return True
        
        # 检查保护扩展名
        if item_path.is_file():
            ext = item_path.suffix.lower()
            if ext in self.protected_extensions:
                # 但如果是缓存文件（如.pyc），即使扩展名受保护也要删除
                if item_name.endswith('.pyc') or item_name.endswith('.pyo'):
                    return False
                return True
        
        # 检查是否是Python包文件
        if item_name == '__init__.py':
            return True
            
        return False
    
    def format_size(self, size_bytes):
        """格式化文件大小"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names)-1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def display_scan_results(self, scan_results):
        """显示扫描结果"""
        protected = scan_results['protected']
        to_delete = scan_results['to_delete']
        cache_items = scan_results['cache']
        
        print(f"\n📊 扫描结果:")
        print(f"  • 受保护项目: {len(protected)} 个")
        print(f"  • 待删除常规项目: {len(to_delete)} 个")
        print(f"  • 待删除缓存项目: {len(cache_items)} 个")
        
        # 计算总大小
        total_size = sum(item['size'] for item in to_delete) + sum(item['size'] for item in cache_items)
        print(f"  • 总删除大小: {self.format_size(total_size)}")
        
        if protected:
            print(f"\n🛡️  受保护的项目:")
            for item in protected:
                item_type = "文件" if item['is_file'] else "文件夹"
                print(f"    • {item['name']} ({item_type})")
        
        if to_delete:
            print(f"\n🗑️  待删除的常规项目:")
            for item in to_delete:
                item_type = "文件" if item['is_file'] else "文件夹"
                size_info = f" - {self.format_size(item['size'])}" if item['is_file'] else ""
                print(f"    • {item['name']} ({item_type}){size_info}")
        
        if cache_items:
            print(f"\n🗑️  待删除的缓存项目:")
            for item in cache_items:
                item_type = "文件" if item['is_file'] else "文件夹"
                size_info = f" - {self.format_size(item['size'])}" if item['is_file'] else ""
                print(f"    • {item['name']} ({item_type}){size_info}")
    
    def confirm_deletion(self, total_count):
        """确认删除操作"""
        if total_count == 0:
            print("✅ 没有需要删除的项目")
            return False
        
        print(f"\n{'🚨' * 10} 危险操作 {'🚨' * 10}")
        print("此操作将永久删除上述所有项目!")
        print("此操作不可撤销!")
        print(f"{'🚨' * 30}")
        
        # 第一次确认
        confirm1 = input(f"\n确定要删除 {total_count} 个项目吗? (输入 'DELETE' 确认): ").strip()
        if confirm1 != "DELETE":
            print("❌ 操作取消")
            return False
        
        # 第二次确认
        confirm2 = input("请再次确认，输入 'CONFIRM DELETE': ").strip()
        if confirm2 != "CONFIRM DELETE":
            print("❌ 操作取消")
            return False
        
        # 最终确认
        confirm3 = input("最后警告! 输入 'YES I AM SURE': ").strip()
        if confirm3 != "YES I AM SURE":
            print("❌ 操作取消")
            return False
        
        return True
    
    def delete_items(self, items):
        """删除项目"""
        success_count = 0
        fail_count = 0
        
        for item in items:
            try:
                if item['is_file']:
                    os.remove(item['path'])
                    print(f"  ✅ 删除文件: {item['name']}")
                else:
                    shutil.rmtree(item['path'])
                    print(f"  ✅ 删除文件夹: {item['name']}")
                success_count += 1
            except Exception as e:
                print(f"  ❌ 删除失败 {item['name']}: {e}")
                fail_count += 1
        
        return success_count, fail_count
    
    def run_cleanup(self):
        """执行清理操作"""
        print(f"\n🗑️  开始清理操作...")
        
        # 扫描目录
        scan_results = self.scan_directory()
        
        # 显示扫描结果
        self.display_scan_results(scan_results)
        
        total_to_delete = len(scan_results['to_delete']) + len(scan_results['cache'])
        
        # 确认删除
        if not self.confirm_deletion(total_to_delete):
            return
        
        # 执行删除 - 先删除常规项目
        if scan_results['to_delete']:
            print(f"\n🗑️  删除常规项目...")
            success1, fail1 = self.delete_items(scan_results['to_delete'])
        else:
            success1, fail1 = 0, 0
        
        # 执行删除 - 再删除缓存项目
        if scan_results['cache']:
            print(f"\n🗑️  删除缓存项目...")
            success2, fail2 = self.delete_items(scan_results['cache'])
        else:
            success2, fail2 = 0, 0
        
        total_success = success1 + success2
        total_fail = fail1 + fail2
        
        print(f"\n📊 清理完成:")
        print(f"  • 成功: {total_success}")
        print(f"  • 失败: {total_fail}")
        
        if total_fail == 0:
            print(f"\n🎉 项目已完全清理! 现在可以重新开始一个新项目")
            print("💡 建议: 运行 'python finance_advice.py' 开始新的投资周期")
        else:
            print(f"\n⚠️  清理完成，但有 {total_fail} 个项目删除失败")
    
    def show_final_message(self):
        """显示最终消息"""
        print(f"\n{'='*60}")
        print("🔄 项目重置完成")
        print(f"{'='*60}")
        print("现在您可以:")
        print("  1. 运行 'python finance_advice.py' 开始新的投资周期")
        print("  2. 检查项目根目录，确保所有生成文件已清理")
        print("  3. 如果需要，重新配置API密钥或其他设置")
        print(f"{'='*60}")
    
    def run(self):
        """运行主程序"""
        if not self.initialize():
            return
        
        # 执行清理
        self.run_cleanup()
        
        # 显示最终消息
        self.show_final_message()

if __name__ == "__main__":
    try:
        cleaner = ProjectCleaner()
        cleaner.run()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n程序发生错误: {e}")
        import traceback
        traceback.print_exc()
