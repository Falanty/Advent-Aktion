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
        index_to_non_zero_count = {index: np.count_nonzero(layer) for index, layer in enumerate(self.layers)}
        layer_fewest_zero = self.layers[max(index_to_non_zero_count.keys(), key=(lambda k: index_to_non_zero_count[k]))]
        return len(layer_fewest_zero[layer_fewest_zero == 1]) * len(layer_fewest_zero[layer_fewest_zero == 2])

    def print(self):
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


test = Image(2, 2, filename="data/test_day_08.txt")
print(test.check_corruption())
test.print()

image = Image(25, 6)
print(image.check_corruption())
image.print()
