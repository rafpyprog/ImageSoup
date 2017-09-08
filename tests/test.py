

soup = ImageSoup()
images = soup.search('"folheto supermercado" site:.com.br', n_images=100)
images[8].show()

for n, i in enumerate(images):
    im_colors = i.main_color(n=2, reduce_size=True)
    print(n, im_colors)


url = images[4].URL



blacklist.delete('vermelha.org')
blacklist = BlacklistDomain()
blacklist.domains
blacklist.reset()
blacklist.query_string()



len([blacklist.add(i.URL) for i in images])
