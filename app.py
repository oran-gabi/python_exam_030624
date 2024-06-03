import csv
import statistics
from enum import Enum
from print_color import print

class DiamondFeatures(Enum):
    HIGHEST_PRICE = 1
    AVERAGE_PRICE = 2
    IDEAL_DIAMONDS = 3
    DIFFERENT_COLORS = 4
    MEDIAN_CARAT_PREMIUM = 5
    AVERAGE_CARAT_BY_CUT = 6
    AVERAGE_PRICE_BY_COLOR = 7
    EXIT = 8

def readlines(file_path):
    lines = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            lines.append(row)
    return lines

def highest_price(lines):
    highest = 0
    for line in lines[1:]:  # Skip the header row
        price = float(line[6])  # Assuming price is at index 6
        if price > highest:
            highest = price
    return highest

def average_price(lines):
    total_price = 0
    num_diamonds = len(lines) - 1  # Exclude the header row
    for line in lines[1:]:  # Skip the header row
        total_price += float(line[6])  # Assuming price is at index 6
    if num_diamonds > 0:
        return total_price / num_diamonds
    else:
        return 0  # Avoid division by zero

def count_ideal_cut_diamonds(lines):
    count = 0
    for line in lines[1:]:  # Skip the header row
        if line[1] == 'Ideal':  # Assuming cut type is at index 1
            count += 1
    return count

def count_diamond_colors(lines):
    colors = set(line[2] for line in lines[1:])  # Assuming color is at index 2
    return len(colors), colors

def calculate_median_carat(lines, cut_type):
    carats = []
    for line in lines[1:]:  # Skip the header row
        if line[1] == cut_type:  # Assuming cut type is at index 1
            carats.append(float(line[0]))  # Assuming carat is at index 0
    if carats:
        return statistics.median(carats)
    else:
        return None

def calculate_average_carat_by_cut_type(lines):
    cut_types = set(line[1] for line in lines[1:])  # Assuming cut type is at index 1
    average_carats = {}
    for cut_type in cut_types:
        carats = [float(line[0]) for line in lines[1:] if line[1] == cut_type]  # Assuming carat is at index 0
        if carats:
            average_carats[cut_type] = sum(carats) / len(carats)
    return average_carats

def calculate_average_price_by_color(lines):
    color_prices = {}
    for line in lines[1:]:  # Skip the header row
        color = line[2]  # Assuming color is at index 2
        price = float(line[6])  # Assuming price is at index 6
        if color in color_prices:
            color_prices[color].append(price)
        else:
            color_prices[color] = [price]
    average_prices = {color: sum(prices) / len(prices) for color, prices in color_prices.items()}
    return average_prices

# Example usage
file_path = 'data.csv'
lines = readlines(file_path)

while True:
    print("Select a number to choose a feature:", color='blue')
    for feature in DiamondFeatures:
        print(f"{feature.value}: {feature.name.replace('_', ' ')}", color='blue')

    selection = input("Enter your selection (1-8): ")
    try:
        selected_feature = DiamondFeatures(int(selection))
        if selected_feature == DiamondFeatures.EXIT:
            print("Exiting the program...", color='red')
            break
        elif selected_feature == DiamondFeatures.HIGHEST_PRICE:
            print(f"Highest Price of Diamond: {highest_price(lines)}")
        elif selected_feature == DiamondFeatures.AVERAGE_PRICE:
            print(f"Average Price of Diamonds: {average_price(lines)}")
        elif selected_feature == DiamondFeatures.IDEAL_DIAMONDS:
            print(f"Total Number of Diamonds with Cut Type 'Ideal': {count_ideal_cut_diamonds(lines)}")
        elif selected_feature == DiamondFeatures.DIFFERENT_COLORS:
            total_colors, colors = count_diamond_colors(lines)
            print(f"Total Number of Different Colors of Diamonds: {total_colors}")
            print("Colors:")
            for color in colors:
                print(color)
        elif selected_feature == DiamondFeatures.MEDIAN_CARAT_PREMIUM:
            print(f"Median Carat of Diamonds with 'Premium' Cut: {calculate_median_carat(lines, 'Premium')}")
        elif selected_feature == DiamondFeatures.AVERAGE_CARAT_BY_CUT:
            print("Average Carat by Cut Type:")
            average_carats = calculate_average_carat_by_cut_type(lines)
            for cut_type, average_carat in average_carats.items():
                print(f"Cut Type: {cut_type}, Average Carat: {average_carat}")
        elif selected_feature == DiamondFeatures.AVERAGE_PRICE_BY_COLOR:
            print("Average Price by Color:")
            average_prices = calculate_average_price_by_color(lines)
            for color, average_price in average_prices.items():
                print(f"Color: {color}, Average Price: {average_price}")
        else:
            print("Invalid selection. Please enter a number from 1 to 8.", color='yellow')
    except ValueError:
        print("Invalid input. Please enter a number.", color='yellow')
