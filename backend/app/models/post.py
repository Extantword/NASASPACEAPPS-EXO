class post:
    def __init__(self, autor: str, titulo: str, descripcion: str, contenido: str):
        self.autor = autor
        self.titulo = titulo
        self.descripcion = descripcion
        self.contenido = contenido

    def get_summary(self):
        return f"Post by {self.autor}: {self.titulo}"

    def getAutor(self):
        return self.autor
    def getTitulo(self):
        return self.titulo
    def getDescripcion(self):
        return self.descripcion
    def getContenido(self):
        return self.contenido

    def obtener(self):
        print("\n================================")
        print(f"Título: {self.titulo}")
        print(f"Autor: {self.autor.name}")
        print("--------------------------------")
        print(f"Descripción: {self.descripcion}")
        print(f"Contenido: {self.contenido}")
        print("================================")
    