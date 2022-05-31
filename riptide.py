from pystyle import *

from py_compile import compile
from os import listdir, remove, mkdir, chdir
from os.path import isdir, isfile
from shutil import rmtree, copy
from subprocess import check_output

from etc.pyinstxtractor import extract



banner = """
           ▄████████  ▄█     ▄███████▄     ███      ▄█  ████████▄     ▄████████
          ███    ███ ███    ███    ███ ▀█████████▄ ███  ███   ▀███   ███    ███
          ███    ███ ███▌   ███    ███    ▀███▀▀██ ███▌ ███    ███   ███    █▀ 
         ▄███▄▄▄▄██▀ ███▌   ███    ███     ███   ▀ ███▌ ███    ███  ▄███▄▄▄    
        ▀▀███▀▀▀▀▀   ███▌ ▀█████████▀      ███     ███▌ ███    ███ ▀▀███▀▀▀    
        ▀███████████ ███    ███            ███     ███  ███    ███   ███    █▄ 
          ███    ███ ███    ███            ███     ███  ███   ▄███   ███    ███
          ███    ███ █▀    ▄████▀         ▄████▀   █▀   ████████▀    ██████████
          ███    ███"""[1:]



banner = Colorate.Vertical(Colors.DynamicMIX((Col.light_blue, Col.cyan)), Center.XCenter(banner))



class Riptide:

  def __init__(self, path: str):
    stage("Starting extraction...")
    if isdir('extracted'):
      rmtree('extracted')
    stage("Renewing 'extracted' directory...")
    mkdir('extracted')
    chdir('extracted')
    npath = path.split('\\')[-1]
    copy(path, npath)
    self.path = npath
    stage("Extracting files from .EXE with pyinstxtractor...")
    if not self.EXE_to_PYC():
      self.extracted = False
      chdir('..')
      rmtree('extracted')
      return
    else:
      stage("Getting the .PYC file with the compiled bytecode of the program...")
      stage("Fixing the header of the .PYC file...")
      self.PYCFIXER()
      stage("Decompiling the .PYC file with pycdc...")
      self.PYC_to_PY()
      self.extracted = True


  def EXE_to_PYC(self):
    self.pyc = extract(self.path)
    if not self.pyc:
      return False
    chdir('..')
    pycpath = f'{self.path}_extracted/{self.pyc}'
    copy(pycpath, self.pyc)
    return True

  def PYCFIXER(self):
    header = self.GET_HEADER()
    with open(self.pyc, mode='rb') as f:
      content = f.read()[16:]
    with open(self.pyc, mode='wb') as f:
      f.write(header + content)

  def PYC_to_PY(self):
    check_output(f'start ..\\etc\\pycdc.exe -o "{self.pyc[:-1]}" "{self.pyc}"', shell=True)

  def GET_HEADER(self):
    with open('header.py', mode='w') as f:
      f.write('...')
    compile('header.py')
    pycache = '__pycache__'
    compiled = listdir(pycache)[0]
    with open(f'__pycache__/{compiled}', mode='rb') as f:
      header = f.read(16)
    rmtree(pycache)
    remove('header.py')
    return header



blue = Col.light_blue
lblue = Colors.StaticMIX((Col.light_blue, Col.white, Col.white))


def stage(text: str, symbol: str = '...') -> str:
    if symbol == '...':
      return print(f""" {Col.Symbol(symbol, lblue, blue)} {lblue}{text}{Col.reset}""")
    else:
      return f""" {Col.Symbol(symbol, blue, lblue)} {blue}{text}{Col.reset}"""

def tui():
  System.Clear()
  System.Title("Riptide")
  System.Size(160, 40)
  Cursor.HideCursor()
  print('\n')
  print(banner)
  print('\n'*3)


def main():
  tui()
  path = input(stage(f"Drag the .EXE you want to decompile {lblue}-> ", '?')).replace('"','').replace("'","")
  print('\n')
  try:
    if not isfile(path):
      int('error')
  except:
    input(f""" {Col.Symbol('!', blue, lblue)} {Col.light_red}Invalid file!{Col.reset}""")
    exit()

  decompiled = Riptide(path)
  chdir('..')
  print('\n')
  if decompiled.extracted:
    path = f'extracted/{decompiled.pyc[:-1]}'
    if isfile(path):
      input(stage(f"Decompiled in '{lblue}{path}{blue}'!", '!'))
    else:
      input(stage(f"Decompiled in '{lblue}{path[:-1]}{blue}'!", '!'))
  else:
    input(f""" {Col.Symbol('!', blue, lblue)} {Col.light_red}Couldn't decompile the file! Maybe it's not a pyinstaller archive?{Col.reset}""")


main()