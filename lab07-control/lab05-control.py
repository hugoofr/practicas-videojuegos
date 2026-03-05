""" Lab 7 - User Control """
import arcade

#CONSTANTES
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MOVEMENT_SPEED = 3
DEAD_ZONE = 0.02

#CLASE SOL (Objeto que probamos en esta práctica para moverlo con el ratón, teclado...)
class Sol:
    def __init__(self, posicion_x, posicion_y, change_x, change_y, escala):
        self.x = posicion_x
        self.y = posicion_y
        self.change_x = change_x 
        self.change_y = change_y 
        self.escala = escala
        self.radio = 40 * self.escala
        self.grosor_borde = 2 * self.escala

    def draw(self):
        """Método que le dice al sol cómo dibujarse a sí mismo"""
        arcade.draw_circle_filled(self.x, self.y, self.radio, arcade.color.YELLOW)
        arcade.draw_circle_outline(self.x, self.y, self.radio, arcade.color.ORANGE, self.grosor_borde)

    def on_update(self):
        """Método que actualiza la posición del sol según su velocidad"""
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
    # Izquierda=0, Derecha=800, Abajo=0, Arriba=200
    arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, 0, 200, arcade.color.SANDY_BROWN)

def dibujar_piramide(x, y, escala):
    ancho_medio = 100 * escala
    altura = 200 * escala
    arcade.draw_triangle_filled(
        x - ancho_medio, y,
        x + ancho_medio, y,
        x, y + altura,
        arcade.color.BROWN
    )

def dibujar_cactus(x, y, escala):
    ancho = 20 * escala
    alto = 100 * escala
    
    # Calculamos los bordes a partir de un punto base (x, y)
    izq = x - (ancho / 2)
    der = x + (ancho / 2)
    abajo = y
    arriba = y + alto
    
    # Tronco principal
    arcade.draw_lrbt_rectangle_filled(izq, der, abajo, arriba, arcade.color.DARK_GREEN)
    
    # Brazos (Líneas para mantener tu estilo original)
    grosor = 8 * escala
    arcade.draw_line(x, y + 50 * escala, x - 20 * escala, y + 50 * escala, arcade.color.DARK_GREEN, grosor)
    arcade.draw_line(x - 20 * escala, y + 50 * escala, x - 20 * escala, y + 70 * escala, arcade.color.DARK_GREEN, grosor)

def dibujar_piedra(x, y, escala):
    arcade.draw_ellipse_filled(x, y, 80 * escala, 40 * escala, arcade.color.GRAY)


class MyGame(arcade.Window):
    """ Our Custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Lab 7 - User Control")
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)

        self.mi_sol = Sol(400, 300, 0, 0, 1) #Creamos el sol
         
        self.set_mouse_visible(False) #Ocultamos el cursor del ratón

        joysticks = arcade.get_joysticks() #Pedimos a arcade la lista de mandos enchufados

        if joysticks:
            #Si hay al menos uno, nos guardamos el primero [0]
            self.joystick = joysticks[0]
            self.joystick.open() #Lo encendemos para leerlo
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
        self.mi_sol.on_update()
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