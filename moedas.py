import argparse
import cv2 as cv
import numpy as np

class ContagemMoedas:
    def __init__(self, image_path):
            self.img = cv.imread(image_path)
            self.moedas = 0
            self.total_value = 0.00
            self.diameters = []

    def __get_background_color(self):
        region = (0, 10, 0, 10)
        roi = self.img[region[0]:region[1], region[2]:region[3]]
        self.bg_color = np.median(roi, axis=(0, 1)).astype(np.uint8)

    def __pre_process(self): 
        self.__get_background_color()
        mask = cv.inRange(self.img, self.bg_color, self.bg_color)
        self.inverted = cv.bitwise_not(mask)
        kernel = np.ones((5, 5), np.uint8)
        erosion = cv.erode(self.inverted, kernel, iterations=1)
        self.img_pre_processed = erosion

    def __detecta_moedas(self):
        edges = cv.Canny(self.img_pre_processed, 100, 200)
        self.contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    def __processa_img(self):
        self.__detecta_moedas()
        for contour in self.contours:
            area = cv.contourArea(contour)
            approx = cv.approxPolyDP(contour, 0.02 * cv.arcLength(contour, True), True)

            if len(approx) >= 8 and area > 100:
                (x, y, w, h) = cv.boundingRect(approx)
                diameter = max(w, h)
                self.diameters.append(diameter)
                cv.drawContours(self.img, [contour], -1, (0, 255, 0), 2)

    def _moedas_real(self, diameter):
        normalized = diameter / self.max_diameter
        diameters = {
            (0.72, 0.76): 0.10, # 10 centavos
            (0.78, 0.83): 0.05, # 5 centavos
            (0.84, 0.87): 0.50, # 50 centavos
            (0.90, 0.93): 0.25, # 25 centavos
            (0.98, 1.10): 1.00, # 1 real
        }

        for start, end in diameters:
            if start <= normalized <= end:
                return diameters[(start, end)]

        return 0.00  # Não identificado
    
    def _moedas_euro(self, diameter):
        normalized = diameter / self.max_diameter
        diameters = {
            (0.61, 0.65): 0.01, # 1 cents
            (0.71, 0.74): 0.02, # 2 cents
            (0.76, 0.78): 0.05, # 5 cents
            (0.80, 0.83): 0.10, # 10 cents
            (0.84, 0.87): 0.20, # 20 cents
            (0.88, 0.90): 0.50, # 50 cents
            (0.92, 0.94): 1.00, # 1 euro
            (0.98, 1.10): 2.00, # 2 euros
        }

        for start, end in diameters:
            if start <= normalized <= end:
                return diameters[(start, end)]

        return 0.00  # Não identificado

    def __conta_moedas(self, moeda):
        self.max_diameter = max(self.diameters)
        for diameter in self.diameters:
            if moeda == 'real':
                self.total_value += self._moedas_real(diameter)
            elif moeda == 'euro':
                self.total_value += self._moedas_euro(diameter)
            self.moedas += 1

    def __waitUntilX(self, window):
        while True:
            k = cv.waitKey(100) & 0xFF
            if k == 27:
                break
            elif k == 113:
                break

        cv.destroyAllWindows()

    def show_image(self):
        window = cv.imshow('Moedas', self.img)
        self.__waitUntilX(window)

    def show_image_pre_processed(self):
        window = cv.imshow('Moedas', self.img_pre_processed)
        self.__waitUntilX(window)

    def get_total_value(self):
        return self.total_value

    def get_moedas(self):
        return self.moedas

    def get_diameters(self):
        return self.diameters
    
    def get_image(self):
        return self.img

    def get_image_pre_processed(self):
        return self.img_pre_processed

    def run(self, moeda='real'):
        self.__pre_process()
        self.__processa_img()
        self.__conta_moedas(moeda)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""
    Este script conta moedas em uma imagem e retorna o valor total. 
    """)
    parser.add_argument("path", help="Caminho para a imagem.")
    parser.add_argument(
        "--moeda",
        default='real' ,
        required=False,
        choices=['real', 'euro'],
        help="Sistema monetário da imagem. Opções: real, euro")
    parser.add_argument(
        "--show",
        required=False,
        action=argparse.BooleanOptionalAction,
        help="Mostra a imagem com as moedas detectadas.")

    args = parser.parse_args()

    contagem = ContagemMoedas(args.path)
    contagem.run(args.moeda)
    total = contagem.get_total_value()
    print(f'{total:.2f}')

    if args.show:
        contagem.show_image()

