<?php
/**
 * This php script acts as a bridge for calling 2C2P APIs
 * pkcs7 encrypt and decrypt functions are required in order to build the requests
 * which only exist as core php functions but not in python
 * 
 * The original plan was to write python ports for the pkcs7 functionality
 * but it was more complex than expected
 * That's why this script serves as a temporary workaround
 */

require('Pkcs7.php');
require('Http.php');

/**
 * This function parses the options passed to this script
 * API credentials, params are supposed to be passed here from the python application
 * options followed by a single colon are required
 * options followed by two colons are optional, must use equal sign form
 * options followed by no colons are optional and with no value
 */
function parseOptions() {
    $longopts  = array(
        "api_url:",
        "version:",
        "mid:",
        "secret:",
        "ruid:",
        "type:",
        "status::",
        "amount::",
        "bill_today",
    );
    return getopt('', $longopts);
}

/**
 * This function receives options parsed from parseOptions
 * It decides what action api to call to 2C2P 
 * and outputs the final response back to python
 */
function Controller($options) {
    if ($options['type'] == 'U') {
        $response = updateRecurringPayment($options);
    } elseif ($options['type'] == 'C') {
        $response = cancelRecurringPayment($options);
    } elseif ($options['type'] == 'I') {
        $response = inquireRecurringPayment($options, false);
    } else {
        $response = '';
    }
    echo $response;
}

/**
 * This calls for an inquire-type PaymentAction to 2C2P
 * The result of the inquiry is needed in the update-type PaymentAction
 */
function inquireRecurringPayment($options, $internal = true) {
    $data['version'] = $options['version'];
    $data['merchantID'] = $options['mid'];
    $data['recurringUniqueID'] = $options['ruid'];
    $data['processType'] = 'I';
    $data['recurringStatus'] = '';
    $data['amount'] = '';
    $data['allowAccumulate'] = '';
    $data['maxAccumulateAmount'] = '';
    $data['recurringInterval'] = '';
    $data['recurringCount'] = '';
    $data['chargeNextDate'] = '';
    $params = '';
    foreach($data as $val) {
        $params .= $val;
    }
    $data['hashValue'] = strtoupper(hash_hmac('sha256', $params, $options['secret'], false));

    // Construct reequest message
    $xml = "<RecurringMaintenanceRequest>\n";
    foreach($data as $key => $val) {
        $xml .= "<$key>$val</$key>\n";
    }
    $xml .= '</RecurringMaintenanceRequest>';

    $keysdir = dirname(__FILE__) . '/keys';
    $pkcs7 = new pkcs7();
    $payload = $pkcs7->encrypt($xml,"$keysdir/demo2.crt");
    // Send request to 2C2P PGW and get back response
    $http = new Http();
    $enc_response = $http->post($options['api_url'], "paymentRequest=".$payload);
    $xml_response = $pkcs7->decrypt($enc_response,"$keysdir/demo2.crt","$keysdir/demo2.pem","2c2p");

    if ($internal) {
        return simplexml_load_string($xml_response);
    } else {
        return $xml_response;
    }
}

/**
 * This function calls the update-type PaymentAction API
 */
function updateRecurringPayment($options) {
    $inquiry = inquireRecurringPayment($options);
    $data['version'] = $options['version'];
    $data['merchantID'] = $options['mid'];
    $data['recurringUniqueID'] = $options['ruid'];
    $data['processType'] = $options['type'];
    $data['recurringStatus'] = $options['status'];
    $data['amount'] = $options['amount'];
    $data['allowAccumulate'] = 'N';
    $data['maxAccumulateAmount'] = '010000000000'; // just an arbitrary number
    $data['recurringInterval'] = $inquiry->recurringInterval;
    $data['recurringCount'] = $inquiry->recurringCount;
    $data['chargeNextDate'] = isset($options['bill_today']) ? '' : $inquiry->chargeNextDate; // empty means today
    $params = '';
    foreach($data as $val) {
        $params .= $val;
    }
    $data['hashValue'] = strtoupper(hash_hmac('sha256', $params, $options['secret'], false));

    // Construct reequest message
    $xml = "<RecurringMaintenanceRequest>\n";
    foreach($data as $key => $val) {
        $xml .= "<$key>$val</$key>\n";
    }
    $xml .= '</RecurringMaintenanceRequest>';

    $keysdir = dirname(__FILE__) . '/keys';
    $pkcs7 = new pkcs7();
    $payload = $pkcs7->encrypt($xml,"$keysdir/demo2.crt");
    // Send request to 2C2P PGW and get back response
    $http = new Http();
    $enc_response = $http->post($options['api_url'], "paymentRequest=".$payload);
    $xml_response = $pkcs7->decrypt($enc_response,"$keysdir/demo2.crt","$keysdir/demo2.pem","2c2p");

    return $xml_response;
}

/**
 * This function calls the cancel-type PaymentAction API
 */
function cancelRecurringPayment($options) {
    $inquiry = inquireRecurringPayment($options);
    $data['version'] = $options['version'];
    $data['merchantID'] = $options['mid'];
    $data['recurringUniqueID'] = $options['ruid'];
    $data['processType'] = $options['type'];
    $data['recurringStatus'] = $inquiry->recurringStatus;
    $data['amount'] = $inquiry->amount;
    $data['allowAccumulate'] = $inquiry->allowAccumulate;
    $data['maxAccumulateAmount'] = $inquiry->maxAccumulateAmount;
    $data['recurringInterval'] = $inquiry->recurringInterval;
    $data['recurringCount'] = $inquiry->recurringCount;
    $data['chargeNextDate'] = $inquiry->chargeNextDate;
    $params = '';
    foreach($data as $val) {
        $params .= $val;
    }
    $data['hashValue'] = strtoupper(hash_hmac('sha256', $params, $options['secret'], false));

    // Construct reequest message
    $xml = "<RecurringMaintenanceRequest>\n";
    foreach($data as $key => $val) {
        $xml .= "<$key>$val</$key>\n";
    }
    $xml .= '</RecurringMaintenanceRequest>';

    $keysdir = dirname(__FILE__) . '/keys';
    $pkcs7 = new pkcs7();
    $payload = $pkcs7->encrypt($xml,"$keysdir/demo2.crt");
    // Send request to 2C2P PGW and get back response
    $http = new Http();
    $enc_response = $http->post($options['api_url'], "paymentRequest=".$payload);
    $xml_response = $pkcs7->decrypt($enc_response,"$keysdir/demo2.crt","$keysdir/demo2.pem","2c2p");

    return $xml_response;
}

/**
 * Run main program
 */
Controller(parseOptions());