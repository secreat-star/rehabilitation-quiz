[app]
title = 康复医学答题
package.name = rehabquiz
package.domain = org.rehab

source.dir = .
source.main = main.py
version = 1.0.0

# 依赖：确保与requirements.txt一致
requirements = python3, kivy==2.1.0

# Android配置：版本与工作流中安装的SDK一致
android.api = 33
android.minapi = 21
# NDK版本设置为稳定且兼容的25b
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
