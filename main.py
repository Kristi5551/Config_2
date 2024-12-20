import os
import configparser
import git
from datetime import datetime
import graphviz
import pytz
import sys


def load_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config['settings']


def get_commits(repo_path, branch_name):
    repo = git.Repo(repo_path)
    branch = repo.branches[branch_name]
    commits = list(repo.iter_commits(branch))
    return commits


def build_graph(commits, output_file):
    # Сортируем коммиты по времени их создания в хронологическом порядке
    commits.sort(key=lambda commit: commit.committed_datetime)

    dot = graphviz.Digraph(comment='Git Commit Dependencies')

    for commit in commits:
        # Добавляем узел с номером коммита
        dot.node(commit.hexsha, commit.hexsha)  # Узел содержит только номер коммита (hexsha)
        for parent in commit.parents:
            dot.edge(parent.hexsha, commit.hexsha)  # Связываем с родительскими коммитами

    dot.render(output_file, view=True)
    print(dot.source)


def main():
    if len(sys.argv) != 5:
        print(
            "Использование: python script.py <path_to_visualization_program> <path_to_repo> <output_file> <branch_name>")
        return

    visualization_program = sys.argv[1]
    repo_path = sys.argv[2]
    output_file = sys.argv[3]
    branch_name = sys.argv[4]

    # Проверяем, существует ли репозиторий
    if not os.path.exists(repo_path):
        print(f"Репозиторий по пути {repo_path} не найден.")
        return

    # Получаем коммиты из указанной ветки
    commits = get_commits(repo_path, branch_name)

    if not commits:
        print(f"Нет коммитов в ветке '{branch_name}'.")
        return

    build_graph(commits, output_file)


if __name__ == "__main__":  # Исправлено на правильное имя
    main()