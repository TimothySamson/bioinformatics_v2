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
        if permutation[i] == i+1:
            continue
        permutation.reverse_to_front(i+1)
        yield str(permutation)
        if permutation.list[i] < 0:
            permutation.list[i] *= -1
            yield str(permutation)


# with open("dataset_286_4 (1).txt") as file, open("GreedySorting.txt") as ans, open("output.txt", "w") as scratch:
#     numlist = [int(x) for x in file.readline().strip().split(" ")]
#     for output, answer in zip(GreedyReversal(numlist), ans.readlines()):
#         answer = answer.strip()
#         print(output, file=scratch)

# with open("dataset_286_4.txt") as file, open("output.txt", "w") as output:
#     numlist = [int(x) for x in file.readline().strip().split(" ")]
#     a = Permutation(numlist)
#
#     for line in GreedyReversal(numlist):
#         print(line, file=output)

a = [int(x) for x in "+2 +6 -8 -17 +7 -14 +18 +3 -5 -16 -11 -19 -4 +10 +13 -20 -1 +9 -12 +15".split()]
for i, line in enumerate(GreedyReversal(a)):
    print(i, line)

b = [int(x) for x in "+6 -12 -9 +17 +18 -4 +5 -3 +11 +19 +20 +10 +8 +15 -14 -13 +2 +7 -16 -1".split()]
print(len(list(Permutation(b).breakpoints())))
