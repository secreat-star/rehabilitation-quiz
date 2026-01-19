[app]
title = 康复医学答题
package.name = rehabquiz
package.domain = org.rehab
source.dir = .
source.main = main.py
version = 1.0.0
requirements = python3,kivy==2.1.0
orientation = portrait
fullscreen = 0

# Android配置 - 更新到支持NDK 25
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a

# 权限
android.permissions = INTERNET

# Gradle配置
android.gradle_dependencies = 'com.android.tools.build:gradle:7.4.2'
android.enable_androidx = True

[buildozer]
log_level = 2
