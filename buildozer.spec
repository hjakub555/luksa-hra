[app]
title = Lukša - Rapová Kariéra
package.name = luksa_rap
package.domain = org.luksa
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json
version = 1.0

# Pygame na Androidu nefunguje, Kivy používá sdl2 automaticky
requirements = python3,kivy

orientation = portrait

# Android konfigurace
android.accept_sdk_license = True
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# iOS konfigurace (ponecháno pro budoucno)
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

[buildozer]
log_level = 2
warn_on_root = 1
