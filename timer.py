import time
import ut

class Timer(object):

    @staticmethod
    def init():
        Timer.stttime = {}
        Timer.ttltime = {}
        Timer.subttl = {}

    @staticmethod
    def start(key):
        if key not in Timer.ttltime:
            Timer.ttltime[key] = 0.0
            Timer.subttl[key] = {}
        Timer.stttime[key] = time.time()

    @staticmethod
    def end(key):
        Timer.ttltime[key] += time.time() - Timer.stttime[key]

    @staticmethod
    def check(key, subkey):
        if subkey not in Timer.subttl[key]:
            Timer.subttl[key][subkey] = 0.0
        Timer.subttl[key][subkey] += time.time() - Timer.stttime[key]

    @staticmethod
    def write(path="", suffix=None):
        if len(path) != 0:
            path = path + "/"
        filename = ut.add_suffix("time", suffix) + ".txt"

        f = open(path + filename, 'w')
        f.write("*" * 50 + "\n")
        f.write(" Calculation Time\n")
        f.write("*" * 50 + "\n")

        for key, ttl in Timer.ttltime.items():
            f.write(key + "\n")
            f.write("Total Time : " + "{:.5f}".format(ttl) + " [sec]\n")
            f.write("-" * 50 + "\n")
            tmp = 0.0
            for subkey, subttl in Timer.subttl[key].items():
                second = subttl - tmp
                parcentage = second / ttl
                f.write(subkey + " : " + "{:.5f}".format(second) + " [sec] " + "{:.2%}".format(parcentage) + "\n")
                tmp = subttl
            f.write("*" * 50 + "\n")

        f.close()
