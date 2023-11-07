# writting logic
import csv
import pickle

# Step 1: Read the CSV data from the CSV file
csv_file = "data.csv"
data = []
with open(csv_file, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        data.append(row)

# Step 2: Process and transform the data (optional)
# You can perform any necessary data processing here

# Step 3: Serialize the data into a binary format
binary_data = pickle.dumps(data)

# Step 4: Write the binary data to a binary file
binary_file = "data.bin"
with open(binary_file, "wb") as bin_file:
    bin_file.write(binary_data)


#reading logic
import pickle

# Step 1: Read the binary data from the binary file
binary_file = "data.bin"
with open(binary_file, "rb") as bin_file:
    binary_data = bin_file.read()

# Step 2: Deserialize the binary data to obtain the original data
data = pickle.loads(binary_data)

# Now, 'data' contains the CSV data that was previously stored in the binary file
