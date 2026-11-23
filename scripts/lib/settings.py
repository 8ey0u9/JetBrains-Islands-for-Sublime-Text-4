"""从推荐配置默认值生成逐项中文说明模板与文档。"""
import json
from . import ROOT, SRC

# key: (中文说明, 生效条件/边界)
SETTINGS = {
    'theme': ('界面主题：控制标签、侧边栏、按钮和弹窗外壳；auto 为跟随系统。', 'auto 需同时配对 light_theme / dark_theme。'),
    'color_scheme': ('编辑区配色：控制语法、光标、选区以及原生 minihtml 内容。', '语法专用设置、项目或视图设置可能覆盖全局值。'),
    'light_theme': ('系统浅色外观对应的界面主题。', '仅 theme=auto 时自动选择；固定 Dark 时不参与当前显示。'),
    'dark_theme': ('系统深色外观对应的界面主题。', '仅 theme=auto 时自动选择；固定 Light 时不参与当前显示。'),
    'light_color_scheme': ('系统浅色外观对应的编辑区配色。', '仅 color_scheme=auto 时自动选择。'),
    'dark_color_scheme': ('系统深色外观对应的编辑区配色。', '仅 color_scheme=auto 时自动选择。'),
    'mdpopups.user_css': ('LSP/mdpopups 弹窗样式入口：适配签名、诊断和动作区。', '依赖已安装的 mdpopups；显式自定义路径优先。模板最后合并 User/mdpopups.css。'),
    'file_tab_style': ('标签形状：rounded 为 Islands 圆角，square 为直角，angled 为原生旧式斜角。', 'angled 使用 Sublime 默认几何，不承诺 Islands 外观。'),
    'themed_title_bar': ('请求主题化标题栏，使可主题化区域跟随当前配色。', 'macOS 上验证；系统原生标题栏、窗口按钮由平台决定。'),
    'highlight_modified_tabs': ('将未保存标签的文字显示为强调色；关闭后保留原生未保存圆点。', '必须存在未保存文件；不依赖关闭按钮是否可见。'),
    'show_tab_close_buttons': ('是否显示标签关闭按钮；未选中标签默认在鼠标经过时显示。', 'false 隐藏按钮；不禁用关闭文件命令。'),
    'show_tab_close_buttons_on_left': ('把标签关闭按钮移到左侧；false 放在右侧。', 'show_tab_close_buttons=true 时才看得见位置变化。'),
    'hide_tab_scrolling_buttons': ('隐藏标签左右滚动箭头，以保持 Islands 紧凑布局。', '仅影响按钮；滚轮和下拉列表仍可导航。'),
    'hide_new_tab_button': ('隐藏标签栏新增按钮。', '不影响新建文件菜单及快捷键。'),
    'enable_tab_scrolling': ('允许标签栏横向滚动，避免标签全部压缩。', '需要标签总宽度超过可用空间。'),
    'mouse_wheel_switches_tabs': ('用鼠标滚轮在标签间切换。', '原生主题规则在 enable_tab_scrolling=false 时启用切换。'),
    'islands_hide_tab_dropdown': ('隐藏标签列表下拉按钮；false 保留 Sublime 原生导航入口。', 'Islands 自定义主题开关，仅 Islands 主题读取。'),
    'bold_folder_labels': ('侧边栏文件夹名称是否加粗；推荐 false，目录和文件均使用常规字重。', '设为 true 可开启目录加粗。'),
    'overlay_scroll_bars': ('滚动条模式：enabled 浮动，disabled 占位，system 跟随系统。', 'Sublime 将枚举转换为主题的浮动滚动条状态；system 由系统偏好决定。'),
    'draw_shadows': ('绘制编辑区边缘阴影；false 保持 Islands 平整边界。', '与 popup_shadows 不同；没有可将阴影改为细线的主题接口。'),
    'popup_shadows': ('绘制原生弹窗外阴影。', '由 Sublime 的 popup_shadow 与平台共同处理。'),
    'show_sidebar_button': ('显示状态栏中的侧边栏切换按钮。', '状态栏隐藏时不可见；侧边栏菜单和快捷键始终有效。'),
    'show_encoding': ('在状态栏显示文件编码，例如 UTF-8。', '普通文本编辑视图与可见状态栏中生效。'),
    'show_line_endings': ('在状态栏显示换行格式，例如 Unix / Windows。', '普通文本编辑视图与可见状态栏中生效。'),
    'show_indentation': ('在状态栏显示缩进方式与宽度，例如 Spaces: 4。', '显示当前视图的有效缩进设置。'),
    'show_syntax': ('在状态栏显示当前语法，并保留原生语法选择菜单。', '普通文本视图中生效。'),
    'show_line_column': ('状态栏行列号：enabled 完整，compact 紧凑，disabled 隐藏。', 'disabled 是用户明确选择；主题不会改回 enabled。'),
    'fold_buttons': ('在行号旁显示原生代码折叠箭头；主题提供右向/下向图形。', 'gutter=true 且语法或缩进识别出可折叠范围时显示。'),
    'fade_fold_buttons': ('折叠箭头仅在鼠标进入 gutter 时显示；false 常显。', 'fold_buttons=true 时生效；由 Sublime 控制淡入淡出。'),
    'fold_style': ('折叠规则：auto 自动，force_indentation 按缩进，scope_only 仅按语法范围。', '不由主题推断或重写折叠范围。'),
    'always_show_minimap_viewport': ('在迷你地图上持续显示当前可视区域；false 在鼠标经过时显示。', '迷你地图需先通过“视图”菜单显示。'),
    'draw_minimap_border': ('在迷你地图的可视区域周围绘制边框。', '不是编辑器与迷你地图之间的分隔线。'),
    'inactive_sheet_dimming': ('弱化没有输入焦点的编辑分组，并轻微调整失焦输入框底色。', '需多分组/失焦控件；不改动语法文字颜色。'),
    'file_icon_theme': ('附加文件图标主题；空数组使用与当前主题同名的图标映射。', '空数组使用与当前主题同名的图标映射；可填入第三方图标主题。'),
    'font_face': ('编辑器字体名称，由用户选择。', '需本机安装字体；不控制所有原生界面字体。'),
    'font_size': ('编辑器字号；minihtml 的 rem 大小也随字号变化。', '不会自动改变主题固定的标签栏/侧边栏字号。'),
    'line_padding_top': ('每行文字上方额外留白，单位为逻辑像素。', '影响编辑行高；不等同于 HTML 文档行距。'),
    'line_padding_bottom': ('每行文字下方额外留白，单位为逻辑像素。', '影响编辑行高；不等同于 HTML 文档行距。'),
    'highlight_line': ('使用配色方案的当前行背景突出光标所在行。', '由当前视图设置控制。'),
    'translate_tabs_to_spaces': ('按 Tab 键时插入空格。', '缩进自动检测、语法或项目设置可能覆盖全局值；不改写已有文件。'),
    'tab_size': ('Tab 的显示/缩进宽度。', '当前视图可被 detect_indentation、语法或项目设置覆盖。'),
    'detect_indentation': ('打开文件时自动检测缩进风格与宽度。', '因此有效 tab_size / translate_tabs_to_spaces 可能不同于全局值。'),
    'ignored_packages': ('禁用列表中的插件包。', '插件管理设置，主题不修改；禁用 LSP 会使其文档动作不可用。'),
    'index_files': ('建立符号索引，支持原生跳转定义、项目符号等功能。', '索引异步完成；LSP 同时维护自身的语言服务数据。'),
    'show_definitions': ('鼠标悬停时显示原生定义位置列表。', '依赖 index_files；LSP 可在支持的视图中接管 hover，这是正常覆盖。'),
    'gutter': ('显示行号、折叠和诊断标记所在的左侧区域。', 'false 会同时隐藏折叠箭头与 gutter 标记。'),
    'line_numbers': ('显示编辑器行号。', '需 gutter=true。'),
    'word_wrap': ('窗口宽度不足时自动换行。', '只影响显示，不向文件写入换行符。'),
    'mini_diff': ('在 gutter 显示修改行标记；auto 仅限 Git 跟踪文件。', '由 Sublime 计算差异；颜色由 Islands 配色控制。'),
}

