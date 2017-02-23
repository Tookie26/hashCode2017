import struct
import sys
from copy import copy

class SFrameImport(object):
    def __init__(self, dataset):
        with open(dataset, "r") as file:
            lines = file.readlines()
            str = lines[0].split(' ')
            self.nb_videos = int(str[0])
            self.nb_endpoints = int(str[1])
            self.nb_requests = int(str[2])
            self.nb_caches = int(str[3])
            self.cache_size = int(str[4])
            self.videos = []
            self.endpoints = []

            str = lines[1].split(' ')
            for size in str:
                self.videos.append({ "size": int(size), "requests": [] })
            i = 2
            nb_endpoints = self.nb_endpoints
            while (i < len(lines) and nb_endpoints > 0):
                str = lines[i].split(' ')
                self.endpoints.append({ "dc_latency": int(str[0]), "caches": [] })
                nb_caches = int(str[1])
                i += 1
                while (nb_caches > 0):
                    str = lines[i].split(' ')
                    self.endpoints[len(self.endpoints) - 1]["caches"].append({ "id": int(str[0]), "latency": int(str[1]) })
                    nb_caches -= 1
                    i += 1
                nb_endpoints -= 1
            while (i < len(lines)):
                str = lines[i].split(' ')
                self.videos[int(str[0])]["requests"].append({ "endpoint": int(str[1]), "amount": int(str[2]) })
                i += 1

    def format(self):
        file = []
        names = [ "size", "dc_latency" ]
        #row: size, data center latency, cache 0 latency, ... , cache n latency, video 0 amount requests, ... , video n amount requests
        for i in range(0, self.nb_endpoints):
            row = [ str(i), str(self.endpoints[i]["dc_latency"]) ]
            for j in range(0, self.nb_caches):
                names.append("cache_" + str(j))
                cache = [x for x in self.endpoints[i]["caches"] if x["id"] == j]
                row.append(struct.Struct('i').size if len(cache) == 0 else cache[0]["latency"])
            for n in range(0, self.nb_videos):
                names.append("video_" + str(n))
                req = [ x for x in self.videos[n]["requests"] if x["endpoint"] == i]
                row.append(0 if len(req) == 0 else req[0]["amount"])
            file.append(copy(row))
        with open("output.csv", "w+") as output:
            for i in range(0, len(names)):
                if i < len(names) - 1:
                    output.write(names[i] + ",")
                else:
                    output.write(names[i] + "\n")
            for row in file:
                for i in range(0, len(row)):
                    if i < len(row) - 1:
                        output.write(str(row[i]) + ",")
                    else:
                        output.write(str(row[i]) + "\n")

def main():
    print(sys.argv)
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: python assignment_1.py dataset\n")
        return 1
    sframe = SFrameImport(sys.argv[1])
    sframe.format()
    return 0

if __name__ == '__main__':
    main()