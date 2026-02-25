import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class MiJuego(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "ANIMACIÓN BÁSICA")
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)
        
        # Posición central X de nuestro cuadrado
        self.posicion_x = 100

    def on_draw(self):
        self.clear()
        
        # Usamos tu función preferida:
        # Left (Izquierda), Right (Derecha), Bottom (Abajo), Top (Arriba)
        arcade.draw_lrbt_rectangle_filled(
            left=self.posicion_x - 25,
            right=self.posicion_x + 25,
            bottom=275,  # Centro Y (300) menos 25
            top=325,     # Centro Y (300) más 25
            color=arcade.color.CANDY_APPLE_RED
        )

    def on_update(self, delta_time):
        self.posicion_x += 3
        
        # Reiniciar si sale de la pantalla
        if self.posicion_x > SCREEN_WIDTH + 25:
            self.posicion_x = -25

if __name__ == "__main__":
    juego = MiJuego()
    arcade.run()