from .helpers import *

"""
The main spine of the library
"""

php_sr = """
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
    header('Location: ' . $_SERVER['HTTP_REFERER']);

    }
?>
"""

style_page = """
<style>
body {
  background-color: black;
}

a, input,body {
  color: white;
  margin-left: 40px;
}
</style>
"""


def return_htmls(ser, ser2):
    """
    Return the html for index, images pages etc along with simple styling
    """
    index_html = f"""
    <head>
    {style_page}
    </head>
    <a href = "{ser2}html/ims.html">Images</a>
    <a href = "{ser2}html/rec.html">Recieved</a>

    """

    index_html2 = f"""
    <head>
    {style_page}
    </head>
    <a href = "{ser2}index.html">Index</a>
    <a href = "{ser2}html/rec.html">Recieved</a>

    """
    index_html3 = f"""
    <head>
    {style_page}
    </head>
    <a href = "{ser2}index.html">Index</a>
    <a href = "{ser2}html/ims.html">Images</a>

    """

    form_sr = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>File Upload</title>
    {style_page}
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
    """

    return index_html, index_html2, index_html3, form_sr


def generate_sites(index_html, index_html2, main_pa, ser2, ser, timefor):
    """
    Generate the site by outputing the data from the log and images folder
    """
    with open(main_pa / "index.html", "w+") as f:
        f.write(index_html)
        with open(main_pa / "data/textclip.txt", "r") as content:
            lin = content.readlines()[::-1]
            f.write("<br>")
            f.write("<br>".join(lin))

    im_list = [
        x.name for x in (main_pa / "data/images").iterdir() if x.stat().st_size > 20
    ]

    with open(main_pa / "html/ims.html", "w+") as f:
        f.write(index_html2)
        f.write("<br>")
        for i in im_list:
            image_default = f"<img src = {ser2}data/images/{i}></img>"
            f.write("<br>" + image_default + "<br>")


def create_recieved_page(main_pa, form_sr):
    """
    Generate the page for recieving
    """
    with open(main_pa / "html/rec.html", "w+") as f:
        f.write(form_sr)
    with open(main_pa / "html/upload.php", "w+") as f:
        f.write(php_sr)
