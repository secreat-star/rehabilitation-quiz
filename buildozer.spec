[app]
title = 康复医学答题
package.name = rehabquiz
package.domain = org.rehab
source.dir = .
source.main = main.py
version = 1.0.0
requirements = python3, kivy==2.1.0, openssl, pyjnius

# 与Action默认环境兼容的Android配置
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
