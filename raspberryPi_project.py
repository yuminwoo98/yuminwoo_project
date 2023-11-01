
import spidev
import time
import RPi.GPIO as GPIO
import time
import board
import busio
import digitalio
import adafruit_ssd1306
import os
import subprocess

from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

menuScreen = 0
numG = 0
count = 0
Click = False
menu1Bool = False
menu2Bool = False
menu3Bool = False
menu4Bool = False

spi = spidev.SpiDev()

spi.open(0,0)

spi.max_speed_hz = 100000

delay = 0.5

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM) 
GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)

oled_reset = digitalio.DigitalInOut(board.D4)  
WIDTH = 128
HEIGHT = 64
BORDER = 5
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)


LOOPTIME = 1.0
oled.fill(0)          
oled.show()

image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

font = ImageFont.truetype('PixelOperator.ttf', 30) 
font2 = ImageFont.truetype('PixelOperator.ttf', 22) 

sw_channel = 0
vrx_channel =1
vry_channel = 2

xZero = 507
yZero = 523
tolerancevalue = 3

def position(adcnum, zerovalue):
return readadc(adcnum)-zerovalue

def readadc(adcnum):
if adcnum > 7 or adcnum < 0:
return -1
r = spi.xfer2([1,(8+adcnum)<< 4,0])
data = ((r[1]&3) << 8 )+ r[2]
return data


 # ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
def button_callback(channel):   #버튼 클릭으로 현재 표시된 메뉴의 활성화/비활성화 조작
global menu1Bool,menu2Bool,menu3Bool,menu4Bool
if numG == 0:                                                               
menu1Bool = not menu1Bool
	if menu1Bool == False:
		GPIO.output(21,1)
		GPIO.output(20,0)
		num1 = '|X|-1--------\nFail2Ban'
		draw.text((0,0) , num1, font=font ,fill = 255)
		oled.image(image).

		oled.show()
		os.system("sudo systemctl disable fail2ban")


  else:
    num1 = '|O|-1--------\\nFail2Ban'
    draw.text((0,0) , num1, font=font ,fill = 255)
    oled.image(image)
    oled.show()
    os.system("sudo systemctl enable fail2ban")
    GPIO.output(21,0)
    GPIO.output(20,1)

if numG == 1:                                                             
    menu2Bool = not menu2Bool
    if menu2Bool == False:            
        GPIO.output(21,1)
        GPIO.output(20,0)
        num2 = '|X|---2------\\n UFW'
        draw.text((0,0) , num2, font=font ,fill = 255)
        oled.image(image)
        oled.show()
        os.system("sudo ufw disable")  
    else:
        GPIO.output(21,0)
        GPIO.output(20,1)
        num2 = '|O|---2------\\n UFW'
        draw.text((0,0) , num2, font=font ,fill = 255)
        oled.image(image)
        oled.show()
        os.system("sudo ufw enable")

if numG == 2:
    menu3Bool = not menu3Bool
    if menu3Bool == False:            
        GPIO.output(21,1)
        GPIO.output(20,0)
        num3 = '|X|-----3----\\nchange ssh port'
        draw.text((0,0) , num3, font=font ,fill = 255)
        oled.image(image)
        oled.show()
        os.system("sudo sed -i '15 s/Port 222/Port 22/' /etc/ssh/sshd_config")  

        print("ssh포트번호 222  -> 22")
    else:
        GPIO.output(21,0)
        GPIO.output(20,1)
        num3 = '|O|-----3----\\nchange ssh port'
        draw.text((0,0) , num3, font=font ,fill = 255)
        oled.image(image)
        oled.show()
        os.system("sudo sed -i '15 s/Port 22/Port 222/' /etc/ssh/sshd_config")
        print("ssh포트번호 22  -> 222")

if numG == 3:
    menu4Bool = not menu4Bool  
    if menu4Bool == True:
        GPIO.output(21,0) 
        GPIO.output(20,0)
        num3 = 'Press the\\nmiddle to run'
        draw.text((0,0) , num3, font=font2 ,fill = 255)
        oled.image(image)
        oled.show()
        #time.sleep(5)
        menu4Bool == False
    else:
        num3 = 'Package\\nupgrade??'
        draw.text((0,0) , num3, font=font ,fill = 255)
        oled.image(image)
        oled.show()
 # ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
