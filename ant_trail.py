class AntTrail:
    def __init__(self, capacity):
        self.capacity = capacity
        self.q = [None] * capacity
        self.head = 0


    def __str__(self):
        s = ""
        for p in self.q[self.head-1::-1] + self.q[:self.head-1:-1]:
            s += str(p) + " - "
        return s[:-3]


    def add(self, data):
        self.q[self.head] = data
        self.head += 1
        if self.head == self.capacity:
            self.head = 0


    def get(self):
        return self.q[self.head-1::-1] + self.q[:self.head-1:-1]

    def get_last_pos(self):
        return self.q[self.head-2]


    def clear(self):
        self.q = [None] * self.capacity
        self.head = 0
