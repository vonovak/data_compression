import sched, time, os, sys

def callback(sc, impath, nbr): 
    print "Doing stuff..."
    temps = []
    for f in os.listdir(impath):
        if not os.path.isfile(os.path.join(impath, f)):
            continue
        os.rename(os.path.join(impath, f), os.path.join(impath, "temp" + f))
        temps.append("temp" + f)
    depthimages = os.path.join(impath, "tempdepth_%06d.png")
    rgbimages = os.path.join(impath, "temprgb_%06d.png")
    avconv = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "libav", "bin", "avconv")) # absolute path on others as well?
    os.system("%s -r 30 -i %s -pix_fmt gray16 -vsync 1 -vcodec ffv1 -coder 1 video%d.mov" % (avconv, depthimages, nbr))
    nbr += 1
    #os.system("../libav/bin/avconv -r 30 -i (IMAGE_FOLDER)/temprgb%06d.tiff -pix_fmt gray16 -vsync 1 -vcodec ffv1 -coder 1 video.mov")
    # avconv -f x11grab -r 15 -s 1366x768 -i :0.0 -c:v libx264 -preset ultrafast -crf 0 test.mkv
    #for f in temps:
        #os.remove(os.path.join(impath, f))
    #sc.enter(5, 1, callback, (sc, impath, nbr)) # possible to schedule it for later irrespective of how long this takes??
# do your stuff

def main(argv):
    s = sched.scheduler(time.time, time.sleep)
    nbr = 0
    s.enter(5, 1, callback, (s, argv, nbr))
    s.run()

if __name__ == "__main__":
    main(sys.argv[1])