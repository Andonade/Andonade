import datetime
import json
import requests
import base64
import os

filled_char = '█'
empty_char = '░'
STAT_URL = 'https://wakatime.com/api/v1/users/current/stats/last_7_days'
DURATION_URL = 'https://wakatime.com/api/v1/users/current/durations?date='
API_Key = os.environ.get('WAKATIME_API_KEY')
headers = {'Authorization': 'Basic ' + base64.b64encode(API_Key.encode('utf-8')).decode('utf-8')}
response = requests.get(STAT_URL, headers=headers)
data = json.loads(response.text)['data']


def convert_to_progress_bar(percentage: float, length: int = 25) -> str:
    """
    Convert a percentage to a progress bar.
    :param percentage: a float number between 0 and 100
    :param length: the length of the progress bar, default is 20
    :return: progress bar as a string
    """
    filled_length = int(length * percentage / 100.0)
    empty_length = length - filled_length
    progress_bar = filled_char * filled_length + empty_char * empty_length
    percentage_text = f' {percentage}%'
    progress_bar += percentage_text
    return progress_bar


def get_activity() -> str:
    """
    Get coding activities.
    :return: string of coding activities with Markdown formatting
    """
    activity = '\n\n🧑‍💻 My coding activity \n\n```text\n'
    date = [datetime.date.today() - datetime.timedelta(days=i) for i in range(1, 8)]
    if response.status_code == 200:
        activity += f"I coded for {data['human_readable_total_including_other_language']} in the last 7 days\n"
    else:
        activity += 'missing data for this week\n'
    activity += '\t\t|🕐      🕗     🕓      🕛|\tcoding hours\n'
    for i in range(6, -1, -1):
        res = requests.get(DURATION_URL + date[i].strftime('%Y-%m-%d'), headers=headers)
        activity += f"{date[i].strftime('%m-%d %a')}\t"
        if res.status_code == 200:
            active = [False] * 24
            projects = json.loads(res.text)['data']
            total = 0.0
            for p in projects:
                start_dt = datetime.datetime.fromtimestamp(p['time'])
                end_dt = datetime.datetime.fromtimestamp(p['time'] + p['duration'])
                total += p['duration']
                for hr in range(start_dt.hour, end_dt.hour + 1):
                    active[hr] = True
            activity += '|'
            for hr in range(24):
                activity += filled_char if active[hr] else empty_char
            activity += '|\t'
            total = round(total / 60)
            hours, minutes = divmod(total, 60)
            if hours > 1:
                activity += f'{hours} hrs '
            elif hours == 1:
                activity += '1 hr '
            activity += f'{minutes} mins\n'
        else:
            activity += 'missing data for this day\n'
    return activity + '```'


def get_language() -> str:
    """
    Get coding languages.
    :return: string of coding languages with Markdown formatting
    """
    language = '\n\n🌱 My main coding languages \n\n```text\n'
    if response.status_code == 200:
        languages = data['languages']
        languages.sort(key=lambda x: x['percent'], reverse=True)
        for lang in languages:
            if lang['percent'] < 3:
                break
            language += "{:<15}\t{:<20}\t{:<}\n".format(lang['name'], lang['text'],
                                                        convert_to_progress_bar(lang['percent']))
    else:
        language += 'missing data for this week\n'
    return language + '```'


def get_editor() -> str:
    """
    Get coding editors.
    :return: string of coding editors with Markdown formatting
    """
    editor = '\n\n🔥 My coding editors \n\n```text\n'
    if response.status_code == 200:
        editors = data['editors']
        editors.sort(key=lambda x: x['percent'], reverse=True)
        for edit in editors:
            editor += "{:<15}\t{:<20}\t{:<}\n".format(edit['name'], edit['text'],
                                                      convert_to_progress_bar(edit['percent']))
    else:
        editor += 'missing data for this week\n'
    return editor + '```'


def get_os() -> str:
    """
    Get operating systems.
    :return: string of operating systems with Markdown formatting
    """
    os = '\n\n🖥️ My operating systems \n\n```text\n'
    if response.status_code == 200:
        oses = data['operating_systems']
        oses.sort(key=lambda x: x['percent'], reverse=True)
        for o in oses:
            os += "{:<15}\t{:<20}\t{:<}\n".format(o['name'], o['text'],
                                                  convert_to_progress_bar(o['percent']))
    else:
        os += 'missing data for this week\n'
    return os + '```'


def get_project() -> str:
    """
    Get coding projects.
    :return: string of coding projects with Markdown formatting
    """
    project = '\n\n📦 Main projects I worked on \n\n```text\n'
    if response.status_code == 200:
        projects = data['projects']
        projects.sort(key=lambda x: x['percent'], reverse=True)
        for p in projects:
            if p['percent'] < 3:
                break
            project += "{:<20}\t{:<20}\t{:<}\n".format(p['name'], p['text'],
                                                       convert_to_progress_bar(p['percent']))
    else:
        project += 'missing data for this week\n'
    return project + '```'


def get_dependency() -> str:
    """
    Get coding dependencies.
    :return: string of coding dependencies with Markdown formatting
    """
    dependency = '\n\n📚 Main dependencies I used \n\n```text\n'
    if response.status_code == 200:
        dependencies = data['dependencies']
        dependencies.sort(key=lambda x: x['percent'], reverse=True)
        for d in dependencies:
            if d['percent'] < 3:
                break
            dependency += "{:<15}\t{:<20}\t{:<}\n".format(d['name'], d['text'],
                                                          convert_to_progress_bar(d['percent']))
    else:
        dependency += 'missing data for this week\n'
    return dependency + '```'
