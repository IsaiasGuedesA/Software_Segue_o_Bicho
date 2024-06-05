import os
import sys

# Obter o caminho absoluto do diretório atual
current_directory = os.path.dirname(os.path.abspath(__file__))

# Adicionar o diretório raiz do projeto ao sys.path
root_directory = os.path.abspath(os.path.join(current_directory, '../../'))

sys.path.append(root_directory)
