<?php

namespace Services;

abstract class ServiceBase
{
    public $location = '';

    protected function getJsonBody()
    {
        $rawData = file_get_contents("php://input");
        $data    = json_decode($rawData);

        if (isset($this->token) && !empty($this->token)) {
            if (!isset($data)) {
                $data = new \stdClass();
            }
            $data->token = $this->token;
        }

        return $data;
    }

    protected function getBody($method)
    {
        $data    = [];
        $rawData = [];

        if ($method == 'POST') {
            $rawData = $_POST;
        } else if ($method == 'GET') {
            $rawData = $_GET;
        }

        foreach ($rawData as $key => $value) {
            $data[$key] = $value;
        }

        if (isset($this->token) && !empty($this->token)) {
            $data['token'] = $this->token;
        }

        return $data;
    }

    protected function parseURL($path)
    {
        if (isset($_SERVER['QUERY_STRING']) && !empty($_SERVER['QUERY_STRING'])) {
            return $this->location . $path . '?' . $_SERVER['QUERY_STRING'];
        }

        return $this->location . $path;
    }

    protected function convertJSONToForm($json)
    {
        if (empty($json)) {
            return $json;
        }

        $form = [];

        foreach ($json as $name => $value) {
            if (is_array($value) || is_object($value)) {
                continue;
            }
            $form[] = $name . '=' . urlencode($value);
        }

        return implode('&', $form);
    }

    protected function parseCURLRequest($method, $url, $body = null)
    {
        // Initialise CURL connection
        $ch = curl_init($url);

        // Set CURL options
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);

        if (!empty($body)) {
            curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
        }

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 120);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 120);

        // Execute and fetch CURL response
        $curl_response = curl_exec($ch);

        $response     = json_decode($curl_response, true);
        $status       = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $error_number = curl_errno($ch);
        $endpoint     = strpos($url, '?') ? substr($url, 0, strpos($url, '?')) : $url;
        // Close CURL request
        curl_close($ch);

        if (isset($response['response']) && $response['response']['status'] == 'error') {
            if (!empty($response['response']['message'])) {
                throw new \Exception($response['response']['message']);
            }
        }

        // Offline & decode related exceptions
        if (in_array($error_number, [CURLE_OPERATION_TIMEOUTED]) || in_array($error_number, [CURLE_COULDNT_CONNECT])) {
            throw new \Exception('Timeout when connecting to ' . $endpoint);
        } else if ($status == '401') {
            throw new \Exception('Unexpected ' . $status . ' received from ' . $endpoint . ', invalid token');
        } else if ($status == '403') {
            throw new \Exception('Unexpected ' . $status . ' received from ' . $endpoint . ', please check token has appropriate permissions');
        } else if ($status == '404') {
            throw new \Exception('Unexpected ' . $status . ' received from ' . $endpoint . ', please check it is correct');
        } else if ($status == '500') {
            throw new \Exception('Unexpected ' . $status . ' received from ' . $endpoint . ', please check server logs');
        } else if (json_last_error() !== JSON_ERROR_NONE) {
            throw new \Exception('Unrecognised response from ' . $endpoint . ', could not decode');
        } else if ($status == 0) {
            throw new \Exception('Could not open connection to ' . $endpoint);
        }

        return $response;
    }
}
