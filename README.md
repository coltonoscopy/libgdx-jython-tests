libgdx-jython-tests
===================

A port of the expansive libGDX test code to Jython, to help others interested in
experimenting with Jython for more serious game development.

### Status:

Handful of tests running; currently in the process of porting Box2D tests.

### Setup:

1. Install Jython (Homebrew for Mac OS X works as well):

    - http://www.jython.org/downloads.html

2. Obtain the libGDX JARs (nightly builds can be found here):

    - https://libgdx.badlogicgames.com/nightlies/

3. Set up libGDX JARs in a lib/ directory at the base of the installation.

4. Reference said libs by appending them to sys.path at the start of any test you would
like to run or create yourself! Examples include using a simple utility function.

5. Profit.
