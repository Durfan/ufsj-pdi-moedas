# Contagem de moedas

## Uso

```bash
python3 moedas.py -h
usage: moedas.py [-h] [--moeda {real,euro}] [--show | --no-show] path

Este script conta moedas em uma imagem e retorna o valor total.

positional arguments:
path                 Caminho para a imagem.

options:
-h, --help           show this help message and exit
--moeda {real,euro}  Sistema monetário da imagem. Opções: real, euro
--show, --no-show    Mostra a imagem com as moedas detectadas.

```

## Exemplos
    
```bash
python3 moedas.py ./imgs/moedas_real.png
python3 moedas.py ./imgs/moedas_real.png --show
python3 moedas.py ./imgs/moedas_euro.png --moeda euro
python3 moedas.py ./imgs/moedas_euro.png --moeda euro --show
```

## Dependências

- Python 3.6
- OpenCV 3.4.2
- Numpy 1.15.4
- Matplotlib 3.0.2 (opcional, jupiter notebook)
- Pandas 0.23.4 (opcional, jupiter notebook)

## Resultados

![Testes em reais](/export/testes_reais.png "Testes em reais")

![Pre Processamento](/export/testes_processed_imgs.png "Pre Processamento")

![Teste em euro](/export/teste_euro.png "Teste em euro")
