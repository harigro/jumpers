from walls.wall import Object
from walls.data_wall import DataWall
from screen import SETTINGS, COLORS
from typing import Union
from random import choice, sample
import pygame

# Inisialisasi Pygame
pygame.init()

# Buat layar game penuh
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# Konstanta layar
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
# Warna dan ukuran kotak
FLOOR_Y = HEIGHT - SETTINGS.box_size  # Posisi lantai
# atur FPS
clock = pygame.time.Clock()


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

    def draw(self, surface: pygame.display, color: tuple[int, int, int]):
        """Menggambar kotak di layar."""
        pygame.draw.rect(surface, color, self.rect)

class BoxWall(Object):
    def __init__(self, x: int, y: int, size: tuple[int, int]):
        """Inisialisasi kotak dengan posisi, ukuran, dan atribut lainnya."""
        super().__init__(x=x, y=y, size=size)
        self.jalan = 0

    def rect_wall(self) -> pygame.Rect:
        """Mengembalikan objek pygame.Rect dari kotak pembatas."""
        return pygame.Rect(self._ox + self.jalan, self._oy, self._osize[0], self._osize[1])

    def move_left(self, velocity: int, batas: int):
        """Menggerakkan kotak pembatas ke kiri dan mengulang ke kanan jika keluar dari layar."""
        self.jalan -= velocity
        if self.jalan <= -batas:  # Reset posisi setelah keluar dari layar
            self.jalan = 0

    def draws_split(self, surface: pygame.display, color: tuple[int, int, int], split: int):
        """Menggambar beberapa kotak pembatas di layar dan mengulang setelah keluar."""
        for i in range(0, WIDTH + SETTINGS.box_size, SETTINGS.box_size):
            pygame.draw.rect(surface, color, pygame.Rect(i + self.jalan, self._oy, self._osize[0] - split, self._osize[1]))

    def draw_split(self, surface: pygame.display, color: tuple[int, int, int]):
        """Menggambar satu kotak pembatas di layar dan mengulang setelah keluar."""
        pygame.draw.rect(surface, color, self.rect_wall())

    def draws(self, surface: pygame.display, color: tuple[int, int, int]):
        """Menggambar beberapa kotak di layar."""
        for i in range(0, WIDTH, SETTINGS.box_size):
            pygame.draw.rect(surface, color, pygame.Rect(i, self._oy, self._osize[0], self._osize[1]))        

    def draw(self, surface: pygame.display, color: tuple[int, int, int]):
        """Menggambar kotak di layar."""
        pygame.draw.rect(surface, color, pygame.Rect(self._ox, self._oy, self._osize[0], self._osize[1]))

def main():
        
    # Buat objek kotak
    box = Box(x=SETTINGS.box_size, y=FLOOR_Y, size=(SETTINGS.box_size, SETTINGS.box_size))
    # tembok penghalang
    data_rintangan = DataWall((100, 50)).height_axis_y(200, 10) # data tinggi dan posisi rintangan
    acak_awal = sample(list(data_rintangan.keys()), 3) # memastikan agar data yang diambil benar-benar tidak sama
    tembok_lantai = BoxWall(x=(WIDTH//2), y=FLOOR_Y, size=(SETTINGS.box_size, SETTINGS.box_size))
    tembok_rintangan = (
        BoxWall(x=WIDTH+(SETTINGS.box_size*2), y=FLOOR_Y-SETTINGS.box_size-(data_rintangan[acak_awal[0]]), size=(SETTINGS.box_size, acak_awal[0])),
        BoxWall(x=WIDTH+(SETTINGS.box_size*2), y=FLOOR_Y-SETTINGS.box_size-(data_rintangan[acak_awal[1]]), size=(SETTINGS.box_size, acak_awal[1])),
        BoxWall(x=WIDTH+(SETTINGS.box_size*2), y=FLOOR_Y-SETTINGS.box_size-(data_rintangan[acak_awal[2]]), size=(SETTINGS.box_size, acak_awal[2]))
    )

    # skor
    skor = SETTINGS.skor
    fon = pygame.font.Font(None, 50)
    
    # Loop utama
    running = True
    while running:
        # Cek event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # keluar dari game dengan tombol ESC
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
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
        tembok_lantai.move_left(1, SETTINGS.box_size)
        tembok_rintangan[0].move_left(choice([4, 5, 6]), (WIDTH+SETTINGS.box_size*3))
        tembok_rintangan[1].move_left(choice([6, 7, 8]), (WIDTH+SETTINGS.box_size*3))
        tembok_rintangan[2].move_left(choice([2, 3, 4]), (WIDTH+SETTINGS.box_size*3))
        # tinggi rintangan
        tinggi_rintangan = choice(list(data_rintangan.keys()))

        # cek tabrakan dengan box dan saat keluar dari lebar layar
        for r in tembok_rintangan:
            if box.rect.colliderect(r.rect_wall()):
                running = False
            if r.jalan == 0:
                skor += 1
                r.set_size = SETTINGS.box_size, tinggi_rintangan
                if r.get_size == (SETTINGS.box_size, tinggi_rintangan):
                    r.set_oy = FLOOR_Y-SETTINGS.box_size-data_rintangan[tinggi_rintangan]

        # Gambar ulang layar
        screen.fill(COLORS.background_color)
        box.draw(surface=screen, color=COLORS.box_color)
        tembok_lantai.draws(surface=screen, color=COLORS.boxs_color)
        tembok_lantai.draws_split(surface=screen, color=COLORS.box_splits_color, split=5)
        tembok_rintangan[0].draw_split(surface=screen, color=COLORS.box_split_color)
        tembok_rintangan[1].draw_split(surface=screen, color=COLORS.box_split_color)
        tembok_rintangan[2].draw_split(surface=screen, color=COLORS.box_split_color)
        teks = fon.render(f"Skor : {skor}", True, COLORS.font_color)
        teks_rect = teks.get_rect(center=(SETTINGS.posisi_fon, SETTINGS.posisi_fon))
        screen.blit(teks, teks_rect)

        
        # atur fps
        clock.tick(SETTINGS.fps)
        pygame.display.update()

    # Keluar dari game
    pygame.quit()

if __name__=="__main__":
    main()
