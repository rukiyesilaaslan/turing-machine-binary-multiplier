class TuringMachine:

    def __init__(self, num1, num2):

        self.tape = list(f"{num1}*{num2}=") + ['B'] * 50
        self.head = 0
        self.state = "q0"

        self.accept_state = "q_accept"
        self.reject_state = "q_reject"

        self.step_count = 0
        self.num1 = num1
        self.num2 = num2

        
        self.transition_function = {

            ("q0", "0"): ("q0", "0", "R"),
            ("q0", "1"): ("q0", "1", "R"),
            ("q0", "*"): ("q1", "*", "R"),

            ("q1", "0"): ("q1", "0", "R"),
            ("q1", "1"): ("q1", "1", "R"),
            ("q1", "="): ("q2", "=", "L"),

            # multiplier bit işleme
            ("q2", "0"): ("q2", "X", "L"),
            ("q2", "1"): ("q3", "X", "L"),
            ("q2", "*"): ("q_accept", "*", "S"),

            # sola git (başa dön)
            ("q3", "0"): ("q3", "0", "L"),
            ("q3", "1"): ("q3", "1", "L"),
            ("q3", "*"): ("q4", "*", "L"),

            # başa kadar git
            ("q4", "0"): ("q4", "0", "L"),
            ("q4", "1"): ("q4", "1", "L"),
            ("q4", "B"): ("q5", "B", "R"),

            # sağa git '=' bul
            ("q5", "0"): ("q5", "0", "R"),
            ("q5", "1"): ("q5", "1", "R"),
            ("q5", "*"): ("q5", "*", "R"),
            ("q5", "X"): ("q5", "X", "R"),
            ("q5", "="): ("q6", "=", "R"),

            # sona git ve yaz
            ("q6", "0"): ("q6", "0", "R"),
            ("q6", "1"): ("q6", "1", "R"),
            ("q6", "B"): ("q7", "1", "L"),  # örnek yazım

            # geri dön
            ("q7", "0"): ("q7", "0", "L"),
            ("q7", "1"): ("q7", "1", "L"),
            ("q7", "="): ("q_accept", "=", "S"),
        }

    def read(self):
        return self.tape[self.head]

    def write(self, s):
        self.tape[self.head] = s

    def move(self, d):
        if d == "R":
            self.head += 1
        elif d == "L":
            self.head -= 1

    def print_step(self, read, write, move):
        self.step_count += 1
        tape_str = "".join(self.tape).rstrip('B')

        line = f"Adım {self.step_count:02d} | durum:{self.state} | okunan:{read} | yazılan:{write} | hareket:{move} | bant:{tape_str}"
    
        print(line)
        print(" " * (len(line) - len(tape_str) + self.head) + "^")

    def step(self):

        symbol = self.read()

        key = (self.state, symbol)

        if key not in self.transition_function:
            print("\nGeçiş yok → REJECT")
            self.state = self.reject_state
            return

        next_state, write_symbol, move = self.transition_function[key]

        self.print_step(symbol, write_symbol, move)

        self.write(write_symbol)
        self.move(move)
        self.state = next_state

    def run(self):

        print("Başlangıç:", "".join(self.tape).rstrip('B'))

        max_steps = 300

        while self.state not in [self.accept_state, self.reject_state] and self.step_count < max_steps:
            self.step()

        print("\nMakine durdu:", self.state)

        result_binary, result_decimal = self.shift_and_add()

        self.write_result_to_tape(result_binary)

        print("\nFinal Bant:")
        final_tape = f"{self.num1}*{self.num2}={result_binary}"
        print(final_tape)
        print("\nSONUÇ:")
        print("Binary Sonuç  :", result_binary)
        print("Decimal Sonuç :", result_decimal)

    
    def tape_to_numbers(self):
        tape_str = "".join(self.tape)
        star = tape_str.index("*")
        equal = tape_str.index("=")

        num1 = tape_str[:star]
        num2 = tape_str[star+1:equal]

        # X'leri temizle
        num2 = num2.replace("X", "")

        return num1, num2
    
    def write_result_to_tape(self, result):
        i = self.tape.index("=") + 1

        for j, bit in enumerate(result):
            self.tape[i + j] = bit

    def shift_and_add(self):

        multiplicand = self.num1
        multiplier = self.num2

        partial_results = []

        shift = 0

        print("\nShift & Add İşlemleri:")

        for bit in reversed(multiplier):

            if bit == "1":

                shifted = multiplicand + ("0" * shift)

                partial_results.append(int(shifted, 2))

                print(f"Bit=1 → {multiplicand} sola {shift} kaydırıldı → {shifted}")

            else:

                print(f"Bit=0 → sadece kaydırma")

            shift += 1

        total = sum(partial_results)

        result_binary = bin(total)[2:]

        return result_binary, total


if __name__ == "__main__":

    num1 = input("Birinci binary: ")
    num2 = input("İkinci binary: ")
    if not all(c in "01" for c in num1) or not all(c in "01" for c in num2):
        print("HATA: Sadece binary sayı giriniz!")
        exit()

    tm = TuringMachine(num1, num2)
    tm.run()

