import csv

# method untuk membaca dataset.csv
def load_data(filename):
    data = []
    with open(filename, 'r') as csvfile: # membuka file csv dalam mode read 'r'
        csvreader = csv.reader(csvfile, delimiter=';') # set delimiter karena setiap kolom dipisahkan oleh ';'
        next(csvreader)  # melewati baris pertama karena merupakan nama kolom
        for row in csvreader:
            data.append({key: int(value) for key, value in zip( # membuat dictionary dengan key=nama kolom, value=nilai kolom
                ["SMOKING", "YELLOW_FINGERS", "ANXIETY", "PEER_PRESSURE", "CHRONIC_DISEASE", "FATIGUE", "ALLERGY", "WHEEZING", "ALCOHOL_CONSUMING", "COUGHING", "SHORTNESS_OF_BREATH", "SWALLOWING_DIFFICULTY", "CHEST_PAIN"], row)})
    return data

# method untuk mengembalikan nama kolom
def get_unique_items(data):
    items = set()
    for survey in data:
        for item in survey.keys():
            items.add(item)
    return list(items)

# method untuk menghitung support itemset
def support_count(data, itemset):
    count = 0
    for survey in data:
        if all(survey[item] == 1 for item in itemset):  # memeriksa apakah nilai value=1
            count += 1
    return count

# method untuk menghasilkan association rule
def generate_association_rules(data, min_support, min_confidence):
    itemset = get_unique_items(data)
    frequent_itemsets = []
    rules = []
    survey_row = len(data) # menghitung jumlah baris pada dataset
    min_support = survey_row * min_support # menghitung min_support

    for item in itemset: # melakukan iterasi melalui setiap item dalam itemset
        support = support_count(data, [item])
        if support >= min_support: # jika support item >= min support, maka item ditambahkan ke frequent itemsets
            frequent_itemsets.append([item])
    
    for item in frequent_itemsets: # melakukan iterasi melalui setiap item dalam frequent itemsets
        support_item = support_count(data, item)
        for item2 in frequent_itemsets:
            if item[0] != item2[0]: # jika support dari kedua item (1 itemset) >= dengan min support, maka association rule dibuat
                itemset = list(set(item + item2))
                if len(itemset) == 2:
                    support_itemset = support_count(data, itemset)
                    confidence = support_itemset / support_item
                    if confidence >= min_confidence:
                        rules.append((item, item2, confidence))
    
    return rules

# path dataset yang saya digunakan
data = load_data("C:\\Users\\edoar\\Documents\\College\\dataset_survey_lung_cancer.csv")

print(f"")

# print jumlah baris pada dataset
print(f"The dataset contains {len(data)} rows.")

print(f"")

# meminta inputan min support & min confidence
min_support = float(input("Enter minimum support (antara 0 and 1) > "))  
min_confidence = float(input("Enter minimum confidence (antara 0 and 1) > "))  

rules = generate_association_rules(data, min_support, min_confidence)

print(f"")
print(f"Sehingga dengan minimal support {min_support*100}% dan minimal confidence {min_confidence*100}%,")
print(f"Maka association rule yang didapatkan adalah :")
print(f"")

# print association rule
for rule in rules:
    # print(f"Rule: {rule[0]} => {rule[1]}, Confidence: {rule[2]:.2f}")
    print(f"{str(rule[0]).replace('\'', '')} ==> {str(rule[1]).replace('\'', '')}, (Confidence: {rule[2]:.2f})")
