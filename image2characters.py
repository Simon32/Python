from PIL import Image, ImageDraw, ImageFont
import operator, bisect


def getChar(val):
    """
    return a char for a given gray value
    """
    index = bisect.bisect_left(scores, val)  # find index of val in scores

    # check and choose the nearer one between current index and former index
    if index > 0 and sorted_weights[index][1] + sorted_weights[index -
                                                               1][1] > 2 * val:
        index -= 1
    return sorted_weights[index][0]


def transform(image_file):
    """
    return a string containing characters representing each pixel
    """
    image_file = image_file.convert("L")  # transform image to black-white
    codePic = ''
    for h in range(image_file.size[1]):
        for w in range(image_file.size[0]):
            gray = image_file.getpixel((w, h))
            codePic += getChar(maximum * (1 - gray / 255))  # append characters
        codePic += '\r\n'  # change lines

    return codePic


readinFilePath = 'test.jpg'
outputTextFile = 'ycy_ascii.txt'
outputImageFile = 'ycy_ascii.jpg'
fnt = ImageFont.truetype('Courier New.ttf', 10)
chrx, chry = fnt.getsize(chr(32))
normalization = chrx * chry * 255

weights = {}
# get gray density for characters in range [32, 126]
for i in range(32, 127):
    chrImage = fnt.getmask(chr(i))
    sizex, sizey = chrImage.size
    ctr = sum(
        chrImage.getpixel((x, y)) for y in range(sizey) for x in range(sizex))
    weights[chr(i)] = ctr / normalization

weights[chr(32)] = 0.01  # increase it to make blank space ' ' more available
weights.pop('_', None)  # remove '_' since it is too directional
weights.pop('-', None)  # remove '-' since it is too directional
sorted_weights = sorted(weights.items(), key=operator.itemgetter(1))

scores = [y for (x, y) in sorted_weights]
maximum = scores[-1]

base = Image.open(open(readinFilePath, 'rb'))

resolution = 2.5  # resolution of result ascii image, the higher the better
sizes = [resolution * i for i in (0.665, 0.3122, 4)]
imagefile = base.resize((int(base.size[0] * sizes[0]),
                         int(base.size[1] * sizes[1])))

result = transform(imagefile)

# output to text file
asc_text = open(outputTextFile, 'w')
asc_text.write(result)
asc_text.close()

# output to image file and show it
asc_image = Image.new(
    'L', (int(base.size[0] * sizes[2]), int(base.size[1] * sizes[2])), 255)
d = ImageDraw.Draw(asc_image)
d.text((0, 0), result, font=fnt, fill=0)
asc_image.save(outputImageFile)
#asc_image.show()
#asc_image.close()
