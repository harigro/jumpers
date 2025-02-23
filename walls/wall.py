class Object:
    def __init__(self, x: int, y: int, size: tuple[int, int]):
        """Inisialisasi objek dengan posisi, ukuran, dan atribut lainnya."""
        self._ox = x
        self._oy = y
        self._osize = size

    @property
    def get_size(self) -> tuple[int, int]:
        """Mengambil nilai size saat ini"""
        return self._osize
    
    @get_size.setter
    def set_size(self, new_size: tuple[int, int]):
        """Mengedit nilai size saat ini"""
        self._osize = new_size