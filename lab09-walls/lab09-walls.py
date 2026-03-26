""" Práctica Sprites and Walls """

import arcade

# --- Constants ---
SPRITE_SCALING_BOX = 0.5
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_WALL = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

MOVEMENT_SPEED = 5


class MyGame(arcade.Window):
    """ This class represents the main window of the game. """

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprites With Walls Example")

        #Lista de Sprites
        self.player_list = None
        self.wall_list = None

        #Configuramos el jugador
        self.player_sprite = None

        #Variable que contiene nuestro sencillo "motor de física"
        self.physics_engine = None

    def setup(self):
        #Elegimos el color de fondo
        arcade.set_background_color(arcade.color.AMAZON)

        #Listas de Sprites
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        #Reiniciamos la puntuación
        self.score = 0

        # --- DIBUJAMOS EL CIRCUITO ---
        mapa = [
            "OOOOOOOOOOOOOOOOOOOO",
            "O                  O",
            "O  XXXX  XXXXXXX   O",
            "O  X     X     X   O",
            "O  X  XXXX  X  X   O",
            "O  X        X  X   O",
            "O  XXXXXXXXXX  X   O",
            "O                  O",
            "OOOOOOOOOOOOOOOOOOOO"
        ]

        TAMANO_CAJA = 64  # Ajusta este número si las cajas no encajan bien
        SPRITE_SCALING_WALL = 0.5

        for fila_index in range(len(mapa)):
            fila = mapa[fila_index]
            for columna_index in range(len(fila)):
                letra = fila[columna_index]
                
                # Calculamos las coordenadas x e y (sirve para ambos tipos de caja)
                centro_x = columna_index * TAMANO_CAJA
                centro_y = (len(mapa) - fila_index) * TAMANO_CAJA
                
                # Si es una 'O', ponemos la caja del borde exterior
                if letra == "O":
                    #Usamos los muros para hacer el recinto
                    wall = arcade.Sprite("lab09-walls/muro.png", SPRITE_SCALING_BOX)
                    wall.center_x = centro_x
                    wall.center_y = centro_y
                    self.wall_list.append(wall)
                    
                # Si es una 'X', ponemos la caja del laberinto
                elif letra == "X":
                    #Usamos las cajas para hacer el laberinto
                    wall = arcade.Sprite("lab09-walls/caja.png", SPRITE_SCALING_BOX)
                    wall.center_x = centro_x
                    wall.center_y = centro_y
                    self.wall_list.append(wall)

        #Creamos el jugador
        self.player_sprite = arcade.Sprite("lab09-walls/jugador.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 64
        self.player_list.append(self.player_sprite)

        #Creamos el motor de física: esto identifica al jugador y a un alista de sprites por los que el jugador no tiene permitido pasar
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
       
        #Creamos dos cámaras: una para el mundo exterior y otra para la puntuación (o cualquier elemento de la interaz)
        self.camera_for_sprites = arcade.Camera2D()
        self.camera_for_gui = arcade.Camera2D()
 
    def on_draw(self):
        self.clear()        
        
        #Selccionamos la cámara para nuestros sprites
        self.camera_for_sprites.use()
        
        #Dibujamos los Sprites
        self.wall_list.draw()
        self.player_list.draw()

        #Seleccionamos la cámara para los elementos de la interfaz
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

        #Centramos la cámara en el jugador
        self.camera_for_sprites.position = self.player_sprite.position

def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()