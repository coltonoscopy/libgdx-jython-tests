import sys

def imp(path):
    sys.path.append(path + 'gdx.jar')
    sys.path.append(path + 'gdx-backend-lwjgl.jar')
    sys.path.append(path + 'gdx-backend-lwjgl-natives.jar')
    sys.path.append(path + 'gdx-sources.jar')
    sys.path.append(path + 'lwjgl-natives.jar')
    sys.path.append(path + 'gdx-natives.jar')
