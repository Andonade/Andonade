import util

README_PREFIX = ('## Andonade\n\n'
                 'Hi there 👋, this is Andonade.\n\n'
                 'Undergraduate student at Tsinghua University, majoring in Computer Science and Technology.\n\n'
                 '### WakaTime Weekly Stats\n\n'
                 '[![wakatime](https://wakatime.com/badge/user/018bd8cc-ca3d-4a3e-a11d-74879d0e0c99.svg)]('
                 'https://wakatime.com/@018bd8cc-ca3d-4a3e-a11d-74879d0e0c99)')

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(README_PREFIX)
    f.write(util.get_activity())
    f.write(util.get_language())
    f.write(util.get_editor())
    f.write(util.get_os())
    f.write(util.get_project())
    f.write(util.get_dependency())
    f.write(util.get_time_info())
