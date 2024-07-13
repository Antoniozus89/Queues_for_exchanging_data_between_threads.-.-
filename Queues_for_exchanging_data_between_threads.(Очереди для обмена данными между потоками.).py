import time
import queue
import threading

class Table:
    def __init__(self, number):
        self.number = number
        self.is_busy = False

class Cafe:
    def __init__(self, tables):
        self.queue = queue.Queue()
        self.tables = tables
        self.customer_count = 0
        self.customer_threads = []

    def customer_arrival(self):
        while self.customer_count < 20:
            self.customer_count += 1
            customer = Customer(self.customer_count, self)
            print(f"Посетитель номер {self.customer_count} прибыл.")
            self.serve_customer(customer)
            time.sleep(1)

    def serve_customer(self, customer):
        for table in self.tables:
            if not table.is_busy:
                table.is_busy = True
                print(f"Посетитель номер {customer.number} сел за стол {table.number}.")
                customer.table = table
                customer_thread = threading.Thread(target=customer.run)
                customer_thread.start()
                self.customer_threads.append(customer_thread)
                return
        print(f"Посетитель номер {customer.number} ожидает свободный стол.")
        self.queue.put(customer)

    def release_table(self, table):
        table.is_busy = False
        if not self.queue.empty():
            customer = self.queue.get()
            self.serve_customer(customer)

class Customer:
    def __init__(self, number, cafe):
        self.number = number
        self.cafe = cafe
        self.table = None

    def run(self):
        time.sleep(6)
        print(f"Посетитель номер {self.number} покушал и ушёл.")
        self.cafe.release_table(self.table)


def main():
    table1 = Table(1)
    table2 = Table(2)
    table3 = Table(3)
    tables = [table1, table2, table3]

    cafe = Cafe(tables)

    customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
    customer_arrival_thread.start()
    customer_arrival_thread.join()

    for t in cafe.customer_threads:
        t.join()

if __name__ == "__main__":
    main()