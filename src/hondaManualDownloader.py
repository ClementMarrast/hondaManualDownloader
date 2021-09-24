from bs4 import BeautifulSoup as bs
import wget
import urllib

def rename_manual(chapter, name):
  """Rename each part of the manual using the chapter and description from the link
  The chapter contains two levels, they need to be printed with 0 before to avoid
  having the chapter 1- going after the chapter 10-, for both levels.

  Using 2 digits for the main chapter and 3 digits for the subchapter allow
  to have alphabetic order correct for merging all PDF parts into one.
  """
  try:
    chapters = chapter[chapter.find('/')+1:].replace('.pdf','').split('-')
    newName = name.replace('\r','').replace('\n','').replace(' ','').replace('/','')
    return (f"{int(chapters[0]):02}-{int(chapters[1]):03}_{newName}.pdf")
  except Exception as err:
    print(err)

def get_frames(base_url, html_page):
  """Get all frames from the main HTML pages
  """
  htmlPagesFound = {}
  # print(html_page)
  for frame in html_page.find_all('frame'):
    frame_link = frame.get('src')
    print("frame:" + frame_link)
    frame = urllib.request.urlopen(base_url+frame_link).read()
    frame_bs = bs(frame, features="lxml")
    htmlPagesFound[frame_link] = frame_bs
    htmlPagesFound.update(get_frames(base_url, frame_bs))
  return htmlPagesFound

def get_extHtml(base_url, parent, htmlPagesFound, html_page):
  """Get all external HTML pages
  """
  # print("parent:" + parent)
  for link in html_page.find_all('a'):
    # print(link)
    href = link.get('href')
    if href.endswith('html'):
      print("new HTML:" + href)
      if href in htmlPagesFound:
        print("Already parsed")
      else:
        try:
          extHtml = urllib.request.urlopen(base_url+href).read()
          extHtml_bs = bs(extHtml, features="lxml")
          # print(extHtml_bs)
          htmlPagesFound[href] = extHtml_bs
          htmlPagesFound.update(get_frames(base_url, extHtml_bs))
          get_extHtml(base_url, href, htmlPagesFound, extHtml_bs)
        except urllib.error.HTTPError as e:
          # do something
          print('Error code: ', e.code)
        except urllib.error.URLError as e:
          # do something
          print('Reason: ', e.reason)
        # else:
          # do something
          # print('good!')

def urlScrapping(url):
  """Support any URL
  It will get all frame and external HTML pages"""
  html_main = urllib.request.urlopen(url).read()
  html_page = bs(html_main, features="lxml") 
  base = urllib.request.urlparse(url)
  print("base",base)

  # Load all frames
  html_pages = {
    url: html_page
  }
  html_pages.update(get_frames(url, html_page))
  html_pages_tmp = html_pages.copy()

  for key in html_pages_tmp.keys():
    get_extHtml(url, key, html_pages, html_pages_tmp[key])

  return html_pages

def downloadManual(htmlPages, url, folder):
  """Download all PDF files from provided links
  Use the PDF name and link description as name for the PDF:
  Chapter-SubChapter-description.pdf"""
  links = {}
  # parse all HTML pages
  for html in htmlPages.values():
    for link in html.find_all('a'):
      current_link = link.get('href')
      if current_link.endswith('pdf'):
        name = rename_manual(current_link, link.text)
        links[name] = url + current_link
        print(name)
        # print(my_url + current_link)
        
  # Donwload all PDFs
  i = 0
  for key in links.keys():
    try: 
      print("\nDownload " + str(i) + "/" + str(len(links)))
      print(links[key])
      wget.download(links[key], folder+key)
      i+=1
    except Exception as err:
      print("\nFailed to download the file")
      print(err)
  print('\n')

def main():
  """Download the manual
  """
  print("Enter Link: ")
  my_url = input()
  # my_url = "http://media.honda.co.uk/car/owner/media/manuals/PreludeManual/"
  my_folder = "./PDFs/"

  # Scrap all HTML pages from the URL
  print("Scrapping...")
  htmlPages = urlScrapping(my_url)

  # Download all PDFs from HTML pages
  print("Downloading...")
  downloadManual(htmlPages, my_url, my_folder)

  print("All PDFs are in your folder")

main()
