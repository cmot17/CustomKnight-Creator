#This was used to create duplicatedata.json. It's not actually used at runtime.

from PIL import Image
from pathlib import Path
#import imagehash
import os, os.path
import json
#from PIL import ImageChops

basepath = "C:/path/to/your/sprites"
info = []
images = []
hashes = []
for file in Path(basepath).rglob("SpriteInfo.json"):
    info.append(str(file))
print("start")
dataArray = []
for file in info:
    io = open(file, "r")
    data = json.load(io)
    dataArray.append(data)
spriteXR = []
spriteYR = []
spriteW = []
spriteH = []
spriteFlipped = []
spritePath = []
for data in dataArray:
    spriteXR += data["sxr"]
    spriteYR += data["syr"]
    spriteW += data["swidth"]
    spriteH += data["sheight"]
    spriteFlipped += data["sfilpped"]
    spritePath += data["spath"]
hashDict = {}
for i in range(0, len(spritePath)):
    im = Image.open(basepath + "/" + spritePath[i])
    im = im.crop(
        (
            spriteXR[i],
            im.size[1] - spriteYR[i] - spriteH[i],
            spriteXR[i] + spriteW[i],
            im.size[1] - spriteYR[i],
        )
    )
    hashValue = hash(tuple(map(tuple, im.getdata())))
    if hashValue in hashDict:
        hashDict[hashValue].append(spritePath[i])
    else:
        hashDict[hashValue] = [spritePath[i]]
for k, v in hashDict.items():
    hashDict[k] = list(v)
outputfile = open("duplicatedata.json", "w")
outputfile.write(json.dumps(hashDict))
outputfile.close()
out = Image.new("RGBA", (1000, 50000), (0, 0, 0, 0))
xpos = 0
ypos = 0
for hash in hashDict:
    xpos = 0
    for path in hashDict[hash]:
        i = spritePath.index(path)
        print(xpos)
        im = Image.open(basepath + "/" + path)
        im = im.crop(
            (
                spriteXR[i],
                im.size[1] - spriteYR[i] - spriteH[i],
                spriteXR[i] + spriteW[i],
                im.size[1] - spriteYR[i],
            )
        )
        out.paste(im, (xpos, ypos))
        xpos += im.width
    yheighttest = Image.open(basepath + "/" + hashDict[hash][0])
    ypos += yheighttest.height
out.save(basepath + "/output.png")
