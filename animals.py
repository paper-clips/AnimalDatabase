import sqlite3

# Create empty database named PetHavenDatabase (.db indicates database)
# When you click the db file it will not be readable to people
connection = sqlite3.connect("PetHavenDatabase.db")

cursor = connection.cursor()    # Allows us to use SQL commands

# Animal entity class, will automatically create the tables
class Animal():
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.createAnimalTable()    # Create base class table (Animal)
        self.createCatsTable()      # Create subclass 1 table (Cats)
        self.createDogsTable()      # Create subclass 2 table (Dogs)
        self.createOtherTable()     # Create subclass 3 table (Other)
    
    # Create base class table (Animal)
    # NOTE: Feel free to change the domains
    # NOTE: Didn't add a reference (foreign key) for kennelID for now
    def createAnimalTable(self):
        # Create new table (checks if the table already exists) in database
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Animal(
                                AID CHAR(8) PRIMARY KEY, 
                                Name VARCHAR(40), 
                                Sex CHAR(1),
                                DOB DATE,
                                DateOfIntake DATE,
                                Picture BLOB,
                                KennelID INTEGER)""")
    
    # Create subclass 1 table (Cats)
    def createCatsTable(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Cats(
                                AID CHAR(8) PRIMARY KEY NOT NULL REFERENCES Animal ON DELETE CASCADE, 
                                Name VARCHAR(40), 
                                Sex CHAR(1),
                                DOB DATE,
                                DateOfIntake DATE,
                                Picture BLOB,
                                KennelID INTEGER,
                                Type VARCHAR(30))""")

    # Create subclass 2 table (Dogs)
    def createDogsTable(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Dogs(
                                AID CHAR(8) PRIMARY KEY NOT NULL REFERENCES Animal ON DELETE CASCADE, 
                                Name VARCHAR(40), 
                                Sex CHAR(1),
                                DOB DATE,
                                DateOfIntake DATE,
                                Picture BLOB,
                                KennelID INTEGER,
                                Breed VARCHAR(30))""")

    # Create subclass 3 table (Other)
    def createOtherTable(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Other(
                                AID CHAR(8) PRIMARY KEY NOT NULL REFERENCES Animal ON DELETE CASCADE, 
                                Name VARCHAR(40), 
                                Sex CHAR(1),
                                DOB DATE,
                                DateOfIntake DATE,
                                Picture BLOB,
                                KennelID INTEGER)""")

    """ -------------------------------------------------------------------- Functions to use ----------------------------------------------------------------------------- """        
    
    def insert(self, aID, name, sex, dob, dateOfIntake, picture, kennelID, animalType, catType, dogBreed):
        # OR IGNORE checks if it already exists and won't insert the same value again
        self.cursor.execute("INSERT OR IGNORE INTO Animal VALUES (?, ?, ?, ?, ?, ?, ?)", (aID, name, sex, dob, dateOfIntake, picture, kennelID))
        
        # Add to corresponding table (Cats, Dogs, or Other)
        if animalType == "Cat":
            self.cursor.execute("INSERT OR IGNORE INTO Cats VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (aID, name, sex, dob, dateOfIntake, picture, kennelID, catType))
        elif animalType == "Dog":
            self.cursor.execute("INSERT OR IGNORE INTO Dogs VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (aID, name, sex, dob, dateOfIntake, picture, kennelID, dogBreed))
        elif animalType == "Other":
            self.cursor.execute("INSERT OR IGNORE INTO Other VALUES (?, ?, ?, ?, ?, ?, ?)", (aID, name, sex, dob, dateOfIntake, picture, kennelID))
        else:
            print("Error: Animal type not specified or type is not correct")

        self.connection.commit()    # Commit to actual database when inserting

    # Sort the animals by the animal which was born first
    def sortAnimalsByDOB(self, orderType):
        if orderType == "Descending":
            print("Animals sorted by descending DOB:")
            sortedOrder = self.cursor.execute("SELECT * FROM Animal ORDER BY DOB DESC")
        else:
            print("Animals sorted by ascending DOB:")
            sortedOrder = self.cursor.execute("SELECT * FROM Animal ORDER BY DOB")
        for row in sortedOrder:
            print(row)
        #return sortedOrder

    # Print animals based on sex
    def getAnimalsBasedOnSex(self, sex):
        if sex == 'F':
            self.cursor.execute("SELECT * FROM Animal WHERE SEX = ?", (sex,))
            femaleAnimals = self.cursor.fetchall()
            print("Female animals: ")
            for row in femaleAnimals:
                print(row)
        elif sex == 'M':
            self.cursor.execute("SELECT * FROM Animal WHERE SEX = ?", (sex,))
            maleAnimals = self.cursor.fetchall()
            print("Male animals: ")
            for row in maleAnimals:
                print(row)

    # Print name of animal based on its ID
    def getAnimalNameFromID(self, aID):
        self.cursor.execute("SELECT Name FROM Animal WHERE AID = ?", (aID,))
        animalName = self.cursor.fetchone()
        print("Animal name: ", animalName)

    # Print Animal table
    def printAnimalTable(self):
        print("Animal Table:")
        for row in cursor.execute("SELECT * FROM Animal"):
            print(row)

    # Print Cats table
    def printCatsTable(self):
        print("Cats Table:")
        for row in cursor.execute("SELECT * FROM Cats"):
            print(row)
    
    # Print Dogs Table
    def printDogsTable(self):
        print("Dogs Table:")
        for row in cursor.execute("SELECT * FROM Dogs"):
            print(row)
    
    # Print other animals table
    def printOtherTable(self):
        print("Other Table:")
        for row in cursor.execute("SELECT * FROM Other"):
            print(row)


animal = Animal(connection, cursor)
animal.printAnimalTable()   # Will show if the table is empty or if it has data, can remove this if you want
print("")

#Dog info: https://www.humanesocietyofpinellas.org/adoptable-dogs/
#Cat info: https://www.humanesocietyofpinellas.org/adoptable-cats/
#Other info: https://spcatampabay.org/pocket-pets/
noAttribute = ""    # Use to symbolize that there isn't an attribute
# Insert dogs
animal.insert("50372287", "Bonita", 'F', "2018-12-08", "2022-04-18", "NULL", 14567, "Dog", noAttribute, "Mix")
animal.insert("50236597", "Marvel", 'M', "2012-05-25", "2013-09-17", "NULL", 14568, "Dog", noAttribute, "Chihuahua")
# Insert cats
animal.insert("50070467", "Honey", 'M', "2012-04-25", "2014-12-03", "NULL", 14569, "Cat", "Domestic Shorthair", noAttribute)
animal.insert("45628920", "Kate", 'F', "2020-08-25", "2020-09-05", "NULL", 14570, "Cat", "Domestic Shorthair", noAttribute)
# Insert other animals
animal.insert("50513720", "Lola", 'F', "2020-06-23", "2020-10-12", "NULL", 14571, "Other", noAttribute, noAttribute)
animal.insert("47978637", "Marshmallow", 'F', "2021-05-25", "2022-03-14", "NULL", 14572, "Other", noAttribute, noAttribute)

""" Random queries """
# Print the animal tables
animal.printAnimalTable()
animal.printCatsTable()
animal.printDogsTable()
animal.printOtherTable()

# Sort animals by DOB
animal.sortAnimalsByDOB("Descending")
animal.sortAnimalsByDOB("Ascending")

# Print name of animal based on its ID
animal.getAnimalNameFromID("50236597")
animal.getAnimalNameFromID("47978637")

# Print animals based on sex
animal.getAnimalsBasedOnSex('F')
animal.getAnimalsBasedOnSex('M')


connection.close()  # Terminate connection
