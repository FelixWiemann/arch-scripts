import sys
import os
import io
import binascii
import time

if len(sys.argv) == 1:
  print ("extract jpgs from an image of a failed sd-card")
  print ("to get the image, copy it via 'dd if=/dev/sdx/ of=/path/to/image'")
  print ("")
  print ("usage: python extractimages.py <image> <output> [<offset>]")
  print ("  image : image to be extract the jpgs from, result of dd")
  print ("  output: output path the jpgs should be extracted to")
  print ("  offset: optional offset to start from")
  exit(0)

jpgheader = [0xff, 0xd8]
jpgfooter = [0xff, 0xd9]  
inJpg = False
wasInJpg = False
imageCount = 0
pic = 0
bytecount = 0.0

filesize = os.path.getsize(sys.argv[1])
percent = filesize/1000
print (jpgheader)
inThumb = False
currentImageSize = 0

lastReadBytes = [None] * len(jpgheader)
if len(sys.argv)>3:
  imgstartaddress = int(sys.argv[3],16)
else:
  imgstartaddress=0

def moveBytes():
  nmax = len(lastReadBytes)-1
  for i in range(0,nmax):
    lastReadBytes[i] = lastReadBytes[i+1]

try:
  with open(sys.argv[1],"rb") as image:
    image.read(imgstartaddress)
    byte = image.read(1)
    bytecount = imgstartaddress + 1
    while byte != b'':
      moveBytes()
      lastReadBytes[len(lastReadBytes)-1] = ord(byte)
      #print lastReadBytes, jpgheader
      # new image conditions:
      # 1. not already in image
      # 2. header matches with last read bytes
      #if not inJpg and (jpgheader[count] == ord(byte)):
      if not inJpg and lastReadBytes==jpgheader:
        #count = count + 1
        #if( count == len(jpgheader)-1):
        inJpg = True
        wasInJpg = False
        imageCount = imageCount + 1
        #if imageCount > 60:
        #  exit(0)
        count = 0
      elif inJpg:
        pass
      else:
        count = 0
          
      if inJpg:
        if not wasInJpg:
          currentImageSize = 0
          pic = io.open(os.path.join(sys.argv[2], "image_"+hex(int(bytecount))+".jpg"), 'wb')
          imgstartaddress=bytecount-2
          for bt in jpgheader[:len(jpgheader)-1]:
            pic.write(bt.to_bytes(1))
          wasInJpg = True
          count = 0
          pic.write(bytes(byte))
          byte = image.read(2)
          bytecount +=2
          pic.write(bytes(byte))
          byte = image.read(2)
          bytecount +=2
          pic.write(bytes(byte))
          bytecount += (byte[0]<<8) + byte[1]
          byte = image.read((byte[0]<<8) + byte[1])
          pic.write(bytes(byte))
          byte = image.read(1)
          bytecount +=2
          
        pic.write(bytes(byte))

        #current image too big?
        if (bytecount - imgstartaddress) > 1024 * 1024 * 6:
          # print("panic; image too big at " , hex(int(imgstartaddress)))
          # raise KeyboardInterrupt
          pic.close()
          wasInJpg = False
          inJpg = False
          inThumb = False
          count = 0
          time.sleep(0.1)

        if not inThumb and lastReadBytes==jpgheader:
          inThumb = True
          # print("have thumb")
        if ord(byte) == jpgfooter[count]:
          #print count, "in footer"
          count += 1
          if count == 2:
            if inThumb:
              # print("ended thumb")
              inThumb = False
              count = 0
            else:
              print(chr(27) + "[2J")
              print ("did: " , str((bytecount/filesize)*100) + "%")
              print ("found ", imageCount, " images so far.")
              pic.close()
              wasInJpg = False
              inJpg = False
              count = 0
              time.sleep(0.1)
        else:
          count = 0
      byte = image.read(1)
      bytecount +=1
      if int(bytecount) % 10000000 == 0:
        print(chr(27) + "[2J")
        print ("did: " , str((bytecount/filesize)*100) + "%")
        print ("found ", imageCount, " images so far.")
except KeyboardInterrupt:
  print ("aborting...")
  print ("currently at: ", hex(int(bytecount)))
  print ("found image: ", inJpg)
  print ("last image startaddress: ", hex(int(imgstartaddress)))
  exit(0)
   