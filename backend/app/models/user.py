class user:
    def __init__(self, username: str, email: str):
        self._username = username
        self._email = email
        self._posts = []

    def get_info(self):
        return f"Username: {self._username}, Email: {self._email}"
    def set_email(self, new_email):
        self._email = new_email
    def set_username(self, new_username):
        self._username = new_username
    def __repr__(self):
        return f"user(username={self._username}, email={self._email})"

    def crear_post(self, titulo: str, descripcion: str, contenido: str):
        from backend.app.models.post import post
        nuevo_post = post(self._username, titulo, descripcion, contenido)
        self._posts.append(nuevo_post)
        print(f"--- El usuario '{self._username}' ha creado el post: '{titulo}' ---")
        return nuevo_post