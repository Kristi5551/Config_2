import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock
import os
import sys
from main import load_config, get_commits, build_graph, main


class TestMainFunctions(unittest.TestCase):

    @patch('configparser.ConfigParser.read')
    def test_load_config(self, mock_read):
        mock_config = MagicMock()
        mock_config.__getitem__.return_value = {'key': 'value'}
        with patch('configparser.ConfigParser', return_value=mock_config):
            config = load_config('dummy.ini')
            self.assertEqual(config['key'], 'value')

    @patch('git.Repo')
    def test_get_commits(self, mock_repo):
        mock_commit = MagicMock()
        mock_commit.hexsha = 'abc123'
        mock_commit.committed_datetime = datetime(2021, 1, 1)
        mock_repo.return_value.iter_commits.return_value = [mock_commit]

        commits = get_commits('dummy_path', 'main')
        self.assertEqual(len(commits), 1)
        self.assertEqual(commits[0].hexsha, 'abc123')

    @patch('graphviz.Digraph')
    def test_build_graph(self, mock_Digraph):
        mock_commit = MagicMock()
        mock_commit.hexsha = 'abc123'
        mock_commit.parents = []
        mock_commit.committed_datetime = datetime(2021, 1, 1)

        commits = [mock_commit]
        output_file = 'output_file'

        build_graph(commits, output_file)

        # Проверяем, что метод render был вызван
        mock_Digraph.return_value.render.assert_called_with(output_file, view=True)

    @patch('sys.exit')
    @patch('os.path.exists', return_value=True)
    @patch('main.get_commits', return_value=[])
    @patch('main.build_graph')
    def test_main_no_commits(self, mock_build_graph, mock_get_commits, mock_exists, mock_exit):
        sys.argv = ['script.py', 'path_to_visualization_program', 'path_to_repo', 'output_file', 'branch_name']
        with patch('builtins.print') as mocked_print:
            main()
            mocked_print.assert_called_with("Нет коммитов в ветке 'branch_name'.")

    @patch('sys.exit')
    @patch('os.path.exists', return_value=False)
    def test_main_repo_not_found(self, mock_exists, mock_exit):
        sys.argv = ['script.py', 'path_to_visualization_program', 'invalid_path', 'output_file', 'branch_name']
        with patch('builtins.print') as mocked_print:
            main()
            mocked_print.assert_called_with("Репозиторий по пути invalid_path не найден.")


if __name__ == '__main__':
    unittest.main()