import os
import zipfile
from pathlib import Path
import re
import yaml

skill_path = Path('f:/src/rd-cost-eval-skill')
output_dir = Path('f:/src/rd-cost-eval-skill')

# 验证SKILL.md存在
skill_md = skill_path / 'SKILL.md'
if not skill_md.exists():
    print('❌ SKILL.md not found')
    exit(1)

# 读取并验证frontmatter
content = skill_md.read_text(encoding='utf-8')
if not content.startswith('---'):
    print('❌ No YAML frontmatter found')
    exit(1)

match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
if not match:
    print('❌ Invalid frontmatter format')
    exit(1)

frontmatter_text = match.group(1)
try:
    frontmatter = yaml.safe_load(frontmatter_text)
    if not isinstance(frontmatter, dict):
        print('❌ Frontmatter must be a YAML dictionary')
        exit(1)
except yaml.YAMLError as e:
    print(f'❌ Invalid YAML in frontmatter: {e}')
    exit(1)

# 检查必需字段
if 'name' not in frontmatter:
    print('❌ Missing required field: name')
    exit(1)
if 'description' not in frontmatter:
    print('❌ Missing required field: description')
    exit(1)

skill_name = frontmatter['name']
print(f'✅ Skill name: {skill_name}')
print(f'✅ Validation passed!')

# 创建skill包
skill_package = output_dir / f'{skill_name}.skill'
with zipfile.ZipFile(skill_package, 'w', zipfile.ZIP_DEFLATED) as zf:
    for file_path in skill_path.rglob('*'):
        if file_path.is_file() and file_path.suffix != '.skill' and file_path.name != 'package.py':
            arcname = file_path.relative_to(skill_path)
            zf.write(file_path, arcname)
            print(f'  📄 Added: {arcname}')

print(f'✅ Skill packaged: {skill_package}')
