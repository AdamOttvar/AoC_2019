#!python3

def first_task():
    with open('input8.txt') as input_file:
        image_input = input_file.read().strip()

    pixels_in_each_layer = 25*6
    nbr_of_layers = int(len(image_input)/pixels_in_each_layer)
    image = []
    layer = []
    layer_counter = []

    index_counter = 0
    for current_layer in range(0, nbr_of_layers):
        layer = []
        zero_counter = 0
        one_counter = 0
        two_counter = 0
        for row in range(0,6):
            first_index = 25*(index_counter)
            second_index = 25*(index_counter+1)
            row = image_input[first_index:second_index]
            zero_counter += row.count('0')
            one_counter += row.count('1')
            two_counter += row.count('2')
            index_counter += 1
            layer.append(row)
        image.append(layer)
        layer_counter.append([zero_counter, one_counter, two_counter])

    f = lambda x: x[0]
    list_of_zeros = [f(x) for x in layer_counter]
    min_value = min(list_of_zeros)
    min_index = list_of_zeros.index(min_value)
    prod_of_1_and_2 = layer_counter[6][1] * layer_counter[6][2]
    print("Product of 1s and 2s: {}".format(prod_of_1_and_2))
    return image

def second_task(raw_image):
    from PIL import Image

    nbr_of_layers = len(raw_image)
    img = Image.new( 'RGB', (25,6), "red") # Create a new red image
    pixels = img.load() # Create the pixel map
    for i in range(img.size[0]):    # For every pixel:
        for j in range(img.size[1]):
            for layer in range(0,nbr_of_layers):
                if raw_image[layer][j][i] == '0':
                    colour = (0, 0, 0)
                    break
                elif raw_image[layer][j][i] == '1':
                    colour = (255, 255, 255)
                    break
                else:
                    continue
            pixels[i,j] = colour # Set the colour accordingly
    img.show()

image = first_task()
second_task(image)