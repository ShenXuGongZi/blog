# HANGZAI学术研究博客

这是一个使用 Flask 构建的简单博客系统，专注于学术研究内容的分享。

## 功能特点

- 用户认证（登录/登出）
- 文章的创建、编辑和查看
- Markdown 支持
- 响应式设计

## 安装说明

1. 克隆仓库：
   ```
   git clone https://github.com/你的用户名/你的仓库名.git
   cd 你的仓库名
   ```

2. 创建并激活虚拟环境：
   ```
   python -m venv venv
   source venv/bin/activate  # 在 Windows 上使用 venv\Scripts\activate
   ```

3. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

4. 初始化数据库：
   ```
   flask init-db
   ```

5. 运行应用：
   ```
   flask run
   ```

6. 在浏览器中访问 `http://localhost:5000`

## 使用说明

- 默认管理员账户：
  - 用户名：admin
  - 密码：password

请在首次登录后立即更改密码。

## 贡献

欢迎提交 issues 和 pull requests。

## 许可证

[MIT License](https://opensource.org/licenses/MIT)
