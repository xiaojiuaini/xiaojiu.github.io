<?php
$targetDir = "file/";
$targetFile = $targetDir . basename($_FILES["file"]["name"]);

if (move_uploaded_file($_FILES["file"]["tmp_name"], $targetFile)) {
    echo "文件上传成功";
} else {
    echo "文件上传失败原因：我不知道";
}
?>
