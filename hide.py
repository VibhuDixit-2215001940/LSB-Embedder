from stegano import lsb

secret = open("secret.txt","r",encoding="utf-8").read()
lsb.hide("one.jpg", secret).save("output.png")