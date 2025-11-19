"""
Módulo de estilos y colores para la interfaz
Define colores modernos y estilos consistentes
"""

# Paleta de colores moderna
COLORS = {
    # Colores principales
    'primary': '#2C3E50',      # Azul oscuro elegante
    'secondary': '#3498DB',    # Azul claro
    'success': '#27AE60',      # Verde
    'warning': '#F39C12',      # Naranja
    'danger': '#E74C3C',       # Rojo
    'info': '#3498DB',         # Azul info
    
    # Colores de fondo
    'bg_main': '#ECF0F1',      # Gris claro
    'bg_card': '#FFFFFF',      # Blanco
    'bg_light': '#F8F9FA',     # Gris muy claro
    'bg_dark': '#34495E',      # Gris oscuro
    
    # Colores de texto
    'text_primary': '#2C3E50',
    'text_secondary': '#7F8C8D',
    'text_light': '#FFFFFF',
    
    # Colores de estado
    'mesa_libre': '#2ECC71',   # Verde claro
    'mesa_reservada': '#E74C3C', # Rojo
    'mesa_ocupada': '#F39C12',  # Naranja
    'mesa_seleccionada': '#3498DB', # Azul
    
    # Colores hover
    'hover_primary': '#1A252F',
    'hover_success': '#229954',
    'hover_danger': '#C0392B',
    'hover_warning': '#D68910',
}

# Iconos Unicode (emojis)
ICONS = {
    'usuario': '👤',
    'candado': '🔒',
    'registro': '📝',
    'mesa': '🪑',
    'añadir': '➕',
    'editar': '✏️',
    'eliminar': '🗑️',
    'buscar': '🔍',
    'confirmar': '✅',
    'cancelar': '❌',
    'info': 'ℹ️',
    'warning': '⚠️',
    'error': '❌',
    'exito': '✅',
    'admin': '👨‍💼',
    'cliente': '👤',
    'restaurante': '🍽️',
    'ubicacion': '📍',
    'personas': '👥',
}

# Estilos de fuente
FONTS = {
    'title': ('Segoe UI', 18, 'bold'),
    'subtitle': ('Segoe UI', 14, 'bold'),
    'body': ('Segoe UI', 11),
    'small': ('Segoe UI', 9),
    'button': ('Segoe UI', 11, 'bold'),
}

def get_button_style(bg_color, hover_color=None):
    """Retorna estilo para botones"""
    if hover_color is None:
        hover_color = COLORS['hover_primary']
    
    return {
        'bg': bg_color,
        'fg': COLORS['text_light'],
        'activebackground': hover_color,
        'activeforeground': COLORS['text_light'],
        'relief': 'flat',
        'bd': 0,
        'padx': 15,
        'pady': 8,
        'cursor': 'hand2',
        'font': FONTS['button']
    }

def get_entry_style():
    """Retorna estilo para campos de entrada"""
    return {
        'font': FONTS['body'],
        'relief': 'flat',
        'bd': 2,
        'highlightthickness': 1,
        'highlightbackground': COLORS['secondary'],
        'highlightcolor': COLORS['secondary'],
        'bg': COLORS['bg_card'],
    }

