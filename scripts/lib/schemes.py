"""
Build both JetBrains Islands editor and hidden input-widget color schemes.

Colours are taken from the IntelliJ IDEA Islands editor schemes
(platform-resources/src/themes/islands/IslandSchemeDark.xml and the expUI
Light scheme). Every scope rule below maps one IntelliJ attribute name to its
Sublime Text scope selector, so the two flavours stay structurally identical.
"""
import json
import os
import re

from . import ROOT, SRC

DARK = {
    "name": "JetBrains Islands Dark",
    "background": "#191A1C",
    "foreground": "#BCBEC4",
    "caret": "#CED0D6",
    "line_highlight": "#1F2024",
    "selection": "#2A4371",
    "selection_fg": "#D1D3D9",
    "inactive_selection": "#33353B",
    "gutter": "#191A1C",
    "gutter_fg": "#4B5059",
    "gutter_fg_highlight": "#A1A3AB",
    "guide": "#323438",
    "active_guide": "#4E5157",
    "stack_guide": "#3B3E44",
    "keyword": "#CF8E6D",
    "string": "#6AAB73",
    "number": "#2AACB8",
    "comment": "#7A7E85",
    "doc_comment": "#5F826B",
    "function": "#56A8F5",
    "constant": "#C77DBB",
    "metadata": "#B3AE60",
    "operator": "#BCBEC4",
    "punct": "#BCBEC4",
    "tag": "#D5B778",
    "attr": "#BCBEC4",
    "entity": "#56A8F5",
    "invalid": "#F75464",
    "invalid_bg": "#402929",
    "deprecated": "#6F737A",
    "find_bg": "#114957",
    "find_fg": "#D1D3D9",
    "highlight": "#2D543F",
    "fold_fg": "#868991",
    "fold_bg": "#393B40",
    "inlay_fg": "#868A91",
    "inlay_bg": "#393B40",
    "todo": "#8BB33D",
    "doc_tag": "#67A37C",
    "doc_tag_value": "#ABADB3",
    "link": "#548AF7",
    "match_bg": "#43454A",
    "misspelling": "#7EC482",
    "shadow": "#000000",
    "diff_added": "#549159",
    "diff_modified": "#375FAD",
    "diff_deleted": "#868A91",
    "scroll_result": "#42BD77",
    "widget_fg": "#D1D3D9",
    "widget_placeholder": "#9FA2A8",
    "popup_bg": "#26282C",
    "popup_muted": "#9FA2A8",
    "popup_fg": "#D1D3D9",
    "popup_link": "#71A1FE",
    "popup_code_bg": "#212326",
    "popup_inline_bg": "#73767C42",
    "popup_rule": "#33353B",
    "popup_footer_bg": "#26282C",
    "popup_error_bg": "#56272B",
    "popup_error_border": "#80383E",
    "popup_warning_bg": "#44321D",
    "popup_warning_border": "#694820",
    "popup_info_bg": "#233558",
    "popup_info_border": "#2E4D89",
    "comment_italic": False,
}

