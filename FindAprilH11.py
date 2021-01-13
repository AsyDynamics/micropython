# AprilTags 3d measurement
#
# Using gc0328 camera and linear regression to measure real z_translation

import sensor, image, time, math, lcd

lcd.init()
lcd.mirror(0)
sensor.reset()
sensor.set_hmirror(0)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.skip_frames(50)
#sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
#sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    img.draw_string(5,10,str('%.2f' % clock.fps()),color=(255,0,0))
    result = img.find_apriltags() # defaults to TAG36H11 without "families". families = image.TAG16H5
    num = len(result)
#    print(num)
    for i in range(num): 
        tag = result[i]
        degress = '%.2f' % (180 * tag.rotation() / math.pi)
        img.draw_rectangle(tag.rect(), color = (255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
        img.draw_string(100, 10, "find tag: "+str(num), color=(255,0,0))
        img.draw_string(5, 30+i*15, str(tag.id()), color=(0,0,255))
        z_dis = '%.2f' % (-17.173* tag.z_translation() + 3.6789)
        img.draw_string(20, 30+i*15,str(z_dis)+", "+str(degress), color=(0,0,255))
        print(tag.id(),z_dis, degress)
    lcd.display(img)
