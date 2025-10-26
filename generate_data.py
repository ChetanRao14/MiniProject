import pandas as pd
import random

# --- 1. DEFINE YOUR TEMPLATES ---
# Your team can add MANY more items to these lists to create more variety!

templates = {
    'Water': {
        'Urgent': [
            "A major water main has burst on {loc}, and it's flooding the street!",
            "Raw sewage is backing up into homes on {loc}. This is a critical health hazard.",
            "Our entire apartment complex ({loc}) has had no water for 24 hours. We need a tanker.",
            "A water pipe is gushing water onto the road at {loc}, causing a huge sinkhole.",
            "The community water tank at {loc} is overflowing and about to collapse."
        ],
        'Medium': [
            "The water pressure in {loc} has been extremely low for three days.",
            "A water pipe has a constant, steady leak at {loc}. Wasting so much water.",
            "The main manhole cover is broken and open at {loc}, it's dangerous.",
            "Our water has been brown and muddy for 2 days at {loc}. It's undrinkable.",
            "Requesting a check on our water meter at {loc}, the bill is 10x the normal amount."
        ],
        'Low': [
            "The public tap at {loc} is constantly dripping.",
            "My water bill for {loc} seems to be incorrect. Please check the reading.",
            "The water from my tap has a slight odor. Can someone inspect {loc}?",
            "Requesting information on the water supply schedule for {loc}.",
            "The cap on the water tank at {loc} is loose and needs to be fixed."
        ]
    },
    'Roads': {
        'Urgent': [
            "A huge sinkhole has opened up in the middle of {loc}! A car could fall in.",
            "The traffic lights at {loc} junction are all dead, causing massive chaos and near-accidents.",
            "A large tree has fallen and is completely blocking {loc}.",
            "A multi-car accident just happened at {loc} due to a broken road. Need help.",
            "The bridge at {loc} has a visible, large crack in it. It looks unsafe!"
        ],
        'Medium': [
            "There is a very large, deep pothole at {loc} that has damaged my car's tire.",
            "The speed breaker at {loc} is broken, and sharp metal rods are sticking out.",
            "The footpath on {loc} is completely broken, forcing pedestrians to walk on the road.",
            "All the streetlights on {loc} are out, making it very dark and unsafe at night.",
            "Road signs are missing at the {loc} intersection, and cars are going the wrong way."
        ],
        'Low': [
            "The zebra crossing paint at {loc} is completely faded.",
            "A small pothole is forming at {loc}. Please fix it before it gets bigger.",
            "Request to repaint the lane markings on {loc}.",
            "The 'No Parking' sign at {loc} has been knocked down.",
            "Please install a new speed bump in our residential area at {loc}."
        ]
    },
    'Electricity': {
        'Urgent': [
            "A high-tension power line has snapped and is sparking on the ground at {loc}!",
            "The transformer at {loc} just exploded! There is smoke and fire.",
            "I smell burning plastic from the main electrical box at {loc}. It's a fire hazard.",
            "A car crashed into the electric pole at {loc}, and it's about to fall.",
            "Live wires are exposed in a flooded area at {loc}. Extremely dangerous."
        ],
        'Medium': [
            "Our entire area ({loc}) has had no power for over 8 hours.",
            "The voltage at {loc} is fluctuating wildly, and it's damaging our appliances.",
            "The main power cable to our building at {loc} is visibly damaged.",
            "An entire street ({loc}) has no working streetlights, it's pitch black.",
            "The electrical junction box at {loc} is open and exposed to rain."
        ],
        'Low': [
            "The streetlight (Pole #E-99) at {loc} is on 24/7. It never turns off.",
            "My electricity meter at {loc} is not working. The display is blank.",
            "Tree branches at {loc} are touching the power lines and need to be trimmed.",
            "Request for a new electricity connection at {loc}.",
            "The streetlight at {loc} is flickering non-stop."
        ]
    },
    'Waste': {
        'Urgent': [
            "Medical waste (needles, masks) has been dumped in the children's park at {loc}!",
            "A large dead animal (cow/dog) is on {loc} and needs to be removed immediately.",
            "The community garbage bin at {loc} is on fire!",
            "The main sewer line at {loc} is blocked and overflowing into the street.",
            "Toxic chemical barrels have been dumped near the lake at {loc}."
        ],
        'Medium': [
            "Garbage has not been collected from {loc} for 5 days. It stinks and is attracting dogs.",
            "The public toilet at {loc} is unusable, filthy, and has no water.",
            "The storm drain on {loc} is completely blocked with plastic. It will flood when it rains.",
            "A large pile of construction debris is blocking the footpath at {loc}.",
            "The garbage collection truck keeps spilling trash all over {loc} and not cleaning it."
        ],
        'Low': [
            "My neighbor at {loc} is burning plastic waste every night, causing pollution.",
            "Request to place a new community garbage bin at {loc}.",
            "The street sweeper has not come to {loc} in two weeks.",
            "Request for a bulk waste pickup for an old mattress at {loc}.",
            "The 'Do Not Litter' sign at {loc} is broken."
        ]
    }
}

# A list of locations to make the data more varied
locations = [
    "1st Main, BTM Layout", "Town Hall Circle", "near SIT College", "in front of the Railway Station",
    "5th Cross, SS Puram", "MG Road", "B.H. Road", "near the District Hospital", "at Gandhinagar Park",
    "in front of Adarsh School", "at the City Market", "near the KSRTC Bus Stand", "on the Ring Road",
    "in Jayanagar 3rd Block", "at Vinayaka Nagar", "near the old post office", "at Melekote",
    "on Kuvempu Main Road", "in the Industrial Area", "at Gandhi Circle"
]

# --- 2. GENERATE THE DATA ---

dataset = []
categories = list(templates.keys())
priorities = ['Urgent', 'Medium', 'Low']

# We want 500 rows total. 500 / 12 combinations = ~41.6
# We will make 42 rows for each combination to get 12 * 42 = 504 rows.
rows_per_combo = 42 

print(f"Generating {rows_per_combo * 12} rows of data...")

for category in categories:
    for priority in priorities:
        for _ in range(rows_per_combo):
            # Pick a random template and a random location
            complaint_template = random.choice(templates[category][priority])
            location = random.choice(locations)
            
            # Combine them to create the final text
            complaint_text = complaint_template.format(loc=location)
            
            # Add the row to our dataset
            dataset.append({
                'complaint_text': complaint_text,
                'category': category,
                'priority': priority
            })

# Shuffle the dataset so the rows are not in order
random.shuffle(dataset)

# --- 3. SAVE TO CSV ---
df = pd.DataFrame(dataset)

# Save to a CSV file
df.to_csv('complaints.csv', index=False)

print(f"\nSuccessfully generated and saved 'complaints.csv' with {len(df)} rows.")
print("\nFirst 5 rows of your dataset:")
print(df.head())