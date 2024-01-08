
<!DOCTYPE html>
<html>
<head>
    <title><?php echo "XX网盘"; ?></title>
</head>
<body>
    <h1>XX网盘</h1>
    <h1>文件下载</h1>
    <h1>右击复制链接再粘贴到下载器</h1>
    <?php
    $files = glob("file/*");

    foreach ($files as $file) {
        echo '<a href="' . $file . '">' . basename($file) . '</a><br>';
    }
    ?>
</body>
</html>
