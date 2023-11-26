import datetime
import util

README_PREFIX = ('## Andonade\n\n'
                 'Hi there 👋, this is Andonade.\n\n'
                 'Undergraduate student at Tsinghua University, majoring in Computer Science and Technology.\n\n'
                 '### WakaTime Weekly Stats')

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(README_PREFIX)
    f.write(util.get_activity())
    f.write(util.get_language())
    f.write(util.get_editor())
    f.write(util.get_os())
    f.write(util.get_project())
    f.write(util.get_dependency())
    f.write('\n\n🌏 Timezone: `Asia/Shanghai`')
    f.write(f"\n\n⏰ Updated on `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")
