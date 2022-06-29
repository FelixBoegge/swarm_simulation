class AntTrail:
    def __init__(self, capacity):
        self.capacity = capacity
        self.q = [None] * capacity
        self.head = 0


    def add(self, data):
        self.q[self.head] = data
        self.head += 1
        if self.head == self.capacity:
            self.head = 0


    def get_trail(self):
        return self.q[self.head-1:] + self.q[:self.head-1]