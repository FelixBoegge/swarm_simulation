class CircularQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.q = [0] * capacity
        self.head = 0


    def add(self, data):
        self.q[self.head] = data
        self.head += 1
        if self.head == self.capacity:
            self.head = 0


    def get_circular_queue(self):
        pass