LIGHT = {
    "name": "JetBrains Islands Light",
    "background": "#FFFFFF",
    "foreground": "#080808",
    "caret": "#000000",
    "line_highlight": "#F5F8FE",
    "selection": "#A6D2FF",
    "selection_fg": "#000000",
    "inactive_selection": "#E9EAEE",
    "gutter": "#FFFFFF",
    "gutter_fg": "#AEB3C2",
    "gutter_fg_highlight": "#767A8A",
    "guide": "#EBECF0",
    "active_guide": "#AEB3C2",
    "stack_guide": "#DAE6FD",
    "keyword": "#0033B3",
    "string": "#067D17",
    "number": "#1750EB",
    "comment": "#8C8C8C",
    "doc_comment": "#8C8C8C",
    "function": "#00627A",
    "constant": "#871094",
    "metadata": "#9E880D",
    "operator": "#080808",
    "punct": "#080808",
    "tag": "#0033B3",
    "attr": "#174AD4",
    "entity": "#174BE6",
    "invalid": "#DE1B2E",
    "invalid_bg": "#FFCCCC",
    "deprecated": "#9FA2A8",
    "find_bg": "#FCD47E",
    "find_fg": "#000000",
    "highlight": "#C47233",
    "fold_fg": "#414D41",
    "fold_bg": "#E9F5E6",
    "inlay_fg": "#494B57",
    "inlay_bg": "#EBECF0",
    "todo": "#8D5A12",
    "doc_tag": "#999999",
    "doc_tag_value": "#3D3D3D",
    "link": "#2F5EB9",
    "match_bg": "#93D9D9",
    "misspelling": "#DE1B2E",
    "shadow": "#000000",
    "diff_added": "#7FC784",
    "diff_modified": "#88ADF7",
    "diff_deleted": "#767A8A",
    "scroll_result": "#C47233",
    "widget_fg": "#080808",
    "widget_placeholder": "#5F6269",
    "popup_bg": "#FFFFFF",
    "popup_muted": "#5F6269",
    "popup_fg": "#000000",
    "popup_link": "#2F5EB9",
    "popup_code_bg": "#F7F8F9",
    "popup_inline_bg": "#8B8E941F",
    "popup_rule": "#E9EAEE",
    "popup_footer_bg": "#F7F8F9",
    "popup_error_bg": "#FFF6F5",
    "popup_error_border": "#FFC4C5",
    "popup_warning_bg": "#FFF6E9",
    "popup_warning_border": "#F4CD9A",
    "popup_info_bg": "#F7F8FF",
    "popup_info_border": "#BDD3FF",
    "comment_italic": True,
}


def popup_css_for(p):
    """Expand design tokens only. Popup contents and actions belong to providers."""
    with open(os.path.join(SRC, "styles", "popup.css"), encoding="utf-8") as f:
        css = f.read()
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"@@(\w+)@@", lambda match: p[match.group(1)], css)
    # Resolve our aliases at build time, leaving provider variables as literal
    # values. This avoids depending on custom-property chaining in minihtml.
    aliases = dict(re.findall(r"(--islands-[\w-]+):\s*([^;]+);", css))
    for key, value in aliases.items():
        css = css.replace("var(" + key + ")", value)
    css = re.sub(r"\s*--islands-[\w-]+:\s*[^;]+;", "", css)
    return css.strip()


def globals_for(p):
    # NOTE: Sublime rejects a whole color scheme when a globals value is a raw
    # JSON number, so every numeric setting must be written as a string.
    return {
        "background": "var(bg)",
        "foreground": "var(fg)",
        "caret": "var(caret)",
        "line_highlight": "var(line_highlight)",
        "selection": "var(selection)",
        "selection_foreground": "var(selection_fg)",
        "selection_border": "transparent",
        "selection_border_width": "0",
        "selection_corner_style": "round",
        "selection_corner_radius": "2",
        "inactive_selection": "var(inactive_selection)",
        "inactive_selection_border": "transparent",
        "inactive_selection_foreground": "var(fg)",
        "gutter": "var(gutter)",
        "gutter_foreground": "var(gutter_fg)",
        "gutter_foreground_highlight": "var(gutter_fg_highlight)",
        "guide": "var(guide)",
        "active_guide": "var(active_guide)",
        "stack_guide": "var(stack_guide)",
        "highlight": "var(highlight)",
        "find_highlight": "var(find_bg)",
        "find_highlight_foreground": "var(find_fg)",
        "scroll_highlight": "var(scroll_result)",
        "scroll_selected_highlight": "var(scroll_result)",
        "misspelling": "var(misspelling)",
        "fold_marker": "var(fold_fg)",
        "minimap_border": "var(active_guide)",
        "shadow": "var(shadow)",
        "shadow_width": "8",
        "rulers": "var(guide)",
        "invisibles": "color(var(fg) a(0.5))",
        "accent": "#3871E1",
        # Sublime can only underline/tint brackets -- it has no background
        # highlight for them, so IntelliJ's filled bracket marker is out of
        # reach. Give the strongest available signal instead: a solid
        # underline plus a foreground change, and drop the faint stipple.
        "brackets_options": "foreground bold underline",
        "brackets_foreground": "var(link)",
        "bracket_contents_options": "underline",
        "bracket_contents_foreground": "var(link)",
        "tags_options": "underline",
        "tags_foreground": "var(link)",
        "line_diff_width": "3",
        "line_diff_added": "var(diff_added)",
        "line_diff_modified": "var(diff_modified)",
        "line_diff_deleted": "var(diff_deleted)",
        "popup_css": popup_css_for(p),
        # Otherwise Sublime falls back to popup_css for inline phantoms.
        # Keep provider-specific inlay hints/code lenses and their geometry.
        "phantom_css": "html { background-color: transparent; color: var(--foreground); }",
    }


