<?php
include_once "header.php";
include "function/style.php";
?>
<div class="container">
    <div class="search-bar">
        <input type="text" placeholder="🔍 Vous aussi, trouvez une communautés et bien d'autres choses encore !">
        <button id="search">Search</button>
    </div>
</div>
<div class="background" style="background-image: url('<?php echo getRandomImage(); ?>'); top: 15%;">
</div>


<?php
include_once "footer.php";
?>