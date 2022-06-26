"""
Handles sprite data, packing, and deduplication.
"""

import copy
import json
import math
import os
import os.path
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

from PIL import Image

# from PyQt6.QtWidgets import


@dataclass
class Sprite:
    sprite_id: int
    pos: NamedTuple
    pos_r: NamedTuple
    size: NamedTuple
    flipped: bool
    path: Path
    collection: str


class SpriteHandler:
    dataArray: list[dict[str, list[str]]] = []
    categories: dict[str, bool] = {}
    animationsList: list[str] = []
    basepath = ""
    savedOutputFolder = ""

    sprites: list[Sprite] = []

    spriteIDs: list[int] = []
    spriteX: list[int] = []
    spriteY: list[int] = []
    spriteXR: list[int] = []
    spriteYR: list[int] = []
    spriteW: list[int] = []
    spriteH: list[int] = []
    spriteFlipped: list[bool] = []
    spritePath: list[str] = []
    spriteCollection: list[str] = []

    duplicatesHashList: list[str] = []
    duplicatesList: list[list[str]] = []

    @staticmethod
    def load_sprite_info(files: list[str]) -> list[str]:
        categories: list[str] = []
        SpriteHandler.dataArray = []
        for file in files:
            data = json.load(open(file, "r", encoding="utf-8"))
            SpriteHandler.dataArray.append(data)
            sprite_collection_list = list(
                dict.fromkeys(data["scollectionname"])
            )  # remove duplicates
            categories += sprite_collection_list

        final_categories = list(dict.fromkeys(categories))  # remove duplicates
        # print(finalCategories)
        SpriteHandler.categories.clear()
        for category in final_categories:
            SpriteHandler.categories[category] = True
        return final_categories

    @staticmethod
    def load_animations(filter_str: str) -> list[str]:
        SpriteHandler.spriteIDs.clear()
        SpriteHandler.spriteX.clear()
        SpriteHandler.spriteY.clear()
        SpriteHandler.spriteXR.clear()
        SpriteHandler.spriteYR.clear()
        SpriteHandler.spriteW.clear()
        SpriteHandler.spriteH.clear()
        SpriteHandler.spriteFlipped.clear()
        SpriteHandler.spritePath.clear()
        SpriteHandler.spriteCollection.clear()

        for data in SpriteHandler.dataArray:
            SpriteHandler.spriteIDs += [int(x) for x in data["sid"]]
            SpriteHandler.spriteX += [int(x) for x in data["sx"]]
            SpriteHandler.spriteY += [int(x) for x in data["sy"]]
            SpriteHandler.spriteXR += [int(x) for x in data["sxr"]]
            SpriteHandler.spriteYR += [int(x) for x in data["syr"]]
            SpriteHandler.spriteW += [int(x) for x in data["swidth"]]
            SpriteHandler.spriteH += [int(x) for x in data["sheight"]]
            SpriteHandler.spriteFlipped += [
                bool(x) for x in data["sfilpped"]
            ]  # there is a type in the exported json files
            SpriteHandler.spritePath += data["spath"]
            SpriteHandler.spriteCollection += data["scollectionname"]
        for i in reversed(range(0, len(SpriteHandler.spriteCollection))):
            if (not SpriteHandler.categories[SpriteHandler.spriteCollection[i]]) or (
                str.casefold(filter_str)
                not in str.casefold(SpriteHandler.spritePath[i])
            ):
                del SpriteHandler.spriteIDs[i]
                del SpriteHandler.spriteX[i]
                del SpriteHandler.spriteY[i]
                del SpriteHandler.spriteXR[i]
                del SpriteHandler.spriteYR[i]
                del SpriteHandler.spriteW[i]
                del SpriteHandler.spriteH[i]
                del SpriteHandler.spriteFlipped[i]
                del SpriteHandler.spritePath[i]
                del SpriteHandler.spriteCollection[i]
        animations = []
        for path in SpriteHandler.spritePath:
            if os.path.basename(os.path.dirname(path)) not in animations:
                animations.append(os.path.basename(os.path.dirname(path)))
        SpriteHandler.animationsList = copy.copy(animations)
        return animations

    @staticmethod
    def load_sprites(animation: str) -> list[str]:
        sprites = []
        for path in SpriteHandler.spritePath:
            if os.path.basename(os.path.dirname(path)) == animation:
                sprites.append(os.path.basename(path))
        return sprites

    @staticmethod
    def pack_sprites(output_dir: str) -> bool:
        sprite_collection_list = list(SpriteHandler.categories.keys())
        for category in enumerate(sprite_collection_list):
            if SpriteHandler.categories[category[1]]:
                max_width = 0
                max_height = 0
                # print(len(spriteCollectionList))
                # print(spriteCollectionList[j])
                for i in range(0, len(SpriteHandler.spriteIDs)):
                    # print(spriteHandler.spriteCollection[i])
                    # print(spriteCollectionList[j])
                    if SpriteHandler.spriteCollection[i] == category[1]:
                        if SpriteHandler.spriteFlipped[i]:
                            max_width = max(
                                max_width,
                                SpriteHandler.spriteX[i] + SpriteHandler.spriteH[i],
                            )
                            max_height = max(
                                max_height,
                                SpriteHandler.spriteY[i] + SpriteHandler.spriteW[i],
                            )
                            # print("flipped:")
                            # print(maxH)
                        else:
                            max_width = max(
                                max_width,
                                SpriteHandler.spriteX[i] + SpriteHandler.spriteW[i],
                            )
                            max_height = max(
                                max_height,
                                SpriteHandler.spriteY[i],
                            )
                            # print("not flipped:")
                            # print(maxH)
                # print(maxW)
                # print(maxH)
                max_width = 2 ** math.ceil(math.log2(max_width - 1))
                max_height = 2 ** math.ceil(math.log2(max_height - 1))
                # print(maxW)
                # print(maxH)

                out = Image.new("RGBA", (max_width, max_height), (0, 0, 0, 0))

                for i in range(0, len(SpriteHandler.spriteIDs)):
                    if SpriteHandler.spriteCollection[i] == category[1]:
                        image = Image.open(
                            SpriteHandler.basepath + "/" + SpriteHandler.spritePath[i]
                        )
                        image = image.crop(
                            (
                                SpriteHandler.spriteXR[i],
                                image.size[1]
                                - SpriteHandler.spriteYR[i]
                                - SpriteHandler.spriteH[i],
                                SpriteHandler.spriteXR[i] + SpriteHandler.spriteW[i],
                                image.size[1] - SpriteHandler.spriteYR[i],
                            )
                        )
                        if SpriteHandler.spriteFlipped[i]:
                            x_pos = SpriteHandler.spriteX[i]
                            y_pos = (
                                out.size[1]
                                - SpriteHandler.spriteY[i]
                                - SpriteHandler.spriteW[i]
                            )
                        else:
                            x_pos = SpriteHandler.spriteX[i]
                            y_pos = (
                                out.size[1]
                                - SpriteHandler.spriteY[i]
                                - SpriteHandler.spriteH[i]
                            )

                        if SpriteHandler.spriteFlipped[i]:
                            image = image.rotate(90, expand=True)
                            image = image.transpose(Image.FLIP_LEFT_RIGHT)

                        out.paste(image, (x_pos, y_pos))
                try:
                    out.save(output_dir + "/" + category[1] + ".png")
                except OSError:
                    return False
        return True

    @staticmethod
    def load_duplicates(animation: str) -> None:
        SpriteHandler.duplicatesHashList = []
        SpriteHandler.duplicatesList = []
        file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "resources/duplicatedata.json")
        )
        duplicates_dict = json.load(open(file_path, "r", encoding="utf-8"))
        key_list = list(duplicates_dict.keys())
        value_list = list(duplicates_dict.values())
        for path in SpriteHandler.spritePath:
            filtered_values = [x for x in value_list if path in x]
            # print(filtered_values)
            if len(filtered_values) != 0:
                group_of_duplicates = filtered_values[0]
                loaded_duplicates = [
                    x for x in group_of_duplicates if x in SpriteHandler.spritePath
                ]
                # #print(groupOfDuplicates)
                # #print(loadedDuplicates)
                if not loaded_duplicates in SpriteHandler.duplicatesList:
                    if len(loaded_duplicates) > 1:
                        if animation in path or animation == "":
                            SpriteHandler.duplicatesHashList.append(
                                key_list[value_list.index(group_of_duplicates)]
                            )
                            SpriteHandler.duplicatesList.append(loaded_duplicates)
        # print(spriteHandler.duplicatesList)

    @staticmethod
    def copy_main(main: str) -> None:
        # print(main)
        # print(spriteHandler.duplicatesList)
        group_of_duplicates = copy.deepcopy(
            [x for x in SpriteHandler.duplicatesList if main in x][0]
        )
        # print(groupOfDuplicates)
        group_of_duplicates.remove(main)
        main_index = SpriteHandler.spritePath.index(main)
        main_image = Image.open(SpriteHandler.basepath + "/" + main)
        main_image = main_image.crop(
            (
                SpriteHandler.spriteXR[main_index],
                main_image.size[1]
                - SpriteHandler.spriteYR[main_index]
                - SpriteHandler.spriteH[main_index],
                SpriteHandler.spriteXR[main_index] + SpriteHandler.spriteW[main_index],
                main_image.size[1] - SpriteHandler.spriteYR[main_index],
            )
        )
        for image in group_of_duplicates:
            duplicate_index = SpriteHandler.spritePath.index(image)
            duplicate_image = Image.open(SpriteHandler.basepath + "/" + image)
            duplicate_image.paste(
                main_image,
                (
                    SpriteHandler.spriteXR[duplicate_index],
                    duplicate_image.size[1]
                    - SpriteHandler.spriteYR[duplicate_index]
                    - SpriteHandler.spriteH[duplicate_index],
                ),
            )
            duplicate_image.save(SpriteHandler.basepath + "/" + image)

    @staticmethod
    def sort_by_hash(index: int, vanilla_hash: str) -> list[str]:
        # print(spriteHandler.duplicatesList[index])

        def sort_func(file: str) -> int:
            if file in SpriteHandler.spritePath:
                i = SpriteHandler.spritePath.index(file)
                image = Image.open(SpriteHandler.basepath + "/" + file)
                image = image.crop(
                    (
                        SpriteHandler.spriteXR[i],
                        image.size[1]
                        - SpriteHandler.spriteYR[i]
                        - SpriteHandler.spriteH[i],
                        SpriteHandler.spriteXR[i] + SpriteHandler.spriteW[i],
                        image.size[1] - SpriteHandler.spriteYR[i],
                    )
                )
                im_data = image.getdata()
                new_hash = hash(tuple(map(tuple, im_data)))
                # print(file)
                # print(type(newHash))
                # print(type(vanillaHash))
                if str(new_hash) == vanilla_hash:
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
        return sorted(SpriteHandler.duplicatesList[index], key=sort_func)

    @staticmethod
    def check_completion(duplicates: list[str], vanilla_hash: str) -> int:
        custom_hash = ""
        for sprite in duplicates:
            i = SpriteHandler.spritePath.index(sprite)
            image = Image.open(
                SpriteHandler.basepath + "/" + SpriteHandler.spritePath[i]
            )
            image = image.crop(
                (
                    SpriteHandler.spriteXR[i],
                    image.size[1]
                    - SpriteHandler.spriteYR[i]
                    - SpriteHandler.spriteH[i],
                    SpriteHandler.spriteXR[i] + SpriteHandler.spriteW[i],
                    image.size[1] - SpriteHandler.spriteYR[i],
                )
            )
            im_data = image.getdata()
            new_hash = hash(tuple(map(tuple, im_data)))
            # print(sprite)
            # print(type(newHash))
            # print(type(vanillaHash))
            if str(new_hash) == vanilla_hash:
                # print("equal")
                return 0
            else:
                if custom_hash == "":
                    custom_hash = str(new_hash)
                else:
                    if custom_hash != str(new_hash):
                        return 0
        return 1
