import sys

class Person:
  def __init__(self, name, born, died):
    self.name = name
    self.born = born
    self.died = died
  def greet( self ):
    print( "hello " + self.name )

 #p = Person( "you")
 #p.greet()

class Print:
  def __init__(self, edition, print_id, partiture):
    self.edition = edition
    self.print_id = print_id
    self.partiture = partiture
  def format(self):
    #TODO

class Voice:
  def __init__(self, name, range):
    self.name = name
    self.range = range

class Edition:
  def __init__(self, composition, authors, name):
    self.composition = composition
    self.authors = authors
    self.name = name

class Composition:
  def __init__(self, name, incipit, key, genre, year, voices, authors):
    self.name = name
    self.incipit = incipit
    self.key = key
    self.genre = genre
    self.year = year
    self.voices = voices
    self.authors = authors

def load(filename):
  #TODO
