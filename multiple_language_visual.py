import requests
from plotly.graph_objs import Bar
from plotly import offline
import copy

"""
A file that generates a visual of the most starred 
repositories on GitHub for the given languages
"""

def generate_multiple_language_visual(*args):
    languages = 'language:'
    runs = 0
    arguments_copy = copy.deepcopy(args)

    for arg in args:
        adding = ''
        if runs == 0:
            adding += arg
        else:
            adding += f'+language:{arg}'
        languages += adding
        runs += 1

    url = f'https://api.github.com/search/repositories?q={languages}' \
          f'&sort' \
          '=stars'
    headers = {'Accept': 'application/vnd.github.v3+json'}
    r = requests.get(url, headers=headers)
    response_dicts = r.json()
    repo_dicts = response_dicts['items']
    repo_links, stars, labels, repo_language = [], [], [], []


    for repo_dict in repo_dicts:
        repo_name = repo_dict['name']
        repo_url = repo_dict['html_url']
        repo_link = f"<a href='{repo_url}'>{repo_name}</a>"
        repo_links.append(repo_link)
        repo_language = repo_dict['language']

        stars.append(repo_dict['stargazers_count'])

        owner = repo_dict['owner']['login']
        description = repo_dict['description']
        label = f"{owner}<br />{description} <br /> Language: {repo_language}"
        labels.append(label)

    file_lang = ''
    title_langs =''
    for arg in arguments_copy:
        adding_file = f"{arg}_"
        file_lang += adding_file

        adding_title = f"{arg.title()} "
        title_langs += adding_title

    # Make visualization
    data = [{
        'type': 'bar',
        'x': repo_links,
        'y': stars,
        'hovertext': labels,
        'marker': {
            'color': 'rgb(60,100,150)',
            'line': {'width': 1.5, 'color': 'rgb(25,25,25)'}
        },
        'opacity': 0.6,
    }]
    my_layout = {
        'title': f'Most-Starred {title_langs} Projects on GitHub',
        'titlefont': {'size': 28},
        'xaxis': {
            'title': 'Repository',
            'titlefont': {'size': 24},
            'tickfont': {'size': 14},
        },
        'yaxis': {
            'title': 'Stars',
            'titlefont': {'size': 24},
            'tickfont': {'size': 14},
        },
    }

    fig = {'data': data, 'layout': my_layout}
    new_file = f"{file_lang}_repos.html"
    offline.plot(fig, filename=new_file)

generate_multiple_language_visual("java", "python", "C", "go", "ruby",
                                  "perl", "haskell")
