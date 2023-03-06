"""
texture_unifier.py
"""
_author_ = "Mirafiori Elia el.mirafiori@gmail.com"
_date_ = "2018-02-22"
_version_ = "01.01.01"

import bpy
import os
import time

boold = True

def images():
    """
    Returns every image used in the scene

    :return images: images in scene
    """
    images = []
    
    for image in bpy.data.images:
        images.append(image)

    return images


def material_from_image(image):
    """
    Recovers the material from the image

    :param image: image
    :return material: material
    """
    try:
        material = (bpy.data.textures[str(image.name)].users_material[0])

    except:
        return None

    return material


def select_objects(obj):
    """
    Selects the specified object

    :param obj: object
    """
    obj.select = True


def deselect_objects(obj):
    """
    Deselects the specified object

    :param obj: object
    """
    obj.select = False
    

def link(material):
    """
    Link all the selected objects to the active object

    :param material: object's material
    """
    bpy.ops.object.make_links_data(type = 'MATERIAL')
    
    
def rename(name):
    """
    Rename the imae's name

    :param name: name to rename
    :return string: name renamed
    """
    name = name.split(".")
    string = ""

    if len(name) > 2:
        for part in name[0:2]:
            string += part + "."

    
    return string[0:len(string) - 1]


def object_from_material(material):
    """
    Recovers the object from the material

    :param material: object's material
    :return obj: object
    """
    mat = material

    for obj in bpy.data.objects:
        for slot in obj.material_slots:
            if slot.material == mat:
               return obj
    

def scene_objects():
    """
    Returns every object used in the scene

    :return objects: object in scene
    """
    objects = []
    
    for obj in bpy.data.objects:
        objects.append(obj)
        
    return objects


def boold(message):
    """
    Write the step in the Toggle System Console and on a CSV file

    :param message: message (String)
    """
    print(message)

    log = open(str(bpy.path.abspath("//")) + "\\texture_unifier\\texture_unifier.log", "a")
    log.write(message)
    log.close()
        
if __name__ == "__main__":
    if not os.path.exists(str(bpy.path.abspath("//")) + "\\texture_unifier"):
        os.makedirs(str(bpy.path.abspath("//") + "\\texture_unifier"))

    boold(time.strftime("==========Started %d-%m-%y at %H:%M:%S==========\n"))
    boold("Searching images in scene\n")
    images = images()
    
    unity = {}

    boold("Matching the image's name\n")
    for image in images:
        if len(str(image).split(".")) == 2:
            unity[image] = []

    for image in images:
        if len(str(image).split(".")) > 2:
            for key in unity.keys():
                if image.filepath in key.filepath:
                    unity[key].append(image)

    boold("Main process in execution\n")
    bpy.ops.object.select_all(action='DESELECT')
    for base_image in unity:
        boold(str(base_image.name) + "\n")
        mat = material_from_image(base_image)
      
        for obj in bpy.data.objects:
            for slot in obj.material_slots:                
                if slot.material == mat:
                    select_objects(obj)
                    bpy.context.scene.objects.active = obj

                    for image in unity[base_image]:
                        material = material_from_image(image)
                        obj_to_be_selected = object_from_material(material)
                        
                        try:
                            select_objects(obj_to_be_selected)
                            
                        except:
                            pass
                        
                    link(obj)
                    bpy.ops.object.select_all(action='DESELECT')
                    
    boold("Done\n")
    boold(time.strftime("==========Ended %d-%m-%y at %H:%M:%S==========\n"))
