import arcade

#CONSTANTES
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

MOVEMENT_SPEED = 5 #Velocidad a la que se moverá el cubo
CUBE_SIZE = 50 #Tamaño del cubo



#CLASE CUBO (Objeto que podremos controlar con el teclado y con el mando)
class Cubo:
    def __init__(self):
        self.size = CUBE_SIZE
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = 200 + (self.size / 2) #Lo colocamos justo encima del suelo 
        
        self.change_0 = 0 
        self.change = 0

    def draw(self):
        """Dibujamos la cara del cubo usando formas geométricas"""
        #Calculamos los bordes absolutos
        left = self.center_x - (self.size / 2)
        right = self.center_x + (self.size / 2)
        bottom = self.center_y - (self.size / 2)
        top = self.center_y + (self.size / 2)

        #Borde exterior negro
        arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, arcade.color.BLACK, border_width = 4)
        #Relleno amarillo
        arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, arcade.color.YELLOW)
        #Ojo izquierdo
        arcade.draw_lrbt_rectangle_filled(self.center_x - 14, self.center_x - 4, self.center_y + 4, self.center_y + 14, arcade.color.CYAN)
        arcade.draw_lrbt_rectangle_outline(self.center_x - 14, self.center_x - 4, self.center_y + 4, self.center_y + 14, arcade.color.BLACK, border_width = 3)
        #Ojo derecho
        arcade.draw_lrbt_rectangle_filled(self.center_x + 4, self.center_x + 14, self.center_y + 4, self.center_y + 14, arcade.color.CYAN)
        arcade.draw_lrbt_rectangle_outline(self.center_x + 4, self.center_x + 14, self.center_y + 4, self.center_y + 14, arcade.color.BLACK, border_width = 3)
        #Boca
        arcade.draw_lrbt_rectangle_filled(self.center_x - 18, self.center_x + 18, self.center_y - 14, self.center_y - 4, arcade.color.CYAN)
        arcade.draw_lrbt_rectangle_outline(self.center_x - 18, self.center_x + 18, self.center_y - 14, self.center_y - 4, arcade.color.BLACK, border_widht = 3)
        
    def on_update(self):
        """Método que actualiza la posición del cubo y comprueba las colisiones con los bordes"""
        self.y += self.change_y
        self.x += self.change_x

        #Lógica para que el sol no se salga de la pantalla
        if self.x < self.radio:
            self.x = self.radio
            
        elif self.x > SCREEN_WIDTH - self.radio:
            self.x = SCREEN_WIDTH - self.radio

        if self.y < self.radio:
            self.y = self.radio
            
        elif self.y > SCREEN_HEIGHT - self.radio:
            self.y = SCREEN_HEIGHT - self.radio

#FUNCIONES DE DIBUJO DE FONDO
def dibujar_suelo():
    arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, 0, 200, arcade.color.BLUE)


class MyGame(arcade.Window):
    """ Our Custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "GEOMETRY DASH")
        arcade.set_background_color(arcade.color.BABY_BLUE)
                                                                                                                                                                                                                                                                                                                                                               
        self.mi_sol = Sol(400, 300, 0, 0, 1) #Creamos el sol
         
        self.set_mouse_visible(False) #Ocultamos el cursor del ratón

        joysticks = arcade.get_game_controllers() #Pedimos al sistema operativo una lista de los mandos que están conectados al ordeandor

        if joysticks:
            #Si hay al menos uno, nos guardamos el primero [0]
            self.joystick = joysticks[0] #Tomamos el primer mando que encontremos 
            self.joystick.open() #Abrimos la comunicación con este mando
            print("Mando detectado correctamente.")
        else:
            print("No hay mandos conectados.")
            self.joystick = None

    def on_draw(self):
        self.clear()

        #LLAMAMOS A NUESTRAS FUNCIONES PARA CREAR EL PAISAJE
        # Suelo
        dibujar_suelo()

        # Sol
        self.mi_sol.draw()
        
        # Pirámides
        dibujar_piramide(200, 200, 1.0)
        dibujar_piramide(450, 200, 0.7)
        
        # Cactus
        dibujar_cactus(100, 180, 0.8)
        dibujar_cactus(650, 200, 1.2)
        
        # Piedras
        dibujar_piedra(550, 100, 1.0)
        dibujar_piedra(720, 120, 0.5)

    def on_mouse_motion(self, x, y, dx, dy):
        """Función para mover con el ratón el sol (La función se activa cada vez que el ratón se mueve)"""
        #Actualizamos las variables con la posición del ratón
        self.mi_sol.x = x
        self.mi_sol.y = y

    def on_key_press(self, key, modifiers):
        """Función que se llama cada vez que se pulsa una tecla"""
        if key == arcade.key.LEFT:
            self.mi_sol.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.mi_sol.change_x = MOVEMENT_SPEED
        if key == arcade.key.UP:
            self.mi_sol.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.mi_sol.change_y = -MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.mi_sol.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.mi_sol.change_y = 0

    def on_update(self, delta_time):
        
        if self.joystick:
            if abs(self.joystick.x) > DEAD_ZONE:
                self.mi_sol.change_x = self.joystick.x * MOVEMENT_SPEED
            else:
                #Si no tocamos la palanca (o se mueve menos de la zona muerta), se para
                self.mi_sol.change_x = 0
                
            #Movimiento Vertical (Eje Y)
            if abs(self.joystick.y) > DEAD_ZONE:
                # Le ponemos un signo negativo delante a la 'y' porque en la mayoría 
                # de mandos empujar hacia arriba da valores negativos.
                self.mi_sol.change_y = -self.joystick.y * MOVEMENT_SPEED
            else:
                self.mi_sol.change_y = 0
        
        self.mi_sol.on_update()

def main():
    window = MyGame()
    arcade.run()


main()