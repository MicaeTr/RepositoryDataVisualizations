import requests
from plotly.graph_objs import Bar
from plotly import offline


"""
A file that generates a visual of the most starred 
repositories on GitHub for the given language
"""


def generate_language_visual(language):
    # Make an API call and store the response
    url = f'https://api.github.com/search/repositories?q=language:{language}' \
          f'&sort' \
          '=stars'
    headers = {'Accept': 'application/vnd.github.v3+json'}
    r = requests.get(url, headers=headers)

    # Process Results
    response_dict = r.json()
    repo_dicts = response_dict['items']
    repo_links, stars, labels = [], [], []
    for repo_dict in repo_dicts:
        repo_name = repo_dict['name']
        repo_url = repo_dict['html_url']
        repo_link = f"<a href='{repo_url}'>{repo_name}</a>"
        repo_links.append(repo_link)
        stars.append(repo_dict['stargazers_count'])

        owner = repo_dict['owner']['login']
        description = repo_dict['description']
        label = f"{owner}<br />{description}"
        labels.append(label)

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
        'title': 'Most-Starred Python Projects on GitHub',
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
    new_file = f"{language}_repos.html"
    offline.plot(fig, filename=new_file)

language = input("Please type in a programming language: ")
generate_language_visual(language)
