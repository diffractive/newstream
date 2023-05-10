<?php
Class pkcs7
{
	function encrypt($text,$publickey)
	{
		//write text to file
		if(!file_exists( dirname(__FILE__)."/tmp/"))
		{
			mkdir( dirname(__FILE__)."/tmp/");
		}
		$filename = dirname(__FILE__)."/tmp/".time().".txt";
		$this->text_to_file($text,$filename);
		$filename_enc = dirname(__FILE__)."/tmp/".time().".enc";

		$key = file_get_contents($publickey);
		if (openssl_pkcs7_encrypt($filename, $filename_enc, $key,
		array())) {
		    // message encrypted - send it!
			unlink($filename);
			if (!$handle = fopen($filename_enc, 'r')) {
			         echo "Cannot open file ($filename_enc)";
			         exit;
			    }

				$contents = fread($handle, filesize($filename_enc));
				fclose($handle);
				$contents = str_replace("MIME-Version: 1.0
Content-Disposition: attachment; filename=\"smime.p7m\"
Content-Type: application/pkcs7-mime; smime-type=enveloped-data; name=\"smime.p7m\"
Content-Transfer-Encoding: base64
","",$contents);
				$contents = str_replace("\n","",$contents);
				unlink($filename_enc);
				return $contents;
		}
	}

	function decrypt($text,$publickey,$privatekey,$password)
	{
		$arr = str_split($text,64);
		$text = "";
		foreach($arr as $val)
		{
			$text .= $val."\n";
		}

		$text = "MIME-Version: 1.0
Content-Disposition: attachment; filename=\"smime.p7m\"
Content-Type: application/pkcs7-mime; smime-type=enveloped-data; name=\"smime.p7m\"
Content-Transfer-Encoding: base64

".$text;
		$text = rtrim($text,"\n");
		if(!file_exists( dirname(__FILE__)."/tmp/"))
		{
			mkdir( dirname(__FILE__)."/tmp/");
		}

		$infilename = dirname(__FILE__)."/tmp/".time().".txt";
		$this->text_to_file($text,$infilename);
				// echo $infilename;exit;
		$outfilename = dirname(__FILE__)."/tmp/".time().".dec";

		$public = file_get_contents($publickey);

		$private = array(file_get_contents($privatekey), $password);
		//$private = openssl_pkey_get_private($privatekey, $password);

		if (openssl_pkcs7_decrypt($infilename, $outfilename, $public, $private)) {
			unlink($infilename);
			$content = file_get_contents($outfilename);
			unlink($outfilename);
			return $content;
		}
		else{
			unlink($outfilename);
			unlink($infilename);
			echo "DECRYPT FAIL";exit;
		}
	}

	private function text_to_file($text,$filename)
	{
		if (!$handle = fopen($filename, 'w')) {
		         echo "Cannot open file ($filename)";
		         exit;
		    }

		    // Write $somecontent to our opened file.
		    if (fwrite($handle, $text) === FALSE) {
		        echo "Cannot write to file ($filename)";
		        exit;
		    }
	}
}
