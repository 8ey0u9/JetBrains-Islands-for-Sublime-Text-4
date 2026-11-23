"""Validate the built package without launching Sublime."""
import json, os, re, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG = os.path.join(ROOT, "dist", "JetBrains Islands.sublime-package")

def strip_comments(text):
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    return re.sub(r'^\s*//.*$', '', text, flags=re.M)

def load_json(text):
    return json.loads(strip_comments(text))

failures = []
def check(cond, msg):
    if not cond:
        failures.append(msg)

# 1. Every JSON config parses.
configs = [f for f in os.listdir(ROOT) if re.search(r'\.(sublime-theme|sublime-color-scheme|sublime-file-icons|sublime-commands|sublime-settings)$', f)]
configs += ["settings/" + f for f in os.listdir(os.path.join(ROOT, "settings"))]
for name in configs:
    try:
        load_json(open(os.path.join(ROOT, name)).read())
    except Exception as e:
        failures.append(f"invalid JSON: {name}: {e}")

# 2. Theme texture references resolve.
for theme in ("JetBrains Islands Dark.sublime-theme", "JetBrains Islands Light.sublime-theme"):
    data = load_json(open(os.path.join(ROOT, theme)).read())
    for rule in data.get("rules", []):
        for key, value in rule.items():
            if key.endswith("texture") and isinstance(value, str) and value.startswith("JetBrains Islands/"):
                rel = value.split("/", 1)[1]
                check(os.path.exists(os.path.join(ROOT, rel)), f"{theme}: missing texture {value}")

# 3. Icon mappings reference existing PNGs.
for mapping in ("JetBrains Islands Dark.sublime-file-icons", "JetBrains Islands Light.sublime-file-icons"):
    data = load_json(open(os.path.join(ROOT, mapping)).read())
    for ext, icon in data["icons"].items():
        p = os.path.join(ROOT, "icons", icon + ".png")
        check(os.path.exists(p), f"{mapping}: missing icon {icon} ({ext})")

# 4. Both flavours define the same rule count and variable set.
dark = load_json(open(os.path.join(ROOT, "JetBrains Islands Dark.sublime-theme")).read())
light = load_json(open(os.path.join(ROOT, "JetBrains Islands Light.sublime-theme")).read())
check(len(dark["rules"]) == len(light["rules"]), "rule count differs between flavours")
check(set(dark["variables"]) == set(light["variables"]), "variable sets differ between flavours")

# 5. Plugin compiles.
import py_compile
try:
    py_compile.compile(os.path.join(ROOT, "islands_theme.py"), doraise=True)
except Exception as e:
    failures.append(f"plugin does not compile: {e}")

# 6. The .sublime-package contains no build scripts or caches.
if os.path.exists(PKG):
    with zipfile.ZipFile(PKG) as z:
        names = z.namelist()
    for bad in ("scripts/", "__pycache__/", ".DS_Store"):
        check(not any(n.startswith(bad) for n in names), f"package contains {bad}")
    for required in ("JetBrains Islands Dark.sublime-theme", "JetBrains Islands Light.sublime-theme",
                     "JetBrains Islands Dark.sublime-color-scheme", "JetBrains Islands Light.sublime-color-scheme",
                     "JetBrains Islands Dark.sublime-file-icons", "JetBrains Islands Light.sublime-file-icons",
                     "islands_theme.py", "LICENSE", "THIRD-PARTY-NOTICES.md", "docs/INSTALLATION.md"):
        check(required in names, f"package missing {required}")
else:
    failures.append("package not built")

print("\n".join("FAIL " + f for f in failures) if failures else "all checks passed")
sys.exit(1 if failures else 0)
