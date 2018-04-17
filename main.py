from geopy.geocoders import Nominatim
import csv

geolocator = Nominatim()

class SpeedTest:
    def getCity(self):
        location = geolocator.reverse(self.lat + ", " + self.lon)
        self.city = location.raw['address']['suburb']

    def __init__(self, date, connType, lat, lon, download, upload, ping):
        self.date = date
        self.connType = connType
        self.lat = lat
        self.lon = lon
        self.download = float(download) / 1000.0
        self.upload = float(upload) / 1000.0
        self.ping = int(ping)
        self.city = "Unloaded"

    def __str__(self):
        return self.date + ", " + self.connType + ", " + self.lat + ", " + self.lon + ", " + str(self.download) + ", " + str(self.upload) + ", " + str(self.ping) + ", " + str(self.city)

def loadCityNames(tests, totalRows):
    print("Attempting to fetch location of " + str(totalRows) + " rows. This should take about " + str(round(totalRows * .9)) + " seconds.")
    for test in tests:
        while True:
            try:
                test.getCity()
            except geopy.exc.GeocoderTimedOut as error:
                print(error)
                continue
            break

def readData():
    tests = []
    with open('tests.csv', newline='') as csvfile:
        # reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        reader = csv.DictReader(csvfile)
        for row in reader:
            if ''.join(row).strip():
                tests.append(SpeedTest(row['Date'], row['ConnType'], row['Lat'], row['Lon'], row['Download'], row['Upload'], row['Latency']))
    return tests

def printAllTests(tests):
    for test in tests:
        print(test)

def getTestDataFromCity(city, tests):
    downloadAverage = 0
    uploadAverage = 0
    pingAverage = 0
    bestDownload = 0
    bestUpload = 0
    bestPing = 100
    totalTests = 0

    if len(tests) == 0:
        print("No tests exist.")
        return

    for test in tests:
        if test.city.lower() == city.lower():
            downloadAverage += test.download
            uploadAverage += test.upload
            pingAverage += test.ping

            if test.download > bestDownload:
                bestDownload = test.download
            if test.upload > bestUpload:
                bestUpload = test.upload
            if test.ping < bestPing:
                bestPing = test.ping  

            totalTests += 1
    
    downloadAverage /= totalTests
    uploadAverage /= totalTests
    pingAverage /= totalTests

    downloadAverage = round(downloadAverage, 2)
    uploadAverage = round(uploadAverage, 2)
    pingAverage = round(pingAverage)

    bestDownload = round(bestDownload, 2)
    bestUpload = round(bestUpload, 2)
    bestPing = round(bestPing)

    oldestDate = tests[len(tests) - 1].date.split(" ")[0]
    newestDate = tests[0].date.split(" ")[0]

    print("")
    print("Data from " + str(len(tests)) + " tests from " + oldestDate + " to " + newestDate)
    print("")
    print("Download: " + str(downloadAverage) + " Mbps")
    print("  Upload: " + str(uploadAverage) + " Mbps")
    print("    Ping: " + str(pingAverage) + " ms")
    print("")
    print("")
    print(" -= Best Results =- ")
    print("")
    print("Download: " + str(bestDownload) + " Mbps")
    print("  Upload: " + str(bestUpload) + " Mbps")
    print("    Ping: " + str(bestPing) + " ms")
    print("")

tests = readData()
totalRows = len(tests)

# Default name is 'Unloaded' to save time. 
# loadCityNames(tests, totalRows)
getTestDataFromCity("Unloaded", tests)
