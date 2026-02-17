"""
System theme detection utility for Windows.
This module provides the ThemeChecker class, which can be used to detect whether the current Windows system theme is dark or light.
It reads the Windows registry key that controls application theme preference.
"""
import winreg


def is_system_dark_theme() -> bool:
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
    value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
    winreg.CloseKey(key)
    return value == 0
