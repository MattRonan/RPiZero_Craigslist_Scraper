<?php
	header("refresh: 180;");
error_reporting(E_ALL);    
ini_set('ignore_repeated_errors', TRUE); 

ini_set('display_errors', TRUE); 
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
			
			//open up and store the id list so we know the number of hits and what's new.
			$myfile = fopen('CLScraper/IDList.txt', 'r+') or die("Unable to open file!");
			
			$numHits = 0;
			$idList = array();
			while(!feof($myfile)) {
				$numHits += 1;
				array_push($idList,fgets($myfile));
			}
			
			$numHits -= 1; #!feof($myfile) seems to cause numHits to be one greater than actual number...will check later
			
			fclose($myfile);
			
			//now open up and store the info list.  First line is the url to the search.
			$myfile = fopen('CLScraper/hitInfoList.txt', 'r') or die("Unable to open file!");
			$infoList = array();
			$groupSize = 5; //how many lines are in each hit group. rn its title,radius,price,date,link
			$searchURL = fgets($myfile);
			$lineOffset = 1; //might eventually include the itemized search terms in the header of the info list too. for now its just the url.
			for($i = 0; $i < $numHits; $i++){
				for($ii = 0; $ii < $groupSize; $ii++){
					array_push($infoList,fgets($myfile));
				}
			}
			fclose($myfile);

			if(isset($_POST['button1'])) {
				
				//here we open the idlist file and overwreite it so that nothing has an asterisk
				//all we have to do is check for * at the beginning of each item in $idList and subr if needed
				$myfile = fopen('CLScraper/IDList.txt', 'w') or die("Unable to open file!");
				for($i = 0; $i < $numHits; $i++){
					if(strcmp(substr($idList[$i],0,1),"*") == 0){ //need to remove *
						fwrite($myfile,substr($idList[$i],1,strlen($idList[$i])-1));
						//echo substr($idList[$i],1,strlen($idList[$i])-1) . "<br>";
					}
					else{
						fwrite($myfile,$idList[$i]);
					}
				}
				fclose($myfile);
				
				echo "<meta http-equiv='refresh' content='0'>"; #refreshes page after click to repopulate with no new items
			}
			
			if(isset($_POST['button2'])) {
				echo "poptart";
			}
		?>

		<div id = "headerDiv">

			<h1> Craigslist Scrape Results 
			
			<form method="post" id = "butt">
				<input type = "submit" name="button1" class="button2" value="Clear LED"></button>
			</form>
			</h1>

	  </div>

		<a id="mainLink" style = "display:inline-block" href="<?php echo $searchURL?>" target="_blank">See Results On Craigslist </a>
		<br>
		<div id = "resultsDiv">
			<?php
				//generate divs
				$vis;
				for($i = 0; $i < $numHits; $i++){
					if(strcmp(substr($idList[$i],0,1),"*") == 0){ //unseen
						$vis = 'hitDivUnseen';
					}
					else{
						$vis = 'hitDivSeen';
					}
						echo "<div class = " . $vis . "> <a class = 'titles' href = '" . $infoList[($i*$groupSize)+4] . "'>" .
								 $infoList[($i*$groupSize)+0] . $i . "," . $numHits ."</a>
								<br> <h4>" . $infoList[($i*$groupSize)+2] . "</h4> " . $infoList[($i*$groupSize)+1] . ", " . $infoList[($i*$groupSize)+3] .
						"</div>";
				
				}
			?>
		</div>

		<script><!--block resubmission of the button on refresh-->
			if ( window.history.replaceState ) {
				window.history.replaceState( null, null, window.location.href );
		}
		</script>
	</body>
</html>
