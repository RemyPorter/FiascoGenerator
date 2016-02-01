import sys
import os
from . import loader, generator
def main():
    file_source = os.path.realpath(sys.argv[1])
    characters = sys.argv[2].split(",")
    playset = None
    with open(file_source) as f:
        playset = loader.process(f)
    fiasco = generator.Setup(playset, characters)
    f = fiasco.build()
    print(f)

main()