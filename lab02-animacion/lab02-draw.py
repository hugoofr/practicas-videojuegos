import arcade

# --- Configuración de la Ventana ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Desierto con lrbt_rectangle - Arcade 3.3.3"

def dibujar_suelo():
    """Dibuja el suelo usando bordes: Izquierda, Derecha, Abajo, Arriba."""
    # Izquierda=0, Derecha=800, Abajo=0, Arriba=200
    arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, 0, 200, arcade.color.SANDY_BROWN)

def dibujar_sol(x, y, escala):
    """Dibuja el sol."""
    radio = 40 * escala
    arcade.draw_circle_filled(x, y, radio, arcade.color.YELLOW)
    arcade.draw_circle_outline(x, y, radio, arcade.color.ORANGE, 2 * escala)

def dibujar_piramide(x, y, escala):
    """Dibuja una pirámide."""
    ancho_medio = 100 * escala
    altura = 200 * escala
    arcade.draw_triangle_filled(
        x - ancho_medio, y,
        x + ancho_medio, y,
        x, y + altura,
        arcade.color.BROWN
    )

def dibujar_cactus(x, y, escala):
    """Dibuja un cactus usando draw_lrbt_rectangle_filled para el tronco."""
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
    """Dibuja una piedra."""
    arcade.draw_ellipse_filled(x, y, 80 * escala, 40 * escala, arcade.color.GRAY)

def main():
    # Abrir ventana y configurar fondo
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)
    
    # Iniciar renderizado
    arcade.start_render()

    # --- Llamadas a las funciones ---
    dibujar_suelo()
    
    dibujar_sol(700, 525, 1.0)
    
    dibujar_piramide(200, 200, 1.0)
    dibujar_piramide(400, 200, 0.6)
    
    dibujar_cactus(650, 200, 1.2)
    dibujar_cactus(100, 180, 0.7)
    
    dibujar_piedra(550, 100, 1.0)
    dibujar_piedra(720, 120, 0.5)

    # Finalizar
    arcade.finish_render()
    arcade.run()

if __name__ == "__main__":
    main()
