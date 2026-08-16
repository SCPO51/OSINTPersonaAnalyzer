import markdown
from pygments.formatters import HtmlFormatter

def md_to_html(md_text, css_theme='friendly'):
    extensions = [
        'extra',
        'codehilite',
        'toc'
    ]
    html = markdown.markdown(md_text, extensions=extensions)

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown.min.css">
        <style>
            .markdown-body {{ box-sizing: border-box; min-width: 200px; max-width: 980px; margin: 0 auto; padding: 45px; }}
            {HtmlFormatter(style=css_theme).get_style_defs()}  <!-- Pygments 代码样式 -->
        </style>
    </head>
    <body>
        <div class="markdown-body">
            {html}
        </div>
    </body>
    </html>
    '''
