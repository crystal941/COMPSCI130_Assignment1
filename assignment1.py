class Births:

    def __init__(self, year=1990, number_of_births=0):
        self.year = year
        self.number_of_births = number_of_births

    def __str__(self):
        return "Births: {} ({})".format(self.number_of_births, self.year)


class Deaths:

    def __init__(self, year=1990, number_of_deaths=0):
        self.year = year
        self.number_of_deaths = number_of_deaths
    
    def __str__(self):
        return "Deaths: {} ({})".format(self.number_of_deaths, self.year)


class Region:

    def __init__(self, name="Unknown", land_area=1):
        self.name = name
        self.land_area = land_area
        self.births_list = []
        self.deaths_list = []

    def __str__(self):
        return "{} ({} km^2)".format(self.name, self.land_area)

    def __eq__(self, other):
        if not isinstance(other, Region):
            return False
        elif self.name == other.name:
            return True
        else:
            return False
        
    def __lt__(self, other):
        if not isinstance(other, Region):
            return False
        elif self.name < other.name:
            return True
        else:
            return False
        
    def add_birth_record(self, birth_record):
        self.births_list.append(birth_record)

    def add_death_record(self, death_record):
        self.deaths_list.append(death_record)
    
    def get_number_of_births(self, start_year, end_year):
        sum_of_births = 0
        for birth in self.births_list:
            if birth.year >= start_year and birth.year <= end_year:
                sum_of_births += birth.number_of_births
        return sum_of_births
        
    def get_number_of_deaths(self, start_year, end_year):
        sum_of_deaths = 0
        for death in self.deaths_list:
            if death.year >= start_year and death.year <= end_year:
                sum_of_deaths += death.number_of_deaths
        return sum_of_deaths


class Country:

    def __init__(self, country_name="Unknown", abbreviation="N/A"):
        self.country_name = country_name
        self.abbreviation = abbreviation
        self.regions = []

    def add_region(self, region):
        self.regions.append(region)
        self.regions.sort()

    def __str__(self):
        if not self.regions:
            return "{} ({})\n".format(self.country_name, self.abbreviation)
        else:  
            return ("{} ({})\n".format(self.country_name, self.abbreviation) 
                    + "\n".join([str(region) for region in self.regions]))

    def search_region(self, region_name):
        for region in self.regions:
            if region.name == region_name:
                return region
        return None
    
    def print_births_table(self, start_year, end_year):
        for region in self.regions:
            print("{:18}|{}".format(region.name, region.get_number_of_births(start_year, end_year)))
    
    def print_deaths_table(self, start_year, end_year):
        for region in self.regions:
            print("{:18}|{}".format(region.name, region.get_number_of_deaths(start_year, end_year)))

    def get_total_births(self, start_year, end_year):
        total_births = 0
        for region in self.regions:
            total_births += region.get_number_of_births(start_year, end_year)
        return total_births
    
    def get_total_deaths(self, start_year, end_year):
        total_deaths = 0
        for region in self.regions:
            total_deaths += region.get_number_of_deaths(start_year, end_year)
        return total_deaths


def display_banner():
    title = "Welcome to Births/Deaths Statistics"
    print("*" * len(title), title, "*" * len(title), sep="\n")

def set_a_country():
    country_name = input("Enter the name of a country: ")
    abbreviation = input("Enter the abbreviation of a country: ")
    return Country(country_name, abbreviation)

def read_file(file_name):
    try:
        input_file = open(file_name, 'r')
    except FileNotFoundError:
        print ("ERROR: The file '{}' does not exist.".format(file_name))
    else:
        file_content = input_file.read().split("\n")
        input_file.close()
        return file_content
    
def add_regions_to_country(file_content):
    for line in file_content:
        try:
            values = line.strip().split("\t")
            region_name, land_area = values[0], int(values[1])
            if land_area <= 0:
                raise ValueError
            country.add_region(Region(region_name, land_area))
        except ValueError:
            pass

def add_data_records(data_content):
    for line in data_content:
        try:
            values = line.strip().split("\t")
            year, label, region, number = int(values[0]), values[1], values[2], int(values[3])
            region_for_record = country.search_region(region)
            if label == "Births":
                region_for_record.add_birth_record(Births(year, number))
            elif label == "Deaths":
                region_for_record.add_death_record(Deaths(year, number))
            else:
                raise ValueError
        except ValueError:
            pass

def print_banner():
    title = "Printing Births/Deaths Statistics"
    print("*" * len(title), title, "*" * len(title), sep="\n")

def display_total_births(start_year, end_year):
    header = "Births by Regions:"
    print("*" * len(header), header, "*" * len(header), sep="\n")
    country.print_births_table(start_year, end_year)
    footer = "Births Total: {}".format(country.get_total_births(start_year, end_year))
    print("*" * len(footer), footer, "*" * len(footer), sep="\n")

def display_total_deaths(start_year, end_year):
    header = "Deaths by Regions:"
    print("*" * len(header), header, "*" * len(header), sep="\n")
    country.print_deaths_table(start_year, end_year)
    footer = "Deaths Total: {}".format(country.get_total_deaths(start_year, end_year))
    print("*" * len(footer), footer, "*" * len(footer), sep="\n")


def main():
    global country
    display_banner()
    country = set_a_country()

    file_name = input("Enter the filename for reading a list of regions: ")
    file_content = read_file(file_name)
    if file_content is not None:
        add_regions_to_country(file_content)

    data_name = input("Enter the filename for reading Births/Deaths data: ")
    data_content = read_file(data_name)
    if data_content is not None:
        add_data_records(data_content)

    print_banner()
    start_year = int(input("Enter the start year: "))
    end_year = int(input("Enter the end year: "))
    display_total_births(start_year, end_year)
    display_total_deaths(start_year, end_year)


main()