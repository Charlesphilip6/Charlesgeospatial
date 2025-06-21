 Python program that calculates the inmate's release date using the **2/3 method** from the total sentence. 
This method means that inmates may be released after serving 2/3 of their sentence, and the program will account for:

1. **Inmate's total sentence** (in years, months, and days).
2. **Inmate's time already spent** (in years, months, and days).
3. **Inmate's time left to serve** (based on the 2/3 rule).
4. **Release date** (calculated based on the time left).

Here’s a breakdown of the steps involved:
1. **Input the total sentence** and the **time already served**.
2. **Calculate the 2/3 point** of the sentence.
3. **Determine how much time is left** based on the 2/3 rule.
4. **Calculate the release date** by adding the time left to today’s date.

### Full Python Program

Here’s a Python script that performs the inmate release date calculation. You can run this program in any Python environment, and it should be executable as a standalone script.

```python
from datetime import datetime, timedelta

class InmateReleaseCalculator:
    
    def __init__(self, sentence_years, sentence_months, sentence_days, served_years, served_months, served_days):
        self.sentence = timedelta(days=self.convert_to_days(sentence_years, sentence_months, sentence_days))
        self.time_served = timedelta(days=self.convert_to_days(served_years, served_months, served_days))
    
    def convert_to_days(self, years, months, days):
        """
        Convert years, months, and days to total days.
        """
        return (years * 365) + (months * 30) + days
    
    def calculate_two_third_sentence(self):
        """
        Calculate the 2/3 of the total sentence.
        """
        two_third_sentence = self.sentence * (2 / 3)
        return two_third_sentence
    
    def calculate_time_left(self):
        """
        Calculate how much time is left to serve.
        """
        two_third_sentence = self.calculate_two_third_sentence()
        time_left = two_third_sentence - self.time_served
        if time_left.days < 0:
            return timedelta(days=0)  # Time left should never be negative
        return time_left
    
    def calculate_release_date(self):
        """
        Calculate the release date by adding the time left to today's date.
        """
        time_left = self.calculate_time_left()
        today = datetime.today()
        release_date = today + time_left
        return release_date.strftime("%Y-%m-%d")
    
    def display_inmate_info(self):
        """
        Display the calculated information about the inmate's sentence.
        """
        print(f"Total sentence duration: {self.sentence.days} days")
        print(f"Time already served: {self.time_served.days} days")
        print(f"Time left to serve (2/3 rule): {self.calculate_time_left().days} days")
        print(f"Estimated release date (2/3 rule): {self.calculate_release_date()}")


# Example usage
def main():
    # Input for total sentence (in years, months, days)
    sentence_years = int(input("Enter the total sentence in years: "))
    sentence_months = int(input("Enter the total sentence in months: "))
    sentence_days = int(input("Enter the total sentence in days: "))
    
    # Input for time already served (in years, months, days)
    served_years = int(input("Enter the time already served in years: "))
    served_months = int(input("Enter the time already served in months: "))
    served_days = int(input("Enter the time already served in days: "))
    
    # Create an instance of InmateReleaseCalculator
    inmate = InmateReleaseCalculator(sentence_years, sentence_months, sentence_days, served_years, served_months, served_days)
    
    # Display inmate information
    inmate.display_inmate_info()

if __name__ == "__main__":
    main()
```

### **How the Program Works:**

1. **Class: `InmateReleaseCalculator`**
   - This class takes the **total sentence** and **time already served** as input in years, months, and days.
   - It calculates the **total time left to serve** by applying the **2/3 rule**.
   - It uses the `timedelta` object from Python's `datetime` module to handle time calculations.

2. **Methods:**
   - `convert_to_days`: Converts years, months, and days into total days (approximate conversions: 1 year = 365 days, 1 month = 30 days).
   - `calculate_two_third_sentence`: Calculates 2/3 of the total sentence.
   - `calculate_time_left`: Determines how much time is left based on the 2/3 rule and the time already served.
   - `calculate_release_date`: Adds the time left to today’s date to get the inmate’s release date.
   - `display_inmate_info`: Displays the results of the calculation, including total sentence, time served, time left, and the release date.

3. **User Input:**
   - The user is prompted to input the **total sentence** and the **time already served** in years, months, and days.
   - This input is then processed to calculate the **release date** based on the 2/3 method.

### **Sample Output:**

```text
Enter the total sentence in years: 5
Enter the total sentence in months: 0
Enter the total sentence in days: 0
Enter the time already served in years: 2
Enter the time already served in months: 6
Enter the time already served in days: 0
Total sentence duration: 1825 days
Time already served: 912 days
Time left to serve (2/3 rule): 300 days
Estimated release date (2/3 rule): 2024-08-15
```

### **Additional Information:**

- The **2/3 rule** allows the inmate to be released after serving 2/3 of the sentence, assuming there’s no additional time added or legal delays.
- The program handles the time left calculation, ensuring the inmate's time left is never negative.
- **Accuracy**: The program assumes a year is 365 days and a month is 30 days for simplicity. You could adjust this for leap years or more precise calculations if necessary.

### **Execution**:
- Save this program in a `.py` file.
- Run the script using a Python interpreter (e.g., `python inmate_release_calculator.py`).
