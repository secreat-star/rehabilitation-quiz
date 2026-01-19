[app]

# (1) 应用基本信息：与你项目一致
title = 康复医学答题
package.name = rehabquiz
package.domain = org.rehab
source.dir = .
source.main = main.py
version = 1.0.0

# (2) Python依赖：必须精简准确，与 requirements.txt 呼应
requirements = python3, kivy==2.1.0
# 注意：工作流中未安装Pillow等，此处不要添加多余依赖。

# (3) Android核心配置：与工作流安装的环境严格对应
android.api = 33                # 与工作流中 `platforms;android-33` 一致
android.minapi = 21             # 最低支持版本
android.sdk = 33                # 与 android.api 保持一致
android.ndk = 25b               # ！！！关键：与工作流下载的 `android-ndk-r25b` 完全一致
android.ndk_api = 21

# (4) 架构与编译选项
android.archs = arm64-v8a       # 推荐使用64位架构，兼容性更好。如需32位可改为 armeabi-v7a
# android.archs = armeabi-v7a, arm64-v8a  # 如果希望构建多版本APK，但会延长构建时间
android.stl = libc++_shared
android.build_tools_version = 33.0.0  # 与工作流中 `build-tools;33.0.0` 一致

# (5) 权限与功能
android.permissions = INTERNET
android.allow_backup = False

# (6) 应用特性
orientation = portrait
fullscreen = 0

###############
[buildozer]
###############
# (7) 日志与构建控制
log_level = 2                   # 详细信息，调试必备
warn_on_root = 0                # 配合工作流中的 BUILDOZER_ALLOW_ROOT=1
android.accept_sdk_license = True # 自动接受SDK许可证，CI环境下必需
