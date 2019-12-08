import numpy as np


class Image:
    def __init__(self, width, height, filename="data/input_day_08.txt"):
        self.width = width
        self.height = height
        self.filename = filename
        self.layers = self.build_layers()

    def build_layers(self):
        with open(self.filename, 'r') as input_file:
            input_list = list(map(int, list(input_file.read())))
        layers = np.reshape(input_list, (-1, self.height, self.width))
        return layers

    def check_corruption(self):
        layer = None
        most_non_zeroes = -1
        for index in range(len(self.layers)):
            non_zero_count = np.count_nonzero(self.layers[index])
            if non_zero_count > most_non_zeroes:
                most_non_zeroes = non_zero_count
                layer = self.layers[index]
        return len(layer[layer == 1]) * len(layer[layer == 2])

    def decode_message(self):
        non_transparent = np.transpose(np.where(self.layers != 2))
        result = list()
        for x in range(self.height):
            for y in range(self.width):
                index = non_transparent[np.logical_and(non_transparent[:, 1] == x, non_transparent[:, 2] == y), :][0]
                color = self.layers[tuple(index)]
                background = "\u001B[37;40m" if color == 1 else "\u001B[47m"
                result.append(background + str(color) + "\u001B[0m")
            result.append("\n")
        print(''.join(result))
        return result


test = Image(2, 2, filename="data/test_day_08.txt")
print(test.check_corruption())
test.decode_message()

image = Image(25, 6)
print(image.check_corruption())
image.decode_message()
