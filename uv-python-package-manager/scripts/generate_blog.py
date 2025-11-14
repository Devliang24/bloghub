#!/usr/bin/env python3
"""
UV Tutorial Blog Generator
使用 Python 和 UV 生成的博客系统
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape
import yaml

class BlogGenerator:
    def __init__(self, content_dir="content", output_dir="public", template_dir="templates"):
        self.content_dir = Path(content_dir)
        self.output_dir = Path(output_dir)
        self.template_dir = Path(template_dir)

        # 初始化 Jinja2 环境
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )

        # 确保输出目录存在
        self.output_dir.mkdir(exist_ok=True)

        # Markdown 扩展
        self.md = markdown.Markdown(extensions=[
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.attr_list'
        ])

    def parse_frontmatter(self, content):
        """解析 Markdown 文件的前置元数据"""
        if content.startswith('---\n'):
            try:
                end_index = content.find('\n---\n', 4)
                if end_index == -1:
                    return {}, content

                frontmatter_str = content[4:end_index]
                frontmatter = yaml.safe_load(frontmatter_str)
                markdown_content = content[end_index + 5:]
                return frontmatter, markdown_content
            except yaml.YAMLError:
                return {}, content
        else:
            return {}, content

    def render_markdown(self, content):
        """渲染 Markdown 内容为 HTML"""
        html = self.md.convert(content)
        toc = getattr(self.md, 'toc', '')
        return html, toc

    def copy_static_files(self):
        """复制静态文件到输出目录"""
        static_dir = Path("static")
        if static_dir.exists():
            import shutil
            output_static = self.output_dir / "static"
            if output_static.exists():
                shutil.rmtree(output_static)
            shutil.copytree(static_dir, output_static)
            print(f"✅ 复制静态文件到 {output_static}")

    def generate_article(self, md_file):
        """生成单篇文章"""
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 解析前置元数据
            frontmatter, markdown_content = self.parse_frontmatter(content)

            # 渲染 Markdown
            html_content, toc = self.render_markdown(markdown_content)

            # 获取文件信息
            stat = md_file.stat()
            modified_time = datetime.fromtimestamp(stat.st_mtime)

            # 准备模板变量
            template_vars = {
                'title': frontmatter.get('title', md_file.stem.replace('-', ' ').title()),
                'content': html_content,
                'toc': toc,
                'date': frontmatter.get('date', modified_time.strftime('%Y-%m-%d')),
                'author': frontmatter.get('author', 'Devliang24'),
                'description': frontmatter.get('description', ''),
                'tags': frontmatter.get('tags', []),
                'category': frontmatter.get('category', '教程'),
                'reading_time': self.estimate_reading_time(markdown_content),
                'file_path': str(md_file.relative_to(self.content_dir)),
                'last_modified': modified_time.strftime('%Y-%m-%d %H:%M:%S')
            }

            # 加载模板
            template = self.jinja_env.get_template('article.html')

            # 渲染 HTML
            html_output = template.render(**template_vars)

            # 确定输出路径
            relative_path = md_file.relative_to(self.content_dir)
            output_path = self.output_dir / relative_path.with_suffix('.html')

            # 创建输出目录
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # 写入文件
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_output)

            print(f"✅ 生成文章: {output_path}")
            return {
                'title': template_vars['title'],
                'url': str(output_path.relative_to(self.output_dir)),
                'date': template_vars['date'],
                'description': template_vars['description'],
                'tags': template_vars['tags'],
                'category': template_vars['category'],
                'reading_time': template_vars['reading_time']
            }

        except Exception as e:
            print(f"❌ 生成文章失败 {md_file}: {e}")
            return None

    def estimate_reading_time(self, content, words_per_minute=200):
        """估算阅读时间（分钟）"""
        word_count = len(content.split())
        minutes = max(1, round(word_count / words_per_minute))
        return minutes

    def find_markdown_files(self):
        """查找所有 Markdown 文件"""
        md_files = []
        for pattern in ['**/*.md', '**/*.markdown']:
            md_files.extend(self.content_dir.glob(pattern))
        return sorted(md_files)

    def generate_index(self, articles):
        """生成首页"""
        try:
            template_vars = {
                'title': 'UV Python 包管理器教程',
                'description': '快速入门 UV，体验超快的 Python 包管理',
                'articles': articles[:10],  # 最新10篇文章
                'featured_articles': articles[:3],  # 精选文章
                'total_articles': len(articles)
            }

            template = self.jinja_env.get_template('index.html')
            html_output = template.render(**template_vars)

            output_path = self.output_dir / 'index.html'
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_output)

            print(f"✅ 生成首页: {output_path}")

        except Exception as e:
            print(f"❌ 生成首页失败: {e}")

    def generate_blog(self):
        """生成整个博客"""
        print("🚀 开始生成博客...")

        # 复制静态文件
        self.copy_static_files()

        # 查找所有文章
        md_files = self.find_markdown_files()
        print(f"📝 找到 {len(md_files)} 篇文章")

        # 生成所有文章
        articles = []
        for md_file in md_files:
            article = self.generate_article(md_file)
            if article:
                articles.append(article)

        # 按日期排序
        articles.sort(key=lambda x: x['date'], reverse=True)

        # 生成首页
        self.generate_index(articles)

        print(f"✅ 博客生成完成！共生成 {len(articles)} 篇文章")
        print(f"📂 输出目录: {self.output_dir.absolute()}")

        return articles

def create_default_templates():
    """创建默认模板文件"""
    templates_dir = Path("templates")
    templates_dir.mkdir(exist_ok=True)

    # 基础模板
    base_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}UV Tutorial{% endblock %} - UV Python包管理器教程</title>
    <meta name="description" content="{% block description %}学习 UV Python 包管理器，提升开发效率{% endblock %}">
    <link rel="stylesheet" href="/static/css/style.css">
    <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
</head>
<body>
    <header>
        <div class="container">
            <div class="header-content">
                <a href="/" class="logo">🚀 UV Tutorial</a>
                <nav>
                    <ul>
                        <li><a href="/">首页</a></li>
                        <li><a href="/tutorials/uv/getting-started.html">UV教程</a></li>
                        <li><a href="https://github.com/astral-sh/uv" target="_blank">GitHub</a></li>
                    </ul>
                </nav>
            </div>
        </div>
    </header>

    <main>
        <div class="container">
            {% block content %}{% endblock %}
        </div>
    </main>

    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>关于教程</h3>
                    <p>本教程专注于 UV Python 包管理器的快速入门和实战应用，特别针对国内用户进行了优化。</p>
                </div>
                <div class="footer-section">
                    <h3>快速链接</h3>
                    <ul>
                        <li><a href="/tutorials/uv/getting-started.html">UV 快速入门</a></li>
                        <li><a href="https://docs.astral.sh/uv/" target="_blank">官方文档</a></li>
                        <li><a href="https://pypi.tuna.tsinghua.edu.cn/" target="_blank">清华镜像源</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h3>联系方式</h3>
                    <ul>
                        <li><a href="https://github.com/Devliang24/myblog" target="_blank">GitHub</a></li>
                    </ul>
                </div>
            </div>
            <hr style="border-color: rgba(255,255,255,0.2); margin: 2rem 0;">
            <p>&copy; 2025 UV Tutorial. 使用 ❤️ 和 UV 构建。</p>
        </div>
    </footer>

    <script>
        // 简单的交互功能
        document.addEventListener('DOMContentLoaded', function() {
            // 代码复制功能
            const codeBlocks = document.querySelectorAll('pre code');
            codeBlocks.forEach(function(block) {
                const button = document.createElement('button');
                button.className = 'copy-button';
                button.textContent = '复制';
                button.style.position = 'absolute';
                button.style.top = '10px';
                button.style.right = '10px';
                button.style.background = '#4CAF50';
                button.style.color = 'white';
                button.style.border = 'none';
                button.style.padding = '5px 10px';
                button.style.borderRadius = '4px';
                button.style.cursor = 'pointer';
                button.style.fontSize = '12px';

                const pre = block.parentNode;
                pre.style.position = 'relative';
                pre.appendChild(button);

                button.addEventListener('click', function() {
                    navigator.clipboard.writeText(block.textContent).then(function() {
                        button.textContent = '已复制!';
                        setTimeout(function() {
                            button.textContent = '复制';
                        }, 2000);
                    });
                });
            });
        });
    </script>
</body>
</html>"""

    # 首页模板
    index_template = """{% extends "base.html" %}

{% block title %}{{ title }}{% endblock %}

{% block description %}{{ description }}{% endblock %}

{% block content %}
<div class="hero-section" style="text-align: center; padding: 4rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; margin: -2rem -20px 4rem -20px; border-radius: 0;">
    <div class="container">
        <h1 style="font-size: 3rem; margin-bottom: 1rem;">🚀 UV Python 包管理器</h1>
        <p style="font-size: 1.5rem; margin-bottom: 2rem;">超快的 Python 包管理工具，比 pip 快 10-100 倍</p>
        <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
            <a href="/tutorials/uv/getting-started.html" class="btn">开始学习</a>
            <a href="https://github.com/astral-sh/uv" target="_blank" class="btn" style="background: #24292e;">GitHub</a>
        </div>
    </div>
</div>

<div class="quick-guide">
    <h2>🎯 快速入门</h2>
    <div class="guide-steps">
        <div class="step">
            <div class="step-number">1</div>
            <h3>安装 UV</h3>
            <code style="color: #333;">pip install uv</code>
        </div>
        <div class="step">
            <div class="step-number">2</div>
            <h3>配置清华源</h3>
            <code style="color: #333;">uv add requests --index-url https://pypi.tuna.tsinghua.edu.cn/simple/</code>
        </div>
        <div class="step">
            <div class="step-number">3</div>
            <h3>创建项目</h3>
            <code style="color: #333;">uv init my-project</code>
        </div>
        <div class="step">
            <div class="step-number">4</div>
            <h3>安装依赖</h3>
            <code style="color: #333;">uv add fastapi</code>
        </div>
    </div>
</div>

<div class="articles-section">
    <h2 style="text-align: center; margin-bottom: 3rem;">📚 最新文章</h2>

    {% if articles %}
    <div class="feature-grid">
        {% for article in featured_articles %}
        <div class="feature-card">
            <div class="feature-icon">📝</div>
            <h3 class="feature-title"><a href="{{ article.url }}" style="color: inherit; text-decoration: none;">{{ article.title }}</a></h3>
            <p style="color: #666; margin-bottom: 1rem;">{{ article.description[:100] }}{% if article.description|length > 100 %}...{% endif %}</p>
            <div style="display: flex; justify-content: space-between; align-items: center; color: #999; font-size: 0.9rem;">
                <span>📅 {{ article.date }}</span>
                <span>⏱️ {{ article.reading_time }} 分钟</span>
            </div>
            {% if article.tags %}
            <div style="margin-top: 1rem;">
                {% for tag in article.tags[:3] %}
                <span style="background: #e3f2fd; color: #1976d2; padding: 0.2rem 0.5rem; border-radius: 12px; font-size: 0.8rem; margin-right: 0.5rem;">{{ tag }}</span>
                {% endfor %}
            </div>
            {% endif %}
        </div>
        {% endfor %}
    </div>

    {% if articles|length > 3 %}
    <div style="text-align: center; margin-top: 3rem;">
        <h3>更多文章</h3>
        <div style="display: grid; gap: 2rem; margin-top: 2rem;">
            {% for article in articles[3:] %}
            <div style="background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); border-left: 4px solid #3498db;">
                <h3><a href="{{ article.url }}" style="color: #2c3e50; text-decoration: none;">{{ article.title }}</a></h3>
                <p style="color: #666; margin: 1rem 0;">{{ article.description[:150] }}{% if article.description|length > 150 %}...{% endif %}</p>
                <div style="display: flex; justify-content: space-between; align-items: center; color: #999; font-size: 0.9rem;">
                    <span>📅 {{ article.date }}</span>
                    <span>⏱️ {{ article.reading_time }} 分钟</span>
                    <span>📁 {{ article.category }}</span>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    {% endif %}

    {% else %}
    <div style="text-align: center; padding: 4rem 0;">
        <h3>📝 敬请期待更多内容</h3>
        <p style="color: #666; margin-top: 1rem;">我们正在努力编写更多 UV 相关教程，请稍后再来查看。</p>
    </div>
    {% endif %}
</div>

<div class="stats-section" style="text-align: center; padding: 3rem 0; background: #f8f9fa; margin: 4rem -20px -2rem -20px; border-radius: 0 0 8px 8px;">
    <div class="container">
        <h2>📊 教程统计</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; margin-top: 2rem;">
            <div style="background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="font-size: 2rem; font-weight: bold; color: #3498db;">{{ total_articles }}</div>
                <div style="color: #666;">篇文章</div>
            </div>
            <div style="background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="font-size: 2rem; font-weight: bold; color: #27ae60;">10-100x</div>
                <div style="color: #666;">速度提升</div>
            </div>
            <div style="background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="font-size: 2rem; font-weight: bold; color: #e74c3c;">15分钟</div>
                <div style="color: #666;">快速入门</div>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""

    # 文章模板
    article_template = """{% extends "base.html" %}

