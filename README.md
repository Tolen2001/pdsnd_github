# 🚀 Bike Rental Data Analysis

## 📅 Date Created

09/01/2025

## 🏷 Project Title

Bike Rental Data Analysis

## 📄 Project Description

This project analyzes bike rental data in three major cities: **Chicago, New York, and Washington**. The program provides comprehensive analysis of trips and customers based on user inputs.

## 📊 Data Used

The project relies on three **CSV** data files containing information about bike rental trips, such as:

- Trip start and end times. 
- Start and end stations.
- Duration of each trip.
- User type (Subscriber or Customer).
- Additional data such as gender and birth year (available for some cities only).

## 🛠 Requirements 

To ensure successful program execution, make sure you have:

- **Python 3.x**
- The following libraries installed:
  ```sh
  pandas
  numpy
  tabulate
  ```
  Install them using:
  ```sh 
  pip install pandas numpy tabulate
  ```
- Data files (`chicago.csv`, `new_york_city.csv`, `washington.csv`) placed in the same project directory.

## 🛠‍🎫 How to Run the Program

1. **Clone the repository (Git Clone) or download it manually**

   ```sh
   git clone https://github.com/Tolen2001/pdsnd_github.git
   cd pdsnd_github
   ```

2. **Run the program**

   ```sh
   python bikeshare.py
   ```

3. **Enter the required inputs**:

   - Choose the city (Chicago, New York, Washington)
   - Select a specific month or all months
   - Choose a specific day or all days
   - Select the type of analysis (Customer data or Trip data)

## 📈 Available Analyses

- **Trip Analysis:**
  - Total and average trip durations.
  - Most popular months, days, and hours for trip starts.
  - Most commonly used start and end stations.
- **Customer Analysis:**
  - User distribution by gender.
  - Birth year analysis (oldest, youngest, and average birth year of users).

## 📂 Included Files

- `bikeshare.py` - The main script for data analysis.
- `chicago.csv`, `new_york_city.csv`, `washington.csv` - Bike rental data files (must be added manually).
- `README.md` - This file!

## 🔧 Known Issues

- Some files may lack user data (such as gender or birth year).
- If incorrect input is entered, the user is prompted to retry.

## 🗓 Changelog

### Version 1.0.0 - (Today's Date)

- Initial project release with support for trip and customer data analysis.

