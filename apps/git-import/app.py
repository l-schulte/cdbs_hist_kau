# import schedule
# import time

import importer.importer as importer

# if __name__ == "__main__":

# schedule.every().day.at("21:14").do(importer.go)

# while True:

#     schedule.run_pending()
#     time.sleep(1)

importer.go()