```


 # ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
def showScreen(num): # 버튼 눌림 상태와 조이스틱 조작에 따른 OLED 상태 변경 
global numG
global Click

if num  == 0 and menu1Bool == False:
	GPIO.output(21,1)
	GPIO.output(20,0)
	numG = num
	#print("test 메뉴1")
	num1 = '|X|-1--------\nFail2Ban'
	draw.text((0,0) , num1, font=font ,fill = 255)
	oled.image(image)
	oled.show()
elif num  == 0 and menu1Bool == True:
	GPIO.output(21,0)
	GPIO.output(20,1)
	numG = num
	num1 = '|O|-1--------\nFail2Ban'
	draw.text((0,0) , num1, font=font ,fill = 255)
	oled.image(image)
	oled.show()

elif num == 1 and menu2Bool == False:
	GPIO.output(21,1)
	GPIO.output(20,0)
	numG = num
	num2 = '|X|---2------\n UFW'
	draw.text((0,0) , num2, font=font ,fill = 255)
	oled.image(image)
	oled.show()
elif num == 1 and menu2Bool == True:
	GPIO.output(21,0)
	GPIO.output(20,1)
	numG = num
	num2 = '|O|---2------\n UFW'
	draw.text((0,0) , num2, font=font ,fill = 255)
	oled.image(image)
	oled.show()

elif num == 2 and menu3Bool == False:
	GPIO.output(21,1)
	GPIO.output(20,0)
	numG = num
	num3 = '|X|-----3----\nchange ssh port'
	draw.text((0,0) , num3, font=font ,fill = 255)
	oled.image(image)
	oled.show()
elif num == 2 and menu3Bool == True:
	GPIO.output(21,0)
	GPIO.output(20,1)
	numG = num
	num3 = '|O|-----3----\nchange ssh port'
	draw.text((0,0) , num3, font=font ,fill = 255)
	oled.image(image)
	oled.show()

elif num == 3 and menu4Bool == False:
	GPIO.output(21,0)
	GPIO.output(20,0)
	numG = num
	num1 = 'Package\nupgrade??'
	draw.text((0,0) , num1, font=font ,fill = 255)
	oled.image(image)
	oled.show()
elif num == 3 and menu4Bool == True:
	numG = num
	num1 = 'Press the\nmiddle to run'
	draw.text((0,0) , num1, font=font2 ,fill = 255)
	oled.image(image)
	oled.show()
 # ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ



 # ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
def menu4():   # 조이스틱 중앙을 꾹 눌렀을때 apt upgrade 실행
	global Click,numG,menu4Bool
	if numG == 3 and menu4Bool == True and Click == True:
		print("업데이트")  #  os.system("sudo apt upgrade -y")
		# 불필요할 때에 업그레이드를 하지 않기위해 "sudo apt upgrade -y">"업데이트" 로 대체
		    
		Click = not Click
	else:
		pass
 # ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ


 # ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
def menuNum(num):  # 조이스틱으로 OLED 메뉴화면을 컨트롤 하는 함수
	global menuScreen
	if num > 900: 
		menuScreen -= 1
		if menuScreen <= -1:  
			menuScreen = 3
			showScreen(menuScreen)  
		else:
			showScreen(menuScreen)
	elif num <100:
		menuScreen += 1
		if menuScreen >= 4: 
			menuScreen = 0
			showScreen(menuScreen) 
		else:
			showScreen(menuScreen)
	else:
		showScreen(menuScreen) 
 # ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

GPIO.setup(15,[GPIO.IN](http://gpio.in/), pull_up_down = GPIO.PUD_DOWN)
GPIO.add_event_detect(15,GPIO.RISING, callback=button_callback, bouncetime=300)
while True:
	sw_val = readadc(sw_channel)
	xPos = readadc(vrx_channel)
	yPos = readadc(vry_channel)
	draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0) ###
	num = sw_val
	if num == 0:
    count += 1
	else:
    count = 0
	if count >= 10:
    Click = not Click
    menu4()
    count = 0


if xPos > 900:
    menuNum(xPos)
if xPos <100:
    menuNum(xPos)

time.sleep(0.2)

