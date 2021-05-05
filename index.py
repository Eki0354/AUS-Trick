import subprocess
from PIL import Image
import re
import time

# 运行命令
def run(cmd):
  screenExecute = subprocess.Popen(
    str(cmd),
    stderr = subprocess.PIPE,
    stdout = subprocess.PIPE,
    shell = True
  )
  stdout, stderr = screenExecute.communicate()
  stdout = stdout.decode("utf-8")
  stderr = stderr.decode("utf-8")
  if (stderr != ""):
    print(stderr)
    return None
  else:
    return stdout

# 获取设备分辨率
# def getDeviceSize():
#   result = run("adb shell wm size")
#   print("大小", result)
#   print(re.match(r'(\d+)x(\d+)', result))

# getDeviceSize()

# 对比颜色是否相同
def isSameColor(c1, c2):
  for i in range(len(c2)):
    if (int(c1[i]) != int(c2[i])):
      return False
  return True

class AUS(): # ALIVE UNTIL SUNSET 日落即逝
  colorDict = {
    "startBlue": {
      "x": 1760,
      "y": 956,
      "color": [0, 146, 212, 255]
    },
    "startRed": {
      "x": 1599,
      "y": 943,
      "color": [185, 69, 0, 255]
    },
    "over": {
      "x": 87,
      "y": 990,
      "color": [255, 255, 255, 255]
    }
  }

  def __init__(self):
    self.devices = self.getDevices()
    if (self.chooseDevice(self.devices) != True):
      return
    print("演唱会开始！")
    self.times = 0
    self.circle()

  # 获取已连接的设备列表
  def getDevices(self):
    print("正在获取已连接的设备. . .")
    stdout = run("adb devices")
    if (stdout != None):
      devicesStr = stdout.replace("List of devices attached", "").strip()
      devices = []
      for deviceStr in devicesStr.split('\r\n'):
        deviceIndex = deviceStr.find('\t')
        devices.append(deviceStr[0:deviceIndex])
      print("获取设备成功")
      return devices
    else:
      print("设备获取失败，请检查后重试。")
      return None

  # 确认目标设备
  def chooseDevice(self, devices):
    if (devices == None or len(devices) < 1):
      print("未检测到已连接的设备，请检查后重试。")
      return
    # elif (len(devices) > 1):
    #   prompt = "检测到多个设备，请选择目标设备：\r\n0 - 全部\r\n"
    #   for index in range(len(devices)):
    #     prompt += str(index + 1) + " - " + devices[index] + "\r\n"
    #   choice = int(input(prompt))
    #   if (choice < 0 or choice > len(devices) - 1):
    #     print("目标序列号不正确，请重试。")
    #     return
    #   elif (choice == 0):
    #     self.device = ""
    #   else:
    #     self.device = devices[choice - 1]
    # else:
    #   self.device = devices[0]
    # 暂不支持多设备
    self.device = devices[0]
    deviceStr = self.device
    if (deviceStr == ""):
      deviceStr = "全部"
    print("已确认目标设备：" + deviceStr)
    return True

  def screenshot(self): # 截图并传至电脑
    run("adb shell /system/bin/screencap -p /sdcard/aus.png")
    run("adb pull /sdcard/aus.png aus.png")
    imgSrc = Image.open("aus.png").convert("RGBA")
    self.imgData = imgSrc.load()
    imgSrc.close()

  # 获取图片坐标像素
  def getPixel(self, x = 1, y = 1):
    # print("x", x, "y", y)
    return self.imgData[int(x), int(y)]

  # 分析某个像素点信息
  def analysisPixel(self, key):
    item = AUS.colorDict[key]
    realColor = self.getPixel(item["x"], item["y"])
    if (isSameColor(realColor, item["color"])):
      cmd = "adb shell input tap " + repr(item["x"]) + " " + repr(item["y"])
      run(cmd)
      return True
    else:
      return False

  # 分析图片像素
  def analysisImage(self):
    if (self.analysisPixel("over")):
      print("点击 行动结束")
    elif (self.analysisPixel("startBlue")):
      print("点击 开始行动 （蓝色）")
    elif (self.analysisPixel("startRed")):
      print("点击 开始行动 （红色）")
    else:
      print("无事发生")
      # cmd = "adb shell input tap 959 69"
      # run(cmd)


  # 基础循环
  def circle(self, duration = 3):
    self.times = self.times + 1
    print("获取现场实况. . .第 " + str(self.times) + " 次")
    self.screenshot()
    print("分析粉丝热情中. . .")
    self.analysisImage()
    time.sleep(duration)
    return self.circle()


aus = AUS()
aus.screenshot()
