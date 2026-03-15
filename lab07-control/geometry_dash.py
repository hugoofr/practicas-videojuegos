import arcade

#CONSTANTES
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

MOVEMENT_SPEED = 5 #Velocidad horizontal del cubo
CUBE_SIZE = 60 #Tamaño del cubo
GROUND_HEIGHT = 200 #Altura del suelo

GRAVITY = 0.5 #Fuera con la que el cubo cae
JUMP_SPEED = 12 #Fuerza con la que el cubo salta
ROTATION_SPEED = 3.75 #Grados que gira el cubo en cada fotograma mientras está en el aire

def dibujar_cubo_estatico(center_x, center_y, size):
        """ Dibujamos la cara del cubo usando formas geométricas para hacerle un foto """
        #Calculamos los bordes absolutos
        left = center_x - (size / 2)
        right = center_x + (size / 2)
        bottom = center_y - (size / 2)
        top = center_y + (size / 2)

        #Fondo negro solido para hacer el borde
        arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, arcade.color.BLACK)
        #Relleno amarillo ligeramente más pequeño que el cuadrado negro
        arcade.draw_lrbt_rectangle_filled(left + 2, right - 2, bottom + 2, top - 2, arcade.color.YELLOW)
        #Ojo izquierdo
        arcade.draw_lrbt_rectangle_filled(center_x - 14, center_x - 4, center_y + 4, center_y + 14, arcade.color.CYAN)
        arcade.draw_lrbt_rectangle_outline(center_x - 14, center_x - 4, center_y + 4, center_y + 14, arcade.color.BLACK, border_width = 2.5)
        #Ojo derecho
        arcade.draw_lrbt_rectangle_filled(center_x + 4, center_x + 14, center_y + 4, center_y + 14, arcade.color.CYAN)
        arcade.draw_lrbt_rectangle_outline(center_x + 4, center_x + 14, center_y + 4, center_y + 14, arcade.color.BLACK, border_width = 2.5)
        #Boca
        arcade.draw_lrbt_rectangle_filled(center_x - 18, center_x + 18, center_y - 14, center_y - 4, arcade.color.CYAN)
        arcade.draw_lrbt_rectangle_outline(center_x - 18, center_x + 18, center_y - 14, center_y - 4, arcade.color.BLACK, border_width = 2.5)

#Funciones de dibujo de fondo
def dibujar_suelo():
    arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, 0, 200, arcade.color.BLUE)

#CLASE CUBO (Hereda de Sprite para poder rotar)
class Cubo(arcade.Sprite):
    def __init__(self, textura):
        """Constructor"""
        super().__init__(textura)

        self.lado = CUBE_SIZE
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = GROUND_HEIGHT + (self.lado / 2) #Lo colocamos justo encima del suelo 

    def update(self):
        """ Método que actualiza la posición, aplica la gravedad y comprueba colisiones del cubo """
        
        #Aplicamos la gravedad
        self.change_y -= GRAVITY
        
        #Actualizamos la posición
        self.center_x += self.change_x
        self.center_y += self.change_y

        #Rotación 180º
        if self.center_y > GROUND_HEIGHT + (self.lado / 2):
            #Si está en el aire, gira (negativo = sentido de las agujas del reloj)
            self.angle -= ROTATION_SPEED
        else:
            #Si toca el suelo, redondeamos el ángulo para que quede totalmente de pie o oca abajo
            self.angle = round(self.angle / 180.0) * 180.0

        #--- Límites de la pantalla ---
        #Izquierda y derecha
        if self.center_x < self.lado / 2:
            self.center_x = self.lado / 2   
        elif self.center_x > SCREEN_WIDTH - self.lado / 2:
            self.center_x = SCREEN_WIDTH - self.lado / 2
        #Suelo
        if self.center_y < GROUND_HEIGHT + (self.lado / 2):
            self.center_y = GROUND_HEIGHT + (self.lado / 2)
            self.change_y = 0 #Frenamos la caída al tocar el suelo
        #Techo    
        elif self.center_y > SCREEN_HEIGHT - self.lado / 2:
            self.center_y = SCREEN_HEIGHT - self.lado / 2
            self.change_y = 0 #Si toca con el techo, deja de subir

class MyGame(arcade.Window):
    """ Clase principal que controla la ventana """

    def __init__(self):
        """ Constructor """
        #Creamos la ventana
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "GEOMETRY DASH")
        #Color de fondo (lo dejamos por si la imagen falla)
        arcade.set_background_color(arcade.color.BABY_BLUE)
        
        self.cubo = None

        #Creamos la lista que guardará nustros sprites
        self.lista_sprites = arcade.SpriteList()

        #Cargamos una imagen para el fondo
        self.textura_fondo =  arcade.load_texture("lab07-control/fondo_geometry_dash.jpg")                                                                                                                                                                                                                                                                                                                                                     
       
        #PARA JUGAR CON UN MANDO
        joysticks = arcade.get_controllers() #Pedimos al sistema operativo una lista de los mandos que están conectados al ordeandor
        if joysticks:
            #Si hay al menos uno, nos guardamos el primero [0]
            self.joystick = joysticks[-1] #Tomamos el primer mando que encontremos 
            self.joystick.open() #Abrimos la comunicación con este mando
            self.joystick.push_handlers() #El mando envía sus señales a la ventana
            print("Mando detectado correctamente.")

            @self.joystick.event
            def on_button_press(controller, button_name):
                """ Se ejecuta cada vez que pulsas un botón del mando """
                if button_name == 'a':
                    if self.cubo.center_y <= GROUND_HEIGHT + (self.cubo.lado / 2):
                        self.cubo.change_y = JUMP_SPEED
                
        else:
            print("No hay mandos conectados.")
            self.joystick = None
    
    def setup(self):
        """ Configuración inicial: Aquí crearemos la textura inicial del cubo """
        self.clear()

        dibujar_cubo_estatico(CUBE_SIZE / 2, CUBE_SIZE / 2, CUBE_SIZE)

        #Le sacamos la foto y creamos el Sprite
        imagen = arcade.get_image(0, 0, CUBE_SIZE, CUBE_SIZE)
        textura = arcade.Texture(imagen)

        self.cubo = Cubo(textura)

        #Metemos el cubo en la lista de sprites
        self.lista_sprites.append(self.cubo)

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(self.textura_fondo, arcade.LBWH(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        # Suelo
        dibujar_suelo()
        #Dibujamos el cubo
        self.lista_sprites.draw()

    def on_key_press(self, key, modifiers):
        """ Función que se llama cada vez que se pulsa una tecla """
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if self.cubo.center_y <= GROUND_HEIGHT + (self.cubo.lado / 2):
                self.cubo.change_y = JUMP_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.cubo.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.cubo.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.cubo.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """ Se ejecuta al solatar una tecla """
        #Solo frenamos el eje X
        #Si frenamos el eje Y, al soltar la tecla el salto se corta
        if key in (arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D):
            self.cubo.change_x = 0  
        
    def on_update(self, delta_time):
        """Lógica del juego, movimiento y rotación"""

        #Movimiento con el mando: (Movimiento horizontal del cubo mediante el joystick izquierdo)
        if self.joystick:
            if self.joystick.leftx < -0.2:
                self.cubo.change_x = -MOVEMENT_SPEED
            elif self.joystick.leftx > 0.2:
                self.cubo.change_x = MOVEMENT_SPEED
            else:
                self.cubo.change_x = 0

        self.cubo.update()

def main():
    window = MyGame()
    window.setup()
    arcade.run()

main()