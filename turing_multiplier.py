class TuringMachine:

    def __init__(self, num1, num2):

        # Başlangıç ve özel durumlar
        self.accept_state = "q_accept"
        self.reject_state = "q_reject"

        # Durum kümesi
        self.states = {
            "q0",          # başlangıç
            "q1",          # '*' arama
            "q2",          # operand ayırma
            "q3",          # shift işlemi
            "q4",          # toplama işlemi
            "q_accept",    # kabul
            "q_reject"     # red
        }

        # Giriş alfabesi
        self.input_alphabet = {'0', '1'}

        # Bant alfabesi
        self.tape_alphabet = {'0', '1', '*', '=', 'B'}

        # Geçiş fonksiyonu (örnek temsil)
        self.transition_function = {

            ("q0", "0"): ("q0", "0", "R"),
            ("q0", "1"): ("q0", "1", "R"),

            ("q0", "*"): ("q1", "*", "R"),

            ("q1", "0"): ("q1", "0", "R"),
            ("q1", "1"): ("q1", "1", "R"),

            ("q1", "="): ("q2", "=", "L")

        }

        # Binary kontrolü
        if not self.is_binary(num1) or not self.is_binary(num2):

            self.state = self.reject_state

            print("\nHATA: Girdiler sadece 0 ve 1 içermelidir!")
            print("Makine q_reject durumunda durdu.")

            exit()

        self.num1 = num1
        self.num2 = num2

        # Bant oluşturma
        self.tape = list(f"{num1}*{num2}=") + ['B'] * 50

        # Kafa pozisyonu
        self.head = 0

        # Başlangıç durumu
        self.state = "q0"

        # Adım sayacı
        self.step = 0

    # Binary kontrol fonksiyonu
    def is_binary(self, s):
        return all(c in "01" for c in s)

    # Mevcut sembolü oku
    def read_symbol(self):
        return self.tape[self.head]

    # Banda yaz
    def write_symbol(self, symbol):
        self.tape[self.head] = symbol

    # Sağa hareket
    def move_right(self):
        self.head += 1

    # Sola hareket
    def move_left(self):
        self.head -= 1

    # Bandı yazdır
    def print_tape(self):

        tape_str = "".join(self.tape).rstrip('B')

        print("\nBant :", tape_str)

        pointer = " " * self.head + "^"
        print("       ", pointer)

        print("Durum :", self.state)

    # Adım bilgisi yazdır
    def print_step(self, read_char, write_char, move):

        self.step += 1

        print("\n===================================")
        print(f"ADIM {self.step}")
        print("===================================")

        print("Mevcut Durum :", self.state)
        print("Okunan Sembol:", read_char)
        print("Yazılan Sembol:", write_char)
        print("Kafa Hareketi:", move)

        self.print_tape()

    # '*' karakterini bul
    def find_delimiter(self):

        self.state = "q1"

        print("\n--- '*' karakteri aranıyor ---")

        while self.read_symbol() != "*":

            current_symbol = self.read_symbol()

            self.print_step(current_symbol, current_symbol, "R")

            self.move_right()

        print("\n'*' karakteri bulundu!")
        print("Head Pozisyonu:", self.head)

    # Operandları ayır
    def separate_operands(self):

        self.state = "q2"

        tape_str = "".join(self.tape)

        star_index = tape_str.index("*")
        equal_index = tape_str.index("=")

        first_number = tape_str[:star_index]
        second_number = tape_str[star_index + 1:equal_index]

        print("\n===================================")
        print("OPERAND AYRIŞTIRMA")
        print("===================================")

        print("Birinci Sayı :", first_number)
        print("İkinci Sayı  :", second_number)

        return first_number, second_number

    # Shift & Add binary çarpma
    def binary_multiply(self):

        self.state = "q3"

        multiplicand = self.num1
        multiplier = self.num2

        result = 0

        shift = 0

        print("\n===================================")
        print("SHIFT & ADD BAŞLADI")
        print("===================================")

        for bit in reversed(multiplier):

            self.step += 1

            print("\n===================================")
            print(f"ADIM {self.step}")
            print("===================================")

            print("İşlenen Bit:", bit)

            if bit == '1':

                self.state = "q4"

                shifted_value = int(multiplicand, 2) << shift

                shifted_binary = bin(shifted_value)[2:]

                print(f"{multiplicand} sola {shift} kaydırıldı")

                print("Kaydırılmış Değer :", shifted_binary)

                result += shifted_value

                print("Ara Sonuç :", bin(result)[2:])

            else:

                print("Bit 0 olduğu için toplama yapılmadı")

            shift += 1

        return bin(result)[2:]

    # Makineyi çalıştır
    def run(self):

        print("\n===================================")
        print("TURING MAKİNESİ BAŞLATILDI")
        print("===================================")

        self.print_tape()

        # '*' karakterini bul
        self.find_delimiter()

        # Operandları ayır
        self.separate_operands()

        # Binary çarpma işlemi
        result_binary = self.binary_multiply()

        # Kabul durumu
        self.state = self.accept_state

        print("\n===================================")
        print("SONUÇ")
        print("===================================")

        print("Giriş İfadesi :", f"{self.num1} * {self.num2}")

        print("Binary Sonuç  :", result_binary)

        print("Decimal Sonuç :", int(result_binary, 2))

        print("\nMakine q_accept durumunda durdu.")


# Program başlangıcı
if __name__ == "__main__":

    num1 = input("Birinci binary sayıyı girin: ")
    num2 = input("İkinci binary sayıyı girin: ")

    tm = TuringMachine(num1, num2)

    tm.run()