import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from admin_detector.core import (
    AdminDetector,
    UnixAdminDetector,
    WindowsAdminDetector
)


class TestAdminDetector(unittest.TestCase):
    """测试 AdminDetector"""

    @patch('admin_detector.core.platform.system')
    def test_is_admin_windows_true(self, mock_system):
        mock_system.return_value = 'Windows'
        with patch('admin_detector.core.ctypes.windll.shell32.IsUserAnAdmin', return_value=True):
            self.assertTrue(AdminDetector.is_admin())

    @patch('admin_detector.core.platform.system')
    def test_is_admin_windows_false(self, mock_system):
        mock_system.return_value = 'Windows'
        with patch('admin_detector.core.ctypes.windll.shell32.IsUserAnAdmin', return_value=False):
            self.assertFalse(AdminDetector.is_admin())

    @patch('admin_detector.core.platform.system')
    def test_is_admin_windows_fallback(self, mock_system):
        # Simulate ctypes failing, then fallback file write succeeds
        mock_system.return_value = 'Windows'
        with patch('admin_detector.core.ctypes.windll.shell32.IsUserAnAdmin', side_effect=Exception):
            with patch('admin_detector.core.os.environ.get', return_value='C:\\Windows'):
                with patch('admin_detector.core.open', MagicMock()) as mock_open:
                    with patch('admin_detector.core.os.remove') as mock_remove:
                        self.assertTrue(AdminDetector.is_admin())
                        mock_open.assert_called_once()
                        mock_remove.assert_called_once()

    @patch('admin_detector.core.platform.system')
    def test_is_admin_unix_root(self, mock_system):
        mock_system.return_value = 'Linux'
        with patch('admin_detector.core.os.geteuid', return_value=0):
            self.assertTrue(AdminDetector.is_admin())

    @patch('admin_detector.core.platform.system')
    def test_is_admin_unix_sudo(self, mock_system):
        mock_system.return_value = 'Linux'
        with patch('admin_detector.core.os.geteuid', return_value=1000):
            with patch.dict('os.environ', {'SUDO_USER': 'user'}):
                self.assertTrue(AdminDetector.is_admin())

    @patch('admin_detector.core.platform.system')
    def test_is_admin_unix_regular(self, mock_system):
        mock_system.return_value = 'Linux'
        with patch('admin_detector.core.os.geteuid', return_value=1000):
            with patch.dict('os.environ', clear=True):
                self.assertFalse(AdminDetector.is_admin())

    def test_unix_detector_root(self):
        with patch('admin_detector.core.os.geteuid', return_value=0):
            self.assertTrue(UnixAdminDetector.is_root())
            self.assertTrue(UnixAdminDetector.is_sudo())  # Not sudo, but root is admin

    def test_unix_detector_sudo(self):
        with patch('admin_detector.core.os.geteuid', return_value=1000):
            with patch.dict('os.environ', {'SUDO_USER': 'alice'}):
                self.assertFalse(UnixAdminDetector.is_root())
                self.assertTrue(UnixAdminDetector.is_sudo())

    @patch('admin_detector.core.ctypes.windll.shell32.IsUserAnAdmin')
    def test_windows_detector(self, mock_api):
        mock_api.return_value = True
        self.assertTrue(WindowsAdminDetector.is_user_admin())
        mock_api.return_value = False
        self.assertFalse(WindowsAdminDetector.is_user_admin())

    def test_get_admin_info_windows(self):
        with patch('admin_detector.core.platform.system', return_value='Windows'):
            with patch('admin_detector.core.AdminDetector.is_admin', return_value=True):
                with patch.dict('os.environ', {'USERNAME': 'testuser'}):
                    info = AdminDetector.get_admin_info()
                    self.assertEqual(info['system'], 'windows')
                    self.assertEqual(info['username'], 'testuser')
                    self.assertEqual(info['admin_method'], 'Windows UAC')

    def test_get_admin_info_unix(self):
        with patch('admin_detector.core.platform.system', return_value='Linux'):
            with patch('admin_detector.core.AdminDetector.is_admin', return_value=True):
                with patch('admin_detector.core.os.geteuid', return_value=0):
                    with patch.dict('os.environ', {'USER': 'root'}):
                        info = AdminDetector.get_admin_info()
                        self.assertEqual(info['system'], 'linux')
                        self.assertEqual(info['username'], 'root')
                        self.assertEqual(info['euid'], 0)

    def test_check_admin_with_reason_windows_admin(self):
        with patch('admin_detector.core.platform.system', return_value='Windows'):
            with patch('admin_detector.core.ctypes.windll.shell32.IsUserAnAdmin', return_value=True):
                result = AdminDetector.check_admin_with_reason()
                self.assertTrue(result['has_admin'])
                self.assertEqual(result['reason'], 'Windows UAC 管理员权限')

    def test_check_admin_with_reason_unix_root(self):
        with patch('admin_detector.core.platform.system', return_value='Linux'):
            with patch('admin_detector.core.os.geteuid', return_value=0):
                result = AdminDetector.check_admin_with_reason()
                self.assertTrue(result['has_admin'])
                self.assertEqual(result['reason'], 'root 用户权限')


if __name__ == '__main__':
    unittest.main()