#TrainResFunEx1.py
#It is an seat booking on bus . I had used the threads for develop them.
import threading, time

# Use a set for efficient O(1) checking, adding, and removing elements
L = threading.Lock()
AVAILABLE_SEATS = set(range(1, 25)) # Seats are 1 to 24
RESERVED_SEATS = set()

def reservation(requester_name, seat_numbers_to_reserve):
    """
    Attempts to reserve specified seat numbers for a given requester.
    Prints the status of the reservation and the updated seat availability.
    """
    
    # Optional: Input validation for non-positive or out-of-range seat numbers
    invalid_requests = [seat for seat in seat_numbers_to_reserve if seat <= 0 or seat > 24]
    if invalid_requests:
        print(f"Hi:{requester_name}, Invalid seat numbers requested: {invalid_requests}. Seat numbers must be between 1 and 24.")
        return

    global AVAILABLE_SEATS, RESERVED_SEATS

    # Use 'with L:' for safer and more Pythonic lock handling
    with L:
        # Check which of the requested seats are actually available
        current_available_for_request = AVAILABLE_SEATS.intersection(set(seat_numbers_to_reserve))
        
        # Determine seats that are requested but not available
        unavailable_seats_in_request = set(seat_numbers_to_reserve) - AVAILABLE_SEATS

        if unavailable_seats_in_request:
            # Some requested seats are not available
            print(f"Hi:{requester_name}, The following seats are NOT AVAILABLE: {sorted(list(unavailable_seats_in_request))} -- Please try again.")
            time.sleep(0.5) # Simulate delay for processing failed attempt
        
        if current_available_for_request:
            # Reserve the seats that are available within the request
            AVAILABLE_SEATS.difference_update(current_available_for_request)
            RESERVED_SEATS.update(current_available_for_request)
            print(f"Hi:{requester_name}, Successfully RESERVED seats: {sorted(list(current_available_for_request))} -- Happy Journey!")
            time.sleep(0.5) # Simulate delay for processing successful reservation
        
        # Always print the current status after each transaction attempt
        print(f"\tCurrent Reserved Seats: {sorted(list(RESERVED_SEATS))}")
        print(f"\tCurrent Available Seats: {sorted(list(AVAILABLE_SEATS))}")
        print("-" * 50) # Separator for clarity

# main program
print(f"\tINITIAL TOTAL AVAILABLE SEATS: {sorted(list(AVAILABLE_SEATS))}")
print(f"\tINITIAL RESERVED SEATS: {sorted(list(RESERVED_SEATS))}")
print("-" * 50)

# Define threads with specific seat number requests
p1 = threading.Thread(target=reservation, args=("surya", [4, 5, 6]), name="surya")
p2 = threading.Thread(target=reservation, args=("chandu", [1, 2, 3, 4]), name="chandu") # Seat 4 requested by Surya and Chandu
p3 = threading.Thread(target=reservation, args=("shiva", [10, 11]), name="shiva")
p4 = threading.Thread(target=reservation, args=("Sumanth", [5, 12, 13]), name="Sumanth") # Seat 5 requested by Surya and Sumanth
p5 = threading.Thread(target=reservation, args=("Vinod", [1, 2, 7]), name="Vinod") # Seats 1,2 requested by Chandu and Vinod
p6 = threading.Thread(target=reservation, args=("mani", [20, 21, 22]), name="mani")
p7 = threading.Thread(target=reservation, args=("Divya", [24, 25]), name="Divya") # Seat 25 is invalid, 24 is valid

# Dispatch the threads
p1.start()
p2.start()
p3.start()
p4.start()
p5.start()
p6.start()
p7.start()

# Wait for all threads to complete
p1.join()
p2.join()
p3.join()
p4.join()
p5.join()
p6.join()
p7.join()

print("\n--- ALL RESERVATION ATTEMPTS COMPLETE ---")
print(f"FINAL RESERVED SEATS: {sorted(list(RESERVED_SEATS))}")
print(f"FINAL AVAILABLE SEATS: {sorted(list(AVAILABLE_SEATS))}")