{% block title %}{{ title }}{% endblock %}

{% block description %}{{ description }}{% endblock %}

{% block content %}
<article>
    <div class="article-header">
        <div class="article-meta">
            <div class="meta-item">📅 <time datetime="{{ date }}">{{ date }}</time></div>
            <div class="meta-item">✍️ {{ author }}</div>
            <div class="meta-item">📁 {{ category }}</div>
            <div class="meta-item">⏱️ {{ reading_time }} 分钟阅读</div>
        </div>
        <h1 class="article-title">{{ title }}</h1>
        {% if description %}
        <p class="article-subtitle">{{ description }}</p>
        {% endif %}
    </div>

    <div class="article-content">
        {{ content|safe }}

        {% if tags %}
        <div style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #eee;">
            <h3>🏷️ 标签</h3>
            <div style="margin-top: 1rem;">
                {% for tag in tags %}
                <span style="background: #e3f2fd; color: #1976d2; padding: 0.4rem 0.8rem; border-radius: 16px; font-size: 0.9rem; margin-right: 0.5rem; margin-bottom: 0.5rem; display: inline-block;">{{ tag }}</span>
                {% endfor %}
            </div>
        </div>
        {% endif %}

        <div style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #eee;">
            <h3>🔗 相关链接</h3>
            <ul>
                <li><a href="/">返回首页</a></li>
                <li><a href="https://docs.astral.sh/uv/" target="_blank">UV 官方文档</a></li>
                <li><a href="https://github.com/astral-sh/uv" target="_blank">UV GitHub 仓库</a></li>
                <li><a href="https://pypi.tuna.tsinghua.edu.cn/" target="_blank">清华大学 PyPI 镜像</a></li>
            </ul>
        </div>
    </div>
