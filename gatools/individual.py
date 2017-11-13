class Individual(object):
  
  def __init__(self, chromosome):
    self.chromosome = chromosome
    self.distance = None
    self.fitness = None

  def __eq__(self, other):
    if other is None or type(self) != type(other): return False
    return self.chromosome == other.chromosome

  def __ne__(self, other):
    return not self.__eq__(other)

  def get_nvehicle(self):
    nvehicle = len(self.chromosome)
    return nvehicle