def variables_for(p):
    v = {
        "bg": p["background"],
        "fg": p["foreground"],
        "caret": p["caret"],
        "line_highlight": p["line_highlight"],
        "selection": p["selection"],
        "selection_fg": p["selection_fg"],
        "inactive_selection": p["inactive_selection"],
        "gutter": p["gutter"],
        "gutter_fg": p["gutter_fg"],
        "gutter_fg_highlight": p["gutter_fg_highlight"],
        "guide": p["guide"],
        "active_guide": p["active_guide"],
        "stack_guide": p["stack_guide"],
        "keyword": p["keyword"],
        "string": p["string"],
        "number": p["number"],
        "comment": p["comment"],
        "doc_comment": p["doc_comment"],
        "function": p["function"],
        "constant": p["constant"],
        "metadata": p["metadata"],
        "operator": p["operator"],
        "punct": p["punct"],
        "tag": p["tag"],
        "attr": p["attr"],
        "entity": p["entity"],
        "invalid": p["invalid"],
        "invalid_bg": p["invalid_bg"],
        "deprecated": p["deprecated"],
        "find_bg": p["find_bg"],
        "find_fg": p["find_fg"],
        "highlight": p["highlight"],
        "fold_fg": p["fold_fg"],
        "fold_bg": p["fold_bg"],
        "inlay_fg": p["inlay_fg"],
        "inlay_bg": p["inlay_bg"],
        "todo": p["todo"],
        "doc_tag": p["doc_tag"],
        "doc_tag_value": p["doc_tag_value"],
        "link": p["link"],
        "match_bg": p["match_bg"],
        "misspelling": p["misspelling"],
        "shadow": p["shadow"],
        "scroll_result": p["scroll_result"],
        "diff_added": p["diff_added"],
        "diff_modified": p["diff_modified"],
        "diff_deleted": p["diff_deleted"],
    }
    return v


