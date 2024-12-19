import sqlite3
from datetime import datetime
import hashlib
import os

class Database:
    def __init__(self, db_name='airline_system.db'):
        self.db_name = db_name
        self.create_tables()
        # Проверяем, есть ли уже данные в таблицах
        if self.is_database_empty():
            self.insert_sample_data()
    
    def create_tables(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Создание таблицы users
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            login VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            salt BLOB NOT NULL,
            role VARCHAR(20) DEFAULT 'user'
        )
        ''')
        
        # Check if admin exists
        cursor.execute('SELECT * FROM users WHERE login = ?', ('admin',))
        if not cursor.fetchone():
            # Хешируем пароль администратора
            admin_password = 'admin123'
            hashed_password, salt = self.hash_password(admin_password)
            cursor.execute('''
            INSERT INTO users (login, email, password, salt, role)
            VALUES (?, ?, ?, ?, ?)
            ''', ('admin', 'admin@example.com', hashed_password, salt, 'admin'))

        # Create Airlines table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Airlines (
            AirlineID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name VARCHAR(100) NOT NULL,
            IATA_Code VARCHAR(3),
            ContactInfo VARCHAR(255)
        )
        ''')
        
        # Create Country table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Country (
            CountryID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name VARCHAR(255) NOT NULL
        )
        ''')
        
        # Create City table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS City (
            CityID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name VARCHAR(255) NOT NULL,
            CountryID INTEGER,
            FOREIGN KEY (CountryID) REFERENCES Country(CountryID)
        )
        ''')
        
        # Create Airports table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Airports (
            AirportID INTEGER PRIMARY KEY AUTOINCREMENT,
            AirportName VARCHAR(100) NOT NULL,
            CityID INTEGER,
            IATA_Code VARCHAR(3),
            FOREIGN KEY (CityID) REFERENCES City(CityID)
        )
        ''')
        
        # Create Flights table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Flights (
            FlightID INTEGER PRIMARY KEY AUTOINCREMENT,
            AirlineID INTEGER,
            DepartureDate DATETIME,
            ArrivalDate DATETIME,
            OriginAirportID INTEGER,
            DestinationAirportID INTEGER,
            Price REAL(10,2),
            AvailableSeats INTEGER DEFAULT 100,
            FOREIGN KEY (AirlineID) REFERENCES Airlines(AirlineID),
            FOREIGN KEY (OriginAirportID) REFERENCES Airports(AirportID),
            FOREIGN KEY (DestinationAirportID) REFERENCES Airports(AirportID)
        )
        ''')
        
        # Create Purchased Tickets table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS PurchasedTickets (
            TicketID INTEGER PRIMARY KEY AUTOINCREMENT,
            FlightID INTEGER,
            UserID INTEGER,
            PurchaseDate DATETIME DEFAULT CURRENT_TIMESTAMP,
            PassengerName VARCHAR(100),
            PassengerEmail VARCHAR(100),
            PassengerPhone VARCHAR(20),
            SeatNumber VARCHAR(10),
            Status VARCHAR(20) DEFAULT 'active',
            FOREIGN KEY (FlightID) REFERENCES Flights(FlightID),
            FOREIGN KEY (UserID) REFERENCES users(user_id)
        )
        ''')
        
        # Create Passengers table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Passengers (
            PassengerID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName VARCHAR(50) NOT NULL,
            LastName VARCHAR(50) NOT NULL,
            Email VARCHAR(100),
            PhoneNumber VARCHAR(15)
        )
        ''')
        
        # Create Tickets table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tickets (
            TicketID INTEGER PRIMARY KEY AUTOINCREMENT,
            FlightID INTEGER,
            SeatNumber VARCHAR(10),
            Price REAL(10,2),
            Status VARCHAR(20),
            Class VARCHAR(20),
            PassengerID INTEGER,
            BookingDate DATETIME,
            FOREIGN KEY (PassengerID) REFERENCES Passengers(PassengerID),
            FOREIGN KEY (FlightID) REFERENCES Flights(FlightID)
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password, salt=None):
        """Хеширует пароль с использованием SHA-256 и соли"""
        if salt is None:
            salt = os.urandom(32)  # 32 байта случайной соли
        # Комбинируем пароль и соль
        salted_password = password.encode() + salt
        # Хешируем комбинацию
        hashed = hashlib.sha256(salted_password).hexdigest()
        return hashed, salt

    def verify_password(self, stored_password, stored_salt, provided_password):
        """Проверяет соответствие введенного пароля хешированному"""
        # Хешируем предоставленный пароль с сохраненной солью
        hashed_provided, _ = self.hash_password(provided_password, stored_salt)
        return stored_password == hashed_provided

    def is_database_empty(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Проверяем количество записей в основных таблицах
        cursor.execute("SELECT COUNT(*) FROM Airlines")
        airlines_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Country")
        country_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Flights")
        flights_count = cursor.fetchone()[0]
        
        conn.close()
        
        # Возвращаем True, если все таблицы пустые
        return airlines_count == 0 and country_count == 0 and flights_count == 0
    
    def register_user(self, login, email, password, role='user'):
        if self.check_login_exists(login):
            return False, "Логин уже существует"
        if self.check_email_exists(email):
            return False, "Email уже существует"
        
        # Хешируем пароль перед сохранением
        hashed_password, salt = self.hash_password(password)
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (login, email, password, salt, role) VALUES (?, ?, ?, ?, ?)',
                          (login, email, hashed_password, salt, role))
            conn.commit()
            return True, "Регистрация успешна"
        except Exception as e:
            return False, f"Ошибка при регистрации: {str(e)}"
        finally:
            conn.close()

    def check_credentials(self, login, password):
        """Проверяет учетные данные пользователя и возвращает роль в случае успеха"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            # Получаем хешированный пароль и соль для данного логина
            cursor.execute('SELECT password, salt, role FROM users WHERE login = ?', (login,))
            result = cursor.fetchone()
            
            if result:
                stored_password, stored_salt, role = result
                # Проверяем пароль
                if self.verify_password(stored_password, stored_salt, password):
                    return role
            return None
        finally:
            conn.close()

    def check_user_exists(self, login, password):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT role FROM users WHERE login = ? AND password = ?', (login, password))
        result = cursor.fetchone()
        conn.close()
        if result:
            return True, result[0]  # Return True and user role
        return False, None
    
    def check_login_exists(self, login):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE login = ?', (login,))
        user = cursor.fetchone()
        conn.close()
        return user is not None
    
    def check_email_exists(self, email):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        return user is not None

    def get_user_id(self, login):
        """Получает ID пользователя по логину"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM users WHERE login = ?', (login,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def search_tickets(self, origin_city, destination_city, departure_date, return_date=None, passenger_count=1, travel_class='Economy'):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        query = '''
        SELECT 
            f.FlightID,
            a.Name as Airline,
            f.FlightID as FlightNumber,
            oc.Name as Origin,
            o.IATA_Code as OriginCode,
            dc.Name as Destination,
            d.IATA_Code as DestinationCode,
            date(f.DepartureDate) as DepartureDate,
            time(f.DepartureDate) as DepartureTime,
            time(f.ArrivalDate) as ArrivalTime,
            f.Price
        FROM Flights f
        JOIN Airlines a ON f.AirlineID = a.AirlineID
        JOIN Airports o ON f.OriginAirportID = o.AirportID
        JOIN Airports d ON f.DestinationAirportID = d.AirportID
        JOIN City oc ON o.CityID = oc.CityID
        JOIN City dc ON d.CityID = dc.CityID
        WHERE oc.Name = ? AND dc.Name = ?
        AND date(f.DepartureDate) = ?
        ORDER BY f.Price ASC
        '''
        
        params = [origin_city, destination_city, departure_date]
        cursor.execute(query, params)
        outbound_tickets = cursor.fetchall()
        
        return_tickets = []
        if return_date:
            cursor.execute(query, [destination_city, origin_city, return_date])
            return_tickets = cursor.fetchall()
        
        conn.close()
        return outbound_tickets, return_tickets

    def insert_sample_data(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            # Insert Countries
            cursor.execute("INSERT OR IGNORE INTO Country (Name) VALUES ('Россия'), ('США'), ('Франция'), ('Германия'), ('Италия'), ('Испания'), ('Турция')")
            
            # Insert Cities
            city_data = [
                ('Москва', 'Россия'),
                ('Санкт-Петербург', 'Россия'),
                ('Нью-Йорк', 'США'),
                ('Париж', 'Франция'),
                ('Берлин', 'Германия'),
                ('Рим', 'Италия'),
                ('Барселона', 'Испания'),
                ('Стамбул', 'Турция'),
                ('Сочи', 'Россия'),
                ('Казань', 'Россия')
            ]
            for city, country in city_data:
                cursor.execute("""
                    INSERT OR IGNORE INTO City (Name, CountryID)
                    SELECT ?, CountryID FROM Country WHERE Name = ?
                """, (city, country))
            
            # Insert Airlines
            airlines_data = [
                ('Aeroflot', 'SU'),
                ('Air France', 'AF'),
                ('American Airlines', 'AA'),
                ('Lufthansa', 'LH'),
                ('Turkish Airlines', 'TK'),
                ('S7 Airlines', 'S7')
            ]
            cursor.executemany("INSERT OR IGNORE INTO Airlines (Name, IATA_Code) VALUES (?, ?)", airlines_data)
            
            # Insert Airports
            airports_data = [
                ('Международный аэропорт Шереметьево', 'Москва', 'SVO'),
                ('Международный аэропорт Домодедово', 'Москва', 'DME'),
                ('Аэропорт Пулково', 'Санкт-Петербург', 'LED'),
                ('Аэропорт Шарль-де-Голль', 'Париж', 'CDG'),
                ('Международный аэропорт Джона Кеннеди', 'Нью-Йорк', 'JFK'),
                ('Аэропорт Берлин-Бранденбург', 'Берлин', 'BER'),
                ('Аэропорт Леонардо да Винчи', 'Рим', 'FCO'),
                ('Аэропорт Эль-Прат', 'Барселона', 'BCN'),
                ('Аэропорт Стамбул', 'Стамбул', 'IST'),
                ('Международный аэропорт Сочи', 'Сочи', 'AER'),
                ('Международный аэропорт Казань', 'Казань', 'KZN')
            ]
            for airport_name, city_name, iata in airports_data:
                cursor.execute("""
                    INSERT OR IGNORE INTO Airports (AirportName, CityID, IATA_Code)
                    SELECT ?, CityID, ? FROM City WHERE Name = ?
                """, (airport_name, iata, city_name))
            
            # Insert Flights
            flights_data = [
                # Внутренние рейсы
                ('Aeroflot', 'SVO', 'LED', '2024-12-20 10:00:00', '2024-12-20 11:30:00', 8500.00),
                ('Aeroflot', 'LED', 'SVO', '2024-12-20 15:00:00', '2024-12-20 16:30:00', 8000.00),
                ('S7 Airlines', 'DME', 'LED', '2024-12-20 12:00:00', '2024-12-20 13:30:00', 7500.00),
                ('S7 Airlines', 'LED', 'DME', '2024-12-20 17:00:00', '2024-12-20 18:30:00', 7000.00),
                ('Aeroflot', 'SVO', 'AER', '2024-12-21 09:00:00', '2024-12-21 11:30:00', 12000.00),
                ('Aeroflot', 'AER', 'SVO', '2024-12-25 12:00:00', '2024-12-25 14:30:00', 11500.00),
                ('S7 Airlines', 'DME', 'KZN', '2024-12-22 08:00:00', '2024-12-22 09:30:00', 6500.00),
                ('S7 Airlines', 'KZN', 'DME', '2024-12-26 10:00:00', '2024-12-26 11:30:00', 6000.00),

                # Международные рейсы
                ('Aeroflot', 'SVO', 'CDG', '2024-12-21 08:00:00', '2024-12-21 10:30:00', 35000.00),
                ('Air France', 'CDG', 'SVO', '2024-12-25 11:00:00', '2024-12-25 13:30:00', 34000.00),
                ('Lufthansa', 'DME', 'BER', '2024-12-22 09:00:00', '2024-12-22 11:00:00', 32000.00),
                ('Lufthansa', 'BER', 'DME', '2024-12-26 12:00:00', '2024-12-26 14:00:00', 31000.00),
                ('Turkish Airlines', 'SVO', 'IST', '2024-12-23 10:00:00', '2024-12-23 13:30:00', 28000.00),
                ('Turkish Airlines', 'IST', 'SVO', '2024-12-27 14:00:00', '2024-12-27 17:30:00', 27000.00),
                ('Aeroflot', 'SVO', 'FCO', '2024-12-24 11:00:00', '2024-12-24 13:30:00', 33000.00),
                ('S7 Airlines', 'DME', 'BCN', '2024-12-24 12:00:00', '2024-12-24 15:30:00', 36000.00)
            ]
            
            for airline, origin, dest, dep_time, arr_time, price in flights_data:
                cursor.execute("""
                    INSERT OR IGNORE INTO Flights (AirlineID, DepartureDate, ArrivalDate, 
                                   OriginAirportID, DestinationAirportID, Price)
                    SELECT 
                        a.AirlineID,
                        ?, ?,
                        o.AirportID,
                        d.AirportID,
                        ?
                    FROM Airlines a
                    CROSS JOIN Airports o
                    CROSS JOIN Airports d
                    WHERE a.Name = ?
                    AND o.IATA_Code = ?
                    AND d.IATA_Code = ?
                """, (dep_time, arr_time, price, airline, origin, dest))
            
            # Insert Tickets for each flight with different classes
            cursor.execute("SELECT FlightID, Price FROM Flights")
            flights = cursor.fetchall()
            
            for flight in flights:
                flight_id, base_price = flight
                
                # Economy class tickets (3 seats)
                for seat_num in ['1A', '2A', '3A']:
                    cursor.execute("""
                        INSERT OR IGNORE INTO Tickets (FlightID, SeatNumber, Price, Status, Class)
                        VALUES (?, ?, ?, 'Доступен', 'Economy')
                    """, (flight_id, seat_num, base_price))
                
                # Business class tickets (2 seats)
                for seat_num in ['10A', '10B']:
                    cursor.execute("""
                        INSERT OR IGNORE INTO Tickets (FlightID, SeatNumber, Price, Status, Class)
                        VALUES (?, ?, ?, 'Доступен', 'Business')
                    """, (flight_id, seat_num, base_price * 2))
                
                # First class ticket (1 seat)
                cursor.execute("""
                    INSERT OR IGNORE INTO Tickets (FlightID, SeatNumber, Price, Status, Class)
                    VALUES (?, ?, ?, 'Доступен', 'First')
                """, (flight_id, '20A', base_price * 3))
            
            conn.commit()
            print("Тестовые данные успешно добавлены")
            
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении тестовых данных: {e}")
            conn.rollback()
        finally:
            conn.close()

    def add_flight(self, airline_name, from_city, to_city, departure_datetime, arrival_datetime, price):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Get or create airline
            cursor.execute('SELECT AirlineID FROM Airlines WHERE Name = ?', (airline_name,))
            airline_result = cursor.fetchone()
            if airline_result:
                airline_id = airline_result[0]
            else:
                cursor.execute('INSERT INTO Airlines (Name) VALUES (?)', (airline_name,))
                airline_id = cursor.lastrowid
            
            # Get or create cities and airports
            def get_or_create_city_and_airport(city_name):
                cursor.execute('SELECT CityID FROM City WHERE Name = ?', (city_name,))
                city_result = cursor.fetchone()
                if city_result:
                    city_id = city_result[0]
                else:
                    cursor.execute('INSERT INTO City (Name, CountryID) VALUES (?, 1)', (city_name,))
                    city_id = cursor.lastrowid
                
                cursor.execute('SELECT AirportID FROM Airports WHERE CityID = ?', (city_id,))
                airport_result = cursor.fetchone()
                if airport_result:
                    return airport_result[0]
                else:
                    cursor.execute('INSERT INTO Airports (AirportName, CityID) VALUES (?, ?)',
                                 (f"{city_name} Airport", city_id))
                    return cursor.lastrowid
            
            origin_airport_id = get_or_create_city_and_airport(from_city)
            dest_airport_id = get_or_create_city_and_airport(to_city)
            
            # Add flight
            cursor.execute('''
                INSERT INTO Flights (AirlineID, DepartureDate, ArrivalDate, 
                                   OriginAirportID, DestinationAirportID, Price)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (airline_id, departure_datetime, arrival_datetime,
                  origin_airport_id, dest_airport_id, price))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error adding flight: {e}")
            return False

    def purchase_ticket(self, flight_id, user_id, passenger_name, passenger_email, passenger_phone):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Check if flight exists and has available seats
            cursor.execute('SELECT AvailableSeats FROM Flights WHERE FlightID = ?', (flight_id,))
            result = cursor.fetchone()
            if not result or result[0] <= 0:
                return False, "Нет доступных мест"
            
            # Generate seat number (simple implementation)
            cursor.execute('SELECT COUNT(*) FROM PurchasedTickets WHERE FlightID = ?', (flight_id,))
            seat_count = cursor.fetchone()[0]
            seat_number = f"A{seat_count + 1}"
            
            # Add purchased ticket
            cursor.execute('''
                INSERT INTO PurchasedTickets 
                (FlightID, UserID, PassengerName, PassengerEmail, PassengerPhone, SeatNumber)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (flight_id, user_id, passenger_name, passenger_email, passenger_phone, seat_number))
            
            # Update available seats
            cursor.execute('UPDATE Flights SET AvailableSeats = AvailableSeats - 1 WHERE FlightID = ?', 
                         (flight_id,))
            
            conn.commit()
            conn.close()
            return True, f"Билет успешно куплен. Номер места: {seat_number}"
            
        except Exception as e:
            print(f"Error purchasing ticket: {e}")
            return False, "Ошибка при покупке билета"

    def get_user_tickets(self, user_id):
        """Получает все билеты пользователя с детальной информацией"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        query = """
        SELECT 
            pt.TicketID,
            pt.PassengerName,
            pt.PassengerEmail,
            pt.PassengerPhone,
            pt.SeatNumber,
            pt.PurchaseDate,
            a.Name as AirlineName,
            orig.AirportName as OriginAirport,
            oc.Name as OriginCity,
            dest.AirportName as DestinationAirport,
            dc.Name as DestinationCity,
            f.DepartureDate,
            f.ArrivalDate,
            f.Price
        FROM PurchasedTickets pt
        JOIN Flights f ON pt.FlightID = f.FlightID
        JOIN Airlines a ON f.AirlineID = a.AirlineID
        JOIN Airports orig ON f.OriginAirportID = orig.AirportID
        JOIN City oc ON orig.CityID = oc.CityID
        JOIN Airports dest ON f.DestinationAirportID = dest.AirportID
        JOIN City dc ON dest.CityID = dc.CityID
        WHERE pt.UserID = ?
        ORDER BY pt.PurchaseDate DESC
        """
        
        cursor.execute(query, (user_id,))
        tickets = cursor.fetchall()
        conn.close()
        return tickets