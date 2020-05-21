<?php

namespace Service;

use Services\ServiceBase;

class UploadService extends ServiceBase
{
    public function __construct()
    {
    }

    public function uploadFile()
    {
        $result = ['data' => '', 'status' => ''];

        try {
            if (!isset($_FILES['uploadedFile']) || empty($_FILES['uploadedFile']['name'])) {
                throw new \Exception('Please chose a file to upload');
            }

            if ($_FILES['uploadedFile']['error'] > 0) {
                $errorMessage = $this->uploadCodeToMessage($_FILES['uploadedFile']['error']);
                 throw new \Exception('Error occurred when uploading. Error: ' . $errorMessage);
            }

            if (!is_uploaded_file($_FILES['uploadedFile']['tmp_name'])) {
                throw new \Exception('File is not uploaded successfully');
            }

            // Check if image file is a actual image or fake image
            $check = getimagesize($_FILES["uploadedFile"]["tmp_name"]);

            if($check === false) {
                throw new \Exception("File is not an image.");
            }

            $target_dir = __DIR__ . "/../public/img/";
            // Remove space in the file name
            $uploadedFile = str_replace(' ', '', $_FILES["uploadedFile"]["name"]);
            $target_file = $target_dir . basename($uploadedFile);
            $imageFileType = strtolower(pathinfo($target_file, PATHINFO_EXTENSION));

            // Check if file already exists
            if (file_exists($target_file)) {
                unlink($target_file);
//                 throw new \Exception("file already exists.");
            }

            // Allow certain file formats
            if($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg") {
                throw new \Exception("Only JPG, JPEG, and PNG files are allowed.");
            }

            if (move_uploaded_file($_FILES["uploadedFile"]["tmp_name"], $target_file)) {
                // Call script to run detection
                $prediction_script = __DIR__ . '/../../pdtry.py';

                $command = escapeshellcmd('python3 ' . $prediction_script . ' --input ' . $target_file . ' --output ' . $target_dir . ' --web 1');
                $predicted_img_path = shell_exec($command);
//                 echo $output;
//                 $result = ['status' => 'success', 'data' => 'img/' . basename($_FILES["uploadedFile"]["name"])];
                $result = ['status' => 'success', 'data' => 'img/' . $uploadedFile];

            } else {
                throw new \Exception("Failed to upload your file.");
            }
        } catch (\Exception $e) {
            $result = ['status' => 'error', 'data' => $e->getMessage()];
        }

        return $result;
    }

    private function uploadCodeToMessage($code) {
        switch ($code) {
            case 1:
                $message = 'the uploaded file exceeds the upload_max_filesize directive in php.ini';
                break;
            case 2:
                $message = 'the uploaded file exceeds the MAX_FILE_SIZE directive that was specified in the HTML form';
                break;
            case 3:
                $message = 'the uploaded file was only partially uploaded';
                break;
            case 4:
                $message = 'no file was uploaded';
                break;
            case 6:
                $message = 'missing a temporary folder';
                break;
            case 7:
                $message = 'failed to write file to disk.';
                break;
            case 8:
                $message = 'a PHP extension stopped the file upload.';
                break;
            default:
                $message = $code;
        }
        return $message;
    }


}