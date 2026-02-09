import json
import math
from PIL import Image
import os
import os.path
from PySide6.QtWidgets import *
import copy


class spriteHandler:
    dataArray = []
    categories = {}
    animationsList = []
    basepath = ""
    savedOutputFolder = ""

    spriteIDs = []
    spriteX = []
    spriteY = []
    spriteXR = []
    spriteYR = []
    spriteW = []
    spriteH = []
    spriteFlipped = []
    spritePath = []
    spriteCollection = []

    duplicatesHashList = []
    duplicatesList = []

    @staticmethod
    def loadSpriteInfo(files):
        categories = []
        spriteHandler.dataArray = []
        for file in files:
            io = open(file, "r")
            data = json.load(io)
            spriteHandler.dataArray.append(data)
            spriteCollectionList = []
            [
                spriteCollectionList.append(x)
                for x in data["scollectionname"]
                if x not in spriteCollectionList
            ]
            categories += spriteCollectionList

        finalCategories = []
        [finalCategories.append(x) for x in categories if x not in finalCategories]
        print("here")
        print(finalCategories)
        spriteHandler.categories.clear()
        for category in finalCategories:
            spriteHandler.categories[category] = True
        return finalCategories

    @staticmethod
    def loadAnimations(filter):
        spriteHandler.spriteIDs = []
        spriteHandler.spriteX = []
        spriteHandler.spriteY = []
        spriteHandler.spriteXR = []
        spriteHandler.spriteYR = []
        spriteHandler.spriteW = []
        spriteHandler.spriteH = []
        spriteHandler.spriteFlipped = []
        spriteHandler.spritePath = []
        spriteHandler.spriteCollection = []
        for data in spriteHandler.dataArray:
            spriteHandler.spriteIDs += data["sid"]
            spriteHandler.spriteX += data["sx"]
            spriteHandler.spriteY += data["sy"]
            spriteHandler.spriteXR += data["sxr"]
            spriteHandler.spriteYR += data["syr"]
            spriteHandler.spriteW += data["swidth"]
            spriteHandler.spriteH += data["sheight"]
            spriteHandler.spriteFlipped += data["sfilpped"]
            spriteHandler.spritePath += data["spath"]
            spriteHandler.spriteCollection += data["scollectionname"]
        for i in reversed(range(0, len(spriteHandler.spriteCollection))):
            if (not spriteHandler.categories[spriteHandler.spriteCollection[i]]) or (
                str.casefold(filter) not in str.casefold(spriteHandler.spritePath[i])
            ):
                del spriteHandler.spriteIDs[i]
                del spriteHandler.spriteX[i]
                del spriteHandler.spriteY[i]
                del spriteHandler.spriteXR[i]
                del spriteHandler.spriteYR[i]
                del spriteHandler.spriteW[i]
                del spriteHandler.spriteH[i]
                del spriteHandler.spriteFlipped[i]
                del spriteHandler.spritePath[i]
                del spriteHandler.spriteCollection[i]
        animations = []
        for path in spriteHandler.spritePath:
            if os.path.basename(os.path.dirname(path)) not in animations:
                animations.append(os.path.basename(os.path.dirname(path)))
        spriteHandler.animationsList = copy.copy(animations)
        return animations

    @staticmethod
    def loadSprites(animation):
        sprites = []
        for path in spriteHandler.spritePath:
            if os.path.basename(os.path.dirname(path)) == animation:
                sprites.append(os.path.basename(path))
        return sprites

    @staticmethod
    def packSprites(outputDir):
        spriteCollectionList = list(spriteHandler.categories.keys())
        for j in range(0, len(spriteCollectionList)):
            if spriteHandler.categories[spriteCollectionList[j]]:
                maxW = 0
                maxH = 0
                # print(len(spriteCollectionList))
                # print(spriteCollectionList[j])
                for i in range(0, len(spriteHandler.spriteIDs)):
                    # print(spriteHandler.spriteCollection[i])
                    # print(spriteCollectionList[j])
                    if spriteHandler.spriteCollection[i] == spriteCollectionList[j]:
                        if spriteHandler.spriteFlipped[i]:
                            maxW = max(
                                maxW,
                                spriteHandler.spriteX[i] + spriteHandler.spriteH[i],
                            )
                            maxH = max(
                                maxH,
                                spriteHandler.spriteY[i] + spriteHandler.spriteW[i],
                            )
                            # print("flipped:")
                            # print(maxH)
                        else:
                            maxW = max(
                                maxW,
                                spriteHandler.spriteX[i] + spriteHandler.spriteW[i],
                            )
                            maxH = max(
                                maxH,
                                spriteHandler.spriteY[i],
                            )
                            # print("not flipped:")
                            # print(maxH)
                # print(maxW)
                # print(maxH)
                if maxW <= 1:
                    maxW = 1
                else:
                    maxW = 2 ** math.ceil(math.log2(maxW - 1))
                if maxH <= 1:
                    maxH = 1
                else:
                    maxH = 2 ** math.ceil(math.log2(maxH - 1))
                # print(maxW)
                # print(maxH)

                out = Image.new("RGBA", (maxW, maxH), (0, 0, 0, 0))

                for i in range(0, len(spriteHandler.spriteIDs)):
                    if spriteHandler.spriteCollection[i] == spriteCollectionList[j]:
                        im = Image.open(
                            spriteHandler.basepath + "/" + spriteHandler.spritePath[i]
                        )
                        im = im.crop(
                            (
                                spriteHandler.spriteXR[i],
                                im.size[1]
                                - spriteHandler.spriteYR[i]
                                - spriteHandler.spriteH[i],
                                spriteHandler.spriteXR[i] + spriteHandler.spriteW[i],
                                im.size[1] - spriteHandler.spriteYR[i],
                            )
                        )
                        if spriteHandler.spriteFlipped[i] == True:
                            x = spriteHandler.spriteX[i]
                            y = (
                                out.size[1]
                                - spriteHandler.spriteY[i]
                                - spriteHandler.spriteW[i]
                            )
                        else:
                            x = spriteHandler.spriteX[i]
                            y = (
                                out.size[1]
                                - spriteHandler.spriteY[i]
                                - spriteHandler.spriteH[i]
                            )

                        if spriteHandler.spriteFlipped[i]:
                            im = im.rotate(90, expand=True)
                            im = im.transpose(Image.FLIP_LEFT_RIGHT)

                        out.paste(im, (x, y))
                try:
                    out.save(outputDir + "/" + spriteCollectionList[j] + ".png")
                except OSError:
                    return False

    @staticmethod
    def loadDuplicates(animation):
        spriteHandler.duplicatesHashList = []
        spriteHandler.duplicatesList = []
        filePath = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "resources/duplicatedata.json")
        )
        duplicatesDict = json.load(open(filePath, "r"))
        keyList = list(duplicatesDict.keys())
        valueList = list(duplicatesDict.values())
        for path in spriteHandler.spritePath:
            filteredValues = [x for x in valueList if path in x]
            # print(filteredValues)
            if len(filteredValues) != 0:
                groupOfDuplicates = filteredValues[0]
                loadedDuplicates = [
                    x for x in groupOfDuplicates if x in spriteHandler.spritePath
                ]
                # #print(groupOfDuplicates)
                # #print(loadedDuplicates)
                if not loadedDuplicates in spriteHandler.duplicatesList:
                    if len(loadedDuplicates) > 1:
                        if animation in path or animation == "":
                            spriteHandler.duplicatesHashList.append(
                                keyList[valueList.index(groupOfDuplicates)]
                            )
                            spriteHandler.duplicatesList.append(loadedDuplicates)
        # print(spriteHandler.duplicatesList)

    @staticmethod
    def copyMain(main):
        # print(main)
        # print(spriteHandler.duplicatesList)
        groupOfDuplicates = copy.deepcopy(
            [x for x in spriteHandler.duplicatesList if main in x][0]
        )
        # print(groupOfDuplicates)
        groupOfDuplicates.remove(main)
        mainIndex = spriteHandler.spritePath.index(main)
        mainImage = Image.open(spriteHandler.basepath + "/" + main)
        mainImage = mainImage.crop(
            (
                spriteHandler.spriteXR[mainIndex],
                mainImage.size[1]
                - spriteHandler.spriteYR[mainIndex]
                - spriteHandler.spriteH[mainIndex],
                spriteHandler.spriteXR[mainIndex] + spriteHandler.spriteW[mainIndex],
                mainImage.size[1] - spriteHandler.spriteYR[mainIndex],
            )
        )
        for image in groupOfDuplicates:
            duplicateIndex = spriteHandler.spritePath.index(image)
            duplicateImage = Image.open(spriteHandler.basepath + "/" + image)
            duplicateImage.paste(
                mainImage,
                (
                    spriteHandler.spriteXR[duplicateIndex],
                    duplicateImage.size[1]
                    - spriteHandler.spriteYR[duplicateIndex]
                    - spriteHandler.spriteH[duplicateIndex],
                ),
            )
            duplicateImage.save(spriteHandler.basepath + "/" + image)

    @staticmethod
    def sortByHash(index, vanillaHash):
        # print(spriteHandler.duplicatesList[index])

        def sortFunc(file):
            if file in spriteHandler.spritePath:
                i = spriteHandler.spritePath.index(file)
                im = Image.open(
                    spriteHandler.basepath + "/" + spriteHandler.spritePath[i]
                )
                im = im.crop(
                    (
                        spriteHandler.spriteXR[i],
                        im.size[1]
                        - spriteHandler.spriteYR[i]
                        - spriteHandler.spriteH[i],
                        spriteHandler.spriteXR[i] + spriteHandler.spriteW[i],
                        im.size[1] - spriteHandler.spriteYR[i],
                    )
                )
                imData = im.getdata()
                newHash = hash(tuple(map(tuple, imData)))
                # print(file)
                # print(type(newHash))
                # print(type(vanillaHash))
                if str(newHash) == vanillaHash:
                    # print("equal")
                    return 1
                else:
                    # print("not equal")
                    return 0
            else:
                return 2

        # print("sorted list")
        # print(sorted(spriteHandler.duplicatesList[index], key=sortFunc))
        # print("done sort")
        return sorted(spriteHandler.duplicatesList[index], key=sortFunc)

    @staticmethod
    def checkCompletion(duplicates, vanillaHash):
        customHash = ""
        for sprite in duplicates:
            i = spriteHandler.spritePath.index(sprite)
            im = Image.open(spriteHandler.basepath + "/" + spriteHandler.spritePath[i])
            im = im.crop(
                (
                    spriteHandler.spriteXR[i],
                    im.size[1] - spriteHandler.spriteYR[i] - spriteHandler.spriteH[i],
                    spriteHandler.spriteXR[i] + spriteHandler.spriteW[i],
                    im.size[1] - spriteHandler.spriteYR[i],
                )
            )
            imData = im.getdata()
            newHash = hash(tuple(map(tuple, imData)))
            # print(sprite)
            # print(type(newHash))
            # print(type(vanillaHash))
            if str(newHash) == vanillaHash:
                # print("equal")
                return 0
            else:
                if customHash == "":
                    customHash = str(newHash)
                else:
                    if customHash != str(newHash):
                        return 0
        return 1
