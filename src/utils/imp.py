import sys

def imp(path):
    sys.path.append(path + 'gdx.jar')
    sys.path.append(path + 'gdx-backend-lwjgl.jar')
    sys.path.append(path + 'gdx-backend-lwjgl-natives.jar')
    sys.path.append(path + 'gdx-sources.jar')
    sys.path.append(path + 'lwjgl-natives.jar')
    sys.path.append(path + 'gdx-natives.jar')

def imp2d(path):
    imp(path)
    sys.path.append(path + 'gdx-box2d.jar')
    sys.path.append(path + 'gdx-box2d-natives.jar')

import math

def frange(limit1, limit2 = None, increment = 1.):
  """
  Range function that accepts floats (and integers).

  Usage:
  frange(-2, 2, 0.1)
  frange(10)
  frange(10, increment = 0.5)

  The returned value is an iterator.  Use list(frange) for a list.
  """

  if limit2 is None:
    limit2, limit1 = limit1, 0.
  else:
    limit1 = float(limit1)

  count = int(math.ceil(limit2 - limit1)/increment)
  return (limit1 + n*increment for n in range(count))

def dump(obj):
    print dir(obj)
    for attr in dir(obj):
        print "obj.%s = %s" % (attr, getattr(obj, attr))
