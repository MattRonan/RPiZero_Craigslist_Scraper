<?php
error_reporting(E_ALL); // Error/Exception engine, always use E_ALL

ini_set('ignore_repeated_errors', TRUE); // always use TRUE

ini_set('display_errors', TRUE); // Error/Exception display, use FALSE only in production environment or real server. Use TRUE in development environment
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "https://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="https://www.w3.org/1999/xhtml" lang="en" xml:lang="en" class="no-js">

	<head>
		<link rel="stylesheet" type="text/css" href="clScrape.css" />
		<link rel="preconnect" href="https://fonts.googleapis.com">
		<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
		<link href="https://fonts.googleapis.com/css2?family=Ubuntu&display=swap" rel="stylesheet">

	</head>

	<body>

		<?php
			if(isset($_POST['button1'])) {
				
				//here we open the idlist file and overwreite it so that nothing has an asterisk
				//all we have to do is check for * at the beginning of each item in $idList and subr if needed
				$myfile = fopen('CLScraper/IDList.txt', 'w') or die("Unable to open file!");
				for($i = 0; $i < $lines; $i++){
					if(strcmp(substr($idList[$i],0,1),"*") == 0){ //need to remove *
						substr($idList[0],1,strlen($idList[0])-2)
					}
					else{
						
					}
				}
				
				
				
				echo "<meta http-equiv='refresh' content='0'>"; #refreshes page after click to repopulate with no new items
			}
		?>
		
		<?php
			
			$myfile = fopen('CLScraper/IDList.txt', 'r+') or die("Unable to open file!");
			
			$lines = 0;
			$idList = array();
			while(!feof($myfile)) {
				$lines += 1;
				array_push($idList,fgets($myfile));
			}
			fclose($myfile);
		?>

		<div id = "headerDiv">

			<h1> Craigslist Scrape Results 
			
			<form method="post" id = "butt">
				<input type = "submit" name="button1" class="button2" value="Clear LED"></button>
			</form>
			</h1>

	  </div>

		<h3>Current Search: </h3>

		<div id = "resultsDiv">
			<?php
				//generate divs
				for($i = 0; $i < $lines; $i++){
					if(strcmp(substr($idList[$i],0,1),"*") == 0){ //unseen
						echo "<div class = 'hitDivUnseen'>" . $idList[$i] . "</div>";
					}
					else{
						echo "<div class = 'hitDivSeen'>" . $idList[$i] . "</div>";
					}
				}
				
				//subtr($idList[0],1,strlen($idList[0])-2) remove asteerisk
			?>
		</div>

		<script><!--block resubmission of the button on refresh-->
			if ( window.history.replaceState ) {
				window.history.replaceState( null, null, window.location.href );
		}
		</script>
	</body>
</html>