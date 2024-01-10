import unittest
import os
from unittest.mock import patch, MagicMock
from ZWrapper import ZWrapper

class TestZWrapper(unittest.TestCase):
    def setUp(self):
        self.zwrapper = ZWrapper()

    @patch('ZWrapper.zotero.Zotero')
    @patch('ZWrapper.LastVersion.get_or_create')
    @patch('ZWrapper.CollectionCache.get_or_create')
    def test_pull_database(self, mock_get_or_create, mock_last_version, mock_zotero):
        mock_last_version.return_value = [MagicMock(version=13636)]
        mock_zotero.collections.return_value = [{'data': {'key': 'test_key', 'version': '13637'}}]
        mock_get_or_create.return_value = [MagicMock(key='test_key', version=13636)]

        self.zwrapper.pull_database()

        mock_get_or_create.assert_called_once_with(key='test_key')
        mock_last_version.assert_called_once_with(id=1)
        mock_zotero.collections.assert_called_once_with(since=13636)

if __name__ == '__main__':
    unittest.main()