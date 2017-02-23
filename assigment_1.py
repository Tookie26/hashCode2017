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
            self.videos_sizes = []
            self.endpoints = []

            str = lines[1].split(' ')
            for size in str:
                self.videos.append({ "size": int(size), "requests": [] })
            i = 2
            nb_endpoints = self.nb_endpoints
            while (i < len(lines)):
                str = lines[i].split(' ')
                self.endpoints.append({ "dc_latency": int(str[0]), "caches": [] })
                nb_caches = int(str[1])
                while (nb_caches > 0):
                    i += 1
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
        # row: size,
        for i in range(0, self.nb_endpoints):
            row = [ str(i), str(self.endpoints[i]["dc_latency"]) ]
            for j in range(0, self.nb_caches):
                cache = [x for x in self.endpoints[i]["caches"] if x["id"] == j]
                row.append(sys.maxint if len(cache) == 0 else cache["latency"])





def main():
    return 0

if '__name__' == 'main':
    main()