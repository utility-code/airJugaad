import pyperclip
import subprocess
from pathlib import Path
import time

ser = "http://192.168.1.114:8080/"

ser2 = "http://192.168.1.114:8080/"

index_html = f'''
<a href = "{ser}html/ims.html">Images</a>
<a href = "{ser}html/rec.html">Recieved</a>

'''

index_html2 = f'''
<a href = "{ser}index.html">Index</a>
<a href = "{ser}html/rec.html">Recieved</a>

'''
index_html3 = f'''
<a href = "{ser}index.html">Index</a>
<a href = "{ser}html/ims.html">Images</a>

'''

previous_text = ""
previous_im = ""

def iseq(x,y): return x == y

def createIfNot(x):
    Path.mkdir(x, exist_ok=True)        

def get_name(main_pa):
    imPa = Path(main_pa/'data/images')
    ims_exisitng = [x for x in imPa.iterdir()]
    ims_exisitng = [x.name for x in ims_exisitng]
    nfiles = len(ims_exisitng)
    
    if nfiles == 0:
        return Path(imPa/"im_1.png")
    else:
        return Path(imPa/f"im_{str(nfiles+1)}.png")

def get_clip_and_save(main_pa):
    global previous_im
    global previous_text
    txt = pyperclip.paste()
    im = subprocess.run(["xclip", "-selection", "clipboard" ,"-t" ,"image/png", "-o"], stdout=subprocess.PIPE)
    outim = im.stdout
    
    if im.returncode==0:
        if len(outim)>40:
            with open(get_name(main_pa), "wb+") as f:
                    if outim != previous_im:
                        print("saving image")
                        f.write(outim)
        previous_im = outim
    else:
        with open(main_pa/"data/textclip.txt", "a+") as f:
            if txt!= previous_text:
                print("saving text")
                f.write("\n"+txt+"\n")
        previous_text = txt

php_sr = '''
<?php
    $currentDirectory = getcwd();
    $uploadDirectory = "../data/recieved/";

    $errors = []; // Store errors here

    $fileExtensionsAllowed = ['jpeg','jpg','png']; // These will be the only file extensions allowed 

    $fileName = $_FILES['the_file']['name'];
    $fileSize = $_FILES['the_file']['size'];
    $fileTmpName  = $_FILES['the_file']['tmp_name'];
    $fileType = $_FILES['the_file']['type'];
    $fileExtension = strtolower(end(explode('.',$fileName)));

    $uploadPath = $currentDirectory . $uploadDirectory . basename($fileName); 

    if (isset($_POST['submit'])) {

      // if (! in_array($fileExtension,$fileExtensionsAllowed)) {
      //   $errors[] = "This file extension is not allowed. Please upload a JPEG or PNG file";
      // }
      //
      // if ($fileSize > 4000000) {
      //   $errors[] = "File exceeds maximum size (4MB)";
      // }
      //
      if (empty($errors)) {
        $didUpload = move_uploaded_file($fileTmpName, $uploadPath);

        if ($didUpload) {
          echo "The file " . basename($fileName) . " has been uploaded";
        } else {
          echo "An error occurred. Please contact the administrator.";
        }
      } else {
        foreach ($errors as $error) {
          echo $error . "These are the errors" . "\n";
        }
      }

    }
?>
'''

form_sr = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>File Upload</title>
</head>
<a href = "{ser}index.html">Index</a>
<a href = "{ser}html/ims.html">Images</a>

<body>
    <form action="upload.php" method="post" enctype="multipart/form-data">
        Upload a File:
        <input type="file" name="the_file" id="fileToUpload">
        <input type="input" name="fname" id="fileToUpload">
        <input type="submit" name="submit" value="Start Upload">
    </form>
</body>
</html>
'''

def create_recieved_page(main_pa):
    with open(main_pa/"html/rec.html", "w+") as f:
        f.write(form_sr)
    with open(main_pa/"html/upload.php", "w+") as f:
        f.write(php_sr)




def generate_sites(ser,main_pa):
    global ser2
    with open(main_pa/"index.html", "w+") as f:
            f.write(index_html)
            with open(main_pa/"data/textclip.txt", "r") as content:
                lin = content.readlines()[::-1]
                f.write("<br>")
                f.write("<br>".join(lin))

    im_list = [x.name for x in (main_pa/"data/images").iterdir() if x.stat().st_size >20]

    with open(main_pa/"html/ims.html", "w+") as f:
        f.write(index_html2)
        f.write("<br>")
        for i in im_list:

            image_default = f"<img src = {ser2}data/images/{i}></img>"
            f.write("<br>"+image_default+"<br>")



def regenerate_sites(main_pa, ser, waitfor):
    while True:
        time.sleep(waitfor)
        get_clip_and_save(main_pa)
        generate_sites(ser, main_pa)
