""" Sprite Sample Program """

import random
import arcade

# --- Constantes ---
SPRITE_SCALING_PLAYER = 0.4 # Tamaño jugador
SPRITE_SCALING_COIN = 0.2 # Tamaño monedas
SPRITE_SCALING_METEORITO = 0.08 # Tamaño meteoritos

COIN_COUNT = 50
METEORITO_COUNT = 20

MOVEMENT_SPEED = 5 # Velocidad a la que se mueve el jugador

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

            # Las damos velocidad diagonal aleatoria
            coin.change_x = random.choice([-2, 2])
            coin.change_y = random.choice([-2, 2])

            # Añadimos las monedas a la lista
            self.coin_list.append(coin)

        # Creamos los meteoritos (Sprites malos)
        for i in range(METEORITO_COUNT):
            
            meteorito = arcade.Sprite("meteorito.png", SPRITE_SCALING_METEORITO)

            # Posición de las monedas
            meteorito.center_x = random.randrange(SCREEN_WIDTH)
            meteorito.center_y = random.randrange(SCREEN_HEIGHT)

            # Caen hacia abajo
            meteorito.change_y = -2 # Velocidad

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

    # Funciones para mover el jugador con las flechas del teclado
    def on_key_press(self, key, modifiers):
        """ Función que se llama cada vez que se pulsa una tecla """
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED
        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """ Función que se llama cada vez que se suelta una tecla """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0

    def on_update(self, delta_time):
        """ Movimiento y lógica del juego """

        # Actualizamos la posición de todos los sprites
        self.player_list.update()
        self.coin_list.update()
        self.meteorito_list.update()

        # Límites para que el jugador no se salga de la pantalla
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        
        elif self.player_sprite.right > SCREEN_WIDTH:
            self.player_sprite.right = SCREEN_WIDTH

        if self.player_sprite.bottom < 0:
            self.player_sprite.bottom = 0
            
        elif self.player_sprite.top > SCREEN_HEIGHT:
            self.player_sprite.top = SCREEN_HEIGHT

        # Lógica de los meteoritos (Lluvia infinita)
        for meteorito in self.meteorito_list:
            meteorito: arcade.Sprite
            # Si el meteorito se sale por abajo de la pantalla...
            if meteorito.top < 0:
                meteorito.bottom = SCREEN_HEIGHT # Lo teletransportamos arriba
                meteorito.center_x = random.randrange(SCREEN_WIDTH) # En una posición X aleatoria

        # Lógica de las monedas (Rebote en las paredes)
        for coin in self.coin_list:
            coin: arcade.Sprite
            # Si choca con los bordes izquierdo o derecho, invierte su dirección X
            if coin.left < 0 or coin.right > SCREEN_WIDTH:
                coin.change_x *= -1 
            
            # Si choca con los bordes inferior o superior, invierte su dirección Y
            if coin.bottom < 0 or coin.top > SCREEN_HEIGHT:
                coin.change_y *= -1


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