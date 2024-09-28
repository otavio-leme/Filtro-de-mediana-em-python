import numpy as np
import os
from scipy.ndimage import median_filter

def read_pgm(filename):
    with open(filename, 'rb') as f:
        # Lê o cabeçalho do arquivo
        magic_number = f.readline().strip()
        assert magic_number in [b'P2', b'P5'], "Formato PGM incorreto!"

        # Ignora linhas de comentários
        while True:
            line = f.readline()
            if line[0] != ord(b'#'):
                break
        
        # Obtém a largura e altura da imagem
        width, height = map(int, line.split())
        
        # Lê o valor máximo de cinza
        max_val = int(f.readline().strip())
        
        # Lê os dados da imagem
        if magic_number == b'P2':
            # Formato ASCII
            data = np.array([int(value) for value in f.read().split()], dtype=np.uint8)
        elif magic_number == b'P5':
            # Formato binário
            data = np.frombuffer(f.read(), dtype=np.uint8)
        
        # Redimensiona os dados para a forma correta
        image = data.reshape((height, width))
    
    return image, magic_number.decode()

def apply_median_filter(image, filter_size=3):
    # Aplica o filtro de mediana usando scipy
    filtered_image = median_filter(image, size=filter_size)
    return filtered_image

def save_pgm(image, filename, magic_number='P2'):
    height, width = image.shape
    max_val = 255
    with open(filename, 'wb') as f:
        # Escreve o cabeçalho do arquivo PGM
        f.write(f'{magic_number}\n'.encode())
        f.write(f'{width} {height}\n'.encode())
        f.write(f'{max_val}\n'.encode())
        
        # Salva os dados da imagem no formato P2 ou P5
        if magic_number == 'P2':
            # Salvando como texto
            for row in image:
                row_str = ' '.join(str(int(pixel)) for pixel in row) + '\n'
                f.write(row_str.encode())
        elif magic_number == 'P5':
            # Salvando em formato binário
            f.write(image.astype(np.uint8).tobytes())

def process_all_pgms(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.pgm'):
            filepath = os.path.join(directory, filename)
            print(f"Processando {filepath}...")
            
            # Lê a imagem e obtém o formato (P2 ou P5)
            input_image, magic_number = read_pgm(filepath)
            
            # Aplica o filtro de mediana
            filtered_image = apply_median_filter(input_image, filter_size=3)
            
            # Define o novo nome do arquivo com base no formato
            new_filename = filename.replace('.pgm', '_processado.pgm')
            save_path = os.path.join(directory, new_filename)
            
            # Salva a imagem processada
            save_pgm(filtered_image, save_path, magic_number=magic_number)
            print(f"Imagem processada salva em {save_path}")

# Caminho da pasta onde estão os arquivos PGM
directory_path = 'C:\\Users\\otavi\\OneDrive\\Documents\\Computa-grafica'


# Processa todos os arquivos PGM na pasta
process_all_pgms(directory_path)
