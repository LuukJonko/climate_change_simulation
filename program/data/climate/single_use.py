from PIL import Image, ImageDraw
import pickle
import sys

img = Image.open(r"img/climate_map.png")
px = img.load()
img.show()

width, height = img.size

print(width, " ", height)

num_coords = (360, 180)

climate_list = [[None] * num_coords[1]] * num_coords[0]

x_interval, y_interval = width / num_coords[0], height / num_coords[1]


def convert_rgba_to_rgb(rgba):
    alpha = int(rgba[3] / 255)

    return (
        int(rgba[0] * alpha),
        int(rgba[1] * alpha),
        int(rgba[2] * alpha)
    )


color_with_climate = {
    (255, 255, 255): 'Ocean',
    (0, 125, 125): 'dfc',
}


for x in range(num_coords[0]):
    for y in range(num_coords[1]):
        climate_list[x][y] = convert_rgba_to_rgb(color := px[x * x_interval, y * y_interval])
        sys.stdout.write(f"\r({x}, {y}) is done, got color { color }")
        sys.stdout.flush()

with open("climate", "wb") as pickle_file:
    pickle.dump(climate_list, pickle_file)

with open("climate", "rb") as pickle_file:
    itemlist = pickle.load(pickle_file)

img = Image.new('RGB', (width, height), color='white')
px = img.load()
for x_index, x in enumerate(itemlist):
    for y_index, y in enumerate(x):
        img.putpixel((x_index, y_index), tuple(y))
        print((x_index, y_index), ' ', tuple(y))

img.show()

print(climate_list == itemlist)
print(itemlist)
