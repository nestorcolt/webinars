from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import inspect
import os

"""

	Data extraction from www.newegg.com to query the available graphics cards to build a data set with this information
	and store it into a CSV file (Excel)

	Python Webinar Smart-ninja 2020
	
"""

# URL target to scrap
target_url = "https://www.newegg.com/p/pl?Submit=StoreIM&Depa=1197"

# output file
project_root = os.path.dirname(inspect.getfile(inspect.currentframe()))
output_file = os.path.join(project_root, "gc_data_set.csv")

# opening the url
page_request = urlopen(target_url).read()

# html parsing
page_soup = soup(page_request, "html.parser")

# get product containers
containers = page_soup.findAll("div", {"class": "item-container"})

# list will contain as string all the rows that are going to be part of the CVS file
row_list = []

# iterate over all containers to filter data
for container in containers:
	# Brand of the item
	brand = container.div.div.a.img["title"]

	# title of the item
	container_title = container.findAll("a", {"class": "item-title"})
	product_name = container_title[0].text

	# prince of the item
	container_price = container.findAll("li", {"class": "price-current"})
	price = container_price[0].text

	net_price = price.split(".")[0]
	cents = price.split(".")[-1][0:2]
	full_price = net_price + "." + cents

	# shipping details
	container_ship = container.findAll("li", {"class": "price-ship"})
	ship = container_ship[0].text

	data_string = brand + "," + product_name.replace(",", "|") + "," + full_price + "," + ship + "\n"
	row_list.append(data_string)



# Create the CVS file with the data contained in the list row_list
headers = "Brand, Product Name, Price, Shipping\n"

with open(output_file, "w") as writer:

	# create the table headers
	writer.write(headers)

	# iterate and create every row with every card details
	for row in row_list:
		writer.write(row)


	# after for loop finish close the newly created file
	writer.close()


# end of file
