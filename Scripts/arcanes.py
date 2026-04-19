'''Module to handle arcanes'''


class Arcane():
    '''Create arcane obj'''

    def __init__(self, name, rank=0, qty=0):
        self.name = name
        self.rank = rank
        self.qty = qty

    def convert_to_rank0(self):
        '''convert qty to match rank 0'''
        if self.rank > 0 and self.rank < 7:
            match self.rank:
                case 1:
                    self.qty = 3
                case 2:
                    self.qty = 6
                case 3:
                    self.qty = 10
                case 4:
                    self.qty = 15
                case 5:
                    self.qty = 21
            self.rank = 0
            print(self.rank, self.qty)

    def convert_to_rank1(self):
        '''convert qty to match rank 1'''
        if self.rank == 0 or (self.rank > 1 and self.rank < 7):
            isconverted = False
            match self.rank:
                case 0:
                    if self.qty == 3:
                        self.qty = 0
                        isconverted = True
                case 2:
                    self.qty = 0
                case 3:
                    self.qty = 0
                case 4:
                    self.qty = 0
                case 5:
                    self.qty = 0
            if isconverted:
                self.rank = 1

            print(self.rank, self.qty)
