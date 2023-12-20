import gdown

url = 'https://drive.google.com/uc?id=0B9P1L--7Wd2vNm9zMTJWOGxobkU'
output_name = 'model.zip'



def main():
    gdown.download(url, output_name, quiet=False)


if __name__ == '__main__':
    main()