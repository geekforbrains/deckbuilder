import sys
import json
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from imgurpython import ImgurClient

# TODO: get these as cli args
IMGUR_ID = None
IMGUR_SECRET = None

CARD_WIDTH = 250
CARD_HEIGHT = 350

ROWS = 10
COLS = 7

TOTAL_CARDS = ROWS * COLS
TOTAL_WIDTH = ROWS * CARD_WIDTH
TOTAL_HEIGHT = COLS * CARD_HEIGHT

BACK_FONT = 'coolvetica.ttf'
BACK_FONT_SIZE = CARD_WIDTH / 5

TITLE_FONT = 'coolvetica.ttf'
TITLE_FONT_SIZE = CARD_WIDTH / 6

INFO_FONT = 'coolvetica.ttf'
INFO_FONT_SIZE = CARD_WIDTH / 10



def build_sheet(deck):
  title_font = ImageFont.truetype(TITLE_FONT, TITLE_FONT_SIZE)
  info_font = ImageFont.truetype(INFO_FONT, INFO_FONT_SIZE)
  img = Image.new("RGB", (TOTAL_WIDTH, TOTAL_HEIGHT), tuple(deck['rgb']))
  draw = ImageDraw.Draw(img)

  card_list = []
  for i in deck['cards']:
    card_list.extend([i[1]] * i[0])
  cards_to_create = len(card_list)

  if cards_to_create > TOTAL_CARDS:
    raise Exception('Maximum of {0} cards exceeded in {1} deck: {2}'.format(TOTAL_CARDS, deck['name'], cards_to_create))

  for col in range(COLS):
    for row in range(ROWS):
      if len(card_list) <= 0:
        print '{0}: {1} cards created'.format(deck['name'], cards_to_create)
        return img

      card = card_list.pop(0)

      title_font_width, title_font_height = title_font.getsize(card['title'])
      x = (row * CARD_WIDTH) + ((CARD_WIDTH / 2) - title_font_width / 2)
      y = (col * CARD_HEIGHT) + CARD_HEIGHT / 6

      draw.text((x, y), card['title'], (0, 0, 0), font=title_font)
      draw = ImageDraw.Draw(img)

      if card['info']:
        for i in range(len(card['info'])):
          line = card['info'][i]
          info_font_width, info_font_height = info_font.getsize(line)

          info_x = (row * CARD_WIDTH) + ((CARD_WIDTH / 2) - info_font_width / 2)
          info_y = y + (info_font_height * i) + CARD_HEIGHT / 4

          draw.text((info_x, info_y), line, (0, 0, 0), font=info_font)
          draw = ImageDraw.Draw(img)

  print '{0}: {1} cards created'.format(deck['name'], cards_to_create)
  return img


def build_back(deck):
  font = ImageFont.truetype(BACK_FONT, BACK_FONT_SIZE)
  font_width, font_height = font.getsize(deck['name'])

  img = Image.new("RGB", (deck['size'][0], deck['size'][1]), tuple(deck['rgb']))

  x = (deck['size'][0] / 2) - (font_width / 2)
  y = (deck['size'][1] / 2) - font_height

  draw = ImageDraw.Draw(img)
  draw.text((x, y), deck['name'], (0, 0, 0), font=font)
  draw = ImageDraw.Draw(img)

  return img


def build_deck(deck):
  print 'Building deck:', deck['name']

  deck_file_name = deck['name'].lower().replace(' ', '-')

  back = build_back(deck)
  back.save('{0}_back.jpg'.format(deck_file_name), 'JPEG', quality=100)

  sheet = build_sheet(deck)
  sheet.save('{0}_sheet.jpg'.format(deck_file_name), 'JPEG', quality=100)

  if raw_input('Upload images? [y/N]: ') == 'y':
    upload_to_imgur(deck['name'])


def upload_to_imgur(deck_name):
  client = ImgurClient(IMGUR_ID, IMGUR_SECRET)
  back = client.upload_from_path('{0}_back.jpg'.format(deck_name))
  sheet = client.upload_from_path('{0}_sheet.jpg'.format(deck_name))
  print 'Back:', back['link']
  print 'Sheet:', sheet['link']


if __name__ == '__main__':
  card_json = open(sys.argv[1]).read()
  card_data = json.loads(card_json)
  for deck in card_data:
    build_deck(deck)