</article>

<style>
.copy-button:hover {
    background: #45a049 !important;
}
</style>
{% endblock %}"""

    # 写入模板文件
    with open(templates_dir / "base.html", 'w', encoding='utf-8') as f:
        f.write(base_template)

    with open(templates_dir / "index.html", 'w', encoding='utf-8') as f:
        f.write(index_template)

    with open(templates_dir / "article.html", 'w', encoding='utf-8') as f:
        f.write(article_template)

    print(f"✅ 创建默认模板文件到 {templates_dir}")

def main():
    parser = argparse.ArgumentParser(description='UV Tutorial Blog Generator')
    parser.add_argument('--content-dir', default='content', help='Content directory path')
    parser.add_argument('--output-dir', default='public', help='Output directory path')
    parser.add_argument('--template-dir', default='templates', help='Template directory path')
    parser.add_argument('--create-templates', action='store_true', help='Create default template files')

    args = parser.parse_args()

    # 创建默认模板
    if args.create_templates:
        create_default_templates()

    # 检查必要的依赖
    try:
        import yaml
    except ImportError:
        print("❌ 缺少依赖: yaml")
        print("请运行: pip install PyYAML")
        sys.exit(1)

    # 检查模板目录
    if not Path(args.template_dir).exists():
        print(f"❌ 模板目录不存在: {args.template_dir}")
        print("请运行: python generate_blog.py --create-templates")
        sys.exit(1)

    # 生成博客
    generator = BlogGenerator(
        content_dir=args.content_dir,
        output_dir=args.output_dir,
        template_dir=args.template_dir
    )

    try:
        articles = generator.generate_blog()
        print(f"\n🎉 博客生成成功！")
        print(f"📝 共生成 {len(articles)} 篇文章")
        print(f"📂 输出目录: {Path(args.output_dir).absolute()}")
        print(f"\n🚀 可以使用以下命令启动本地服务器:")
        print(f"cd {args.output_dir} && python -m http.server 8000")
        print(f"然后访问: http://localhost:8000")

    except Exception as e:
        print(f"❌ 生成失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()