OPTIONAL = {
    'show_tab_close_buttons': True, 'islands_hide_tab_dropdown': False,
    'enable_tab_scrolling': True, 'mouse_wheel_switches_tabs': False,
    'popup_shadows': True, 'fold_buttons': True, 'fade_fold_buttons': True,
    'fold_style': 'auto', 'always_show_minimap_viewport': False,
    'draw_minimap_border': False, 'inactive_sheet_dimming': False,
    'show_line_column': 'enabled', 'show_syntax': True, 'file_icon_theme': [],
}

LAYOUT = {
    # 默认采用 Islands 圆角标签；用户手动设置 square / angled 时保留。
    "file_tab_style": "rounded",
    # 请求主题化标题栏；实际支持范围由平台和 Sublime 控制。
    "themed_title_bar": True,
    # 使用强调色标识未保存标签。
    "highlight_modified_tabs": True,
    # 侧边栏文件夹使用常规字重；用户仍可手动开启加粗。
    "bold_folder_labels": False,
    # 浮动滚动条；也支持用户选择 system / disabled。
    "overlay_scroll_bars": "enabled",
    # 关闭编辑区边缘阴影，与弹窗阴影 popup_shadows 是两个不同设置。
    "draw_shadows": False,
    # 隐藏状态栏侧边栏按钮；菜单和原快捷键仍可切换侧边栏。
    "show_sidebar_button": False,
    # 状态栏显示文件编码。
    "show_encoding": True,
    # 状态栏显示换行符。
    "show_line_endings": True,
    # 状态栏显示缩进方式和宽度。
    "show_indentation": True,
    # 隐藏标签滚动箭头；仍可通过滚轮和标签下拉列表导航。
    "hide_tab_scrolling_buttons": True,
    # 隐藏新增标签按钮；新建文件菜单和快捷键仍可用。
    "hide_new_tab_button": True,
    # 默认将关闭按钮放在标签右侧。
    "show_tab_close_buttons_on_left": False,
}


