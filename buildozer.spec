[app]

# 应用信息
title = 康复医学答题
package.name = rehabquiz
package.domain = com.medical.rehab
source.dir = .
source.main = main.py
source.include_exts = py,png,jpg,kv,atlas,ttf,otf,json

# 版本
version = 1.0.0
version.code = 1

# 需求包
requirements = python3,kivy==2.1.0

# Android配置
android.api = 30
android.minapi = 21
android.sdk = 24
android.ndk = 23b
android.archs = armeabi-v7a

# 权限
android.permissions = INTERNET

# 特性
android.accept_sdk_license = True

# 方向
orientation = portrait
fullscreen = 0

# 日志级别
log_level = 2

# Buildozer设置
[buildozer]
log_level = 2
warn_on_root = 1