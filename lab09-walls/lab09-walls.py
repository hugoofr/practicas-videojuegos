import arcade

# --- Constants ---
SPRITE_SCALING_BOX = 0.5
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_WALL = 0.3
SPRITE_SCALING_COIN = 0.3  # **NUEVO** Escala para la moneda

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

MOVEMENT_SPEED = 5

class MyGame(arcade.Window):
    """ This class represents the main window of the game. """

    def __init__(self):
        """ Initializer """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprites With Walls Example")

        # Lista de Sprites
        self.player_list = None
        self.wall_list = None
        self.coin_list = None  # **NUEVO** Lista para las monedas

        # Configuramos el jugador
        self.player_sprite = None

        # Variable que contiene nuestro sencillo "motor de física"
        self.physics_engine = None

    def setup(self):
        # Elegimos el color de fondo
        arcade.set_background_color(arcade.color.AMAZON)

        # Listas de Sprites
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()  # **NUEVO** Inicializamos la lista de monedas

        # Reiniciamos la puntuación
        self.score = 0

        # --- DIBUJAMOS EL CIRCUITO ---
        # **NUEVO** He añadido algunas letras 'C' para poner monedas de prueba
        mapa = [
            "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",
            "O C          C               O",
            "O  XXXX  XXXXXXXXXXXXXXXXXXXXO",
            "O  X     X C                 O",
            "O  X  XXXX  X                O",
            "O  X        XXXX           X O",
            "O        C                   O",
            "O  XXXXXXXXXXXXX   XXXXXXXXX O",
            "O              C             O",
            "O      XXXXXXXXXXXXXXXX      0",
            "O P                          O",
            "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
        ]

        TAMANO_CAJA = 85

        for fila_index in range(len(mapa)):
            fila = mapa[fila_index]
            for columna_index in range(len(fila)):
                letra = fila[columna_index]
                
                # Calculamos las coordenadas x e y
                centro_x = columna_index * TAMANO_CAJA
                centro_y = (len(mapa) - fila_index) * TAMANO_CAJA
                
                # Si es una 'O', ponemos la caja del borde exterior
                if letra == "O":
                    wall = arcade.Sprite("lab09-walls/muro.png", SPRITE_SCALING_BOX)
                    wall.center_x = centro_x
                    wall.center_y = centro_y
                    self.wall_list.append(wall)
                    
                # Si es una 'X', ponemos la caja del laberinto
                elif letra == "X":
                    wall = arcade.Sprite("lab09-walls/caja.png", SPRITE_SCALING_BOX)
                    wall.center_x = centro_x
                    wall.center_y = centro_y
                    self.wall_list.append(wall)

                # **NUEVO** Si es una 'C', ponemos una moneda
                elif letra == "C":
                    # ¡Asegúrate de tener una imagen para la moneda en tu carpeta!
                    coin = arcade.Sprite("lab09-walls/moneda.png", SPRITE_SCALING_COIN) 
                    coin.center_x = centro_x
                    coin.center_y = centro_y
                    self.coin_list.append(coin)

                # En la letra P se va a situar el jugador
                elif letra == "P":
                    self.player_sprite = arcade.Sprite("lab09-walls/jugador.png", SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = centro_x
                    self.player_sprite.center_y = centro_y
                    self.player_list.append(self.player_sprite)

        # Creamos el motor de física
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
       
        # Creamos dos cámaras
        self.camera_for_sprites = arcade.Camera2D()
        self.camera_for_gui = arcade.Camera2D()
 
    def on_draw(self):
        self.clear()        
        
        # Seleccionamos la cámara para nuestros sprites
        self.camera_for_sprites.use()
        
        # Dibujamos los Sprites
        self.wall_list.draw()
        self.coin_list.draw()  # **NUEVO** Dibujamos las monedas
        self.player_list.draw()

        # Seleccionamos la cámara para los elementos de la interfaz
        self.camera_for_gui.use()
        arcade.draw_text(f"Score: {self.score}", 10, 10, arcade.color.WHITE, 24)

    def on_key_press(self, key, modifiers):
        """Función que se ejecuta cada vez que se pulsa una tecla"""
        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Función que se ejecuta cada vez que se suelta una tecla"""
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0 

    def on_update(self, delta_time):
        """Movimiento y lógica del juego"""
        
        self.physics_engine.update()

        # **NUEVO** Comprobamos si el jugador ha tocado alguna moneda
        monedas_chocadas = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        # **NUEVO** Recorremos todas las monedas con las que hemos chocado
        for moneda in monedas_chocadas:
            moneda.remove_from_sprite_lists() # La moneda desaparece de la pantalla
            self.score += 10 # Sumamos 10 puntos por cada moneda (puedes cambiar este valor)

        # Centramos la cámara en el jugador
        self.camera_for_sprites.position = self.player_sprite.position

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()