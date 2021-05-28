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
        if len(outim)>3:
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
session_start();
 
$message = ''; 
if (isset($_POST['uploadBtn']) && $_POST['uploadBtn'] == 'Upload')
{
  if (isset($_FILES['uploadedFile']) && $_FILES['uploadedFile']['error'] === UPLOAD_ERR_OK)
  {
    // get details of the uploaded file
    $fileTmpPath = $_FILES['uploadedFile']['tmp_name'];
    $fileName = $_FILES['uploadedFile']['name'];
    $fileSize = $_FILES['uploadedFile']['size'];
    $fileType = $_FILES['uploadedFile']['type'];
    $fileNameCmps = explode(".", $fileName);
    $fileExtension = strtolower(end($fileNameCmps));
 
    // sanitize file-name
    $newFileName = md5(time() . $fileName) . '.' . $fileExtension;
 
    // check if file has one of the following extensions
    $allowedfileExtensions = array('jpg', 'gif', 'png', 'zip', 'txt', 'xls', 'doc');
 
    if (in_array($fileExtension, $allowedfileExtensions))
    {
      // directory in which the uploaded file will be moved
      $uploadFileDir = './uploaded_files/';
      $dest_path = $uploadFileDir . $newFileName;
 
      if(move_uploaded_file($fileTmpPath, $dest_path)) 
      {
        $message ='File is successfully uploaded.';
      }
      else
      {
        $message = 'There was some error moving the file to upload directory. Please make sure the upload directory is writable by web server.';
      }
    }
    else
    {
      $message = 'Upload failed. Allowed file types: ' . implode(',', $allowedfileExtensions);
    }
  }
  else
  {
    $message = 'There is some error in the file upload. Please check the following error.<br>';
    $message .= 'Error:' . $_FILES['uploadedFile']['error'];
  }
}
$_SESSION['message'] = $message;
'''

form_sr = '''

<!DOCTYPE html>
<html>
<body>

<form action="upload.php" method="post" enctype="multipart/form-data">
  Select image to upload:
  <input type="file" name="fileToUpload" id="fileToUpload">
  <input type="submit" value="Upload Image" name="submit">
</form>

</body>
</html>

'''

def create_recieved_page(main_pa):
    with open(main_pa/"html/form.html", "w+") as f:
        f.write(form_sr)
    with open(main_pa/"html/upload.php", "w+") as f:
        f.write(php_sr)




def generate_sites(ser,main_pa):
    global ser2
    with open(main_pa/"index.html", "w+") as f:
            f.write(index_html)
            with open(main_pa/"data/textclip.txt", "r") as content:
                f.write("<br>")
                f.write("<br>".join(content.readlines()[::-1]))

    im_list = [x.name for x in (main_pa/"data/images").iterdir()]

    with open(main_pa/"html/ims.html", "w+") as f:
        f.write(index_html2)
        f.write("<br>")
        for i in im_list:
            #  with open(main_pa/"data/images/"/i, "r") as im_data:
            #      f.write(f'<br><img src="data:image/png;base64, {im_data}"')

            image_default = f"<img src = {ser2}data/images/{i}></img>"
            f.write("<br>"+image_default+"<br>")



def regenerate_sites(main_pa, ser, waitfor):
    while True:
        time.sleep(waitfor)
        get_clip_and_save(main_pa)
        generate_sites(ser, main_pa)
