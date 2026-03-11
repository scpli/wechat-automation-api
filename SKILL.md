---
name: "wechat-automation"
description: "通过 UIAutomation 控制微信发送文本和图片消息"
---

# 微信自动发信 Skill

本 Skill 允许智能体/大语言模型通过 Windows 原生的 UIAutomation 技术，直接控制本机的微信客户端发送消息。

## 前置环境与要求
1. **Windows 系统**：依赖 `uiautomation` 库与 Windows API。
2. **微信客户端**：需在真机登录并保持微信运行。建议开启微信唤醒的默认快捷键 `Ctrl+Alt+W`。
3. **依赖安装**：需执行 `pip install -r requirements.txt` 安装相关 Python 依赖库。

## 作为 Skill 调用

你可以通过直接执行 `scripts/skill_cli.py` 脚本使用此 Skill：

### 发送文本消息
```bash
python scripts/skill_cli.py --to "联系人或群组名称" --content "你好，这是一条来自智能体的消息"
```

### 发送图片消息
```bash
python scripts/skill_cli.py --to "联系人或群组名称" --content "https://example.com/image.png" --action "sendpic"
```

### 执行反馈
- 成功：控制台输出 `发送成功`，退出码为 `0`。
- 失败：控制台输出 `发送失败，未找到窗体或其他错误`，退出码为 `1`。

## 作为独立 HTTP 服务运行

如果需要持续监听并通过 HTTP API 批量发送异步消息：
1. 双击运行根目录的 `run.bat`（其本质是调用 `python scripts/app.py`）。
2. 服务将在配置文件 `config.json` 指定的端口（默认 8808）启动。
3. 外部应用即可发送 POST 请求将消息放入处理队列进行发送。
