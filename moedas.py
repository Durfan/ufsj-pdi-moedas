import sys
import cv2 as cv
import numpy as np

class ContagemMoedas:
    def __init__(self, image_path):
            self.img = cv.imread(image_path)  # Carrega a imagem
            self.moedas = 0  # Inicializa o contador de moedas
            self.total_value = 0  # Inicializa o valor total das moedas
            self.diameters = []  # Inicializa a lista de diâmetros das moedas

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
        return erosion

    def __detecta_moedas(self):
        img_pre_processed = self.__pre_process()
        edges = cv.Canny(img_pre_processed, 100, 200)
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

    def _classifica_moeda(self, diameter):
        # Calcular o diâmetro normalizado da moeda
        normalized_diameter = diameter / self.max_diameter

        if 0.72 <= normalized_diameter <= 0.76:
            return 0.10  # 10 centavos
        elif 0.78 <= normalized_diameter <= 0.83:
            return 0.05  # 5 centavos
        elif 0.84 <= normalized_diameter <= 0.87:
            return 0.50  # 50 centavos
        elif 0.9 <= normalized_diameter <= 0.93:
            return 0.25  # 25 centavos
        elif 0.98 <= normalized_diameter <= 1.1:
            return 1.00  # 1 real
        else:
            return 0.00 # Não identificado

    def _classifica_moeda_euro(self, diameter):
        # Calcular o diâmetro normalizado da moeda
        normalized_diameter = diameter / self.max_diameter

        if 0.61 <= normalized_diameter <= 0.65:
            return 0.01  # 1 cents
        elif 0.71 <= normalized_diameter <= 0.74:
            return 0.02  # 2 cents
        elif 0.76 <= normalized_diameter <= 0.78:
            return 0.05  # 5 cents
        elif 0.80 <= normalized_diameter <= 0.83:
            return 0.10  # 10 cents
        elif 0.84 <= normalized_diameter <= 0.87:
            return 0.20  # 20 cents
        elif 0.88 <= normalized_diameter <= 0.90:
            return 0.50  # 50 cents
        elif 0.92 <= normalized_diameter <= 0.94:
            return 1.00  # 1 euro
        elif 0.98 <= normalized_diameter <= 1.1:
            return 2.00  # 2 euros
        else:
            return 0.00 # Não identificado

    def __conta_moedas(self):
        self.max_diameter = max(self.diameters)
        for diameter in self.diameters:
            self.total_value += self._classifica_moeda(diameter)
            self.moedas += 1

    def __conta_moedas_euro(self):
        self.max_diameter = max(self.diameters)
        for diameter in self.diameters:
            self.total_value += self._classifica_moeda_euro(diameter)
            self.moedas += 1

    def show_image(self):
        cv.imshow('Moedas', self.img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def get_total_value(self):
        return self.total_value

    def get_moedas(self):
        return self.moedas

    def get_diameters(self):
        return self.diameters

    def run(self):
        self.__processa_img()
        self.__conta_moedas()
        #self.show_image()

    def run_euro(self):
        self.__processa_img()
        self.__conta_moedas_euro()
        #self.show_image()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Informe o caminho da imagem')
        exit()

    image_path = sys.argv[1]
    contagem_moedas = ContagemMoedas(image_path)

    try:
        euro = sys.argv[2]
        euro = True
    except:
        euro = False
    
    if euro:
        contagem_moedas.run_euro()
    else:
        contagem_moedas.run()

    total = contagem_moedas.get_total_value()
    print(f'{total:.2f}')