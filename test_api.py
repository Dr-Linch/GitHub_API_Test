import requests
import os
import json
from dotenv import load_dotenv

load_dotenv(os.path.join('.', '.env'))


def test_github_api():
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {os.getenv("TOKEN")}',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    data_for_create_new_repo = {"name": os.getenv('REPO_NAME'),
                                "description": "Just test repo!",
                                "homepage": "https://github.com",
                                "private": False, "is_template": True}

    new_rep = requests.request(method='POST', url='https://api.github.com/user/repos', headers=headers,
                               data=json.dumps(data_for_create_new_repo))

    all_repos = requests.request(method='GET', url='https://api.github.com/user/repos', headers=headers)

    check = 0
    for repo in all_repos.json():
        if repo['name'] == os.getenv('REPO_NAME'):
            check = 1
            break

    if check == 0:
        raise Exception(f'Ошибка при создании репозитория.\n{new_rep.status_code}\n{new_rep.json()}')

    delete_new_rep = requests.request(method='DELETE', url=f'https://api.github.com/repos/{os.getenv("USER_NAME")}/'
                                                           f'{os.getenv("REPO_NAME")}', headers=headers)

    if delete_new_rep.status_code != 204:
        raise Exception(f'Ошибка при удалении репозитория.\n{delete_new_rep.status_code}\n{delete_new_rep.json()}')


if __name__ == '__main__':
    test_github_api()
