import sqlite3
import json
import sys

s1, s2 = sys.argv[1], sys.argv[2]

conn = sqlite3.connect(s2) #creating connection to database and if it is not exits, creating database
c = conn.cursor()   

with open(s1) as f:                						#opening the json file
    data = json.load(f)                                 #reading json file using json.load()
                                                        #data is a list of dictionaries 
#creating brands table with make_id primary key
c.execute("CREATE TABLE IF NOT EXISTS brands (make_id INTEGER, make_name TEXT, make_slug TEXT, first_year INTEGER, last_year INTEGER,PRIMARY KEY (make_id))")

#creating models table with model_id primary key and make_id foreign key referencing to the brands(make_id)
c.execute("CREATE TABLE IF NOT EXISTS models (model_id INTEGER, make_id INTEGER, model_name TEXT, vehicle_type TEXT,model_styles TEXT,PRIMARY KEY (model_id),FOREIGN KEY (make_id) REFERENCES brands (make_id) ON DELETE CASCADE ON UPDATE NO ACTION)")

#creating years table with rowid primary key and model_id foreign key referencing to the models(model_id)
c.execute("CREATE TABLE IF NOT EXISTS years (rowid INTEGER, model_id INTEGER, year INTEGER,PRIMARY KEY (rowid),FOREIGN KEY (model_id) REFERENCES models (model_id) ON DELETE CASCADE ON UPDATE NO ACTION)")
for brand in data:                                      #for every brand in previously created list of brand dictionaries
    make_id = str(brand["make_id"])
    make_name = str(brand["make_name"])
    make_slug = str(brand["make_slug"])
    first_year = str(brand["first_year"])
    last_year = str(brand["last_year"])

    # taking variables from dictionary and creating an insert query string for brand table
    c.execute("INSERT INTO brands (make_id,make_name,make_slug,first_year,last_year)  VALUES("+ make_id + ",'" + make_name + "','" + make_slug + "'," + first_year +","+ last_year + ")"  )
    
    models = brand["models"]                            #there is a model dictonary for every brand
    for model in models:                                #for every model in models dictionary
        model_id = str(models[model]["model_id"])
        model_name = str(models[model]["model_name"])   #take variables and cast them into string
        model_name = model_name.replace("'","''")       #replace single quote character with double single quote for escaping in the query
        vehicle_type = str(models[model]["vehicle_type"])
        c.execute("INSERT INTO models (model_id, make_id, model_name, vehicle_type) VALUES("+ model_id + "," + make_id + ",'" + model_name + "','" + vehicle_type +"')" )
        for year in models[model]["years"]:             #Years element in the json file is a list 
            c.execute("INSERT INTO years (model_id,year)  VALUES("+ model_id + "," + str(year) + ")" )
                                                        #Insert every year with the corresponding model_id to the years table 

conn.commit()                                           #commit for saving changes
conn.close()                                            #closing database connection
