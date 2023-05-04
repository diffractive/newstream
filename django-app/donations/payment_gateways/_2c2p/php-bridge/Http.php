<?php

Class Http {
    function post($url,$fields_string)
       {
            //open connection
            $ch = curl_init();
            curl_setopt($ch,CURLOPT_URL, $url);
            curl_setopt($ch,CURLOPT_POSTFIELDS, $fields_string);
            curl_setopt($ch,CURLOPT_RETURNTRANSFER,true);
            //execute post
            $result = curl_exec($ch); //close connection
            curl_close($ch);
            return $result;
    }
}
