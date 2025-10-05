import sys
from io import StringIO

def intercept_prints(callback_function):
    """Decorador que intercepta prints y ejecuta una función con cada uno"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Guardar stdout original
            original_stdout = sys.stdout
            
            class PrintInterceptor(StringIO):
                def write(self, text):
                    # Ignorar strings vacíos y solo newlines
                    if text and text != '\n':
                        callback_function(text)
                    # También escribir a stdout original si quieres mantener el print visible
                    original_stdout.write(text)
                    return len(text)
            
            # Reemplazar stdout temporalmente
            sys.stdout = PrintInterceptor()
            
            try:
                result = func(*args, **kwargs)
            finally:
                # Restaurar stdout original
                sys.stdout = original_stdout
            
            return result
        return wrapper
    return decorator

# Función que procesa cada print
def procesar_print(texto):
    print(f"[INTERCEPTADO] {texto}")