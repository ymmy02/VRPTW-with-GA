import time

class Timer(object):

    def __init__(self):
        Timer.stttime = {}
        Timer.ttltime = {}
        Timer.checkpoint = {}

    @staticmethod
    def start(key):
        Timer.checkpoint[key] = {}
        Timer.stttime[key] = time.time()

    @staticmethod
    def end(key):
        Timer.ttltime[key] = time.time() - Timer.stttime[key]

    @staticmethod
    def check(key, subkey):
        Timer.checkpoint[key][subkey] = time.time()

    @staticmethod
    def write(path=""):
        if len(path) != 0:
            path = path + "/"

        f = open(path + "time.txt", 'w')
        f.write("*" * 50 + "\n")
        f.write(" Calculation Time\n")
        f.write("*" * 50 + "\n")

        for key, value in Timer.ttltime.items():
            f.write(key + "\n")
            f.write("Total Time : " + "{:.5f}".format(value) + " [sec]\n")
            f.write("-" * 50 + "\n")
            tmp = Timer.stttime[key]
            for subkey, checkpoint in Timer.checkpoint[key].items():
                second = checkpoint - tmp
                parcentage = second / value
                f.write(subkey + " : " + "{:.5f}".format(second) + " [sec]" + "{:.2%}".format(parcentage)+ " [%]\n")
                tmp = checkpoint
            f.write("*" * 50 + "\n")

        f.close()
