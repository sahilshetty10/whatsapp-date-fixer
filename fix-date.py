from datetime import datetime
import piexif
import concurrent.futures
import os
import time

folders = ['./', './Sent/', './Private/']


def get_date(filename):
    date_str = filename.split('-')[1]
    return datetime.strptime(date_str, '%Y%m%d').strftime("%Y:%m:%d %H:%M:%S")


allowedFileEndings = ['jpg', '3gp', 'jpeg']

filenames = []

for folder in folders:
    for filename in os.listdir(folder):
        if filename.split('.')[-1] in allowedFileEndings:
            filenames.append(folder+filename)

number_of_files = len(filenames)
print(f'No. of images found in folder: {number_of_files}')


def fix_date(filename):
    try:
        og_date = get_date(filename)
        exif_dict = {'0th': {piexif.ImageIFD.DateTime: og_date},
                     'Exif': {piexif.ExifIFD.DateTimeOriginal: og_date}}
        exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = og_date
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, './' + filename)
    except:
        print(f"Couldn't process{filename}")


print('starting multiprocess')
t1 = time.time()
with concurrent.futures.ThreadPoolExecutor() as executor:
    if __name__ == "__main__":
        f1 = [executor.submit(fix_date, filename) for filename in filenames]
t2 = time.time()
print(f"Finished in {t2-t1} seconds")
