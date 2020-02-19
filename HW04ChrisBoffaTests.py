import mock
import unittest
import json
from unittest.mock import patch, call
from HW04ChrisBoffa import user_github_activity, pretty_print_repo_info, get_user_repos, get_user_commits_for_repos


def _mock_response(
        status=200,
        content=json.dumps({"content": "test content"}),
        json_data=None,
        raise_for_status=None):
    """
    Mock request function so that we don't call github api every time
    """
    mock_resp = mock.Mock()
    # mock raise_for_status call w/optional error
    mock_resp.raise_for_status = mock.Mock()
    if raise_for_status:
        mock_resp.raise_for_status.side_effect = raise_for_status
    # set status code and content
    mock_resp.status_code = status
    mock_resp.content = content
    # add json data if provided
    if json_data:
        mock_resp.json = mock.Mock(
            return_value=json_data
        )
    return mock_resp


class GithubApi(unittest.TestCase):
    mocked_single_repo = [{"name": "test_repo"}]
    mocked_multiple_repos = [{"name": "test_repo"}, {"name": "test_repo2"}]

    @patch('builtins.print')
    def test_print_user_repo_info(self, mocked_print):
        pretty_print_repo_info(1, 1)
        self.assertEqual(mocked_print.mock_calls, [call('Repo: 1 Number of commits: 1')])

    @mock.patch('requests.get')
    def test_get_user_repos(self, mock_get):
        """test get_user_repos method"""
        mock_response = {"content": "test"}
        mock_resp = _mock_response(content=json.dumps(mock_response))
        mock_get.return_value = mock_resp

        result = get_user_repos('test_user')
        self.assertEqual(result, mock_response)

    @mock.patch('requests.get')
    def test_get_user_repos_failed(self, mock_get):
        """test get_user_repos fails method"""
        mock_response = {"content": "test"}
        mock_resp = _mock_response(status=400, content=json.dumps(mock_response))
        mock_get.return_value = mock_resp

        result = get_user_repos('test_user')
        self.assertEqual(result, [])

    @mock.patch('requests.get')
    def test_get_user_commits_for_repos(self, mock_get):
        """user_commits_for_repos"""
        mock_response = [{
            "sha": "6d7e1fdd7a242711c26a134c5f6a10c99bee46d4",
            "node_id": "MDY6Q29tbWl0Mjg3NjU3OTE6NmQ3ZTFmZGQ3YTI0MjcxMWMyNmExMzRjNWY2YTEwYzk5YmVlNDZkNA==",
            "commit": {
                "author": {
                    "name": "GitHub Student",
                    "email": "githubstudent@users.noreply.github.com",
                    "date": "2014-12-09T16:27:05Z"
                },
            }},
            {
                "sha": "6d7e1fdd7a242711c26a134c5f6a10c99bee46d4",
                "node_id": "MDY6Q29tbWl0Mjg3NjU3OTE6NmQ3ZTFmZGQ3YTI0MjcxMWMyNmExMzRjNWY2YTEwYzk5YmVlNDZkNA==",
                "commit": {
                    "author": {
                        "name": "GitHub Student",
                        "email": "githubstudent@users.noreply.github.com",
                        "date": "2014-12-09T16:27:05Z"
                    },
                }}
        ]
        mock_resp = _mock_response(content=json.dumps(mock_response))
        mock_get.return_value = mock_resp

        result = get_user_commits_for_repos('test_user', 'repo')
        self.assertEqual(result, len(mock_response))

    @mock.patch('requests.get')
    def test_get_user_commits_for_repos_failed(self, mock_get):
        """user_commits_for_repo failing"""
        mock_response = [{
            "sha": "6d7e1fdd7a242711c26a134c5f6a10c99bee46d4",
            "node_id": "MDY6Q29tbWl0Mjg3NjU3OTE6NmQ3ZTFmZGQ3YTI0MjcxMWMyNmExMzRjNWY2YTEwYzk5YmVlNDZkNA==",
            "commit": {
                "author": {
                    "name": "GitHub Student",
                    "email": "githubstudent@users.noreply.github.com",
                    "date": "2014-12-09T16:27:05Z"
                },
            }},
        ]
        mock_resp = _mock_response(status=400, content=json.dumps(mock_response))
        mock_get.return_value = mock_resp

        result = get_user_commits_for_repos('test_user', 'repo')
        self.assertEqual(result, 0)

    @mock.patch('HW04ChrisBoffa.prompt_user', return_value='fake_user')
    @mock.patch('HW04ChrisBoffa.get_user_repos', return_value=None)
    @patch('builtins.print')
    def test_user_github_activity_no_repos(self, mocked_print):
        user_github_activity()
        self.assertEqual(mocked_print.mock_calls, [call('There are no repositories for user: fake_user')])

    @mock.patch('HW04ChrisBoffa.prompt_user', return_value='fake_user')
    @mock.patch('HW04ChrisBoffa.get_user_repos', return_value=mocked_single_repo)
    @mock.patch('HW04ChrisBoffa.get_user_commits_for_repos', return_value=12)
    @patch('builtins.print')
    def test_user_github_activity_single_repo(self, mocked_print):
        user_github_activity()
        self.assertEqual(mocked_print.mock_calls, [call('Repo: test_repo Number of commits: 12')])

    @mock.patch('HW04ChrisBoffa.prompt_user', return_value='fake_user')
    @mock.patch('HW04ChrisBoffa.get_user_repos', return_value=mocked_multiple_repos)
    @mock.patch('HW04ChrisBoffa.get_user_commits_for_repos', return_value=12)
    @patch('builtins.print')
    def test_user_github_activity_multiple_repo(self, mocked_print):
        user_github_activity()
        self.assertEqual(mocked_print.call_count, 2)
        self.assertEqual(mocked_print.mock_calls, [call('Repo: test_repo Number of commits: 12'),
                                                   call('Repo: test_repo2 Number of commits: 12')])


if __name__ == '__main__':
    unittest.main()
