from typing import Union
from walls.wall import Object
import pygame

# Inisialisasi Pygame
pygame.init()

# Konstanta layar
WIDTH, HEIGHT = 700, 500
BACKGROUND_COLOR = (30, 30, 30)

# Warna dan ukuran kotak
BOX_COLOR = (0, 255, 0)
BOX_SIZE = 50
FLOOR_Y = HEIGHT - BOX_SIZE  # Posisi lantai

# FPS
FPS = 60
clock = pygame.time.Clock()

# Buat layar game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jumpers")


class Box:
    """Kelas untuk merepresentasikan kotak yang bisa bergerak dan melompat."""

    def __init__(self, x: int, y: int, size: tuple[int, int]):
        """Inisialisasi kotak dengan posisi, ukuran, dan atribut lainnya."""
        self.rect = pygame.Rect(x, y, size[0], size[1])
        self.velocity_y = 0
        self.on_ground = True

    def apply_gravity(self, velocity: Union[int, float]):
        """Menambahkan efek gravitasi ke kotak."""
        self.velocity_y += velocity  # Tambahkan gravitasi ke kecepatan vertikal
        self.rect.y += self.velocity_y  # Gerakkan kotak ke bawah

        # Cegah kotak jatuh melewati lantai
        if self.rect.bottom >= FLOOR_Y:
            self.rect.bottom = FLOOR_Y
            self.velocity_y = 0
            self.on_ground = True

    def jump(self, velocity: int):
        """Mengatur lompatan saat tombol spasi ditekan."""
        if self.on_ground:
            self.velocity_y = -velocity  # Dorong ke atas
            self.on_ground = False

    def move(self, direction: str, velocity: int):
        """Menggerakkan kotak ke kiri atau kanan."""
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= velocity
        elif direction == "right" and self.rect.right < WIDTH:
            self.rect.x += velocity

    def draw(self, surface: pygame.display):
        """Menggambar kotak di layar."""
        pygame.draw.rect(surface, BOX_COLOR, self.rect)

class BoxWall(Object):

    jalan = 0
    
    def __init__(self, x: int, y: int, size: tuple[int, int]):
        """Inisialisasi kotak dengan posisi, ukuran, dan atribut lainnya."""
        super().__init__(x=x, y=y, size=size)

    def move_left(self, velocity: int, batas: int):
        """Menggerakkan kotak pembatas ke kiri dan mengulang ke kanan jika keluar dari layar."""
        self.jalan -= velocity
        if self.jalan <= -batas:  # Reset posisi setelah keluar dari layar
            self.jalan = 0

    def draws_split(self, surface: pygame.display, color: tuple[int, int, int], split: int):
        """Menggambar beberapa kotak pembatas di layar dan mengulang setelah keluar."""
        for i in range(0, WIDTH + BOX_SIZE, BOX_SIZE):
            pygame.draw.rect(surface, color, pygame.Rect(i + self.jalan, self._oy, self._osize[0] - split, self._osize[1]))

    def draw_split(self, surface: pygame.display, color: tuple[int, int, int], split: int):
        """Menggambar satu kotak pembatas di layar dan mengulang setelah keluar."""
        pygame.draw.rect(surface, color, pygame.Rect(self._ox + self.jalan, self._oy, self._osize[0] - split, self._osize[1]))

    def draws(self, surface: pygame.display, color: tuple[int, int, int]):
        """Menggambar beberapa kotak di layar."""
        for i in range(0, WIDTH, BOX_SIZE):
            pygame.draw.rect(surface, color, pygame.Rect(i, self._oy, self._osize[0], self._osize[1]))        

    def draw(self, surface: pygame.display, color: tuple[int, int, int]):
        """Menggambar kotak di layar."""
        pygame.draw.rect(surface, color, pygame.Rect(self._ox, self._oy, self._osize[0], self._osize[1]))

def main():
        
    # Buat objek kotak
    box = Box(x=BOX_SIZE, y=FLOOR_Y, size=(BOX_SIZE, BOX_SIZE))
    tembok = BoxWall(x=(WIDTH//2), y=FLOOR_Y, size=(BOX_SIZE, BOX_SIZE))
    tembok_rintangan = BoxWall(x=WIDTH, y=FLOOR_Y-BOX_SIZE, size=(BOX_SIZE, BOX_SIZE))

    # Loop utama
    running = True
    while running:
        # Cek event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Ambil input dari keyboard
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            box.move("left", 5)
        if keys[pygame.K_RIGHT]:
            box.move("right", 5)
        if keys[pygame.K_SPACE]:  # Panggil metode jump() jika tombol spasi ditekan
            box.jump(15)

        # Terapkan gravitasi
        box.apply_gravity(0.5)

        # Gerakkan dinding ke kiri
        tembok.move_left(1, BOX_SIZE)
        tembok_rintangan.move_left(2, (WIDTH+BOX_SIZE))

        # Gambar ulang layar
        screen.fill(BACKGROUND_COLOR)
        box.draw(surface=screen)
        tembok.draws(surface=screen, color=(150, 255, 160))
        tembok.draws_split(surface=screen, color=(158, 105, 108), split=5)
        tembok_rintangan.draw_split(surface=screen, color=(158, 105, 108), split=5)

        # atur fps
        clock.tick(FPS)
        pygame.display.update()

    # Keluar dari game
    pygame.quit()

if __name__=="__main__":
    main()
