<?php

require __DIR__ . '/../classes/ServiceBase.php';
require __DIR__ . '/../classes/UploadService.php';

$errorMessage = '';

//echo phpinfo();
if (isset($_POST['submit'])) {
    $upload = new \Service\UploadService();
    $result = $upload->uploadFile();

    if ($result['status'] == 'success') {
        $predictedImage = $result['data'];
    } else {
        $errorMessage = $result['data'];
    }
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <title>Upload</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Inconsolata">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
    <style>
        body, html {
            height: 100%;
            font-family: "Inconsolata", sans-serif;
        }

        .bgimg {
            background-position: center;
            background-size: cover;
            background-image: url("img/predicted_d2.jpg");
            min-height: 75%;
        }

        .menu {
            display: none;
        }
    </style>
</head>
<body>
<div class="w3-content" style="max-width:1400px;">
<header class="w3-container w3-center w3-padding-36 w3-light-grey">
    <h1 class="w3-xxxlarge"><b>Shellfish Detection</b></h1>
</header>
<div class="w3-sand w3-large">
    <div class="w3-container">
        <div class="w3-content w3-padding-16" style="max-width:700px; height:100px;">
            <form method="POST" enctype="multipart/form-data" id="upload_form" class="form-horizontal">
                <div class="form-group" style="text-align: center" style="display:inline-block">
                    <label class="control-label col-sm-2" for="email">Image:</label>
                    <div class="col-sm-4">
                        <input type="file" id="upload_file" name="uploadedFile" required>
                    </div>
                </div>
                <div class="form-group">
                    <div class="col-sm-offset-2 col-sm-10">
                        <input type="submit" name="submit" value="Submit">
                        <span id="warning_form" class="warning"><?php echo $errorMessage;?></span>
                    </div>
                </div>
            </form>
        </div>
        <div id="page_content_thanks" class="w3-content w3-center">
            <?php
            if (isset($predictedImage)) {
//                 echo $predictedImage;
                echo '<img src="' . $predictedImage . '" width="100%" height="100%">';
            }
            ?>
        </div>
    </div>
</div>
</body>

</HTML>