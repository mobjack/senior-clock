
import os
import shutil
import requests


def pullimage(url, image_file, outfile, saveto):
    print(f'pulling file {image_file}')
    download_file = os.path.join(saveto, outfile)
    pull_url = f'{url}/{image_file}'
    res = requests.get(pull_url, stream=True)
    if res.status_code == 200:
        with open(download_file, 'wb') as df:
            shutil.copyfileobj(res.raw, df)
        return(True)
    else:
        return(False)
