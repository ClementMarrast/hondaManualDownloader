# Honda Manual Downloader

This tool has been designed for extracting the Workshop manual from the website `media.honda.co.uk` by:
- Scraping the given URL to get all HTML pages
- Download all listed PDF files
- Rename all PDF for getting the right alphabetic order
This allow to use a PDF merging tool to build an unique PDF file with the complete manual. 

## How to use
### Install
To run the tool, you need first to install dependencies:
- wget
- urllib
- BeautifulSoup

### Getting the Workshop URL
You need to URL of the workshop manual, example: `http://media.honda.co.uk/car/owner/media/manuals/PreludeManual/`


### Start the script
Start the script. It will ask for the link, just copy it and hit `Enter`.
```
python hondaManualDownloader.py
Enter Link: 
http://media.honda.co.uk/car/owner/media/manuals/PreludeManual/
```

It will list all HTML pages, then parse them to get all PDFs and finally download them in the folder `PDFs` .

### Merge into one PDF files
Now you should have the Workshop manual in many small parts. To merge them into one PDF files, you can use a PDF merging tool.  
On linux you can simply run the following command:
```
pdfunite PDFs/* PreludeManual.pdf
```
