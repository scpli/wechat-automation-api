import argparse
import json
import sys
import os

# 修复 Windows 下 stdout 中文乱码问题
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 确保能导入同目录的其他模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    parser = argparse.ArgumentParser(description="微信发信命令行工具(Skill入口)")
    parser.add_argument("--to", required=True, help="接收者联系人名称")
    parser.add_argument("--content", required=True, help="消息内容、图片URL或本地文件路径")
    parser.add_argument("--action", choices=["sendtext", "sendpic", "sendfile"], default="sendtext", help="类型: sendtext(默认)、sendpic 或 sendfile")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出结果，便于 Agent 稳定解析")
    
    args = parser.parse_args()

    def output(success, code, message):
        if args.json:
            print(json.dumps({
                "success": success,
                "code": code,
                "message": message,
                "to": args.to,
                "action": args.action
            }, ensure_ascii=False))
        else:
            if success:
                print(message)
            else:
                print(f"发送失败: {message}")
                print(f"错误代码: {code}")
    
    try:
        try:
            from wechat_controller import WeChatController
        except ModuleNotFoundError as e:
            output(False, "DEPENDENCY_MISSING", f"缺少 Python 依赖: {e.name}。请在项目根目录执行 pip install -r requirements.txt。")
            sys.exit(1)

        controller = WeChatController()
        if args.action == "sendfile":
            result = controller.search_and_send_file_result(args.to, args.content)
        elif args.action == "sendpic":
            result = controller.search_and_send_picture_result(args.to, args.content)
        else:
            result = controller.search_and_send_result(args.to, args.content)
            
        output(result.success, result.code, result.message)
        if result.success:
            sys.exit(0)
        sys.exit(1)
            
    except Exception as e:
        output(False, "CLI_EXCEPTION", f"Skill CLI 执行异常: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
