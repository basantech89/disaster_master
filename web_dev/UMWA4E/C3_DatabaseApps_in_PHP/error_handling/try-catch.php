<?php
/**
 * Created by PhpStorm.
 * User: luv
 * Date: 12/9/18
 * Time: 6:56 PM
 */

require_once "../pdo.php";

// Development Error Handling
try {
    $stmt = $pdo -> prepare("SELECT * FROM users where user_id = :xyz");
    $stmt -> execute(array(":pizza" => $_GET['user_id']));
} catch (Exception $ex) {
    echo "Exception Message: " . $ex -> getMessage();
    return;
}

$row = $stmt -> fetch(PDO::FETCH_ASSOC);

?>

<body>
<form>
    <label for="ip01"> Name: </label>
    <input type="text" id="ip01" name="user_id">
</form>
</body>
