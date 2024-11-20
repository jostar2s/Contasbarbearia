from PIL import Image
import pytesseract
import os
import re  # Importando a biblioteca de expressões regulares

# Defina o caminho do Tesseract no seu sistema (ajuste conforme necessário)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Altere se necessário

# Função para processar a imagem e extrair os números
def processar_imagem(caminho_imagem):
    try:
        # Abrir a imagem
        imagem = Image.open(caminho_imagem)
        
        # Usar o pytesseract para extrair texto da imagem
        texto_extraido = pytesseract.image_to_string(imagem)
        print(f"Texto extraído: \n{texto_extraido}")
        
        # Filtrar os números com uma expressão regular
        numeros = []
        for linha in texto_extraido.split("\n"):
            linha = linha.strip()
            if linha:
                # Usar expressão regular para encontrar números, incluindo os com vírgula como ponto decimal
                matches = re.findall(r'\d+(?:[\.,]\d+)?', linha)  
                for match in matches:
                    try:
                        # Converta o número para float, considerando a vírgula como ponto decimal
                        numero = float(match.replace(',', '.'))
                        numeros.append(numero)
                    except ValueError:
                        pass  # Ignorar qualquer erro de conversão
        
        return numeros
    
    except Exception as e:
        print(f"Ocorreu um erro ao processar a imagem: {e}")
        return []

# Função para somar os valores
def calcular_total_e_iva(valores, taxa_iva=23):
    total = sum(valores)
    iva = total * taxa_iva / 100
    total_com_iva = total + iva
    return total, iva, total_com_iva

# Função para ler os arquivos na pasta
def ler_arquivos_da_pasta(pasta):
    try:
        arquivos = os.listdir(pasta)
        imagens = [f for f in arquivos if f.lower().endswith('.jpg') or f.lower().endswith('.jpeg') or f.lower().endswith('.png')]
        return imagens
    except FileNotFoundError:
        print(f"A pasta {pasta} não foi encontrada.")
        return []

# Função principal para interagir com o usuário
def main():
    pasta_imagens = r'C:\Users\cygnu\source\repos\Contasbarbearia\fotos'  # Atualize com o caminho correto
    
    # Listar arquivos na pasta
    arquivos = ler_arquivos_da_pasta(pasta_imagens)
    if not arquivos:
        print("Não há arquivos de imagem na pasta.")
        return

    # Mostrar arquivos encontrados
    print("Arquivos disponíveis na pasta:")
    for i, arquivo in enumerate(arquivos, 1):
        print(f"{i}. {arquivo}")

    # Solicitar ao usuário o arquivo a ser processado
    try:
        escolha = int(input("Digite o número correspondente ao arquivo que deseja processar: "))
        if escolha < 1 or escolha > len(arquivos):
            print("Escolha inválida.")
            return
    except ValueError:
        print("Valor inválido.")
        return
    
    caminho_imagem = os.path.join(pasta_imagens, arquivos[escolha - 1])
    print(f"Processando a imagem: {caminho_imagem}")

    # Processar a imagem
    valores_extraidos = processar_imagem(caminho_imagem)

    if not valores_extraidos:
        print("Nenhum valor encontrado na imagem.")
        return

    # Calcular totais e IVA
    total, iva, total_com_iva = calcular_total_e_iva(valores_extraidos)
    
    # Exibir resultados
    print(f"Valores extraídos: {valores_extraidos}")
    print(f"Total: {total:.2f} €")
    print(f"IVA (23%): {iva:.2f} €")
    print(f"Total com IVA: {total_com_iva:.2f} €")

# Rodar o programa
if __name__ == "__main__":
    main()