def rules_for(p):
    r = []
    add = r.append

    def rule(name, scope, fg=None, bg=None, style=None):
        o = {"name": name, "scope": scope}
        if fg:
            o["foreground"] = fg
        if bg:
            o["background"] = bg
        if style:
            o["font_style"] = style
        add(o)

    # Comments
    comment_style = "italic" if p["comment_italic"] else None
    rule("Line Comment", "comment.line", "var(comment)", style=comment_style)
    rule("Block Comment", "comment.block", "var(comment)", style=comment_style)
    rule("Comment Punctuation", "punctuation.definition.comment", "var(comment)", style=comment_style)
    rule("Documentation Comment", "comment.block.documentation, comment.line.documentation",
         "var(doc_comment)", style="italic")
    rule("Doc Comment Tag", "comment.block.documentation storage.type.class.doxygen,"
         " comment.block.documentation entity.name.type,"
         " comment.block.documentation keyword", "var(doc_tag)")
    rule("Doc Comment Tag Value", "comment.block.documentation variable.other", "var(doc_tag_value)")
    rule("TODO", "comment.line.keyword.todo, comment.block.keyword.todo,"
         " comment.line.todo, comment.block.todo", "var(todo)", style="bold")
    rule("FIXME", "comment.line.keyword.fixme, comment.block.keyword.fixme,"
         " comment.line.fixme, comment.block.fixme", "var(todo)", style="bold")

    # Strings / numbers
    rule("String", "string", "var(string)")
    rule("String Punctuation", "punctuation.definition.string", "var(string)")
    rule("String Escape", "constant.character.escape, string.quoted.double.constant.character.escape",
         "var(keyword)")
    rule("Invalid Escape", "invalid.illegal.character.escape", "var(invalid)",
         style="squiggly_underline")
    rule("Number", "constant.numeric", "var(number)")
    rule("Number Suffix", "storage.type.numeric, keyword.other.unit", "var(keyword)")

    # Keywords / storage / operators
    rule("Keyword", "keyword - keyword.operator, storage.type, storage.modifier", "var(keyword)")
    rule("Keyword Control", "keyword.control", "var(keyword)")
    rule("Operator Word", "keyword.operator.word", "var(keyword)", style="italic")
    rule("Operator", "keyword.operator", "var(operator)")
    rule("Punctuation", "punctuation.separator, punctuation.terminator, punctuation.accessor",
         "var(punct)")
    rule("Brackets", "punctuation.section, punctuation.definition", "var(punct)")

    # Declarations / calls
    rule("Function Declaration", "entity.name.function, entity.name.function.definition,"
         " meta.function entity.name.function", "var(function)")
    rule("Function Call", "variable.function, meta.function-call variable.function,"
         " support.function, support.macro", "var(function)")
    rule("Method Name", "entity.name.method, meta.method.declaration entity.name.function",
         "var(function)")
    rule("Class Name", "entity.name.type.class, entity.name.class, support.class", "var(fg)")
    rule("Type Name", "entity.name.type, entity.name.type.interface, entity.name.type.enum,"
         " support.type", "var(fg)")
    rule("Namespace", "entity.name.namespace, entity.name.module, support.module,"
         " variable.other.namespace", "var(fg)")
    rule("Constant", "constant.other, variable.other.constant, support.constant",
         "var(constant)")
    rule("Instance Field", "variable.other.member, variable.other.property,"
         " variable.other.field, meta.property", "var(constant)")
    rule("Static Field", "variable.other.static, entity.name.variable.static", "var(constant)",
         style="bold")
    rule("Parameter", "variable.parameter", "var(fg)")
    rule("Local Variable", "variable.other.local", "var(fg)")
    rule("Language Variable", "variable.language, variable.language.this, variable.language.self",
         "var(keyword)", style="italic")
    rule("Annotation", "storage.type.annotation, meta.annotation entity.name.type,"
         " entity.name.function.annotation, support.annotation", "var(metadata)")
    rule("Annotation Punctuation", "punctuation.definition.annotation", "var(metadata)")
    rule("Decorator", "meta.decorator entity.name.function, entity.name.function.decorator",
         "var(metadata)")

    # Markup
    rule("Tag Name", "entity.name.tag, meta.tag entity.name.tag", "var(tag)")
    rule("Tag Punctuation", "punctuation.definition.tag", "var(tag)")
    rule("Attribute Name", "entity.other.attribute-name", "var(attr)")
    rule("Attribute Value", "string.quoted.attribute-value, meta.tag string"
         " - string.other.link", "var(string)")
    rule("Entity Reference", "constant.character.entity, punctuation.definition.entity",
         "var(entity)")
    rule("HTML Tag", "meta.tag.other entity.name.tag", "var(tag)")

    # Config formats
    rule("Property Key", "support.type.property-name, meta.mapping.key string,"
         " source.yaml entity.name.tag, entity.name.tag.yaml", "var(keyword)")
    rule("Property Value", "meta.mapping.value string, meta.mapping.value constant.numeric",
         "var(string)")
    rule("TOML Key", "support.type.property-name.toml", "var(keyword)")

    # Markdown / prose
    rule("Markup Heading", "markup.heading", "var(function)", style="bold")
    rule("Markup Bold", "markup.bold", "var(fg)", style="bold")
    rule("Markup Italic", "markup.italic", "var(fg)", style="italic")
    rule("Markup Underline", "markup.underline", "var(fg)", style="underline")
    rule("Markup Link", "markup.underline.link, string.other.link", "var(link)",
         style="underline")
    rule("Markup Code", "markup.inline.raw, markup.raw.inline, markup.code",
         "var(fg)", "var(inlay_bg)")
    rule("Markup Code Block", "markup.raw.block, markup.fenced_code", "var(fg)", "var(inlay_bg)")
    rule("Markup List", "markup.list punctuation.definition.list_item", "var(comment)")
    rule("Markup Quote", "markup.quote", "var(comment)", style="italic")

    # Diff / VCS
    rule("Diff Inserted", "markup.inserted, diff.inserted, meta.diff.range.inserted",
         "var(diff_added)")
    rule("Diff Changed", "markup.changed, diff.changed", "var(diff_modified)")
    rule("Diff Deleted", "markup.deleted, diff.deleted", "var(diff_deleted)")

    # Diagnostics
    rule("Invalid", "invalid, invalid.illegal", "var(invalid)", "var(invalid_bg)")
    rule("Invalid Deprecated", "invalid.deprecated", "var(deprecated)", style="stippled_underline")
    rule("Unimplemented", "invalid.unimplemented", "var(deprecated)", style="stippled_underline")
    rule("Unresolved", "entity.name.type.unresolved, variable.other.unresolved",
         "var(deprecated)", style="stippled_underline")

    return r


