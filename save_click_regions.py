import pyautogui as mc
import os
import scipy.io as io
import time
import sys

def collect_click_regions(timeDelay = 5):

    print('Move mouse to x input (you have ' + str(timeDelay) + ' seconds)')  # Getting the x input coordinates
    for i in range(timeDelay, 0, -1):
        sys.stdout.write(str(i)+' ')
        sys.stdout.flush()
        time.sleep(1)
    xInput = mc.position()
    xInputx = xInput.x
    xInputy = xInput.y
    print('\n')

    print('X input coordinates')
    print('X:' + '{0:5d}'.format(xInputx) + ', Y:' + '{0:5d}'.format(xInputy) + '\n')

    print('Move mouse to y input (you have ' + str(timeDelay) + ' seconds)')  # Getting the y input coordinates
    for i in range(timeDelay, 0, -1):
        sys.stdout.write(str(i)+' ')
        sys.stdout.flush()
        time.sleep(1)
    yInput = mc.position()
    yInputx = yInput.x
    yInputy = yInput.y
    print('\n')

    print('Y input coordinates')
    print('X:' + '{0:5d}'.format(yInputx) + ', Y:' + '{0:5d}'.format(yInputy) + '\n')

    print('Move mouse to Z input (you have ' + str(timeDelay) + ' seconds)')  # Getting the z input coordinates
    for i in range(timeDelay, 0, -1):
        sys.stdout.write(str(i)+' ')
        sys.stdout.flush()
        time.sleep(1)
    zInput = mc.position()
    zInputx = zInput.x
    zInputy = zInput.y
    print('\n')

    print('Z input coordinates')
    print('X:' + '{0:5d}'.format(zInputx) + ', Y:' + '{0:5d}'.format(zInputy) + '\n')

    print('Move mouse to Angle input (you have ' + str(timeDelay) + ' seconds)')  # Getting the Angle input coordinates
    for i in range(timeDelay, 0, -1):
        sys.stdout.write(str(i) + ' ')
        sys.stdout.flush()
        time.sleep(1)
    angInput = mc.position()
    angInputx = angInput.x
    angInputy = angInput.y
    print('\n')

    print('Angle input coordinates')
    print('X:' + '{0:5d}'.format(angInputx) + ', Y:' + '{0:5d}'.format(angInputy) + '\n')

    print('Move mouse to add button (you have ' + str(timeDelay) + ' seconds)')  # Getting the add button coordinates
    for i in range(timeDelay, 0, -1):
        sys.stdout.write(str(i)+' ')
        sys.stdout.flush()
        time.sleep(1)
    addInput = mc.position()
    addInputx = addInput.x
    addInputy = addInput.y
    print('\n')

    print('Add button coordinates')
    print('X:' + '{0:5d}'.format(addInputx) + ', Y:' + '{0:5d}'.format(addInputy) + '\n')

    print('Move mouse to Set Zf button (you have ' + str(timeDelay) + ' seconds)')  # Getting the add button coordinates
    for i in range(timeDelay, 0, -1):
        sys.stdout.write(str(i)+' ')
        sys.stdout.flush()
        time.sleep(1)
    zfInput = mc.position()
    zfInputx = zfInput.x
    zfInputy = zfInput.y
    print('\n')

    print('Set Zf button coordinates')
    print('X:' + '{0:5d}'.format(zfInputx) + ', Y:' + '{0:5d}'.format(zfInputy) + '\n')

    print('Move mouse to Set Zl button (you have ' + str(timeDelay) + ' seconds)')  # Getting the add button coordinates
    for i in range(timeDelay, 0, -1):
        sys.stdout.write(str(i) + ' ')
        sys.stdout.flush()
        time.sleep(1)
    zlInput = mc.position()
    zlInputx = zlInput.x
    zlInputy = zlInput.y
    print('\n')

    print('Set Zl button coordinates')
    print('X:' + '{0:5d}'.format(zlInputx) + ', Y:' + '{0:5d}'.format(zlInputy) + '\n')

    print('Move mouse to Remove All button (you have ' + str(timeDelay) + ' seconds)')  # Getting the Remove all button coordinates
    for i in range(timeDelay, 0, -1):
        sys.stdout.write(str(i) + ' ')
        sys.stdout.flush()
        time.sleep(1)
    raInput = mc.position()
    raInputx = raInput.x
    raInputy = raInput.y
    print('\n')

    print('Remove All button coordinates')
    print('X:' + '{0:5d}'.format(zlInputx) + ', Y:' + '{0:5d}'.format(zlInputy) + '\n')

    print('Move mouse to Start Experiment button (you have ' + str(
        timeDelay) + ' seconds)')  # Getting the Start Experiment button coordinates
    for i in range(timeDelay, 0, -1):
        sys.stdout.write(str(i) + ' ')
        sys.stdout.flush()
        time.sleep(1)
    sbInput = mc.position()
    sbInputx = sbInput.x
    sbInputy = sbInput.y
    print('\n')

    print('Remove All button coordinates')
    print('X:' + '{0:5d}'.format(zlInputx) + ', Y:' + '{0:5d}'.format(zlInputy) + '\n')

    # Create a dictionary that is necessary to pass the io.savemat function
    posDict = {'xPos':[xInputx, xInputy], 'yPos':[yInputx, yInputy], 'zPos':[zInputx, zInputy],
               'addPos':[addInputx, addInputy], 'zfPos':[zfInputx, zfInputy], 'zlPos':[zlInputx, zlInputy],
               'raPos':[raInputx, raInputy], 'angPos':[angInputx, angInputy], 'sbPos':[sbInputx, sbInputy]}

    if not (os.path.isdir("./mat")):  # Create a directory if it doesn't exist
        os.mkdir('./mat')
    io.savemat('./mat/screenPositions.mat', posDict)  # Save the .mat file that holds the screen positions for input
    return posDict


#     # Sequence
#     time.sleep(5)
#
#     mc.moveTo(xInputx, xInputy, 0.5)
#     mc.click(clicks=2)
#     mc.typewrite('963')
#
#     mc.moveTo(yInputx, yInputy, 0.1)
#     mc.click(clicks=2)
#     mc.typewrite('-98')
#
#     mc.moveTo(zInputx, zInputy, 0.1)
#     mc.click(clicks=2)
#     mc.typewrite('42')
#
#     mc.moveTo(addInputx, addInputy, 1)
#     mc.click(clicks=1)
#
# print('Length of arguments = ' + str(len(sys.argv)))

# if len(sys.argv) == 1:
#     collect_click_regions()
# elif len(sys.argv) == 2:
#     print(sys.argv[1])
#     collect_click_regions(timeDelay = int(sys.argv[1]))
