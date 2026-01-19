[app]
title = 康复医学答题
package.name = rehabquiz
package.domain = org.rehab
source.dir = .
source.main = main.py
version = 1.0.0

# 依赖：最小化，与工作流中安装的版本匹配
requirements = python3, kivy==2.1.0

# Android配置：与工作流中安装的版本严格一致
android.api = 34                # 对应 platforms;android-34
android.minapi = 24             # Android 7.0，兼容性更好
android.sdk = 34                # 与 api 一致
android.ndk = 26.1.10909125    # 对应 android-ndk-r26c
android.ndk_api = 21
android.build_tools_version = 34.0.0  # 对应 build-tools;34.0.0

# 架构与编译
android.archs = arm64-v8a      # 64位架构，推荐
# android.archs = armeabi-v7a  # 如需32位，使用此行并注释上一行

# 权限与特性
android.permissions = INTERNET
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 0
android.accept_sdk_license = True
