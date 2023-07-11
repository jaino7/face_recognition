<?php
// アップロードされたファイルの情報を取得する
$file = $_FILES['image'];
$fileName = $file['name'];
$fileTmpPath = $file['tmp_name'];
$fileSize = $file['size'];
$fileError = $file['error'];

// アップロード先のディレクトリパス
$uploadDir = 'uploads/';

// アップロードされたファイルを移動する
$uploadedFilePath = $uploadDir . $fileName;
move_uploaded_file($fileTmpPath, $uploadedFilePath);

// アップロードされたファイルのパスを返す（任意の処理を追加できます）
echo $uploadedFilePath;
?>