def widget_data(p):
    """Keep widget hints readable without brightening editor rulers."""
    return {
        "name": p["name"] + " 输入控件",
        "variables": variables_for(p),
        "globals": {
            "background": p["background"],
            "foreground": p["widget_fg"],
            "caret": p["caret"],
            "selection": p["selection"],
            "selection_foreground": p["selection_fg"],
            "inactive_selection": p["inactive_selection"],
            "selection_border": "transparent",
            # Native theme/color-scheme pickers use rulers for placeholder text.
            "rulers": p["widget_placeholder"],
            "invisibles": p["widget_placeholder"],
            "accent": "#3871E1",
        },
        # Find/Replace regex and console widgets still need syntax highlighting.
        "rules": rules_for(p),
    }


def build(p):
    data = {
        "name": p["name"],
        "author": "JetBrains Islands for Sublime Text 4",
        "variables": variables_for(p),
        "globals": globals_for(p),
        "rules": rules_for(p),
    }
    path = SRC / "schemes" / f"{p['name']}.sublime-color-scheme"
    path.parent.mkdir(exist_ok=True)
    with open(path, "w") as f:
        f.write("// JetBrains Islands — generated by scripts/lib/schemes.py\n")
        f.write(json.dumps(data, indent=4, ensure_ascii=False))
        f.write("\n")
    # mdpopups inserts provider CSS after the color-scheme stylesheet. Use its
    # public user_css hook to apply the same design after the provider rules.
    flavor = "dark" if p is DARK else "light"
    with open(os.path.join(SRC, "styles", f"popup-{flavor}.css"), "w", encoding="utf-8") as f:
        f.write(popup_css_for(p) + "\n")
    widget_name = "Widget - " + p["name"]
    with open(SRC / "schemes" / (widget_name + ".hidden-color-scheme"), "w", encoding="utf-8") as f:
        f.write("// 自动生成：输入控件配色，勿手工修改。\n")
        f.write(json.dumps(widget_data(p), ensure_ascii=False, indent=4) + "\n")
    (SRC / "settings").mkdir(exist_ok=True)
    with open(SRC / "settings" / (widget_name + ".sublime-settings"), "w", encoding="utf-8") as f:
        f.write('{\n    // 仅用于本主题的原生输入控件：统一输入文字、选区和提示文字。\n')
        f.write('    // 字体与字号沿用用户设置，正则输入语法由 Sublime 原生控件加载。\n')
        f.write('    "color_scheme": ' + json.dumps(widget_name + ".hidden-color-scheme") + '\n}\n')
    return path


def build_all():
    for p in (DARK, LIGHT):
        print("scheme:", build(p))