def layout_defaults():
    return LAYOUT.copy()


def template(flavor):
    active = {'theme': f'JetBrains Islands {flavor}.sublime-theme',
              'color_scheme': f'JetBrains Islands {flavor}.sublime-color-scheme',
              'mdpopups.user_css': 'Packages/JetBrains Islands/styles/mdpopups.css'}
    active.update(layout_defaults())
    for variant in ('light', 'dark'):
        active[f'{variant}_theme'] = f'JetBrains Islands {variant.title()}.sublime-theme'
        active[f'{variant}_color_scheme'] = f'JetBrains Islands {variant.title()}.sublime-color-scheme'
    lines = ['// JetBrains Islands：逐项中文设置说明。',
             '// 按需复制到 User/Preferences.sublime-settings；本模板不会自动加载。',
             '// 主题遵循纯静态规范，不修改用户的偏好设置；可按需复制推荐布局项。',
             '// 如已有自定义 mdpopups.user_css，请保留原值，不要复制该项。', '{']
    for key, value in active.items():
        for text in SETTINGS[key]:
            lines.append('    // ' + text)
        lines.append('    ' + json.dumps(key) + ': ' + json.dumps(value, ensure_ascii=False) + ',')
        lines.append('')
    lines.append('    // 以下为可选设置示例，已注释；取消注释并保存后才会应用。')
    for key, value in OPTIONAL.items():
        for text in SETTINGS[key]:
            lines.append('    // ' + text)
        lines.append('    // ' + json.dumps(key) + ': ' + json.dumps(value, ensure_ascii=False) + ',')
        lines.append('')
    lines.extend(['    // show_minimap 不是公开偏好设置；请使用“视图 → 显示/隐藏迷你地图”。',
                  '    // 原生窗口对话框、面包屑和标签内文件图标无法通过本主题添加。', '}'])
    # Avoid trailing commas among active entries for independent JSON validation.
    last = max(i for i, line in enumerate(lines) if line.startswith('    "'))
    lines[last] = lines[last].rstrip(',')
    return '\n'.join(lines) + '\n'


def documentation():
    lines = ['# 配置项中文说明', '',
             '<!-- 由 scripts/lib/settings.py 生成；请修改 scripts/lib/settings.py 中的说明。 -->', '',
             '范围：本主题管理的设置、主题相关可选开关，以及常见编辑器设置。',
             'Sublime 其余数百项内置选项继续使用原生说明，不将未验证的选项宣称为已适配。', '',
             '模板位于 `settings/`，不自动加载；应编辑 `User/Preferences.sublime-settings`。',
             '命令面板可搜索 **JetBrains Islands: 设置说明（中文）** 打开左右设置页。', '',
             '| 设置项 | 作用 | 条件与限制 |', '|---|---|---|']
    for key, (description, limits) in SETTINGS.items():
        lines.append(f'| `{key}` | {description} | {limits} |')
    lines += ['', '## 主题推荐配置与自定义', '',
              '本主题遵循纯静态规范，安装后不会通过脚本强制改写用户的偏好设置。',
              '用户可通过 `User/Preferences.sublime-settings` 按需选择启用推荐的布局与微调项。',
              '主题没有自定义焦点属性、show_minimap 假开关或模拟 IDE 功能。', '',
              '使用与适配范围见 [README.md](../README.md)。', '']
    return '\n'.join(lines)


def build():
    for flavor in ('Dark', 'Light'):
        path = SRC / 'settings' / f'JetBrains Islands {flavor}.sublime-settings'
        path.write_text(template(flavor), encoding='utf-8')
    (ROOT / 'docs/SETTINGS.zh-CN.md').write_text(documentation(), encoding='utf-8')

