""" Sprite Sample Program """

import random
import arcade

# --- Constantes ---
SPRITE_SCALING_PLAYER = 0.5 # Tamaño jugador
SPRITE_SCALING_COIN = 0.2 # Tamaño monedas
SPRITE_SCALING_METEORITO = 0.08 # Tamaño meteoritos

COIN_COUNT = 50
METEORITO_COUNT = 20

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Constructor """
        # Llamamos a la clase padre
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Ejemplo Sprite")

        # Variables que contendrán listas de sprites
        self.player_list = None
        self.coin_list = None
        self.meteorito_list = None

        # Configuramos la información del jugador
        self.player_sprite = None # Es el sprite que vamos a mover
        self.score = 0  # Lleva la cuenta del jugador

        # No mostramos el cursor del ratón
        self.set_mouse_visible(False)

        # Color del fondo de la ventana
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ Función que configura el juego e inicializa las variables """

        # Lista de Sprites
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.meteorito_list = arcade.SpriteList()

        # Puntuación
        self.score = 0

        # Configuramos el jugador
        self.player_sprite = arcade.Sprite("personaje.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Creamos las monedas (Sprites buenos)
        for i in range(COIN_COUNT):
            
            coin = arcade.Sprite("moneda.png", SPRITE_SCALING_COIN)

            # Posición de las monedas
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            # Añadimos las monedas a la lista
            self.coin_list.append(coin)

        # Creamos los meteoritos (Sprites malos)
        for i in range(METEORITO_COUNT):
            
            meteorito = arcade.Sprite("meteorito.png", SPRITE_SCALING_METEORITO)

            # Posición de las monedas
            meteorito.center_x = random.randrange(SCREEN_WIDTH)
            meteorito.center_y = random.randrange(SCREEN_HEIGHT)

            # Añadimos las monedas a la lista
            self.meteorito_list.append(meteorito)

    def on_draw(self):
        """ Dibujamos la lista de sprites aquí """
        
        self.clear()

        self.coin_list.draw()
        self.player_list.draw()
        self.meteorito_list.draw()

        # Añadimos el texto de la puntuación en la pantalla
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Función para manejar el movimiento del ratón """

        # Movemos el centro del sprite jugador para que coincida con las coordenadas del ratón
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        """ Movimiento y lógica del juego """

        # Llamamos a la función de actualización de todos los sprites
        self.coin_list.update()

        # Lista con las monedas que colisionan con el jugador
        coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        # Lista con los meteoritos que colisionan con el jugador
        meteorito_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.meteorito_list)


        # Si el personaje colisiona con una moneda, la eliminamos y sumamos uno a la puntuación
        for coin in coins_hit_list:
            coin: arcade.Sprite
            coin.remove_from_sprite_lists()
            self.score += 1

        # Si el personaje solisiona con un meteorito, le eliminamos y restamos uno a la puntuación
        for meteorito in meteorito_hit_list:
            meteorito: arcade.Sprite
            meteorito.remove_from_sprite_lists()
            self.score -= 1

def main():
    """ Método main """
    
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()