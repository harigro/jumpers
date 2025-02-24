class DataWall:
    def __init__(self, comb: tuple[int, int]):
        """Kelas untuk mengantur ketinggian dan posisi sumbu y rintangan agar selaras dengan lantai"""
        self.comb = comb

    def height_axis_y(self, stop: int, step: int) -> dict[int, int]:
        """Membuat diktonari dari tinggi dan posisi sumbu y"""
        tinggi = [t for t in range(self.comb[0], stop, step)]
        sumbu_y = [y for y in range(self.comb[1], stop, step)]
        return dict(zip(tinggi, sumbu_y))
