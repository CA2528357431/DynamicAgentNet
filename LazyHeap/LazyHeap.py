import heapq


class LazyHeap:
    def __init__(self, k):
        self.dic = {}
        self.heap = []
        self.topk = set()
        self.k = k

    def push(self, item):
        if item not in self.dic:
            self.dic[item] = 0
        self.dic[item] += 1
        heapq.heappush(self.heap, (self.dic[item], item))
        self.topk.add(item)
        to_delete = None
        while len(self.topk) > self.k:
            fre, item = heapq.heappop(self.heap)
            if fre == self.dic[item]:
                self.topk.remove(item)

        return to_delete

    def clean(self):
        neo_heap = []
        for fre, item in self.heap:
            if self.dic[item] != fre:
                continue
            heapq.heappush(neo_heap, (fre, item))
        self.heap = neo_heap


if __name__ == '__main__':
    lz = LazyHeap(3)
    sequence = [1,2,3,3,4,4,1,5,5,2,2,1,2,3,4,1,1,1,3,4,4,2,1,2,3,4,5,4,2,1,1,3,4]
    sequence = [str(x) for x in sequence]

    count = {}
    for x in sequence:
        lz.push(x)

        if x not in count:
            count[x] = 0
        count[x] += 1
        keys = [k for k in count]
        keys.sort(key = lambda x: -count[x])
        if len(keys)>3:
            keys = [k for k in keys if count[keys[2]]<=count[k]]
            keys.sort(key = lambda x: -count[x])
        # old NNlogN*K
        # ours Nlog(max(N,K))


        print()
        print("ground truth:",keys)
        print("Lazy Heap output:",lz.topk)
        #