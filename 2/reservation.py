import csv
import os


FARE_PER_TICKET = 50
class Train:
    def __init__(self, train_id, train_name, source_station, destination_station, total_seats):
        self.train_id = train_id
        self.train_name = train_name
        self.source_station = source_station
        self.destination_station = destination_station
        self.total_seats = int(total_seats)
        self.available_seats = self.total_seats
        self.revenue = 0

    def check_availability(self, num_tickets):
        return self.available_seats >= num_tickets

    def book_tickets(self, num_tickets):
        if self.check_availability(num_tickets):
            self.available_seats -= num_tickets
            fare = num_tickets * FARE_PER_TICKET
            self.revenue += fare
            return fare
        else:
            return None

def load_train_data(filepath):
    trains = {}
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return trains
    with open(filepath, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            train = Train(
                row['Train ID'],
                row['Train Name'],
                row['Source Station'],
                row['Destination Station'],
                row['Total Seats']
            )
            trains[train.train_id] = train
    return trains

def load_passenger_data(filepath, trains):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
    with open(filepath, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            train_id = row['Train ID']
            if train_id in trains:
                train = trains[train_id]
                num_tickets = int(row['Number of Tickets'])
                fare = train.book_tickets(num_tickets)
                if fare is not None:
                    print(f"Booking confirmed for {row['Passenger Name']} on Train {train.train_name}. Total fare: ${fare}.")
                else:
                    print(f"Insufficient seats for {row['Passenger Name']} on Train {train.train_name}.")
            else:
                print(f"Train ID {train_id} not found.")

def generate_reports(trains):

    print("\nReport 1: Train Details")
    print(f"{'Train ID':<15} {'Train Name':<20} {'Source':<15} {'Destination':<15} {'Total Seats':<15} {'Available Seats':<15}")
    for train in trains.values():
        print(f"{train.train_id:<15} {train.train_name:<20} {train.source_station:<15} {train.destination_station:<15} {train.total_seats:<15} {train.available_seats:<15}")

    print("\nReport 2: Revenue Details")
    print(f"{'Train ID':<15} {'Train Name':<20} {'Revenue':<10}")
    for train in trains.values():
        print(f"{train.train_id:<15} {train.train_name:<20} ${train.revenue:<10}")

def main():
    data_folder = '2\data'
    train_file = os.path.join(data_folder, 'train.csv')
    passenger_file = os.path.join(data_folder, 'passengers.csv')

    trains = load_train_data(train_file)
    load_passenger_data(passenger_file, trains)
    generate_reports(trains)

if __name__ == "__main__":
    main()
