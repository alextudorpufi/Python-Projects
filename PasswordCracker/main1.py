import requests
import data
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

login_url = ('https://the-internet.herokuapp.com/authenticate')
secure_url = ('https://the-internet.herokuapp.com/secure')

payload = {
    'username': data.username,
    'password': data.password
}

download_folder = 'Downloads'
os.makedirs(download_folder, exist_ok=True)

def download_file(url, folder):
    try:
        response=session.get(url, stream=True)
        response.raise_for_status()
        filename=os.path.join(folder, url.split('/')[-1])
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded: {filename}")
        return filename

    except Exception as error:
        print("Couldn't download - {url} - :" + {error})
        return None

def download_resources(soup, url):
    img_folder=os.path.join(download_folder, 'Images' )
    os.makedirs(img_folder, exist_ok=True)
    for img_tag in soup.find_all('img'):
        img_url = img_tag.get('src')
        full_url=urljoin(url, img_url)
        new_path=download_file(full_url, img_folder)
        if new_path is not None:
            img_tag['src']=os.path.relpath(new_path, download_folder)

    css_folder = os.path.join(download_folder, 'CSS')
    os.makedirs(css_folder, exist_ok=True)
    for css_tag in soup.find_all('link',rel='stylesheet'):
        css_url = css_tag.get('href')
        full_url = urljoin(url, css_url)
        new_path=download_file(full_url, css_folder)
        if new_path is not None:
            css_tag['href'] = os.path.relpath(new_path, download_folder)

    js_folder = os.path.join(download_folder, 'Javascript')
    os.makedirs(js_folder, exist_ok=True)
    for js_tag in soup.find_all('script'):
        js_url = js_tag.get('src')
        full_url = urljoin(url, js_url)
        new_path=download_file(full_url, js_folder)
        if new_path is not None:
            js_tag['src'] = os.path.relpath(new_path, download_folder)

# r = requests.post(login_url, data=payload)
# print(r.text)

# # Fara sesiune, astfel secure_url ne duce la login page
# r2 = requests.get(secure_url)
# print(r2.text)
# #

with requests.session() as session:
    session.post(login_url, data=payload)
    r=session.get(secure_url) # Daca foloseam requests.get, nu reuseam
    print(r.text)

    filename=os.path.join(download_folder, 'content.html')
    with open(filename, 'wb') as file:
        file.write(r.content)

    soup = BeautifulSoup(r.text, 'html.parser')

    download_resources(soup, secure_url)

    modified_filename = os.path.join(download_folder, 'modified_content.html')
    with open(modified_filename, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    print(f"Modified HTML saved to {modified_filename}")