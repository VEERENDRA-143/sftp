from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
import io

class SFTPFileTests(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('sftp_files.views.pysftp')
    def test_upload_file_success(self, mock_pysftp):
        mock_sftp = MagicMock()
        mock_pysftp.Connection.return_value.__enter__.return_value = mock_sftp

        file_content = b'test file content'
        test_file = io.BytesIO(file_content)
        test_file.name = 'test.txt'

        response = self.client.post(reverse('upload_file'), {'file': test_file})

        self.assertEqual(response.status_code, 200)
        self.assertIn('File uploaded successfully', response.json()['message'])
        mock_sftp.putfo.assert_called_once()

    @patch('sftp_files.views.pysftp')
    def test_download_file_success(self, mock_pysftp):
        mock_sftp = MagicMock()
        mock_pysftp.Connection.return_value.__enter__.return_value = mock_sftp

        filename = 'test.txt'
        response = self.client.get(reverse('download_file', args=[filename]))

        self.assertEqual(response.status_code, 200)
        mock_sftp.getfo.assert_called_once()
