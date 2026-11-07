from core.errors import ApiError
from models import Artista, Cancion, EstadoCancion, Usuario
from repositories.artista_repository import ArtistaRepository
from repositories.cancion_repository import CancionRepository
from schemas.cancion import CancionEntrada, CancionSalida


class CancionService:
    def __init__(self, canciones: CancionRepository, artistas: ArtistaRepository):
        self.canciones = canciones
        self.artistas = artistas

    def listar(self, usuario: Usuario) -> list[CancionSalida]:
        return [self._a_salida(c) for c in self.canciones.listar_de_usuario(usuario.id)]

    def obtener(self, cancion_id: int, usuario: Usuario) -> CancionSalida:
        return self._a_salida(self._buscar(cancion_id, usuario))

    def crear(self, datos: CancionEntrada, usuario: Usuario) -> CancionSalida:
        cancion = Cancion(usuario_id=usuario.id)
        self._copiar_datos(cancion, datos)
        return self._a_salida(self.canciones.guardar(cancion))

    def reemplazar(self, cancion_id: int, datos: CancionEntrada, usuario: Usuario) -> CancionSalida:
        cancion = self._buscar(cancion_id, usuario)
        self._copiar_datos(cancion, datos)
        return self._a_salida(self.canciones.guardar(cancion))

    def eliminar(self, cancion_id: int, usuario: Usuario):
        self.canciones.eliminar(self._buscar(cancion_id, usuario))

    def _buscar(self, cancion_id: int, usuario: Usuario) -> Cancion:
        cancion = self.canciones.buscar_de_usuario(cancion_id, usuario.id)
        if cancion is None:
            raise ApiError(404, "NO_ENCONTRADA", "La canción no existe")
        return cancion

    def _artista(self, nombre: str) -> Artista:
        return self.artistas.buscar_por_nombre(nombre) or self.artistas.crear(nombre)

    def _copiar_datos(self, cancion: Cancion, datos: CancionEntrada):
        artista = self._artista(datos.artista)
        cancion.titulo = datos.titulo
        cancion.artista = artista
        cancion.tonalidad = datos.tonalidad
        cancion.bpm = datos.bpm
        cancion.duracion_min = datos.duracion_min
        cancion.fecha_ensayo = datos.fecha_ensayo
        cancion.estado = EstadoCancion(datos.estado)
        cancion.letra = datos.letra
        self.canciones.reemplazar_acordes(cancion, datos.acordes)

    def _a_salida(self, cancion: Cancion) -> CancionSalida:
        return CancionSalida(
            id=cancion.id,
            titulo=cancion.titulo,
            artista=cancion.artista.nombre,
            tonalidad=cancion.tonalidad,
            bpm=cancion.bpm,
            duracion_min=float(cancion.duracion_min),
            fecha_ensayo=cancion.fecha_ensayo,
            estado=cancion.estado.value,
            acordes=[a.acorde for a in cancion.acordes],
            letra=cancion.letra,
        )
