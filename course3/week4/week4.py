class Permutation:
    def __init__(self, list):
        self.list = list

    def __str__(self):
        return " ".join([f"+{x}" if x > 0 else str(x) for x in self.list])

    def __len__(self):
        return len(self.list)

    def __getitem__(self, item):
        return self.list[item]

    def reversal(self, left, right):
        self.list[left:right + 1] = [-x for x in self.list[left:right+1][::-1]]

    def reverse_to_front(self, num):
        right = [abs(x) for x in self.list].index(num)
        self.reversal(num-1, right)

    def breakpoints(self):
        prev = 0
        for i, curr in enumerate(self.list):
            curr = self.list[i]
            if prev != curr - 1:
                yield i

            prev = curr

        if self[-1] != len(self):
            yield len(self)

def GreedyReversal(list):
    permutation = Permutation(list)
    for i in range(len(list)):
        permutation.reverse_to_front(i+1)
        print(permutation)
        if permutation.list[i] < 0:
            permutation.list[i] *= -1
            print(permutation)


with open("dataset_287_6.txt") as file:
    numlist = [int(x) for x in file.readline().strip().split(" ")]
    a = Permutation(numlist)


    print(len(list(a.breakpoints())))

