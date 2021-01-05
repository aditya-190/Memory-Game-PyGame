import os, pygame, time, random

class constants:                                                        
  SCREEN_SIZE = 512
  SIDE_TILES = 4
  IMAGE_SIZE = SCREEN_SIZE // SIDE_TILES
  TOTAL_TILES = 16
  MARGIN = 4
  BOX_NAME = 'First Python Game'
  CURRENT_LOCATION = os.getcwd()
  CARD_ICON = os.path.join(CURRENT_LOCATION, r'Images\Card\image.png')
  IMAGES_DIRECTORY = os.path.join(CURRENT_LOCATION, r'Images\Secret')
  BACKGROUD_IMAGE_DIRECTORY = os.path.join(CURRENT_LOCATION, r'Images\Background\image.png')
  THUMBNAIL_ICON_DIRECTORY  = os.path.join(CURRENT_LOCATION, r'Images\Thumbnail\image.png')
  IMAGES = [image for image in os.listdir(IMAGES_DIRECTORY) if image[-3:].lower() == 'png']

class welcome_screen:
  pygame.init()
  pygame.display.set_caption(constants.BOX_NAME)
  screen = pygame.display.set_mode((constants.SCREEN_SIZE, constants.SCREEN_SIZE))
  pygame.display.set_icon(pygame.image.load(constants.THUMBNAIL_ICON_DIRECTORY))
  backgroud_image = pygame.image.load(constants.BACKGROUD_IMAGE_DIRECTORY)
  screen.blit(pygame.transform.scale(backgroud_image, (constants.SCREEN_SIZE, constants.SCREEN_SIZE)), (0,0))
  pygame.display.flip()
  time.sleep(2)
  image_count = dict((keys,0) for keys in constants.IMAGES)

class Image:
  def __init__(self, index):
    self.index   = index
    self.row     = index // constants.SIDE_TILES
    self.column  = index % constants.SIDE_TILES
    self.name    = random.choice(available_image())
    self.path    = os.path.join(constants.IMAGES_DIRECTORY, self.name)
    self.image   = pygame.image.load(self.path)
    self.image   = pygame.transform.scale(self.image, (constants.IMAGE_SIZE - 2 * constants.MARGIN, constants.IMAGE_SIZE - 2 * constants.MARGIN))
    self.Box     = pygame.image.load(constants.CARD_ICON)
    self.Box     = pygame.transform.scale(self.Box, (constants.IMAGE_SIZE - 2 * constants.MARGIN, constants.IMAGE_SIZE - 2 * constants.MARGIN))

    self.skip = False
    welcome_screen.image_count[self.name] += 1
		
def available_image():
  return [key for key, value in welcome_screen.image_count.items() if value < 2]
						
def find_selected(mouse_x, mouse_y):
  row     = mouse_y // constants.IMAGE_SIZE
  column  = mouse_x // constants.IMAGE_SIZE
  region  = row * constants.SIDE_TILES + column
  return region

Image_tile = [Image(index) for index in range(0, constants.TOTAL_TILES)]
current_images = []
game_over = 0
running = True

while running:
  for event in pygame.event.get():  
    if event.type == pygame.QUIT:
      running = False
      pygame.quit()
      quit()
                      
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        running = False
        pygame.quit()
        quit()
                
    if event.type == pygame.MOUSEBUTTONDOWN:        
      mouse_x, mouse_y = pygame.mouse.get_pos()
      image_select = find_selected(mouse_x, mouse_y)
                        
      if image_select not in current_images:
        current_images.append(image_select)
                       
      if len(current_images) > 2:
        current_images = current_images[1:]
                        
    for index, tile in enumerate(Image_tile):
      image_index = tile.image if index in current_images else tile.Box
                
      if not tile.skip:
        welcome_screen.screen.blit(image_index, (tile.column * constants.IMAGE_SIZE + constants.MARGIN, tile.row * constants.IMAGE_SIZE + constants.MARGIN))

    pygame.display.flip()
        
    if len(current_images) == 2:
      image_id_1, image_id_2 = current_images
                
      if Image_tile[image_id_1].name == Image_tile[image_id_2].name:
        Image_tile[image_id_1].skip = True
        Image_tile[image_id_2].skip = True
        game_over += 1
        time.sleep(0.5)
        current_images = []
        
    if game_over == 8:
        time.sleep(1)
        pygame.quit()
        quit()
