import unittest
from python_repos import get_repo

class TestPythonRepos(unittest.TestCase):

    def test_status_code(self):
        repo = get_repo() 
        self.assertEqual(repo.status_code, get_repo().status_code)

    def test_number_repos_returned(self):
        repo_dict = get_repo().json()
        total_count = repo_dict['total_count']
        self.assertEqual(total_count, get_repo().json()['total_count'])

if __name__ == '__main__':
    unittest.main()
